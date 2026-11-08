#!/usr/bin/env python3
"""「ふしぎな絶景の科学」ショート（1080x1920）を、1つの台本ファイルから作る。

使い方:
  bash tools/voicevox_engine.sh
  python3 tools/commons_fetch.py get travel_shorts/genbudo/photos "File:..." ...   # 写真とクレジット
  python3 tools/travel_short.py travel_shorts/genbudo/spot.py
  → 同じフォルダに short.mp4 / cover.png / metadata.md

台本（spot.py）:
  TITLE, PLACE=dict(name, pref, lat, lon)
  SCENES=[dict(spk, say, read, head, sub, show=("photo", ファイル名, ズームの向き) | ("map",) | ("fig", 関数名)), ...]
  FIGS={関数名: draw(t, local_t) -> RGBA}, META=投稿用メタデータ

しくみ:
  写真は画面いっぱいに切り抜き、ゆっくりズーム・横移動させて動きを出す（ケン・バーンズ効果）。
  地図は Commons の日本の位置図（正距円筒図法）に、緯度・経度から計算した位置へピンを落とす。
  写真の撮影者とライセンスを画面の隅と説明欄に必ず出す（CC BY / CC BY-SA の条件）。
"""
import argparse
import importlib.util
import json
import math
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import longform as L  # noqa: E402
import trivia_short as T  # noqa: E402

SW, SH = 1080, 1920
FPS = 15
GAP = 0.25
MAP_DIR = os.path.join(L.ROOT, "assets", "maps")


def cover_crop(im, w, h):
    """縦長の枠いっぱいになるように切り抜く（はみ出した分を左右で落とす）"""
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


class Photo:
    """写真カード。ぼかした同じ写真を画面いっぱいに敷き、その上の枠の中で写真をゆっくりズーム・パンする
    （小さい写真でも、画面全体に引き伸ばすより粗さが目立たない）"""
    CW, CH, CY = 1000, 750, 700  # 枠の幅・高さ・中心のy

    def __init__(self, path, move="in"):
        im = Image.open(path).convert("RGB")
        bg = cover_crop(im, SW // 4, SH // 4).filter(ImageFilter.GaussianBlur(6)).resize((SW, SH), Image.BILINEAR)
        self.bg = Image.blend(bg, Image.new("RGB", (SW, SH), (5, 10, 25)), 0.45).convert("RGBA")
        big = cover_crop(im, int(self.CW * 1.3), int(self.CH * 1.3))
        self.big = big.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
        self.move = move
        m = Image.new("L", (self.CW, self.CH))
        ImageDraw.Draw(m).rounded_rectangle((0, 0, self.CW - 1, self.CH - 1), 36, fill=255)
        self.mask = m

    def frame(self, k):  # k: 0→1
        k = 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, k)))
        bw, bh = self.big.size
        z = {"in": 1.0 - 0.2 * k, "out": 0.8 + 0.2 * k}.get(self.move, 0.8)
        cw, ch = int(bw * z), int(bh * z)
        cx = bw / 2 + {"left": 1, "right": -1}.get(self.move, 0) * (bw - cw) / 2 * (1 - 2 * k)
        x0 = int(min(max(0, cx - cw / 2), bw - cw))
        y0 = (bh - ch) // 2
        card = self.big.crop((x0, y0, x0 + cw, y0 + ch)).resize((self.CW, self.CH), Image.BILINEAR)
        out = self.bg.copy()
        x, y = (SW - self.CW) // 2, self.CY - self.CH // 2
        ImageDraw.Draw(out).rounded_rectangle((x - 8, y - 8, x + self.CW + 8, y + self.CH + 8), 42, fill=(255, 255, 255, 230))
        out.paste(card, (x, y), self.mask)
        return out


