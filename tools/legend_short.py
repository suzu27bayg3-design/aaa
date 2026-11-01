#!/usr/bin/env python3
"""MLBレジェンド紹介ショートの共通ジェネレーター（成績テロップ風・写真入り）

使い方:
  bash tools/voicevox_engine.sh                     # VOICEVOXエンジン起動
  python3 tools/legend_short.py shorts_ruth/legend_cfg.py          # 音声生成 + 動画
  python3 tools/legend_short.py shorts_ruth/legend_cfg.py --no-tts # 既存の音声で動画だけ

設定ファイル (legend_cfg.py) に書くもの:
  NAME_EN, NAME_JP, YEARS, SOURCE, OUT, THUMB(dict), SCENES(list)
  シーンの種類:
    hook  : 写真を大きく + 特大の問いかけ（冒頭1秒で見せる）。名前は約0.9秒後に出る
    big   : 画面いっぱいの数字カウントアップ（value, label, sub）
    board : 成績表（最大4行）。rows = [(項目, 値, バッジ or None)]
    titles: タイトル表。rows = [(項目, 値, 単位, バッジ or None)]
    loop  : 締め。冒頭の問いかけにつながる一言（ループ構成）
  各シーン共通: narration（読み上げ文）, voice（"hook"/"talk"）, photo（photos/ 内のファイル名）
"""
import argparse
import importlib.util
import json
import math
import os
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("base", os.path.join(ROOT, "shorts_honey", "make_short.py"))
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

W, H, FPS, SR = 1080, 1920, 30, 48000
JP = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
JPB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
NUM = "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"
GOLD, NAVY, RED, WHITE = (255, 200, 60), (10, 18, 48), (215, 40, 55), (255, 255, 255)
_FONTS = {}


def jp(size, bold=False):
    k = ("jp", size, bold)
    if k not in _FONTS:
        _FONTS[k] = ImageFont.truetype(JPB if bold else JP, size, index=0)
    return _FONTS[k]


def num(size):
    k = ("num", size)
    if k not in _FONTS:
        _FONTS[k] = ImageFont.truetype(NUM, size)
    return _FONTS[k]


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def fmt(target, p):
    """target の書式（.342 / 2,214 / 1.164）を保ったまま割合 p の値を返す"""
    t = target.replace(",", "")
    dec = len(t.split(".")[1]) if "." in t else 0
    v = float(t) * p
    s = f"{v:.{dec}f}" if dec else (f"{int(round(v)):,}" if "," in target else str(int(round(v))))
    if target.startswith(".") and s.startswith("0"):
        s = s[1:]
    return s


# ---- 写真 -----------------------------------------------------------------------
def load_photo(path):
    im = Image.open(path).convert("L")
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageOps.colorize(im, black=(8, 14, 40), white=(245, 232, 205), mid=(110, 110, 120))
    s = max(W * 1.12 / im.width, H * 1.12 / im.height)
    return im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS).convert("RGBA")


def photo_frame(ph, lt, dur, darkness, seed=0, focus_y=0.3):
    """ケン・バーンズ効果（ゆっくりズーム＋パン）。focus_y: 縦方向の注目位置（0=上,1=下）"""
    p = max(0.0, min(1.0, lt / max(dur, 0.1)))
    z = 1.0 + 0.08 * p
    cw, ch = ph.width / z, ph.height / z
    if cw / ch > W / H:
        cw = ch * W / H
    else:
        ch = cw * H / W
    dx = (ph.width - cw) * (0.5 + 0.25 * math.sin(seed + p * 1.2))
    dy = (ph.height - ch) * min(1.0, max(0.0, focus_y + 0.1 * p))
    img = ph.crop((int(dx), int(dy), int(dx + cw), int(dy + ch))).resize((W, H), Image.BILINEAR)
    return Image.alpha_composite(img, Image.new("RGBA", (W, H), (6, 10, 30, int(255 * darkness))))


_GRAD = {}


def bottom_gradient(start=780, maxa=235):
    """下に向かって暗くなるグラデーション（文字を読みやすく）"""
    k = (start, maxa)
    if k not in _GRAD:
        g = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(g)
        for y in range(start, H, 6):
            d.rectangle((0, y, W, y + 6), fill=(6, 10, 30, int(min(maxa, (y - start) * 0.45))))
        _GRAD[k] = g
    return _GRAD[k]


