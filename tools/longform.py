#!/usr/bin/env python3
"""ずんだもん×四国めたんの掛け合い解説動画（横長1920x1080）ジェネレーター

使い方:
  bash tools/voicevox_engine.sh
  python3 tools/longform.py longform_quantum/script.py            # 音声生成 + 動画
  python3 tools/longform.py longform_quantum/script.py --no-tts   # 既存音声で動画のみ

仕組み: セリフ1つごとに画面（スライド＋話者テロップ）を1枚描き、音声の長さだけ表示して連結する。
出力: 動画 / サムネイル(1280x720) / chapters.txt（YouTube説明欄に貼るチャプター）
"""
import argparse
import importlib.util
import json
import math
import os
import subprocess
import tempfile
import urllib.parse
import urllib.request
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("base", os.path.join(ROOT, "shorts_honey", "make_short.py"))
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

W, H, SR = 1920, 1080, 48000
JP = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
JPB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
NUM = "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"
NAVY, NAVY2, WHITE, GOLD = (10, 16, 40), (24, 34, 78), (255, 255, 255), (255, 200, 60)
SPK = {  # 話者: 表示名, 色, VOICEVOX話者ID, 話速
    "Z": ("ずんだもん", (110, 200, 90), 3, 1.15),
    "M": ("四国めたん", (235, 95, 160), 2, 1.12),
}
_F = {}


def jp(s, b=False):
    k = (s, b)
    if k not in _F:
        _F[k] = ImageFont.truetype(JPB if b else JP, s, index=0)
    return _F[k]


def num(s):
    k = ("n", s)
    if k not in _F:
        _F[k] = ImageFont.truetype(NUM, s)
    return _F[k]


def wrap(d, text, font, width):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if d.textlength(cur + ch, font=font) > width and cur and ch not in "、。！？」）":
            lines.append(cur); cur = ch
        else:
            cur += ch
    lines.append(cur)
    return lines