def japan_map(place, t):
    """日本の位置図にピンを落とす。地図の範囲は assets/maps/japan.json（上下左右の緯度・経度）"""
    meta = json.load(open(os.path.join(MAP_DIR, "japan.json")))
    m = Image.open(os.path.join(MAP_DIR, meta["file"])).convert("RGBA")
    s = 940 / m.width
    m = m.resize((940, int(m.height * s)), Image.LANCZOS)
    lay = Image.new("RGBA", (SW, SH))
    x0, y0 = (SW - m.width) // 2, 760 - m.height // 2
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((x0 - 14, y0 - 14, x0 + m.width + 14, y0 + m.height + 14), 30, fill=(255, 255, 255, 235))
    lay.alpha_composite(m, (x0, y0))
    px = x0 + (place["lon"] - meta["left"]) / (meta["right"] - meta["left"]) * m.width
    py = y0 + (meta["top"] - place["lat"]) / (meta["top"] - meta["bottom"]) * m.height
    drop = min(1, t / 0.5)
    py_now = py - 260 * (1 - drop) ** 2
    if drop >= 1:  # 着地したら波紋
        r = 20 + 60 * ((t - 0.5) % 1.2)
        a = int(200 * max(0, 1 - ((t - 0.5) % 1.2) / 1.2))
        d.ellipse((px - r, py - r * 0.5, px + r, py + r * 0.5), outline=(230, 50, 60, a), width=6)
    d.ellipse((px - 26, py_now - 78, px + 26, py_now - 26), fill=(230, 50, 60))
    d.polygon([(px - 22, py_now - 44), (px + 22, py_now - 44), (px, py_now)], fill=(230, 50, 60))
    d.ellipse((px - 10, py_now - 62, px + 10, py_now - 42), fill=L.WHITE)
    label = f"{place['pref']} {place['name']}"
    f = L.jp(46, True)
    tw = d.textlength(label, font=f)
    lx = min(max(40, px - tw / 2 - 30), SW - tw - 100)
    d.rounded_rectangle((lx, py + 30, lx + tw + 60, py + 110), 40, fill=(230, 50, 60))
    d.text((lx + 30 + tw / 2, py + 70), label, font=f, fill=L.WHITE, anchor="mm")
    d.text((x0 + m.width - 10, y0 + m.height + 30), meta["credit"], font=L.jp(22, True),
           fill=(255, 255, 255, 200), anchor="rm")
    return lay


def head_layer(head, sub, color, y):
    lay = Image.new("RGBA", (SW, SH))
    d = ImageDraw.Draw(lay)
    lines = head.split("\n")
    size = 118
    while size > 70 and max(d.textlength(s, font=L.jp(size)) for s in lines) > SW - 100:
        size -= 6
    lh = size * 1.18
    for i, s in enumerate(lines):
        d.text((SW / 2, y + i * lh), s, font=L.jp(size), fill=color, anchor="mm", stroke_width=12, stroke_fill=L.NAVY)
    if sub:
        sf = L.jp(46, True)
        tw = d.textlength(sub, font=sf)
        yy = y + lh * (len(lines) - 1) + size * 0.6 + 30
        d.rounded_rectangle((SW / 2 - tw / 2 - 36, yy, SW / 2 + tw / 2 + 36, yy + 84), 28, fill=(0, 0, 0, 170))
        d.text((SW / 2, yy + 42), sub, font=sf, fill=L.WHITE, anchor="mm")
    return lay


def subtitle(text, spk, page):
    """画面下の字幕（話者の色の帯つき）。長いときは2行ずつページ送り"""
    lay = Image.new("RGBA", (SW, SH))
    d = ImageDraw.Draw(lay)
    f = L.jp(50, True)
    ls = L.wrap(d, text, f, SW - 160)[page * 2: page * 2 + 2]
    y1 = SH - 150
    y0 = y1 - 40 - 66 * len(ls)
    d.rounded_rectangle((40, y0, SW - 40, y1), 28, fill=(10, 16, 40, 215))
    d.rounded_rectangle((40, y0, 60, y1), 10, fill=L.SPK[spk][1])
    d.text((80, y0 - 26), L.SPK[spk][0], font=L.jp(32, True), fill=L.SPK[spk][1], stroke_width=5, stroke_fill=L.NAVY)
    for i, s in enumerate(ls):
        d.text((SW / 2 + 10, y0 + 20 + 33 + i * 66), s, font=f, fill=L.WHITE, anchor="mm")
    return lay