# ---- 共通パーツ -------------------------------------------------------------------
def header(d, cfg, small=False):
    d.polygon([(0, 150), (400, 150), (360, 214), (0, 214)], fill=RED)
    d.text((40, 156), "MLB LEGENDS", font=num(46), fill=WHITE)
    d.text((60, 228), cfg.NAME_EN, font=num(100), fill=WHITE)
    d.text((66, 350), f"{cfg.NAME_JP}  {cfg.YEARS}", font=jp(38, True), fill=GOLD)
    d.text((60, 92), cfg.SOURCE, font=jp(24, True), fill=(200, 210, 240))


def section(d, head, eng, lt, year=None):
    off = int(-600 * (1 - ease(lt / 0.35)))
    y = 440
    d.polygon([(off, y), (off + 1000, y), (off + 960, y + 130), (off, y + 130)], fill=GOLD)
    d.text((off + 60, y + 8), head, font=jp(84), fill=NAVY)
    hb = d.textbbox((0, 0), head, font=jp(84))
    x = off + 60 + hb[2] + 24
    if year:
        d.text((x, y + 65), year, font=num(108), fill=RED, anchor="lm")
    elif eng:
        d.text((x, y + 88), eng, font=num(34), fill=NAVY, anchor="ls")


def badge(d, x, y, text, fill, color=WHITE):
    """数字の意味を伝える小さなバッジ（例: 歴代2位）"""
    f = jp(32, True)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle((x, y - 26, x + tw + 28, y + 26), 26, fill=fill)
    d.text((x + 14, y), text, font=f, fill=color, anchor="lm")


def big_text(d, lines, y_center, accent_last=True, max_size=150):
    """特大の見出し（行ごとに中央揃え・黒ふち）。最終行は金色で強調"""
    size = max_size
    while size > 70:
        f = jp(size)
        if max(d.textlength(ln, font=f) for ln in lines) <= W - 110:
            break
        size -= 6
    f = jp(size)
    lh = int(size * 1.18)
    y = y_center - lh * len(lines) / 2
    for i, ln in enumerate(lines):
        col = GOLD if (accent_last and i == len(lines) - 1) else WHITE
        d.text((W / 2, y + i * lh), ln, font=f, fill=col, anchor="ma", stroke_width=12, stroke_fill=(0, 0, 0))


# ---- シーン描画 -------------------------------------------------------------------
def draw_hook(img, cfg, sc, lt):
    d = ImageDraw.Draw(img)
    # 問いかけ（0秒から表示。少しだけ下からせり上がる）
    lay = Image.new("RGBA", (W, H))
    big_text(ImageDraw.Draw(lay), sc["text"], 1230 + int(40 * (1 - ease(lt / 0.25))), max_size=160)
    img.alpha_composite(lay)
    # 名前タグは約0.9秒後にフェードイン
    a = ease((lt - 0.9) / 0.3)
    if a > 0:
        tag = Image.new("RGBA", (W, H))
        td = ImageDraw.Draw(tag)
        td.polygon([(0, 150), (400, 150), (360, 214), (0, 214)], fill=RED)
        td.text((40, 156), "MLB LEGENDS", font=num(46), fill=WHITE)
        td.text((60, 228), cfg.NAME_EN, font=num(100), fill=WHITE, stroke_width=4, stroke_fill=(0, 0, 0))
        td.text((66, 350), f"{cfg.NAME_JP}  {cfg.YEARS}", font=jp(38, True), fill=GOLD,
                stroke_width=3, stroke_fill=(0, 0, 0))
        tag.putalpha(tag.split()[3].point(lambda v: int(v * a)))
        img.alpha_composite(tag)