# ---- 背景・枠 ------------------------------------------------------------------
def background():
    y = np.linspace(0, 1, H)[:, None]
    g = (np.array([20, 30, 72]) * (1 - y) + np.array([6, 10, 28]) * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    img = Image.fromarray(g.astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(lay)
    for x in range(0, W, 60):
        d.line((x, 0, x, H), fill=(120, 160, 255, 14), width=1)
    for yy in range(0, H, 60):
        d.line((0, yy, W, yy), fill=(120, 160, 255, 14), width=1)
    return Image.alpha_composite(img, lay)


def frame_base(bg, cfg, ch_i, ch):
    img = bg.copy()
    d = ImageDraw.Draw(img)
    # 上部バー（章番号・章タイトル・シリーズ名）
    d.rectangle((0, 0, W, 96), fill=(6, 10, 30, 235))
    if ch_i > 0:
        d.rounded_rectangle((40, 22, 140, 74), 12, fill=GOLD)
        d.text((90, 48), f"{ch_i}", font=num(40), fill=NAVY, anchor="mm")
    d.text((170 if ch_i > 0 else 40, 48), ch["title"], font=jp(44), fill=WHITE, anchor="lm")
    d.text((W - 40, 48), cfg.TITLE, font=jp(28, True), fill=(180, 195, 240), anchor="rm")
    # 進行バー（章の位置）
    n = len(cfg.CHAPTERS)
    for i in range(n):
        x0 = 40 + i * (W - 80) / n
        d.rectangle((x0 + 3, 92, x0 + (W - 80) / n - 3, 96), fill=GOLD if i <= ch_i else (60, 70, 110))
    return img


# ---- 図 ------------------------------------------------------------------------
def fig_area(img, box, fig, cfg):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    k = fig["kind"]
    if k == "title":
        d.text((W / 2, 330), cfg.TITLE, font=jp(96), fill=WHITE, anchor="mm", stroke_width=6, stroke_fill=NAVY)
        d.text((W / 2, 460), cfg.SUBTITLE, font=jp(54, True), fill=GOLD, anchor="mm")
        for i, (n, c) in enumerate((("Google Willow", (66, 133, 244)), ("ノーベル物理学賞", GOLD),
                                    ("理研×富士通", (230, 80, 80)), ("耐量子暗号", (110, 200, 90)))):
            bx = W / 2 - 760 + i * 390
            d.rounded_rectangle((bx, 560, bx + 360, 640), 40, outline=c, width=5, fill=(0, 0, 0, 120))
            d.text((bx + 180, 600), n, font=jp(38, True), fill=WHITE, anchor="mm")
    elif k == "qubit":
        cy = (y0 + y1) / 2
        # 古典ビット
        for i, v in enumerate("01"):
            cx = x0 + 120 + i * 170
            d.rounded_rectangle((cx - 65, cy - 65, cx + 65, cy + 65), 18, fill=(60, 70, 110), outline=WHITE, width=4)
            d.text((cx, cy), v, font=num(90), fill=WHITE, anchor="mm")
        d.text((x0 + 205, cy + 120), "ビット：どちらか一方", font=jp(34, True), fill=WHITE, anchor="mm")
        # 量子ビット（球と矢印）
        cx, r = x1 - 230, 170
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(150, 190, 255), width=5)
        d.ellipse((cx - r, cy - r * 0.3, cx + r, cy + r * 0.3), outline=(150, 190, 255, 140), width=3)
        d.text((cx, cy - r - 36), "0", font=num(48), fill=WHITE, anchor="mm")
        d.text((cx, cy + r + 36), "1", font=num(48), fill=WHITE, anchor="mm")
        ax, ay = cx + r * 0.75 * math.cos(math.radians(-35)), cy + r * 0.75 * math.sin(math.radians(-35))
        d.line((cx, cy, ax, ay), fill=GOLD, width=10)
        d.ellipse((ax - 16, ay - 16, ax + 16, ay + 16), fill=GOLD)
        d.text((cx, cy + r + 100), "量子ビット：重ね合わせ", font=jp(34, True), fill=GOLD, anchor="mm")
    elif k == "vote":
        rows = [("送りたい値", "0", [None]), ("3つにして送る", None, ["0", "0", "0"]),
                ("1つが壊れた", None, ["0", "1", "0"]), ("多数決で復元", "0", [None])]
        for i, (lab, single, cells) in enumerate(rows):
            yy = y0 + 40 + i * 150
            d.text((x0 + 20, yy + 50), lab, font=jp(34, True), fill=WHITE, anchor="lm")
            vals = [single] if single else cells
            for j, v in enumerate(vals):
                cx = x0 + 420 + j * 120
                bad = v == "1"
                d.rounded_rectangle((cx - 50, yy, cx + 50, yy + 100), 16,
                                    fill=(230, 80, 80) if bad else ((255, 200, 60) if single else (90, 130, 230)),
                                    outline=WHITE, width=3)
                d.text((cx, yy + 50), v, font=num(64), fill=NAVY if single else WHITE, anchor="mm")
            if i < len(rows) - 1:
                d.text((x0 + 540, yy + 125), "↓", font=jp(36), fill=(180, 195, 240), anchor="mm")
    elif k == "noise":
        cy = (y0 + y1) / 2 - 40
        pts_c, pts_n = [], []
        rng = np.random.default_rng(1)
        for i in range(400):
            x = x0 + 40 + i * (x1 - x0 - 80) / 400
            t = i / 400
            pts_c.append((x, cy - 120 + 70 * math.sin(t * 18)))
            pts_n.append((x, cy + 140 + 70 * math.sin(t * 18) * math.exp(-3 * t) + rng.normal(0, 4 + 30 * t)))
        d.line(pts_c, fill=(120, 200, 255), width=6)
        d.line(pts_n, fill=(255, 110, 110), width=5)
        d.text((x0 + 40, cy - 230), "理想：量子状態が保たれる", font=jp(34, True), fill=(120, 200, 255))
        d.text((x0 + 40, cy + 30), "現実：ノイズで状態が壊れる（デコヒーレンス）", font=jp(34, True), fill=(255, 130, 130))
    elif k == "bars":
        items = fig["items"]
        vmax = max(v for _, v, _ in items)
        bw = min(220, (x1 - x0 - 120) / len(items) - 60)
        base_y = y1 - 110
        for i, (lab, v, txt) in enumerate(items):
            cx = x0 + 100 + (i + 0.5) * (x1 - x0 - 200) / len(items)
            hgt = max(8, (base_y - y0 - 120) * v / vmax)
            d.rounded_rectangle((cx - bw / 2, base_y - hgt, cx + bw / 2, base_y), 14,
                                fill=GOLD if i == len(items) - 1 else (110, 150, 255))
            d.text((cx, base_y - hgt - 40), txt, font=jp(44), fill=WHITE, anchor="mm")
            d.text((cx, base_y + 40), lab, font=jp(34, True), fill=WHITE, anchor="mm")
        d.line((x0 + 60, base_y, x1 - 60, base_y), fill=WHITE, width=3)
        d.text((x0 + 60, y0 + 20), fig.get("unit", ""), font=jp(28, True), fill=(180, 195, 240))
        for i, ln in enumerate(wrap(d, fig.get("caption", ""), jp(28, True), x1 - x0 - 100)):
            d.text(((x0 + x1) / 2, y1 - 30 + i * 34), ln, font=jp(28, True), fill=(200, 210, 240), anchor="mm")
    elif k == "cards":
        items = fig["items"]
        hh = (y1 - y0 - 40) / len(items)
        for i, (t, s) in enumerate(items):
            yy = y0 + 20 + i * hh
            d.rounded_rectangle((x0 + 40, yy, x1 - 40, yy + hh - 30), 24, fill=(255, 255, 255, 28), outline=GOLD, width=3)
            d.text((x0 + 80, yy + 26), t, font=jp(34, True), fill=GOLD)
            d.multiline_text((x0 + 80, yy + 80), s, font=jp(46), fill=WHITE, spacing=10)
    elif k == "timeline":
        items = fig["items"]
        ly = (y0 + y1) / 2 - 40
        d.line((x0 + 60, ly, x1 - 60, ly), fill=WHITE, width=6)
        for i, (yr, s) in enumerate(items):
            cx = x0 + 160 + i * (x1 - x0 - 320) / (len(items) - 1)
            plan = "計画" in s
            col = (150, 160, 200) if plan else GOLD
            d.ellipse((cx - 22, ly - 22, cx + 22, ly + 22), fill=col)
            d.text((cx, ly - 70), yr, font=num(64), fill=col, anchor="mm")
            d.multiline_text((cx, ly + 60), s, font=jp(32, True), fill=WHITE, anchor="ma", align="center", spacing=8)
    elif k == "summary":
        for i, s in enumerate(fig["items"]):
            yy = y0 + 30 + i * 112
            d.rounded_rectangle((x0 + 60, yy, x1 - 60, yy + 92), 20, fill=(255, 255, 255, 24))
            d.text((x0 + 110, yy + 46), "✓", font=jp(48), fill=GOLD, anchor="mm")
            d.text((x0 + 160, yy + 46), s, font=jp(46), fill=WHITE, anchor="lm")


def slide(bg, cfg, ch_i, ch):
    img = frame_base(bg, cfg, ch_i, ch)
    panel = (60, 130, W - 60, 800)
    lay = Image.new("RGBA", (W, H))
    ImageDraw.Draw(lay).rounded_rectangle(panel, 30, fill=(0, 0, 0, 90))
    img = Image.alpha_composite(img, lay)
    d = ImageDraw.Draw(img)
    if ch.get("bullets"):
        # 左: 箇条書き / 右: 図
        for i, b in enumerate(ch["bullets"]):
            yy = 190 + i * 140
            d.rounded_rectangle((100, yy, 112, yy + 70), 6, fill=GOLD)
            for j, ln in enumerate(wrap(d, b, jp(44), 760)):
                d.text((135, yy + 4 + j * 56), ln, font=jp(44), fill=WHITE)
        box = (920, 150, W - 80, 790)
    else:
        box = (100, 150, W - 100, 790)
    # 図は透明なレイヤーに描いてから重ねる（半透明の塗りを正しく合成するため）
    fl = Image.new("RGBA", (W, H))
    fig_area(fl, box, ch["fig"], cfg)
    return Image.alpha_composite(img, fl)


def with_line(sl, spk, text):
    img = sl.copy()
    lay = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(lay)
    name, col, _, _ = SPK[spk]
    d.rounded_rectangle((60, 830, W - 60, 1040), 28, fill=(255, 255, 255, 235), outline=col, width=8)
    # 話者アイコン（左右に配置。話している方を強調）
    for k, (nm, c, _, _) in SPK.items():
        cx = 150 if k == "Z" else W - 150
        active = k == spk
        rr = 70 if active else 54
        d.ellipse((cx - rr, 935 - rr, cx + rr, 935 + rr), fill=c + ((255,) if active else (110,)),
                  outline=WHITE, width=5 if active else 2)
        d.text((cx, 935), nm[0], font=jp(64 if active else 48), fill=WHITE, anchor="mm")
    d.rounded_rectangle((250, 800, 250 + d.textlength(name, font=jp(36)) + 60, 856), 18, fill=col)
    d.text((280, 828), name, font=jp(36), fill=WHITE, anchor="lm")
    f = jp(46, True)
    lines = wrap(d, text, f, W - 560)[:3]
    ty = 935 - (len(lines) * 58) / 2
    for i, ln in enumerate(lines):
        d.text((260, ty + i * 58), ln, font=f, fill=NAVY)
    return Image.alpha_composite(img, lay)


# ---- 音声 ------------------------------------------------------------------------
def tts(text, spk, path, host="http://127.0.0.1:50021"):
    _, _, sid, speed = SPK[spk]
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    q = json.loads(op.open(urllib.request.Request(
        f"{host}/audio_query?" + urllib.parse.urlencode({"text": text, "speaker": sid}), data=b"", method="POST")).read())
    q.update(speedScale=speed, intonationScale=1.2, prePhonemeLength=0.05, postPhonemeLength=0.1,
             outputSamplingRate=48000)
    open(path, "wb").write(op.open(urllib.request.Request(
        f"{host}/synthesis?speaker={sid}", data=json.dumps(q).encode(), method="POST",
        headers={"Content-Type": "application/json"})).read())
    return "/".join("".join(m["text"] for m in a["moras"]) for a in q["accent_phrases"])


def thumbnail(bg, cfg, path):
    img = Image.alpha_composite(bg.copy(), Image.new("RGBA", (W, H), (0, 0, 0, 60)))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 300), "量子コンピュータ", font=jp(190), fill=WHITE, anchor="mm", stroke_width=14, stroke_fill=NAVY)
    d.text((W / 2, 560), "いつ使える？", font=jp(220), fill=GOLD, anchor="mm", stroke_width=16, stroke_fill=NAVY)
    d.rounded_rectangle((W / 2 - 700, 760, W / 2 + 700, 900), 70, fill=(230, 60, 80))
    d.text((W / 2, 830), "2024〜2025年の最新研究で解説", font=jp(76), fill=WHITE, anchor="mm")
    for k, (nm, c, _, _) in SPK.items():
        cx = 170 if k == "Z" else W - 170
        d.ellipse((cx - 130, 900 - 130, cx + 130, 900 + 130), fill=c, outline=WHITE, width=8)
        d.text((cx, 900), nm[0], font=jp(130), fill=WHITE, anchor="mm")
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--no-tts", action="store_true")
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("cfg", a.script)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    here = os.path.dirname(os.path.abspath(a.script))
    vdir = os.path.join(here, "voicevox")
    os.makedirs(vdir, exist_ok=True)
    lines = [(ci, li, spk, disp, say or disp) for ci, ch in enumerate(cfg.CHAPTERS)
             for li, (spk, disp, say) in enumerate(ch["lines"])]
    if not a.no_tts:
        for f in os.listdir(vdir):
            os.remove(os.path.join(vdir, f))
        for n, (ci, li, spk, disp, say) in enumerate(lines):
            kana = tts(say, spk, os.path.join(vdir, f"{n:03d}_{spk}.wav"))
            print(f"{n:03d} {SPK[spk][0]}: {kana}")
    voices = [base.load_audio(os.path.join(vdir, f"{n:03d}_{l[2]}.wav"), base.VOICE_FX) for n, l in enumerate(lines)]

    tmp = tempfile.mkdtemp()
    bg = background()
    durs, chapter_starts, t = [], {}, 0.0
    concat = []
    slides = {}
    for n, ((ci, li, spk, disp, say), v) in enumerate(zip(lines, voices)):
        dur = len(v) / SR + 0.35 + (0.6 if li == len(cfg.CHAPTERS[ci]["lines"]) - 1 else 0)
        if li == 0:
            chapter_starts[ci] = t
        if ci not in slides:
            slides[ci] = slide(bg, cfg, ci, cfg.CHAPTERS[ci])
        p = os.path.join(tmp, f"f{n:03d}.png")
        with_line(slides[ci], spk, disp).convert("RGB").save(p)
        concat.append(f"file '{p}'\nduration {dur:.3f}")
        durs.append(dur)
        t += dur
    concat.append(f"file '{os.path.join(tmp, f'f{len(lines) - 1:03d}.png')}'")
    open(os.path.join(tmp, "list.txt"), "w").write("\n".join(concat) + "\n")
    total = t
    print(f"total {total / 60:.1f} min")

    # 音声: セリフを並べ、BGMを小さく重ねてダッキング
    music = base.bgm(total) * 0.6
    vo = np.zeros_like(music)
    pos = 0.0
    for v, dur in zip(voices, durs):
        s = int((pos + 0.1) * SR)
        vo[s:s + len(v)] += v[: max(0, len(vo) - s)]
        pos += dur
    env = np.convolve(np.abs(vo), np.ones(int(0.05 * SR)) / int(0.05 * SR), "same")
    active = np.convolve((env > 0.01).astype(float), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
    music *= 1 - 0.6 * np.clip(active * 1.5, 0, 1)
    mix = np.clip((vo * 0.9 + music) / max(1.0, np.abs(vo * 0.9 + music).max() / 0.95), -1, 1)
    wav = os.path.join(tmp, "mix.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

    out = os.path.join(here, cfg.OUT)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", os.path.join(tmp, "list.txt"), "-i", wav,
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-tune", "stillimage", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    thumbnail(bg, cfg, os.path.join(here, "thumbnail.png"))
    with open(os.path.join(here, "chapters.txt"), "w") as f:
        for ci, st in chapter_starts.items():
            f.write(f"{int(st // 60)}:{int(st % 60):02d} {cfg.CHAPTERS[ci]['title']}\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