def sub_pages(text):
    return max(1, (len(L.wrap(ImageDraw.Draw(Image.new("RGB", (8, 8))), text, L.jp(50, True), SW - 160)) + 1) // 2)


def credit_layer(c):
    lay = Image.new("RGBA", (SW, SH))
    d = ImageDraw.Draw(lay)
    s = f"写真: {c['artist'][:28]} / {c['license']} / Wikimedia Commons"
    f = L.jp(24, True)
    tw = d.textlength(s, font=f)
    y = Photo.CY + Photo.CH // 2 + 34
    d.text((SW / 2, y), s, font=f, fill=(255, 255, 255, 220), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))
    return lay


def write_metadata(cfg, here, total, credits_used):
    m = cfg.META
    src = "\n".join(f"{lab}\n{url}" for lab, url in m["sources"])
    photos = "\n".join(f"・{c['artist']}（{c['license']}）{c['page']}" for c in credits_used)
    desc = (m["lead"] + "\n\n" + "\n".join("・" + p for p in m["points"]) + "\n\n"
            + "【しくみ】" + m["principle"] + "\n\n"
            + f"📍 {cfg.PLACE['pref']} {cfg.PLACE['name']}\n\n"
            + "出典:\n" + src + "\n\n"
            + "写真（Wikimedia Commons）:\n" + photos + "\n地図: " + json.load(open(os.path.join(MAP_DIR, "japan.json")))["credit_full"]
            + "\n\n音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん\n\n" + " ".join(m["hashtags"]))
    tags = ", ".join(dict.fromkeys(m["tags"]))
    assert len(tags) <= 500
    code = lambda s: "```\n" + s + "\n```\n"  # noqa: E731
    md = [f"# {m['title'].split(' #')[0]}（{total:.0f}秒）\n",
          f"- 動画: `short.mp4`（1080×1920 縦長 / 約{total:.0f}秒）/ 表紙候補: `cover.png`\n"
          f"- 作り直し: `python3 tools/travel_short.py {os.path.relpath(here, L.ROOT)}/spot.py`\n",
          "\n**タイトル**\n", code(m["title"])]
    if m.get("alt_titles"):
        md += ["**ほかの候補**\n"] + [code(t) for t in m["alt_titles"]]
    md += ["**説明欄**\n", code(desc), "**タグ**（タグ欄に貼る）\n", code(tags), "**固定コメント**\n", code(m["pinned"])]
    if m.get("notes"):
        md += ["\n**事実確認のメモ**\n"] + [f"- {n}\n" for n in m["notes"]]
    open(os.path.join(here, "metadata.md"), "w", encoding="utf-8").write("".join(md))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spot")
    ap.add_argument("--no-tts", action="store_true")
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("spot", a.spot)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    here = os.path.dirname(os.path.abspath(a.spot))
    credits = {c["file"]: c for c in json.load(open(os.path.join(here, "photos", "credits.json")))}
    sc = cfg.SCENES
    vdir = os.path.join(here, "voicevox")
    os.makedirs(vdir, exist_ok=True)
    if not a.no_tts:
        for n, s in enumerate(sc):
            kana = L.tts(s.get("read") or s["say"], s["spk"], os.path.join(vdir, f"{n:02d}_{s['spk']}.wav"))
            print(f"{n:02d} {L.SPK[s['spk']][0]}: {kana}")
    voices = [L.base.load_audio(os.path.join(vdir, f"{n:02d}_{s['spk']}.wav"), L.base.VOICE_FX) for n, s in enumerate(sc)]
    durs = [len(v) / L.SR + GAP for v in voices]
    durs[-1] += 0.6
    starts = np.cumsum([0.2] + durs[:-1])
    total = float(starts[-1] + durs[-1])
    assert total < 60

    music = L.base.bgm(total) * 0.8
    vo = np.zeros_like(music)
    for v, st in zip(voices, starts):
        s0 = int(st * L.SR)
        vo[s0:s0 + len(v)] += v[: max(0, len(vo) - s0)]
    env = np.convolve(np.abs(vo), np.ones(int(0.05 * L.SR)) / int(0.05 * L.SR), "same")
    act = np.convolve((env > 0.01).astype(float), np.ones(int(0.25 * L.SR)) / int(0.25 * L.SR), "same")
    music *= 1 - 0.6 * np.clip(act * 1.5, 0, 1)
    mix = vo * 0.9 + music
    mix = np.clip(mix / max(1.0, np.abs(mix).max() / 0.95), -1, 1)
    wav = os.path.join(tempfile.mkdtemp(), "mix.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(L.SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

    accent = getattr(cfg, "ACCENT", (255, 200, 60))
    dark = T.background((24, 40, 70), (8, 12, 30))
    band = T.top_band(cfg.TITLE, accent)
    photos, used = {}, []
    for s in sc:
        if s["show"][0] == "photo" and s["show"][1] not in photos:
            photos[s["show"][1]] = Photo(os.path.join(here, "photos", s["show"][1]), s["show"][2] if len(s["show"]) > 2 else "in")
            used.append(credits[s["show"][1]])
    shade = Image.new("RGBA", (SW, SH))
    sd = ImageDraw.Draw(shade)
    for y in range(SH):  # 文字を読みやすくする上下の影
        k = max(0.0, (y - SH * 0.55) / (SH * 0.45)) ** 1.5 * 0.85 + max(0.0, (SH * 0.25 - y) / (SH * 0.25)) * 0.45
        sd.line((0, y, SW, y), fill=(0, 0, 0, int(255 * min(0.9, k))))
    heads = [head_layer(s["head"], s.get("sub", ""), s.get("color", accent),
                        1230 if s["show"][0] == "photo" else 1170) for s in sc]
    figs = getattr(cfg, "FIGS", {})
    npg = [sub_pages(s["say"]) for s in sc]
    out = os.path.join(here, "short.mp4")
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{SW}x{SH}", "-r", str(FPS), "-i", "-", "-i", wav,
                             "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                             "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000",
                             "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                            stdin=subprocess.PIPE)
    cache, cover = {}, None
    for k in range(int(total * FPS)):
        t = k / FPS
        n = max(0, int(np.searchsorted(starts, t, side="right")) - 1)
        s = sc[n]
        lt = t - starts[n]
        kind = s["show"][0]
        if kind == "photo":
            frame = photos[s["show"][1]].frame(lt / durs[n])
            frame.alpha_composite(credit_layer(credits[s["show"][1]]))
        else:
            frame = dark.copy()
            im = japan_map(cfg.PLACE, lt) if kind == "map" else None
            if kind == "map":
                frame.alpha_composite(im)
            else:
                fim = figs[s["show"][1]](t, lt)
                frame.alpha_composite(fim, (int(SW / 2 - fim.width / 2), int(760 - fim.height / 2)))
        if n > 0 and lt < 0.25 and sc[n - 1]["show"] != s["show"]:  # 場面の切りかえは白く一瞬光らせる
            frame = Image.blend(frame, Image.new("RGBA", (SW, SH), (255, 255, 255, 255)), 0.3 * (1 - lt / 0.25))
        frame.alpha_composite(band)
        dy = int(50 * (1 - min(1, lt / 0.25)) ** 2)
        frame.alpha_composite(heads[n].crop((0, 0, SW, SH - dy)), (0, dy))
        page = min(npg[n] - 1, int(lt / max(0.1, durs[n] - GAP) * npg[n]))
        key = (n, page)
        if key not in cache:
            cache.clear()
            cache[key] = subtitle(s["say"], s["spk"], page)
        frame.alpha_composite(cache[key])
        ImageDraw.Draw(frame).rectangle((0, SH - 16, SW * t / total, SH), fill=accent)
        if n == 0 and cover is None and lt > 0.8:
            cover = frame.copy()
        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg failed")
    cover.convert("RGB").save(os.path.join(here, "cover.png"))
    write_metadata(cfg, here, total, used)
    print("wrote", out, f"{total:.1f}s")


if __name__ == "__main__":
    main()
