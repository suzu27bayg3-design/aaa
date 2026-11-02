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
    """1文字ずつ詰めて折り返す。句読点は行頭に置かず、英数字の単語（IBMなど）は途中で切らない"""
    import re
    lines, cur = [], ""
    for tok in re.findall(r"[A-Za-z0-9.,%^]+|\n|.", text):
        if tok == "\n":
            lines.append(cur); cur = ""; continue
        if d.textlength(cur + tok, font=font) > width and cur and tok not in "、。！？」）":
            lines.append(cur); cur = tok
        else:
            cur += tok
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
        chips = getattr(cfg, "TITLE_CHIPS", [("Google Willow", (66, 133, 244)), ("ノーベル物理学賞", GOLD),
                                             ("理研×富士通", (230, 80, 80)), ("耐量子暗号", (110, 200, 90))])
        cw = (W - 240) / len(chips)
        for i, (n, c) in enumerate(chips):
            bx = 120 + i * cw
            d.rounded_rectangle((bx + 10, 560, bx + cw - 10, 640), 40, outline=c, width=5, fill=(0, 0, 0, 120))
            d.text((bx + cw / 2, 600), n, font=jp(36, True), fill=WHITE, anchor="mm")
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
    elif k == "interfere":
        # 上: 山と山（強め合う）/ 下: 山と谷（打ち消し合う）
        hh = (y1 - y0) / 2
        for row, (lab, shift, col) in enumerate((("強め合う（正解）", 0.0, GOLD), ("打ち消し合う（不正解）", math.pi, (255, 120, 120)))):
            cy = y0 + hh * row + hh / 2 + 25
            xs = [x0 + 40 + i * (x1 - x0 - 80) / 300 for i in range(301)]
            a = [(x, cy - 37 * math.sin(i / 300 * 4 * math.pi)) for i, x in enumerate(xs)]
            b = [(x, cy - 37 * math.sin(i / 300 * 4 * math.pi + shift)) for i, x in enumerate(xs)]
            sm = [(x, cy - 75 * math.sin(i / 300 * 4 * math.pi) * (1 if shift == 0 else 0)) for i, x in enumerate(xs)]
            d.line(a, fill=(120, 170, 255, 170), width=3)
            d.line(b, fill=(170, 220, 255, 170), width=3)
            d.line(sm, fill=col, width=7)
            d.text((x0 + 40, cy - hh / 2 + 6), lab, font=jp(32, True), fill=col)
    elif k == "period":
        a, n = fig["a"], fig["n"]
        vals = [pow(a, x, n) for x in range(9)]
        cw = (x1 - x0 - 40) / len(vals)
        top = y0 + 30
        d.text((x0 + 20, top), f"{a}をx回かけて{n}で割った余り", font=jp(32, True), fill=(180, 195, 240))
        for i, v in enumerate(vals):
            cx = x0 + 20 + (i + 0.5) * cw
            d.text((cx, top + 80), f"x={i}", font=jp(26, True), fill=(180, 195, 240), anchor="mm")
            d.rounded_rectangle((cx - cw / 2 + 6, top + 110, cx + cw / 2 - 6, top + 200), 14,
                                fill=GOLD if v == 1 else (90, 130, 230), outline=WHITE, width=2)
            d.text((cx, top + 155), str(v), font=num(48), fill=NAVY if v == 1 else WHITE, anchor="mm")
        p = vals[1:].index(1) + 1
        for j in range(0, 8, p):
            bx0 = x0 + 20 + j * cw + 6
            d.line((bx0, top + 225, bx0 + p * cw - 12, top + 225), fill=GOLD, width=5)
        d.text(((x0 + x1) / 2, top + 260), f"周期 r = {p}", font=jp(40, True), fill=GOLD, anchor="mm")
        h = pow(a, p // 2)
        d.text(((x0 + x1) / 2, top + 330), f"{a}^{p // 2} = {h} → {h - 1} と {h + 1}", font=jp(36, True), fill=WHITE, anchor="mm")
        g1, g2 = math.gcd(h - 1, n), math.gcd(h + 1, n)
        d.text(((x0 + x1) / 2, top + 390), f"{n}との最大公約数 → {g1} と {g2}（{n} = {g1} × {g2}）",
               font=jp(36, True), fill=GOLD, anchor="mm")
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
            small = hh < 190
            d.text((x0 + 80, yy + (10 if small else 26)), t, font=jp(28 if small else 34, True), fill=GOLD)
            d.multiline_text((x0 + 80, yy + (48 if small else 80)), s, font=jp(29 if small else 46), fill=WHITE,
                             spacing=4 if small else 10)
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
    elif k == "platform":
        # 方式ごとの簡単なイラスト（上）と数字のチップ（下）
        cx, top = (x0 + x1) / 2, y0 + 20
        ih = 300
        st = fig["style"]
        if st == "sc":  # 冷凍機の中のチップ
            for i, wdt in enumerate((300, 250, 200, 150)):
                yy = top + 10 + i * 62
                d.rounded_rectangle((cx - wdt / 2, yy, cx + wdt / 2, yy + 46), 10, fill=(200, 170, 90, 200 - i * 25),
                                    outline=(255, 220, 140), width=2)
            for i in range(9):
                d.line((cx - 60 + i * 15, top + 56, cx - 60 + i * 15, top + 250), fill=(150, 220, 255, 160), width=2)
            d.rounded_rectangle((cx - 70, top + 250, cx + 70, top + 290), 6, fill=(90, 130, 230), outline=WHITE, width=3)
            for i in range(5):
                d.rectangle((cx - 55 + i * 25, top + 260, cx - 42 + i * 25, top + 280), fill=GOLD)
            d.text((cx + 170, top + 270), "チップ", font=jp(28, True), fill=WHITE, anchor="lm")
            d.text((cx + 170, top + 40), "冷凍機", font=jp(28, True), fill=WHITE, anchor="lm")
        elif st == "ion":  # 電極の間に浮かぶイオンの列
            for yy in (top + 90, top + 230):
                d.rounded_rectangle((x0 + 60, yy - 18, x1 - 60, yy + 18), 10, fill=(170, 175, 190))
            for i in range(9):
                ax = x0 + 110 + i * (x1 - x0 - 220) / 8
                d.ellipse((ax - 20, top + 140, ax + 20, top + 180), fill=(255, 120, 120), outline=WHITE, width=3)
                d.text((ax, top + 160), "+", font=jp(26, True), fill=WHITE, anchor="mm")
            d.line((x0 + 110, top + 20, x0 + 110 + 3 * (x1 - x0 - 220) / 8, top + 160), fill=(120, 255, 160), width=5)
            d.text((x0 + 70, top + 20), "レーザー", font=jp(26, True), fill=(120, 255, 160), anchor="lm")
            d.text((cx, top + 290), "電極（電場でイオンを浮かせる）", font=jp(28, True), fill=WHITE, anchor="mm")
        elif st == "atom":  # 光ピンセットでつかんだ原子の格子
            for r in range(5):
                for c in range(11):
                    ax = x0 + 90 + c * (x1 - x0 - 180) / 10
                    ay = top + 30 + r * 55
                    d.ellipse((ax - 24, ay - 24, ax + 24, ay + 24), fill=(255, 200, 60, 40))
                    if (r * 11 + c) % 13 != 5:
                        d.ellipse((ax - 11, ay - 11, ax + 11, ay + 11), fill=GOLD)
            d.text((cx, top + 290), "光ピンセット1本に原子1個", font=jp(28, True), fill=WHITE, anchor="mm")
        elif st == "photon":  # 光ファイバーを進む光の波
            for j, col in enumerate(((120, 220, 255), (255, 140, 200))):
                cy = top + 90 + j * 120
                d.rounded_rectangle((x0 + 50, cy - 40, x1 - 50, cy + 40), 40, outline=(120, 140, 200), width=3)
                pts = [(x0 + 70 + i * 2, cy - 25 * math.sin(i / 14 + j)) for i in range(int((x1 - x0 - 140) / 2))]
                d.line(pts, fill=col, width=5)
            d.text((cx, top + 290), "光の粒・光の波を量子ビットに", font=jp(28, True), fill=WHITE, anchor="mm")
        cw = (x1 - x0 - 40) / len(fig["stats"])
        for i, (lab, val) in enumerate(fig["stats"]):
            bx = x0 + 20 + i * cw
            d.rounded_rectangle((bx + 8, top + ih + 40, bx + cw - 8, top + ih + 170), 18, fill=(255, 255, 255, 30),
                                outline=GOLD, width=3)
            d.text((bx + cw / 2, top + ih + 75), lab, font=jp(24, True), fill=(200, 210, 240), anchor="mm")
            d.text((bx + cw / 2, top + ih + 125), val, font=jp(30 if len(val) < 9 else 24, True), fill=WHITE, anchor="mm")
    elif k == "table":
        head, rows = fig["head"], fig["rows"]
        cols = [x0 + 30, x0 + 330, x0 + 960, x1 - 30]
        rh = (y1 - y0 - 100) / len(rows)
        d.rounded_rectangle((cols[0], y0 + 10, cols[-1], y0 + 80), 16, fill=(66, 133, 244, 200))
        for j, h in enumerate(head):
            d.text(((cols[j] + cols[j + 1]) / 2, y0 + 45), h, font=jp(36, True), fill=WHITE, anchor="mm")
        for i, row in enumerate(rows):
            yy = y0 + 95 + i * rh
            d.rounded_rectangle((cols[0], yy, cols[-1], yy + rh - 12), 14, fill=(255, 255, 255, 22 if i % 2 else 36))
            for j, cell in enumerate(row):
                d.text(((cols[j] + cols[j + 1]) / 2, yy + (rh - 12) / 2), cell, font=jp(34 if j == 0 else 31, True),
                       fill=GOLD if j == 0 else WHITE, anchor="mm")
    elif k == "summary":
        for i, s in enumerate(fig["items"]):
            gap = min(112, (y1 - y0 - 30) / len(fig["items"]))  # 立ち絵ワイプと重ならないよう詰める
            yy = y0 + 20 + i * gap
            d.rounded_rectangle((x0 + 60, yy, x1 - 60, yy + gap - 16), 20, fill=(255, 255, 255, 24))
            d.text((x0 + 110, yy + (gap - 16) / 2), "✓", font=jp(46), fill=GOLD, anchor="mm")
            d.text((x0 + 160, yy + (gap - 16) / 2), s, font=jp(44), fill=WHITE, anchor="lm")


def slide(bg, cfg, ch_i, ch):
    img = frame_base(bg, cfg, ch_i, ch)
    panel = (60, 130, W - 60, 800)
    lay = Image.new("RGBA", (W, H))
    ImageDraw.Draw(lay).rounded_rectangle(panel, 30, fill=(0, 0, 0, 90))
    img = Image.alpha_composite(img, lay)
    d = ImageDraw.Draw(img)
    has_port = bool(portraits("Z")) or bool(portraits("M"))
    bottom = 680 if has_port else 790  # 立ち絵ワイプと重ならないよう、図の下端を上げる
    if ch.get("bullets"):
        # 左: 箇条書き / 右: 図
        for i, b in enumerate(ch["bullets"]):
            yy = 175 + i * (120 if has_port else 140)
            d.rounded_rectangle((100, yy, 112, yy + 70), 6, fill=GOLD)
            bf = jp(40) if has_port else jp(44)
            for j, ln in enumerate(wrap(d, b, bf, 760)):
                d.text((135, yy + 4 + j * 50), ln, font=bf, fill=WHITE)
        box = (920, 150, W - 80, bottom)
    else:
        box = (100, 150, W - 100, bottom)
    # 図は透明なレイヤーに描いてから重ねる（半透明の塗りを正しく合成するため）
    fl = Image.new("RGBA", (W, H))
    fig_area(fl, box, ch["fig"], cfg)
    return Image.alpha_composite(img, fl)


# ---- 立ち絵（assets/characters/<名前>/<表情>.png があれば使う） ------------------------
CHAR_DIR = {"Z": "zundamon", "M": "metan"}
_PORT = {}


def portraits(spk):
    """話者の立ち絵を {表情: {目口: RGBA画像}} で返す（枠の幅に合わせて縮小済み）。
    ファイル名は <表情>__<目o|c><口0|1|2>.png（tools/psd_parts.py が書き出す）。
    目口の指定がない <表情>.png は「目を開けて口を閉じた絵」として扱う。"""
    if spk not in _PORT:
        d = os.path.join(ROOT, "assets", "characters", CHAR_DIR[spk])
        out = {}
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.endswith(".png"):
                    ex, _, var = f[:-4].partition("__")
                    im = Image.open(os.path.join(d, f)).convert("RGBA")
                    sc = PW / im.width
                    out.setdefault(ex, {})[var or "o0"] = im.resize((PW, int(im.height * sc)), Image.LANCZOS)
        _PORT[spk] = out
    return _PORT[spk]


def face(spk, ex, eye_closed=False, mouth=0):
    """表情・まばたき・口の開き(0〜2)に合う絵を選ぶ。無い組み合わせは近いもので代用"""
    vs = portraits(spk)[ex]
    for key in (f"{'c' if eye_closed else 'o'}{mouth}", f"o{mouth}", f"o{min(mouth, 1)}", "o0"):
        if key in vs:
            return vs[key]
    return next(iter(vs.values()))


def blinking(spk, t):
    """まばたき: 話者ごとに少しずらした周期で、0.1秒だけ目を閉じる"""
    period = 3.7 if spk == "Z" else 4.3
    return (t + (0.0 if spk == "Z" else 1.6)) % period < 0.1


def subtitle_pages(text):
    """字幕が3行を超える場合のページ分け。各ページの文字数を返す（表示時間の配分に使う）"""
    use_port = bool(portraits("Z")) or bool(portraits("M"))
    bx0, bx1 = (360, W - 360) if use_port else (60, W - 60)
    tx = bx0 + 40 if use_port else 260
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    ls = wrap(d, text, jp(46, True), bx1 - tx - 40)
    return [sum(len(x) for x in ls[i:i + 3]) for i in range(0, len(ls), 3)]


def expression(spk, text, tag=None):
    """表情の選び方: 台本の指定 > 文末の記号から推定 > 既定"""
    ex = portraits(spk)
    if not ex:
        return None
    if tag in ex:
        return tag
    if "……" in text and "panic" in ex:
        return "panic"
    if text.endswith("！") and "smug" in ex and spk == "Z":
        return "smug"
    if spk == "M" and len(text) >= 45 and "explain" in ex:
        return "explain"  # 長い説明のときは指差しポーズ
    return "happy" if "happy" in ex else next(iter(ex))


PW, PH = 290, 340  # 立ち絵ワイプの大きさ


def with_line(sl, spk, text, expr=None, mouth=0, page=0, blink=()):
    img = sl.copy()
    lay = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(lay)
    name, col, _, _ = SPK[spk]
    use_port = bool(portraits("Z")) or bool(portraits("M"))
    bx0, bx1 = (360, W - 360) if use_port else (60, W - 60)
    d.rounded_rectangle((bx0, 830, bx1, 1040), 28, fill=(255, 255, 255, 235), outline=col, width=8)
    for k, (nm, c, _, _) in SPK.items():
        active = k == spk
        ex = portraits(k)
        if ex:
            # 立ち絵ワイプ: 話している方は明るく、声に合わせて口が動く
            x0 = 40 if k == "Z" else W - 40 - PW
            y0 = 700
            win = Image.new("RGBA", (PW, PH), c + (255,))
            wd = ImageDraw.Draw(win)
            for yy in range(PH):
                wd.line((0, yy, PW, yy), fill=tuple(int(v * (0.55 + 0.45 * yy / PH)) for v in c) + (255,))
            e = face(k, expression(k, "", None) if not active else (expr or expression(k, text)),
                     k in blink, mouth if active else 0)
            win.alpha_composite(e, (0, max(0, PH - e.height) if e.height < PH else 0))
            if not active:
                win = Image.alpha_composite(win, Image.new("RGBA", (PW, PH), (0, 0, 0, 120)))
            m = Image.new("L", (PW, PH), 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, PW - 1, PH - 1), 36, fill=255)
            lay.paste(win, (x0, y0), m)
            d.rounded_rectangle((x0, y0, x0 + PW, y0 + PH), 36, outline=WHITE if active else (150, 150, 170),
                                width=6 if active else 3)
            d.rounded_rectangle((x0 + 20, y0 + PH - 58, x0 + PW - 20, y0 + PH - 12), 16, fill=c)
            d.text((x0 + PW / 2, y0 + PH - 35), nm, font=jp(30), fill=WHITE, anchor="mm")
        else:
            cx = 150 if k == "Z" else W - 150
            rr = 70 if active else 54
            d.ellipse((cx - rr, 935 - rr, cx + rr, 935 + rr), fill=c + ((255,) if active else (110,)),
                      outline=WHITE, width=5 if active else 2)
            d.text((cx, 935), nm[0], font=jp(64 if active else 48), fill=WHITE, anchor="mm")
    tx = bx0 + 40 if use_port else 260
    d.rounded_rectangle((tx - 10, 800, tx - 10 + d.textlength(name, font=jp(36)) + 60, 856), 18, fill=col)
    d.text((tx + 20, 828), name, font=jp(36), fill=WHITE, anchor="lm")
    f = jp(46, True)
    lines = wrap(d, text, f, bx1 - tx - 40)[page * 3: page * 3 + 3]
    ty = 935 - (len(lines) * 58) / 2
    for i, ln in enumerate(lines):
        d.text((tx, ty + i * 58), ln, font=f, fill=NAVY)
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
    # 立ち絵（先に描いて、文字を上に重ねる）
    for k, (nm, c, _, _) in SPK.items():
        ex = portraits(k)
        if not ex:
            continue
        want = getattr(cfg, "THUMB_FACE", {}).get(k, "happy")
        e = face(k, want if want in ex else ("happy" if "happy" in ex else next(iter(ex))))
        cw = 470
        e = e.resize((cw, int(e.height * cw / e.width)), Image.LANCZOS)
        e = e.crop((0, 0, cw, min(e.height, 600)))
        if k == "Z":  # 素材の切り抜き端（右側の尻尾）が直線で切れて見えないよう、右端をフェード
            a = np.array(e.split()[3], dtype=float)
            fw = 90
            a[:, -fw:] *= np.linspace(1, 0, fw)[None, :]
            e.putalpha(Image.fromarray(a.astype(np.uint8)))
        img.alpha_composite(e, (-20 if k == "Z" else W - cw + 20, H - e.height))
    d = ImageDraw.Draw(img)
    t1, t2, badge = getattr(cfg, "THUMB", ("量子コンピュータ", "いつ使える？", "2024〜2025年の最新研究で解説"))
    d.text((W / 2, 290), t1, font=jp(190), fill=WHITE, anchor="mm", stroke_width=14, stroke_fill=NAVY)
    d.text((W / 2, 540), t2, font=jp(220), fill=GOLD, anchor="mm", stroke_width=16, stroke_fill=NAVY)
    bw = d.textlength(badge, font=jp(66)) / 2 + 70
    d.rounded_rectangle((W / 2 - bw, 740, W / 2 + bw, 860), 60, fill=(230, 60, 80), outline=WHITE, width=6)
    d.text((W / 2, 800), badge, font=jp(66), fill=WHITE, anchor="mm")
    tag = getattr(cfg, "THUMB_TAG", None)
    if tag:  # シリーズ番号（左上）
        tw = d.textlength(tag, font=jp(56)) + 70
        d.rounded_rectangle((40, 40, 40 + tw, 140), 24, fill=(66, 133, 244), outline=WHITE, width=5)
        d.text((40 + tw / 2, 90), tag, font=jp(56), fill=WHITE, anchor="mm")
    if not portraits("Z"):
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
    lines = [(ci, li, row[0], row[1], row[2] or row[1]) for ci, ch in enumerate(cfg.CHAPTERS)
             for li, row in enumerate(ch["lines"])]
    tags = [row[3] if len(row) > 3 else None for ch in cfg.CHAPTERS for row in ch["lines"]]
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
        ex = expression(spk, disp, tags[n])
        pages = subtitle_pages(disp)
        bounds = np.cumsum([0] + pages) / sum(pages) * (dur - 0.3)  # ページの切り替え時刻
        cache = {}

        def img(page, mouth, blink):
            k = (page, mouth, blink)
            if k not in cache:
                cache[k] = os.path.join(tmp, f"f{n:03d}_{page}_{mouth}_{''.join(blink)}.png")
                with_line(slides[ci], spk, disp, ex, mouth, page, blink).convert("RGB").save(cache[k])
            return cache[k]
        # 0.1秒ごとに「どのページを出すか」「口をどれだけ開けるか」「まばたき中か」を決める
        # 口の開きは、その0.1秒の声の大きさ（RMS = 二乗平均の平方根）で3段階に分ける
        step, tt, prev = 0.1, 0.0, None
        while tt < dur - 1e-6:
            page = max(0, min(len(pages) - 1, int(np.searchsorted(bounds, tt, side="right")) - 1))
            seg = v[int(max(0, tt - 0.1) * SR): int(max(0, tt - 0.1 + step) * SR)]
            rms = float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0
            mouth = 0 if rms < 0.025 else (1 if rms < 0.07 else 2)
            blink = tuple(k for k in SPK if portraits(k) and blinking(k, t + tt))
            cur = img(page, mouth if portraits(spk) else 0, blink)
            dd = min(step, dur - tt)
            if cur == prev:
                concat[-1] = concat[-1].rsplit("duration", 1)[0] + f"duration {float(concat[-1].rsplit(' ', 1)[1]) + dd:.3f}"
            else:
                concat.append(f"file '{cur}'\nduration {dd:.3f}")
            prev = cur
            tt += step
        last_img = prev
        durs.append(dur)
        t += dur
    concat.append(f"file '{last_img}'")
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