def draw_big(img, cfg, sc, lt):
    d = ImageDraw.Draw(img)
    header(d, cfg)
    p = ease(lt / 1.4)
    val = fmt(sc["value"], p)
    f = num(330)
    d.text((W / 2, 900), val, font=f, fill=GOLD, anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
    d.text((W / 2, 1110), sc["label"], font=jp(96), fill=WHITE, anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    if lt > 1.0:
        a = ease((lt - 1.0) / 0.3)
        lay = Image.new("RGBA", (W, H))
        ld = ImageDraw.Draw(lay)
        for i, s in enumerate(sc.get("sub", [])):
            y = 1250 + i * 90
            tw = ld.textlength(s, font=jp(50, True))
            ld.rounded_rectangle(((W - tw) / 2 - 30, y - 40, (W + tw) / 2 + 30, y + 40), 24,
                                 fill=(RED if i == len(sc["sub"]) - 1 else (0, 0, 0)) + (220,))
            ld.text((W / 2, y), s, font=jp(50, True), fill=WHITE, anchor="mm")
        lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
        img.alpha_composite(lay)


def draw_board(img, cfg, sc, lt):
    d = ImageDraw.Draw(img)
    header(d, cfg)
    section(d, sc["head"], sc.get("eng"), lt, sc.get("year"))
    rows = sc["rows"]
    rh, y0 = 168, 620
    for i, row in enumerate(rows):
        t0 = 0.3 + 0.18 * i
        if lt < t0:
            continue
        a = ease((lt - t0) / 0.25)
        x = int(80 * (1 - a))
        y = y0 + i * rh
        lay = Image.new("RGBA", (W, H))
        ld = ImageDraw.Draw(lay)
        hl = sc.get("hl") == i
        fill = GOLD + (240,) if hl else (12, 18, 45, 200)
        ld.rounded_rectangle((60 + x, y, W - 60 + x, y + rh - 18), 20, fill=fill)
        ld.rectangle((60 + x, y, 74 + x, y + rh - 18), fill=NAVY if hl else RED)
        cy = y + (rh - 18) / 2
        tc = NAVY if hl else WHITE
        ld.text((108 + x, cy), row[0], font=jp(62), fill=tc, anchor="lm")
        p = ease((lt - t0 - 0.1) / 0.7)
        val = fmt(row[1], p)
        vc = NAVY if hl else GOLD
        if sc["kind"] == "titles":
            unit, bdg = row[2], (row[3] if len(row) > 3 else None)
            uw = ld.textlength(unit, font=jp(44, True))
            ld.text((W - 90 + x - uw, cy + 10), unit, font=jp(44, True), fill=tc, anchor="lm")
            ld.text((W - 108 + x - uw, cy), val, font=num(112), fill=vc, anchor="rm")
        else:
            bdg = row[2] if len(row) > 2 else None
            ld.text((W - 95 + x, cy), val, font=num(118), fill=vc, anchor="rm")
        if bdg and lt > t0 + 0.6:  # 数字が数え上がった後にバッジ
            lw = ld.textlength(row[0], font=jp(62))
            badge(ld, 108 + x + lw + 22, cy, bdg, NAVY if hl else RED)
        lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
        img.alpha_composite(lay)


def draw_loop(img, cfg, sc, lt):
    d = ImageDraw.Draw(img)
    header(d, cfg)
    lay = Image.new("RGBA", (W, H))
    big_text(ImageDraw.Draw(lay), sc["text"], 1180, max_size=150)
    lay.putalpha(lay.split()[3].point(lambda v: int(v * ease(lt / 0.4))))
    img.alpha_composite(lay)


DRAW = dict(hook=draw_hook, big=draw_big, board=draw_board, titles=draw_board, loop=draw_loop)
DARK = dict(hook=0.10, big=0.55, board=0.55, titles=0.55, loop=0.25)
FOCUS = dict(hook=0.15, big=0.3, board=0.3, titles=0.3, loop=0.15)


# ---- 音声（VOICEVOX） -----------------------------------------------------------
PARAMS = {"hook": dict(speedScale=1.18, pitchScale=0.03, intonationScale=1.35),
          "talk": dict(speedScale=1.24, pitchScale=0.0, intonationScale=1.15)}


def synth(cfg, folder, host="http://127.0.0.1:50021", speaker=3):
    os.makedirs(folder, exist_ok=True)
    for f in os.listdir(folder):
        if f.endswith(".wav"):
            os.remove(os.path.join(folder, f))
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    for i, sc in enumerate(cfg.SCENES, 1):
        q = json.loads(opener.open(urllib.request.Request(
            f"{host}/audio_query?" + urllib.parse.urlencode({"text": sc["narration"], "speaker": speaker}),
            data=b"", method="POST")).read())
        q.update(PARAMS[sc.get("voice", "talk")], prePhonemeLength=0.05, postPhonemeLength=0.08,
                 outputSamplingRate=48000)
        wav = opener.open(urllib.request.Request(f"{host}/synthesis?speaker={speaker}",
                                                 data=json.dumps(q).encode(), method="POST",
                                                 headers={"Content-Type": "application/json"})).read()
        open(os.path.join(folder, f"{i:03d}_ずんだもん.wav"), "wb").write(wav)
        kana = "/".join("".join(m["text"] for m in ap["moras"]) for ap in q["accent_phrases"])
        print(f"{i:03d} {kana}")


# ---- メイン ---------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cfg")
    ap.add_argument("--no-tts", action="store_true")
    args = ap.parse_args()
    spec = importlib.util.spec_from_file_location("cfg", args.cfg)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    here = os.path.dirname(os.path.abspath(args.cfg))
    vdir = os.path.join(here, "voicevox")
    if not args.no_tts:
        synth(cfg, vdir)
    files = sorted(f for f in os.listdir(vdir) if f.endswith(".wav"))
    assert len(files) == len(cfg.SCENES), f"音声 {len(files)} / シーン {len(cfg.SCENES)}"
    voices = [base.load_audio(os.path.join(vdir, f), base.VOICE_FX) for f in files]
    durs = [len(a) / SR + 0.25 + (0.5 if sc["kind"] in ("board", "titles", "big") else 0)
            for a, sc in zip(voices, cfg.SCENES)]
    total = sum(durs) + 0.3
    print(f"total {total:.1f}s")

    music = base.bgm(total)
    vo = np.zeros_like(music)
    starts = np.cumsum([0.1] + durs[:-1])
    for a, s0 in zip(voices, starts):
        s = int(s0 * SR)
        vo[s:s + len(a)] += a[: len(vo) - s]
    env = np.convolve(np.abs(vo), np.ones(int(0.05 * SR)) / int(0.05 * SR), "same")
    active = np.convolve((env > 0.01).astype(float), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
    music *= 1 - 0.55 * np.clip(active * 1.5, 0, 1)
    mix = vo * 0.9 + music * 1.3
    mix = np.clip(mix / max(1.0, np.abs(mix).max() / 0.95), -1, 1)
    wav_path = os.path.join(tempfile.mkdtemp(), "mix.wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

    pdir = os.path.join(here, "photos")
    cache = {}
    def photo(name):
        if name not in cache:
            cache[name] = load_photo(os.path.join(pdir, name))
        return cache[name]
    cpath = os.path.join(pdir, "credits.txt")
    pcredit = open(cpath, encoding="utf-8").read().strip() if os.path.exists(cpath) else ""

    out = os.path.join(here, cfg.OUT)
    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav_path,
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for fi in range(int(total * FPS)):
        t = fi / FPS
        si = max(0, int(np.searchsorted(starts, t, side="right")) - 1)
        lt = t - starts[si]
        sc = cfg.SCENES[si]
        k = sc["kind"]
        frame = photo_frame(photo(sc["photo"]), lt, durs[si], DARK[k], seed=si, focus_y=FOCUS[k])
        if k in ("hook", "loop"):
            frame = Image.alpha_composite(frame, bottom_gradient())
        DRAW[k](frame, cfg, sc, lt)
        d = ImageDraw.Draw(frame)
        d.text((W - 60, 1665), "VOICEVOX:ずんだもん", font=jp(26, True), fill=(220, 225, 255), anchor="ra")
        if pcredit:
            d.text((60, 1705), "Photo: " + pcredit, font=jp(22, True), fill=(220, 225, 255))
        d.rectangle((0, H - 16, int(W * t / total), H), fill=GOLD)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    th = cfg.THUMB
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "add_thumb_frame.py"), out,
                    "--text", th["text"], "--emoji", th.get("emoji", "⚾"), "--color", th.get("color", "#ffc83c"),
                    "--bg", th.get("bg", "#0a1230"), "--tag", th.get("tag", "MLBレジェンド"),
                    "--png", os.path.join(here, "thumb.png")], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
