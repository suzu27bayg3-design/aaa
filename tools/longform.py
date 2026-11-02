#!/usr/bin/env python3
"""ずんだもん×四国めたんの掛け合い解説動画（横長1920x1080）ジェネレーター

使い方:
  bash tools/voicevox_engine.sh
  python3 tools/longform.py longform_quantum/script.py            # 音声生成 + 動画
  python3 tools/longform.py longform_quantum/script.py --no-tts   # 既存音声で動画のみ

仕組み: 1秒に FPS 枚のコマを描いて ffmpeg に流し込む。
  - 図は章の経過時間に合わせて動く（項目が順に出る・棒グラフが伸びる・年表が左から描かれる・波や針が動く）
  - 立ち絵は声の大きさで口が動き、ときどきまばたきする
  - カードには見出しの言葉から選んだアイコンを付ける
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
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

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
FPS = 15  # 動画のコマ数（1秒あたり）。図のアニメーションと口パクをこの間隔で描く
ANIM_T = None  # 章の中の経過秒。None なら止め絵（サムネイルやプレビュー用）
# 時間とともに動き続ける図（毎コマ描き直す）
LIVE_KINDS = {"qubit", "interfere", "noise", "dial", "tower", "pair", "teleport", "landscape", "repeater",
              "pipeline", "platform"}


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


EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
# カードの見出しの言葉から、そえるアイコン（絵文字）を選ぶ。上から順に最初に当てはまったもの
ICON_RULES = [
    ("もつれ", "🔗"), ("つながり", "🔗"), ("かけ算", "🧮"), ("機械", "🖥️"), ("暗号", "🔐"), ("鍵", "🔑"), ("盗", "🕵️"), ("時計", "⏱️"), ("秒", "⏱️"), ("光", "💡"), ("レーザー", "💡"),
    ("原子", "⚛️"), ("イオン", "⚛️"), ("冷", "❄️"), ("超伝導", "❄️"), ("速", "⚡"), ("証明", "📜"), ("論文", "📜"),
    ("実験", "🧪"), ("AI", "🤖"), ("GPS", "🧭"), ("位置", "🧭"), ("地図", "🧭"), ("心臓", "🏥"), ("医療", "🏥"),
    ("病院", "🏥"), ("費用", "💰"), ("お金", "💰"), ("距離", "📏"), ("中継", "📡"), ("通信", "📡"), ("衛星", "🛰️"),
    ("日本", "🗾"), ("国", "🏛️"), ("データ", "💾"), ("計算", "🧮"), ("ノーベル", "🏅"), ("受賞", "🏅"), ("理由", "💭"),
    ("しくみ", "⚙️"), ("仕組み", "⚙️"), ("方法", "⚙️"), ("課題", "⚠️"), ("弱点", "⚠️"), ("難し", "⚠️"), ("反論", "🗣️"),
    ("主張", "📣"), ("結果", "📊"), ("応用", "🚀"), ("できる", "🚀"), ("期待", "🚀"), ("なぜ", "❓"), ("とは", "❓"),
    ("たとえ", "🧤"), ("手袋", "🧤"), ("考え", "💭"), ("強み", "💪"), ("例", "🔍"), ("条件", "✅"), ("①", "1️⃣"),
    ("②", "2️⃣"), ("③", "3️⃣"), ("スマホ", "📱"), ("薬", "💊"), ("電池", "🔋"), ("肥料", "🌱"), ("ダイヤモンド", "💎"),
]
_EMO = {}


def icon_img(ch, size):
    """絵文字を画像にする（カラー絵文字フォントは109pxで描いて縮小する）"""
    k = (ch, size)
    if k not in _EMO:
        im = Image.new("RGBA", (160, 160))
        ImageDraw.Draw(im).text((80, 80), ch, font=ImageFont.truetype(EMOJI, 109), embedded_color=True, anchor="mm")
        bb = im.getbbox()
        im = im.crop(bb) if bb else im
        sc = size / max(im.size)
        _EMO[k] = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    return _EMO[k]


def pick_icon(title):
    for kw, ic in ICON_RULES:
        if kw in title:
            return ic
    return "💡"


def _kind(c):
    if "\u3041" <= c <= "\u309f":
        return "h"  # ひらがな
    if c in "、。・，．）」』！？：；…" or c == " ":
        return "p"  # 区切りの記号
    return "o"


def chunks(text):
    """改行してよい位置で文字列を区切る（日本語の文節のおおまかな切れ目）
    ・ひらがな（助詞など）の次に、ひらがな以外が来るところ
    ・読点や「・」などの記号のあと
    ・カタカナの語、英数字の語、数字と単位はまとめて1つにする"""
    out, cur = [], ""
    for i, c in enumerate(text):
        if cur:
            prev = cur[-1]
            kp, kc = _kind(prev), _kind(c)
            hrun = len(cur) - len(cur.rstrip("\u3041\u3042\u3043\u3044\u3045\u3046\u3047\u3048\u3049\u304a"
                                                 + "".join(chr(x) for x in range(0x304b, 0x309f))))
            # ひらがな1文字だけ（「動き始める」の「き」など送りがな）のあとは、助詞でなければ切らない
            okuri = kp == "h" and hrun == 1 and prev not in "はがをにでとのもへやかねよ"
            close_h = prev in "」』）" and kc == "h"  # 「周期」を のように、閉じかっこの後の助詞は切り離さない
            brk = (kp == "p" and kc != "p" and not close_h) or (kp == "h" and kc not in ("h", "p") and not okuri) \
                or c in "（「『"
            if brk:
                out.append(cur)
                cur = ""
        cur += c
    if cur:
        out.append(cur)
    return out


def wrap(d, text, font, width):
    """文節の切れ目で折り返す。1つの文節が長すぎるときだけ文字の途中で折り返す。
    句読点や閉じかっこは行頭に置かない"""
    lines, cur = [], ""
    for para_i, para in enumerate(text.split("\n")):
        if para_i:
            lines.append(cur); cur = ""
        for tok in chunks(para):
            if d.textlength(cur + tok, font=font) <= width or not cur:
                if d.textlength(cur + tok, font=font) <= width:
                    cur += tok
                    continue
            if cur and d.textlength(tok, font=font) <= width:
                lines.append(cur); cur = tok
                continue
            for ch in tok:  # 長すぎる文節は文字単位で
                if d.textlength(cur + ch, font=font) > width and cur and ch not in "、。！？」）・":
                    lines.append(cur); cur = ch
                else:
                    cur += ch
    lines.append(cur)
    return lines


def fit_size(d, texts, box_w, box_h, start, smallest, bold=False, spacing=0.25, max_lines=9):
    """複数の文字列が、どれも同じ大きさで枠に収まる一番大きな文字サイズ（図の中で大きさをそろえる）"""
    for size in range(start, smallest - 1, -1):
        f = jp(size, bold)
        lh = int(size * (1 + spacing))
        ok = True
        for t in texts:
            ls = wrap(d, t, f, box_w)
            if len(ls) > max_lines or len(ls) * lh > box_h or any(d.textlength(l, font=f) > box_w for l in ls):
                ok = False
                break
        if ok:
            return size
    return smallest


def fit_text(d, text, box_w, box_h, start, smallest, bold=False, spacing=0.25):
    """枠（幅 box_w・高さ box_h）に収まる一番大きな文字サイズで折り返す。(フォント, 行, 行の高さ) を返す"""
    for size in range(start, smallest - 1, -2):
        f = jp(size, bold)
        lines = wrap(d, text, f, box_w)
        lh = int(size * (1 + spacing))
        if len(lines) * lh <= box_h and all(d.textlength(l, font=f) <= box_w for l in lines):
            return f, lines, lh
    f = jp(smallest, bold)
    return f, wrap(d, text, f, box_w), int(smallest * (1 + spacing))


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
    T = ANIM_T  # 章の中の経過秒（None なら止め絵）
    if k == "title":
        d.text((W / 2, 330), cfg.TITLE, font=jp(96), fill=WHITE, anchor="mm", stroke_width=6, stroke_fill=NAVY)
        d.text((W / 2, 460), cfg.SUBTITLE, font=jp(54, True), fill=GOLD, anchor="mm")
        chips = getattr(cfg, "TITLE_CHIPS", [("Google Willow", (66, 133, 244)), ("ノーベル物理学賞", GOLD),
                                             ("理研×富士通", (230, 80, 80)), ("耐量子暗号", (110, 200, 90))])
        fig["chips"] = chips
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
            on = T is not None and int(T) % 2 == i
            d.rounded_rectangle((cx - 65, cy - 65, cx + 65, cy + 65), 18, fill=(200, 150, 40) if on else (60, 70, 110),
                                outline=WHITE, width=4)
            d.text((cx, cy), v, font=num(90), fill=WHITE, anchor="mm")
        d.text((x0 + 205, cy + 120), "ビット：どちらか一方", font=jp(34, True), fill=WHITE, anchor="mm")
        # 量子ビット（球と矢印）
        cx, r = x1 - 230, 170
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(150, 190, 255), width=5)
        d.ellipse((cx - r, cy - r * 0.3, cx + r, cy + r * 0.3), outline=(150, 190, 255, 140), width=3)
        d.text((cx, cy - r - 36), "0", font=num(48), fill=WHITE, anchor="mm")
        d.text((cx, cy + r + 36), "1", font=num(48), fill=WHITE, anchor="mm")
        if T is None:
            ax, ay = cx + r * 0.75 * math.cos(math.radians(-35)), cy + r * 0.75 * math.sin(math.radians(-35))
        else:  # 重ね合わせの状態（矢印）がくるくる回る
            th, ph = math.radians(55 + 25 * math.sin(T * 0.7)), T * 1.4
            ax = cx + r * 0.85 * math.sin(th) * math.cos(ph)
            ay = cy - r * 0.85 * math.cos(th) + r * 0.85 * math.sin(th) * math.sin(ph) * 0.3
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
            ph = (T or 0) * 2.5
            wa = [math.sin(i / 300 * 4 * math.pi - ph) for i in range(301)]
            wb = [math.sin(i / 300 * 4 * math.pi - ph + shift) for i in range(301)]
            a = [(x, cy - 37 * wa[i]) for i, x in enumerate(xs)]
            b = [(x, cy - 37 * wb[i]) for i, x in enumerate(xs)]
            sm = [(x, cy - 37 * (wa[i] + wb[i])) for i, x in enumerate(xs)]
            d.line(a, fill=(120, 170, 255, 170), width=3)
            d.line(b, fill=(170, 220, 255, 170), width=3)
            d.line(sm, fill=col, width=7)
            d.text((x0 + 40, cy - hh / 2 + 6), lab, font=jp(32, True), fill=col)
    elif k == "period":
        a, n = fig["a"], fig["n"]
        vals = [pow(a, x, n) for x in range(9)]
        cw = (x1 - x0 - 40) / len(vals)
        top = y0 + 30
        d.text((x0 + 20, top - 6), f"{a}をx回かけて{n}で割った余り", font=jp(34, True), fill=(180, 195, 240))
        for i, v in enumerate(vals):
            cx = x0 + 20 + (i + 0.5) * cw
            d.text((cx, top + 80), f"x={i}", font=jp(28, True), fill=(180, 195, 240), anchor="mm")
            d.rounded_rectangle((cx - cw / 2 + 6, top + 110, cx + cw / 2 - 6, top + 200), 14,
                                fill=GOLD if v == 1 else (90, 130, 230), outline=WHITE, width=2)
            d.text((cx, top + 155), str(v), font=num(48), fill=NAVY if v == 1 else WHITE, anchor="mm")
        p = vals[1:].index(1) + 1
        for j in range(0, 8, p):
            bx0 = x0 + 20 + j * cw + 6
            d.line((bx0, top + 225, bx0 + p * cw - 12, top + 225), fill=GOLD, width=5)
        d.text(((x0 + x1) / 2, top + 262), f"周期 r = {p}", font=jp(46, True), fill=GOLD, anchor="mm")
        h = pow(a, p // 2)
        d.text(((x0 + x1) / 2, top + 336), f"{a}^{p // 2} = {h} → {h - 1} と {h + 1}", font=jp(40, True), fill=WHITE, anchor="mm")
        g1, g2 = math.gcd(h - 1, n), math.gcd(h + 1, n)
        d.text(((x0 + x1) / 2, top + 400), f"{n}との最大公約数 → {g1} と {g2}（{n} = {g1} × {g2}）",
               font=jp(38, True), fill=GOLD, anchor="mm")
    elif k == "noise":
        cy = (y0 + y1) / 2 - 40
        pts_c, pts_n = [], []
        rng = np.random.default_rng(1 + int((T or 0) * FPS) % 997)
        ph = (T or 0) * 3
        for i in range(400):
            x = x0 + 40 + i * (x1 - x0 - 80) / 400
            t = i / 400
            pts_c.append((x, cy - 120 + 70 * math.sin(t * 18 - ph)))
            pts_n.append((x, cy + 140 + 70 * math.sin(t * 18 - ph) * math.exp(-3 * t) + rng.normal(0, 4 + 30 * t)))
        d.line(pts_c, fill=(120, 200, 255), width=6)
        d.line(pts_n, fill=(255, 110, 110), width=5)
        d.text((x0 + 40, cy - 230), "理想：量子状態が保たれる", font=jp(34, True), fill=(120, 200, 255))
        d.text((x0 + 40, cy + 30), "現実：ノイズで状態が壊れる（デコヒーレンス）", font=jp(34, True), fill=(255, 130, 130))
    elif k == "bars":
        items = fig["items"]
        vmax = max(v for _, v, _ in items)
        bw = min(220, (x1 - x0 - 120) / len(items) - 60)
        base_y = y1 - 120
        for i, (lab, v, txt) in enumerate(items):
            cx = x0 + 100 + (i + 0.5) * (x1 - x0 - 200) / len(items)
            hgt = max(8, (base_y - y0 - 120) * v / vmax)
            d.rounded_rectangle((cx - bw / 2, base_y - hgt, cx + bw / 2, base_y), 14,
                                fill=GOLD if i == len(items) - 1 else (110, 150, 255))
            d.text((cx, base_y - hgt - 44), txt, font=jp(50), fill=WHITE, anchor="mm")
            if i == 0:
                bl_sz = fit_size(d, [it[0] for it in items], (x1 - x0 - 200) / len(items) + 30, 46, 38, 20, bold=True)
            lf, ll, lh = fit_text(d, lab, (x1 - x0 - 200) / len(items) + 30, 46, bl_sz, bl_sz, bold=True)
            for j, ln in enumerate(ll[:1]):
                d.text((cx, base_y + 14 + j * lh), ln, font=lf, fill=WHITE, anchor="ma")
        d.line((x0 + 60, base_y, x1 - 60, base_y), fill=WHITE, width=3)
        d.text((x0 + 60, y0 + 14), fig.get("unit", ""), font=jp(30, True), fill=(180, 195, 240))
        cf, cl, clh = fit_text(d, fig.get("caption", ""), x1 - x0 - 40, 60, 30, 20, bold=True, spacing=0.15)
        for i, ln in enumerate(cl):
            d.text(((x0 + x1) / 2, y1 - 40 + i * clh), ln, font=cf, fill=(200, 210, 240), anchor="mm")
    elif k == "cards":
        items = fig["items"]
        n = len(items)
        gapc = 18
        hh = (y1 - y0 - 10 - gapc * (n - 1)) / n
        isz0 = int(min(hh * 0.62, 120))
        tw0 = x1 - 70 - (x0 + 75 + isz0 + 40)
        tsz = int(min(36, max(26, hh * 0.18)))
        bsz = fit_size(d, [it[1].replace("\n", "") for it in items], tw0, hh - tsz * 1.25 - 44, 48, 24, spacing=0.22)
        for i, it in enumerate(items):
            t, s_ = it[0], it[1]
            yy = y0 + 5 + i * (hh + gapc)
            d.rounded_rectangle((x0 + 40, yy, x1 - 40, yy + hh), 24, fill=(255, 255, 255, 28), outline=GOLD, width=3)
            # 左にアイコン（見出しの言葉から自動で選ぶ。3つ目の要素があればそれを使う）
            isz = int(min(hh * 0.62, 120))
            ic = icon_img(it[2] if len(it) > 2 else pick_icon(t), isz)
            icx, cyc = x0 + 75, yy + hh / 2
            d.ellipse((icx - 10, cyc - isz / 2 - 10, icx + isz + 10, cyc + isz / 2 + 10), fill=(255, 255, 255, 34))
            img.alpha_composite(ic, (int(icx + (isz - ic.width) / 2), int(cyc - ic.height / 2)))
            tx = icx + isz + 40
            tw = x1 - 70 - tx
            tf = jp(tsz, True)
            th = tf.size * 1.25
            bf, bl, lh = fit_text(d, s_.replace("\n", ""), tw, hh - th - 44, bsz, bsz, spacing=0.22)
            block = th + len(bl) * lh
            ty = cyc - block / 2
            d.text((tx, ty), t, font=tf, fill=GOLD)
            for j, ln in enumerate(bl):
                d.text((tx, ty + th + j * lh), ln, font=bf, fill=WHITE)
    elif k == "timeline":
        items = fig["items"]
        ly = (y0 + y1) / 2 - 70
        d.line((x0 + 60, ly, x1 - 60, ly), fill=WHITE, width=6)
        for i, (yr, s) in enumerate(items):
            cx = x0 + 160 + i * (x1 - x0 - 320) / (len(items) - 1)
            plan = "計画" in s
            col = (150, 160, 200) if plan else GOLD
            d.ellipse((cx - 24, ly - 24, cx + 24, ly + 24), fill=col)
            d.text((cx, ly - 80), yr, font=num(80 if len(items) <= 4 else 66), fill=col, anchor="mm")
            colw = (x1 - x0 - 320) / max(1, len(items) - 1) - 20
            if i == 0:
                tl_sz = fit_size(d, [it[1] for it in items], colw, y1 - ly - 70, 40 if len(items) <= 4 else 34, 22,
                                 bold=True)
            lf, ll, lh = fit_text(d, s, colw, y1 - ly - 70, tl_sz, tl_sz, bold=True)
            for j, ln in enumerate(ll):
                d.text((cx, ly + 56 + j * lh), ln, font=lf, fill=WHITE, anchor="ma")
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
                if T is not None:  # 配線を流れるマイクロ波の信号
                    yy = top + 56 + ((T * 110 + i * 23) % 194)
                    d.ellipse((cx - 60 + i * 15 - 5, yy - 5, cx - 60 + i * 15 + 5, yy + 5), fill=(150, 240, 255))
            d.rounded_rectangle((cx - 70, top + 250, cx + 70, top + 290), 6, fill=(90, 130, 230), outline=WHITE, width=3)
            for i in range(5):
                d.rectangle((cx - 55 + i * 25, top + 260, cx - 42 + i * 25, top + 280), fill=GOLD)
            d.text((cx + 170, top + 270), "チップ", font=jp(28, True), fill=WHITE, anchor="lm")
            d.text((cx + 170, top + 40), "冷凍機", font=jp(28, True), fill=WHITE, anchor="lm")
        elif st == "ion":  # 電極の間に浮かぶイオンの列
            for yy in (top + 90, top + 230):
                d.rounded_rectangle((x0 + 60, yy - 18, x1 - 60, yy + 18), 10, fill=(170, 175, 190))
            for i in range(9):
                ax = x0 + 110 + i * (x1 - x0 - 220) / 8 + (4 * math.sin(T * 5 + i) if T is not None else 0)
                d.ellipse((ax - 20, top + 140, ax + 20, top + 180), fill=(255, 120, 120), outline=WHITE, width=3)
                d.text((ax, top + 160), "+", font=jp(26, True), fill=WHITE, anchor="mm")
            tgt = 3 if T is None else int(T / 1.5) % 9  # レーザーが順番にイオンを狙う
            d.line((x0 + 110, top + 20, x0 + 110 + tgt * (x1 - x0 - 220) / 8, top + 160), fill=(120, 255, 160), width=5)
            d.text((x0 + 70, top + 20), "レーザー", font=jp(26, True), fill=(120, 255, 160), anchor="lm")
            d.text((cx, top + 290), "電極（電場でイオンを浮かせる）", font=jp(28, True), fill=WHITE, anchor="mm")
        elif st == "atom":  # 光ピンセットでつかんだ原子の格子
            for r in range(5):
                for c in range(11):
                    ax = x0 + 90 + c * (x1 - x0 - 180) / 10
                    ay = top + 30 + r * 55
                    hr = 24 + (5 * math.sin(T * 3 + r + c * 0.7) if T is not None else 0)
                    d.ellipse((ax - hr, ay - hr, ax + hr, ay + hr), fill=(255, 200, 60, 40))
                    if (r * 11 + c) % 13 != 5:
                        d.ellipse((ax - 11, ay - 11, ax + 11, ay + 11), fill=GOLD)
            d.text((cx, top + 290), "光ピンセット1本に原子1個", font=jp(28, True), fill=WHITE, anchor="mm")
        elif st == "photon":  # 光ファイバーを進む光の波
            for j, col in enumerate(((120, 220, 255), (255, 140, 200))):
                cy = top + 90 + j * 120
                d.rounded_rectangle((x0 + 50, cy - 40, x1 - 50, cy + 40), 40, outline=(120, 140, 200), width=3)
                pts = [(x0 + 70 + i * 2, cy - 25 * math.sin(i / 14 + j - (T or 0) * 4))
                       for i in range(int((x1 - x0 - 140) / 2))]
                d.line(pts, fill=col, width=5)
            d.text((cx, top + 290), "光の粒・光の波を量子ビットに", font=jp(28, True), fill=WHITE, anchor="mm")
        elif st == "nv":  # ダイヤモンドの格子と、窒素＋空孔のペア
            for r in range(5):
                for c in range(9):
                    ax = x0 + 120 + c * (x1 - x0 - 240) / 8 + (30 if r % 2 else 0)
                    ay = top + 30 + r * 55
                    if c < 8:
                        d.line((ax, ay, ax + (x1 - x0 - 240) / 8, ay), fill=(120, 140, 200), width=2)
                    if r < 4:
                        d.line((ax, ay, ax + (-30 if r % 2 else 30), ay + 55), fill=(120, 140, 200), width=2)
                    if (r, c) == (2, 4):
                        if T is not None:  # NVセンターが光る
                            gr = 30 + 10 * (0.5 + 0.5 * math.sin(T * 3))
                            d.ellipse((ax - gr + 30, ay - gr, ax + gr + 30, ay + gr), fill=(255, 220, 120, 50))
                        d.ellipse((ax - 18, ay - 18, ax + 18, ay + 18), fill=(110, 150, 255), outline=WHITE, width=3)
                        d.text((ax, ay), "N", font=jp(22, True), fill=WHITE, anchor="mm")
                    elif (r, c) == (2, 5):
                        d.ellipse((ax - 18, ay - 18, ax + 18, ay + 18), outline=GOLD, width=4)
                        d.text((ax, ay), "V", font=jp(22, True), fill=GOLD, anchor="mm")
                    else:
                        d.ellipse((ax - 9, ay - 9, ax + 9, ay + 9), fill=(200, 210, 230))
            d.text((cx, top + 290), "N＝窒素　V＝原子の抜けた穴（空孔）", font=jp(28, True), fill=WHITE, anchor="mm")
        cw = (x1 - x0 - 40) / len(fig["stats"])
        for i, (lab, val) in enumerate(fig["stats"]):
            bx = x0 + 20 + i * cw
            d.rounded_rectangle((bx + 8, top + ih + 40, bx + cw - 8, top + ih + 170), 18, fill=(255, 255, 255, 30),
                                outline=GOLD, width=3)
            if i == 0:
                st_l = fit_size(d, [a for a, _ in fig["stats"]], cw - 30, 40, 30, 18, bold=True, max_lines=1)
                st_v = fit_size(d, [b for _, b in fig["stats"]], cw - 30, 50, 40, 18, bold=True, max_lines=1)
            lf, vf = jp(st_l, True), jp(st_v, True)
            d.text((bx + cw / 2, top + ih + 72), lab, font=lf, fill=(200, 210, 240), anchor="mm")
            d.text((bx + cw / 2, top + ih + 125), val, font=vf, fill=WHITE, anchor="mm")
    elif k == "table" and len(fig["rows"]) > 6 and not fig.get("_sub"):
        # 行が多い表は、左右2つの表に分けて文字を大きくする（列の幅と文字の大きさは左右でそろえる）
        half = (len(fig["rows"]) + 1) // 2
        mid = (x0 + x1) / 2
        rows = fig["rows"]
        sub = dict(fig, _sub=True, _all=rows)
        fig_area(img, (x0, y0, mid + 15, y1), dict(sub, rows=rows[:half]), cfg)
        fig_area(img, (mid - 15, y0, x1, y1), dict(sub, rows=rows[half:] + [("",) * len(fig["head"])] * (2 * half - len(rows))),
                 cfg)
    elif k == "table":
        head, rows = fig["head"], fig["rows"]
        allrows = [r for r in fig.get("_all", rows) if any(r)]
        nc = len(head)
        hdr = 64 if len(rows) > 6 else 70
        rh = (y1 - y0 - hdr - 20) / len(rows)
        base = int(max(22, min(42, rh * 0.52)))
        # 列の幅: いちばん長い文字に合わせて配分する（表全体の中身で決める）
        need = [max([d.textlength(r[j], font=jp(base, True)) for r in allrows] + [d.textlength(head[j], font=jp(base, True))])
                + 50 for j in range(nc)]
        tot = x1 - x0 - 60
        widths = [w * tot / sum(need) for w in need]
        cols = [x0 + 30]
        for w_ in widths:
            cols.append(cols[-1] + w_)
        # 表の中の文字は、すべて同じ大きさ（1行に収まる大きさを優先し、無理なら2行）
        cells = [(r[j], cols[j + 1] - cols[j] - 30) for r in allrows for j in range(nc)]
        def all_fit(size, nl):
            f = jp(size, True)
            return all(len(wrap(d, c, f, w)) <= nl for c, w in cells) and nl * size * 1.15 <= rh - 12
        one = next((z for z in range(base, 19, -1) if all_fit(z, 1)), 20)
        two = next((z for z in range(base, 19, -1) if all_fit(z, 2)), 20)
        fs = one if one >= two * 0.85 else two
        cf = jp(fs, True)
        clh = int(fs * 1.15)
        d.rounded_rectangle((cols[0], y0 + 10, cols[-1], y0 + 10 + hdr), 16, fill=(66, 133, 244, 200))
        for j, h in enumerate(head):
            d.text(((cols[j] + cols[j + 1]) / 2, y0 + 10 + hdr / 2), h, font=jp(min(40, fs + 2), True), fill=WHITE,
                   anchor="mm")
        for i, row in enumerate(rows):
            yy = y0 + hdr + 18 + i * rh
            d.rounded_rectangle((cols[0], yy, cols[-1], yy + rh - (10 if rh >= 70 else 4)), 14,
                                fill=(255, 255, 255, 22 if i % 2 else 36))
            for j, cell in enumerate(row):
                cl = wrap(d, cell, cf, cols[j + 1] - cols[j] - 30)
                cy0 = yy + (rh - (10 if rh >= 70 else 4)) / 2 - (len(cl) - 1) * clh / 2
                for q, ln in enumerate(cl):
                    d.text(((cols[j] + cols[j + 1]) / 2, cy0 + q * clh), ln, font=cf, fill=GOLD if j == 0 else WHITE,
                           anchor="mm")
    elif k == "tiles":
        # タイルの並び（例: 9回のふりかえり）。番号・題名・ひとことを、すべてのタイルで同じ大きさにそろえる
        items = fig["items"]
        nc = fig.get("cols", 3)
        nr = (len(items) + nc - 1) // nc
        g = 16
        tw_ = (x1 - x0 - g * (nc - 1)) / nc
        th_ = (y1 - y0 + 10 - g * (nr - 1)) / nr
        badge = min(th_ - 24, 64)
        inner = tw_ - badge - 50
        t_sz = fit_size(d, [it[1] for it in items], inner, th_ * 0.4, 40, 22, bold=True, max_lines=1)
        s_sz = fit_size(d, [it[2] for it in items], inner, th_ * 0.5, 32, 18, bold=True, max_lines=2, spacing=0.15)
        tf, sf = jp(t_sz, True), jp(s_sz, True)
        for i, (no, title, sub) in enumerate(items):
            bx = x0 + (i % nc) * (tw_ + g)
            by = y0 - 5 + (i // nc) * (th_ + g)
            d.rounded_rectangle((bx, by, bx + tw_, by + th_), 18, fill=(255, 255, 255, 30), outline=(110, 150, 255), width=3)
            cy = by + th_ / 2
            d.rounded_rectangle((bx + 16, cy - badge / 2, bx + 16 + badge, cy + badge / 2), 14, fill=GOLD)
            d.text((bx + 16 + badge / 2, cy), str(no), font=num(int(badge * 0.62)), fill=NAVY, anchor="mm")
            tx = bx + badge + 34
            sl = wrap(d, sub, sf, inner)
            blk = t_sz * 1.2 + len(sl) * s_sz * 1.15
            ty = cy - blk / 2
            d.text((tx, ty), title, font=tf, fill=GOLD)
            for j, ln in enumerate(sl):
                d.text((tx, ty + t_sz * 1.2 + j * s_sz * 1.15), ln, font=sf, fill=WHITE)
    elif k == "bb84":
        # BB84: 送り手のビットと測り方 → 光子の偏光 → 受け手の測り方と結果 → 鍵
        bits = [0, 1, 1, 0, 1, 0]
        ab = ["+", "×", "+", "×", "×", "+"]
        bb = ["+", "+", "+", "×", "+", "×"]
        labels = ["送り手のビット", "送り手の測り方", "送る光子の向き", "受け手の測り方", "受け手の結果", "鍵に使う？"]
        lw = 250
        cw = (x1 - x0 - lw - 20) / len(bits)
        rh = (y1 - y0 - 20) / len(labels)

        def pol(cx, cy, basis, bit, col):
            r = rh * 0.32
            if basis == "+":
                seg = (cx - r, cy, cx + r, cy) if bit == 0 else (cx, cy - r, cx, cy + r)
            else:
                seg = (cx - r * 0.7, cy + r * 0.7, cx + r * 0.7, cy - r * 0.7) if bit == 0 else \
                      (cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7)
            d.line(seg, fill=col, width=7)
        for r, lab in enumerate(labels):
            cy = y0 + 10 + (r + 0.5) * rh
            d.rounded_rectangle((x0 + 10, cy - rh / 2 + 4, x1 - 10, cy + rh / 2 - 4), 12,
                                fill=(255, 255, 255, 18 if r % 2 else 30))
            d.text((x0 + 24, cy), lab, font=jp(26, True), fill=(200, 210, 240), anchor="lm")
            for i in range(len(bits)):
                cx = x0 + lw + (i + 0.5) * cw
                same = ab[i] == bb[i]
                if r == 0:
                    d.text((cx, cy), str(bits[i]), font=num(44), fill=WHITE, anchor="mm")
                elif r == 1:
                    d.text((cx, cy), ab[i], font=jp(40, True), fill=(120, 200, 255), anchor="mm")
                elif r == 2:
                    pol(cx, cy, ab[i], bits[i], GOLD)
                elif r == 3:
                    d.text((cx, cy), bb[i], font=jp(40, True), fill=(255, 150, 200), anchor="mm")
                elif r == 4:
                    d.text((cx, cy), str(bits[i]) if same else "?", font=num(44) if same else jp(40, True),
                           fill=WHITE if same else (150, 150, 170), anchor="mm")
                else:
                    d.text((cx, cy), "○" if same else "×", font=jp(40, True),
                           fill=(110, 220, 120) if same else (230, 90, 90), anchor="mm")
    elif k == "dial":
        # 量子状態を時計の針にたとえる: 外からの影響があると針が余分に回る（ずれ＝位相）
        tt = None if T is None else T % 8
        for i, (lab, col) in enumerate((("影響なし", (120, 200, 255)), ("磁場・重力あり", GOLD))):
            cx = x0 + (x1 - x0) * (0.27 + 0.46 * i)
            cy = (y0 + y1) / 2 - 10
            r = 140
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(150, 160, 210), width=4)
            for t in range(12):
                a = math.radians(t * 30)
                d.line((cx + (r - 14) * math.sin(a), cy - (r - 14) * math.cos(a), cx + r * math.sin(a), cy - r * math.cos(a)),
                       fill=(150, 160, 210), width=3)
            ref = 90 if tt is None else 90 + 45 * tt  # 影響がないときの針
            ang = (ref + (35 if tt is None else 0.25 * 45 * tt)) if i else ref
            a0 = math.radians(ref)
            d.line((cx, cy, cx + (r - 30) * math.sin(a0), cy - (r - 30) * math.cos(a0)), fill=(120, 200, 255, 140), width=6)
            a = math.radians(ang)
            d.line((cx, cy, cx + (r - 30) * math.sin(a), cy - (r - 30) * math.cos(a)), fill=col, width=9)
            d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=WHITE)
            if i and ang - ref > 1:
                d.arc((cx - r + 40, cy - r + 40, cx + r - 40, cy + r - 40), ref - 90, ang - 90, fill=(255, 120, 120), width=5)
                d.text((cx + r + 8, cy + 70), "ずれ", font=jp(30, True), fill=(255, 120, 120), anchor="lm")
            d.text((cx, cy + r + 40), lab, font=jp(32, True), fill=col, anchor="mm")
    elif k == "tower":
        # スカイツリーの展望台と地上の時計
        bx = x0 + 230
        base, topy = y1 - 60, y0 + 40
        d.polygon([(bx - 70, base), (bx + 70, base), (bx + 14, topy + 60), (bx - 14, topy + 60)], fill=(150, 170, 220))
        d.line((bx, topy, bx, topy + 60), fill=(150, 170, 220), width=8)
        d.rounded_rectangle((bx - 45, topy + 120, bx + 45, topy + 160), 10, fill=(200, 215, 245))
        d.line((x0 + 40, base, x1 - 40, base), fill=WHITE, width=4)
        for (yy, lab, sub, col) in ((topy + 140, "展望台（地上450m）", "1日に約4ナノ秒速く進む", GOLD),
                                    (base - 40, "地上", "基準", (120, 200, 255))):
            cx = bx + 200
            d.ellipse((cx - 36, yy - 36, cx + 36, yy + 36), outline=col, width=5)
            if T is None:
                d.line((cx, yy, cx, yy - 24), fill=col, width=5)
                d.line((cx, yy, cx + 18, yy + 8), fill=col, width=5)
            else:
                sp = 1.06 if lab.startswith("展望台") else 1.0
                a = math.radians(T * 72 * sp)
                d.line((cx, yy, cx + 28 * math.sin(a), yy - 28 * math.cos(a)), fill=col, width=5)
                d.ellipse((cx - 5, yy - 5, cx + 5, yy + 5), fill=col)
            d.line((bx + 50, yy, cx - 40, yy), fill=col, width=3)
            d.text((cx + 60, yy - 20), lab, font=jp(34, True), fill=col, anchor="lm")
            d.text((cx + 60, yy + 24), sub, font=jp(30, True), fill=WHITE, anchor="lm")
        d.text((x1 - 40, (topy + base) / 2 + 40), "重力が弱いほど\n時間は速く進む", font=jp(30, True), fill=(200, 210, 240),
               anchor="rm", align="right")
        if T is not None:
            d.text((x1 - 40, base + 30), "※針の速さのちがいは大げさに表示", font=jp(22, True), fill=(160, 170, 210), anchor="rm")
    elif k == "pair":
        # もつれたペア: 測る前は「0と1の重ね合わせ」、片方を測るともう片方も決まる
        cy1, cy2 = y0 + 120, y0 + 360
        for row, (cy, lab) in enumerate(((cy1, "測る前"), (cy2, "片方を測ると"))):
            d.text((x0 + 30, cy), lab, font=jp(30, True), fill=(200, 210, 240), anchor="lm")
            ax, bx = x0 + 330, x1 - 120
            d.line((ax, cy, bx, cy), fill=(255, 130, 200), width=4)
            for i in range(9):
                t = i / 8
                d.ellipse((ax + (bx - ax) * t - 4, cy - 4 + 14 * math.sin(t * 9), ax + (bx - ax) * t + 4,
                           cy + 4 + 14 * math.sin(t * 9)), fill=(255, 130, 200))
            c = None if T is None else T % 4  # 4秒ごとに「測る」をくり返す
            done = row and (c is None or c >= 1.5)
            for j, xx in enumerate((ax, bx)):
                d.ellipse((xx - 62, cy - 62, xx + 62, cy + 62), fill=(60, 70, 110), outline=WHITE, width=4)
                if T is None:
                    txt, fnt = ("0?1", num(52)) if row == 0 else ("0", num(70))
                elif row == 0 or not done:
                    txt, fnt = str(int(T * (3.3 if j == 0 else 2.7) + j) % 2), num(70)
                else:
                    txt, fnt = "0", num(70)
                d.text((xx, cy), txt, font=fnt, fill=GOLD if done else WHITE, anchor="mm")
                if row and c is not None and 1.5 <= c < 2.1:  # 測った瞬間の光
                    rr = 62 + (c - 1.5) * 120
                    d.ellipse((xx - rr, cy - rr, xx + rr, cy + rr), outline=(255, 230, 120), width=4)
            if row and done:
                d.text((ax, cy + 95), "0が出た", font=jp(28, True), fill=GOLD, anchor="mm")
                d.text((bx, cy + 95), "必ず0になる", font=jp(28, True), fill=GOLD, anchor="mm")
            d.text(((ax + bx) / 2, cy - 50), "どんなに離れていても", font=jp(24, True), fill=(255, 170, 220), anchor="mm")
    elif k == "teleport":
        # アリスとボブ: もつれたペア＋2ビットの通信で状態を移す
        ax, bx = x0 + 280, x1 - 280
        top = y0 + 30
        for xx, nm, col in ((ax, "送り手 アリス", (120, 200, 255)), (bx, "受け手 ボブ", (255, 150, 200))):
            d.rounded_rectangle((xx - 230, top, xx + 230, top + 300), 26, fill=(255, 255, 255, 20), outline=col, width=4)
            d.text((xx, top + 32), nm, font=jp(36, True), fill=col, anchor="mm")
        d.ellipse((ax - 170, top + 110, ax - 70, top + 210), fill=GOLD)
        d.text((ax - 120, top + 160), "ψ", font=jp(54, True), fill=NAVY, anchor="mm")
        d.text((ax - 120, top + 232), "送りたい状態", font=jp(24, True), fill=WHITE, anchor="mm")
        d.ellipse((ax + 60, top + 110, ax + 160, top + 210), fill=(255, 130, 200))
        d.ellipse((bx - 50, top + 110, bx + 50, top + 210), fill=(255, 130, 200))
        d.line((ax + 160, top + 160, bx - 50, top + 160), fill=(255, 130, 200), width=4)
        d.text(((ax + bx) / 2, top + 135), "① もつれたペアを共有", font=jp(28, True), fill=(255, 170, 220), anchor="mm")
        d.rounded_rectangle((ax - 190, top + 90, ax + 180, top + 255), 20, outline=WHITE, width=3)
        d.text((ax, top + 278), "② 2つをまとめて測る", font=jp(28, True), fill=WHITE, anchor="mm")
        yy = top + 360
        d.line((ax, yy, bx - 20, yy), fill=(110, 220, 120), width=6)
        d.polygon([(bx - 20, yy - 16), (bx + 10, yy), (bx - 20, yy + 16)], fill=(110, 220, 120))
        d.text(((ax + bx) / 2, yy - 30), "③ 結果の2ビットを、ふつうの通信で送る（光より速くない）",
               font=jp(28, True), fill=(110, 220, 120), anchor="mm")
        d.text((bx, top + 245), "④ 2ビットに合わせて操作", font=jp(26, True), fill=WHITE, anchor="mm")
        d.text((bx, top + 280), "→ ψ が再現される", font=jp(28, True), fill=GOLD, anchor="mm")
        d.text((ax, yy + 60), "元の状態は測ったときに壊れる（コピーはできない）", font=jp(26, True),
               fill=(200, 210, 240), anchor="lm")
        if T is not None:
            c = T % 9
            if 3 <= c < 6:  # 2ビットの情報がふつうの通信で進む
                for q in range(2):
                    px = ax + (bx - 20 - ax) * min(1, (c - 3) / 2.5 - q * 0.08)
                    if px > ax:
                        d.ellipse((px - 14, yy - 14, px + 14, yy + 14), fill=(110, 220, 120), outline=WHITE, width=2)
                        d.text((px, yy), str(q), font=jp(18, True), fill=NAVY, anchor="mm")
            if c >= 2.5:  # 測ったので、アリス側の元の状態は壊れる
                d.ellipse((ax - 170, top + 110, ax - 70, top + 210), fill=(70, 70, 90))
                d.text((ax - 120, top + 160), "×", font=jp(54, True), fill=(200, 200, 210), anchor="mm")
            if c >= 6:  # ボブ側に元の状態が再現される
                d.ellipse((bx - 50, top + 110, bx + 50, top + 210), fill=GOLD)
                d.text((bx, top + 160), "ψ", font=jp(54, True), fill=NAVY, anchor="mm")
    elif k == "landscape":
        # 答えのよさ＝高さ。小さな谷にはまったボールと、山をすり抜ける量子
        base = y1 - 70
        f = lambda t: 0.62 + 0.22 * math.sin(t * 11) * (1 - 0.3 * t) - 0.55 * math.exp(-((t - 0.72) / 0.06) ** 2)
        xs = [x0 + 40 + i * (x1 - x0 - 80) / 300 for i in range(301)]
        pts = [(x, base - (base - y0 - 90) * f(i / 300)) for i, x in enumerate(xs)]
        d.polygon(pts + [(xs[-1], base + 10), (xs[0], base + 10)], fill=(90, 130, 230, 90))
        d.line(pts, fill=(150, 190, 255), width=5)
        # 一番低い谷
        imin = min(range(301), key=lambda i: f(i / 300))
        mx, my = pts[imin]
        d.text((mx, my + 40), "一番よい答え", font=jp(26, True), fill=GOLD, anchor="mm")
        d.ellipse((mx - 10, my - 22, mx + 10, my - 2), outline=GOLD, width=3)
        # 小さな谷にはまったボール
        loc = min(range(110, 180), key=lambda i: f(i / 300))
        bxp, byp = pts[loc]
        if T is not None:  # 小さな谷の中でゆれるだけで、外に出られない
            bi = int(loc + 9 * math.sin(T * 2.5))
            qx, qy = pts[bi]
            d.ellipse((qx - 18, qy - 36, qx + 18, qy), fill=(255, 120, 120), outline=WHITE, width=3)
        else:
            d.ellipse((bxp - 18, byp - 36, bxp + 18, byp), fill=(255, 120, 120), outline=WHITE, width=3)
        d.text((bxp, byp + 36), "小さな谷にはまる", font=jp(24, True), fill=(255, 150, 150), anchor="mm")
        # トンネル（点線の矢印）
        for i in range(loc, imin, 12):
            x, yv = pts[i]
            d.line((x, byp - 18, x + 6, byp - 18), fill=(110, 220, 120), width=4)
        d.text(((bxp + mx) / 2, byp - 110), "量子：山をすり抜ける（トンネル効果）", font=jp(26, True), fill=(110, 220, 120), anchor="mm")
        if T is not None:  # 緑の玉（量子）が山をすり抜けて一番低い谷へ
            c = T % 4.5
            g = min(1.0, c / 2.5)
            qx = bxp + (mx - bxp) * g
            qy = byp - 18 + ((my - 12) - (byp - 18)) * max(0.0, (g - 0.8) / 0.2)
            d.ellipse((qx - 14, qy - 14, qx + 14, qy + 14), fill=(110, 220, 120), outline=WHITE, width=2)
            if c >= 2.5:
                rr = 16 + 10 * math.sin((c - 2.5) * 6)
                d.ellipse((mx - rr, my - 12 - rr, mx + rr, my - 12 + rr), outline=GOLD, width=4)
        d.text((x0 + 50, y0 + 30), "高さ＝答えの悪さ", font=jp(26, True), fill=(200, 210, 240))
    elif k == "repeater":
        # 上: 区間ごとのもつれ / 下: 中継点でまとめて測る → 端と端がもつれる
        xs = [x0 + 80, x0 + (x1 - x0) / 2 - 40, x0 + (x1 - x0) / 2 + 40, x1 - 80]
        names = ["A", "中継点", "", "B"]
        for row, cy in enumerate((y0 + 120, y0 + 360)):
            d.text((x0 + 20, cy - 85), "① 区間ごとにもつれを作る" if row == 0 else "② 中継点でまとめて測ると…",
                   font=jp(28, True), fill=(200, 210, 240), anchor="lm")
            pairs = [(0, 1), (2, 3)] if row == 0 else [(0, 3)]
            for a, b in pairs:
                yy = cy if row == 0 else cy + 45
                d.line((xs[a], yy, xs[b], yy), fill=(255, 130, 200), width=4)
                for i in range(10):
                    t = i / 9
                    xx = xs[a] + (xs[b] - xs[a]) * t
                    wv = 10 * math.sin(t * 8 - (T or 0) * 4)
                    d.ellipse((xx - 4, yy - 4 + wv, xx + 4, yy + 4 + wv), fill=(255, 130, 200))
            for i, xx in enumerate(xs):
                col = GOLD if i in (0, 3) else (120, 200, 255)
                d.ellipse((xx - 30, cy - 30, xx + 30, cy + 30), fill=(60, 70, 110), outline=col, width=4)
            d.text((xs[0], cy - 50), "A", font=jp(30, True), fill=GOLD, anchor="mm")
            d.text((xs[3], cy - 50), "B", font=jp(30, True), fill=GOLD, anchor="mm")
            d.rounded_rectangle((xs[1] - 50, cy - 45, xs[2] + 50, cy + 45), 18, outline=(120, 200, 255), width=3)
            d.text(((xs[1] + xs[2]) / 2, cy + 70 if row == 0 else cy - 62), "中継点", font=jp(26, True),
                   fill=(120, 200, 255), anchor="mm")
        d.text(((xs[0] + xs[3]) / 2, y0 + 460), "AとBが直接もつれる（もつれ交換）", font=jp(30, True), fill=GOLD, anchor="mm")
    elif k == "pipeline":
        # 入り口 → 量子で計算 → 出口 の3つの箱
        items = fig["items"]
        n = len(items)
        bw = (x1 - x0 - 80 - (n - 1) * 60) / n
        cols = [(255, 130, 130), (110, 220, 120), (255, 130, 130)]
        for i, (t, sub) in enumerate(items):
            bx = x0 + 40 + i * (bw + 60)
            col = cols[i % len(cols)]
            d.rounded_rectangle((bx, y0 + 60, bx + bw, y1 - 60), 24, fill=(255, 255, 255, 22), outline=col, width=5)
            d.text((bx + bw / 2, y0 + 120), t, font=jp(36, True), fill=col, anchor="mm")
            d.multiline_text((bx + bw / 2, y0 + 220), sub, font=jp(30, True), fill=WHITE, anchor="ma", align="center",
                             spacing=12)
            if i < n - 1:
                ax = bx + bw + 8
                cy = (y0 + y1) / 2
                d.polygon([(ax, cy - 22), (ax + 44, cy), (ax, cy + 22)], fill=WHITE)
        d.text(((x0 + x1) / 2, y1 - 25), "真ん中が速くなっても、入り口と出口で時間がかかると全体は速くならない",
               font=jp(28, True), fill=GOLD, anchor="mm")
        if T is not None and n == 3:
            for q in range(8):  # 粒の位置: 箱1と箱3ではゆっくり、箱2では一瞬
                u = (T * 0.12 + q / 8) % 1
                if u < 0.45:
                    bi, f2 = 0, u / 0.45
                elif u < 0.5:
                    bi, f2 = 1, (u - 0.45) / 0.05
                else:
                    bi, f2 = 2, (u - 0.5) / 0.5
                bx = x0 + 40 + bi * (bw + 60)
                px = bx + 30 + (bw - 60) * f2
                py = y1 - 120 - 18 * (q % 3)
                d.ellipse((px - 10, py - 10, px + 10, py + 10), fill=GOLD)
    elif k == "summary":
        for i, s in enumerate(fig["items"]):
            gap = min(112, (y1 - y0 - 30) / len(fig["items"]))  # 立ち絵ワイプと重ならないよう詰める
            yy = y0 + 20 + i * gap
            d.rounded_rectangle((x0 + 60, yy, x1 - 60, yy + gap - 16), 20, fill=(255, 255, 255, 24))
            d.text((x0 + 110, yy + (gap - 16) / 2), "✓", font=jp(50), fill=GOLD, anchor="mm")
            if i == 0:
                sm_sz = fit_size(d, fig["items"], x1 - x0 - 260, gap - 20, 48, 28, max_lines=1)
            sf = jp(sm_sz)
            d.text((x0 + 160, yy + (gap - 16) / 2), s, font=sf, fill=WHITE, anchor="lm")


def slide_parts(bg, cfg, ch_i, ch):
    """章の画面を部品に分けて返す: 背景（動かない）/ 箇条書きのレイヤー / 図を描く枠"""
    img = frame_base(bg, cfg, ch_i, ch)
    panel = (60, 130, W - 60, 800)
    lay = Image.new("RGBA", (W, H))
    ImageDraw.Draw(lay).rounded_rectangle(panel, 30, fill=(0, 0, 0, 90))
    img = Image.alpha_composite(img, lay)
    bul = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(bul)
    has_port = bool(portraits("Z")) or bool(portraits("M"))
    bottom = 680 if has_port else 790  # 立ち絵ワイプと重ならないよう、図の下端を上げる
    rects = []
    if ch.get("bullets"):
        # 左: 箇条書き / 右: 図
        nb = len(ch["bullets"])
        step = min(150, (bottom - 170) / nb)
        b_sz = fit_size(d, ch["bullets"], 750, step - 18, 46, 30, spacing=0.2)
        for i, b in enumerate(ch["bullets"]):
            yy = 170 + i * step
            bf, bl, lh = fit_text(d, b, 750, step - 18, b_sz, b_sz, spacing=0.2)
            hblk = len(bl) * lh
            d.rounded_rectangle((100, yy + 4, 112, yy + max(hblk, 56) - 4), 6, fill=GOLD)
            for j, ln in enumerate(bl):
                d.text((135, yy + j * lh), ln, font=bf, fill=WHITE)
            rects.append((90, yy - 8, 905, yy + step - 8))
        box = (920, 150, W - 80, bottom)
    else:
        box = (100, 150, W - 100, bottom)
    return {"base": img, "bul": bul, "bul_rects": rects, "box": box, "fig": ch["fig"]}


def slide(bg, cfg, ch_i, ch):
    """止め絵の章画面（サムネイルやプレビュー用）"""
    p = slide_parts(bg, cfg, ch_i, ch)
    # 図は透明なレイヤーに描いてから重ねる（半透明の塗りを正しく合成するため）
    fl = Image.new("RGBA", (W, H))
    fig_area(fl, p["box"], ch["fig"], cfg)
    return Image.alpha_composite(Image.alpha_composite(p["base"], p["bul"]), fl)


# ---- 登場アニメーション（項目を順番に出す・棒グラフを伸ばす・年表を左から描く） --------------
def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def gap_for(n, tch):
    """項目を出す間隔: 章の前半（約45%）で全部出しきる。速すぎず遅すぎないように制限"""
    return min(4.0, max(0.6, tch * 0.45 / max(n, 1)))


def item_alpha(i, n, tc, tch):
    return ease((tc - 0.4 - i * gap_for(n, tch)) / 0.45)


def item_rects(fig, box):
    """図の中で、順番に登場させる部分（項目ごとの長方形）"""
    x0, y0, x1, y1 = box
    k = fig["kind"]
    if k == "cards":
        n = len(fig["items"]); hh = (y1 - y0 - 10 - 18 * (n - 1)) / n
        return [(x0, y0 + 5 + i * (hh + 18) - 6, x1, y0 + 5 + i * (hh + 18) + hh + 6) for i in range(n)]
    if k == "summary":
        n = len(fig["items"]); g = min(112, (y1 - y0 - 30) / n)
        return [(x0, y0 + 20 + i * g - 6, x1, y0 + 20 + (i + 1) * g - 10) for i in range(n)]
    if k == "table" and len(fig["rows"]) > 6:
        half = (len(fig["rows"]) + 1) // 2
        mid = (x0 + x1) / 2
        rows = fig["rows"]
        left = item_rects(dict(fig, rows=rows[:half]), (x0, y0, mid + 15, y1))
        right = item_rects(dict(fig, rows=rows[half:] + [("",) * len(fig["head"])] * (2 * half - len(rows))),
                           (mid - 15, y0, x1, y1))
        return left + right[:len(rows) - half]
    if k == "table":
        n = len(fig["rows"]); hdr = 64 if n > 6 else 70; rh = (y1 - y0 - hdr - 20) / n
        return [(x0, y0 + hdr + 18 + i * rh - 3, x1, y0 + hdr + 18 + (i + 1) * rh - 1) for i in range(n)]
    if k == "tiles":
        items = fig["items"]; nc = fig.get("cols", 3); nr = (len(items) + nc - 1) // nc
        tw_ = (x1 - x0 - 16 * (nc - 1)) / nc; th_ = (y1 - y0 + 10 - 16 * (nr - 1)) / nr
        return [(x0 + (i % nc) * (tw_ + 16) - 4, y0 - 9 + (i // nc) * (th_ + 16), x0 + (i % nc) * (tw_ + 16) + tw_ + 4,
                 y0 - 1 + (i // nc) * (th_ + 16) + th_) for i in range(len(items))]
    if k == "vote":
        return [(x0, y0 + 40 + i * 150 - 8, x1, y0 + 40 + i * 150 + 142) for i in range(4)]
    if k == "bb84":
        cw = (x1 - x0 - 270) / 6
        return [(x0 + 250 + i * cw, y0, x0 + 250 + (i + 1) * cw, y1) for i in range(6)]
    if k == "period":
        cw = (x1 - x0 - 40) / 9; top = y0 + 30
        return [(x0 + 20 + i * cw, top + 60, x0 + 20 + (i + 1) * cw, top + 205) for i in range(9)] + \
               [(x0, top + 205, x1, y1 + 10)]
    if k == "title":
        n = len(fig.get("chips", [])) or 4; cw = (W - 240) / n
        return [(120 + i * cw, 545, 120 + (i + 1) * cw, 655) for i in range(n)]
    if k == "platform":
        n = len(fig["stats"]); cw = (x1 - x0 - 40) / n; top = y0 + 20
        return [(x0 + 20 + i * cw, top + 330, x0 + 20 + (i + 1) * cw, top + 480) for i in range(n)]
    if k == "repeater":
        return [(x0, y0, x1, y0 + 240), (x0, y0 + 240, x1, y1 + 10)]
    return None


def fig_mask(fig, box, tc, tch):
    """経過時間 tc での図の見え方（白=見える）。全部見えていれば None"""
    x0, y0, x1, y1 = box
    k = fig["kind"]
    if k == "bars":
        items = fig["items"]; n = len(items)
        bw = min(220, (x1 - x0 - 120) / n - 60); base_y = y1 - 120
        if tc > 0.4 + 0.35 * n + 1.5:
            return None
        m = Image.new("L", (W, H), 255); dm = ImageDraw.Draw(m)
        sp = (x1 - x0 - 200) / n
        hw = min(bw / 2 + 60, sp / 2)  # 隣の棒にかからない幅
        for i in range(n):
            cx = x0 + 100 + (i + 0.5) * sp
            g = ease((tc - 0.4 - 0.35 * i) / 1.3)
            dm.rectangle((cx - hw, y0 + 60, cx + hw, base_y - 3), fill=0)
            top = base_y - g * (base_y - y0 - 60)
            if top < base_y - 3:
                dm.rectangle((cx - hw, top, cx + hw, base_y - 3), fill=255)
        return m
    if k == "timeline":
        span = max(1.5, min(tch * 0.5, 1.4 * len(fig["items"])))
        p = (tc - 0.3) / span
        if p >= 1:
            return None
        m = Image.new("L", (W, H), 255)
        ImageDraw.Draw(m).rectangle((x0 + (x1 - x0) * max(0.0, p), y0 - 10, x1 + 10, y1 + 10), fill=0)
        return m
    rects = item_rects(fig, box)
    if rects:
        n = len(rects)
        if item_alpha(n - 1, n, tc, tch) >= 1:
            return None
        m = Image.new("L", (W, H), 255); dm = ImageDraw.Draw(m)
        for i, r in enumerate(rects):
            a = item_alpha(i, n, tc, tch)
            if a < 1:
                dm.rectangle(r, fill=int(255 * a))
        return m
    a = ease(tc / 0.6)  # そのほかの図は、ふわっと現れる
    return None if a >= 1 else Image.new("L", (W, H), int(255 * a))


def bullets_mask(rects, tc, tch):
    n = len(rects)
    if not n or item_alpha(n - 1, n, tc, tch) >= 1:
        return None
    m = Image.new("L", (W, H), 255); dm = ImageDraw.Draw(m)
    for i, r in enumerate(rects):
        a = item_alpha(i, n, tc, tch)
        if a < 1:
            dm.rectangle(r, fill=int(255 * a))
    return m


def masked(layer, m):
    if m is None:
        return layer
    out = layer.copy()
    out.putalpha(ImageChops.multiply(layer.getchannel("A"), m))
    return out


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
    return Image.alpha_composite(sl, line_overlay(spk, text, expr, mouth, page, blink))


def line_overlay(spk, text, expr=None, mouth=0, page=0, blink=()):
    """話者テロップと立ち絵ワイプだけを描いた透明レイヤー"""
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
    return lay


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
    durs, starts, chapter_starts, t = [], [], {}, 0.0
    for n, ((ci, li, spk, disp, say), v) in enumerate(zip(lines, voices)):
        dur = len(v) / SR + 0.35 + (0.6 if li == len(cfg.CHAPTERS[ci]["lines"]) - 1 else 0)
        if li == 0:
            chapter_starts[ci] = t
        starts.append(t)
        durs.append(dur)
        t += dur
    total = t
    ch_end = {ci: chapter_starts.get(ci + 1, total) for ci in chapter_starts}
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

    # 映像: 1秒に FPS 枚のコマを描いて、そのまま ffmpeg に渡す（図のアニメーション・口パク・まばたき）
    out = os.path.join(here, cfg.OUT)
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
                             "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                             "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000",
                             "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                            stdin=subprocess.PIPE)
    parts, settled = {}, {}

    def slide_frame(ci, tc):
        """章 ci の、章の中の経過時間 tc での画面（立ち絵・テロップ以外）"""
        global ANIM_T
        if ci in settled:
            return settled[ci], ("S", ci)
        if ci not in parts:
            parts[ci] = slide_parts(bg, cfg, ci, cfg.CHAPTERS[ci])
        p = parts[ci]
        fig, tch = p["fig"], ch_end[ci] - chapter_starts[ci]
        live = fig["kind"] in LIVE_KINDS
        if live:
            ANIM_T = tc
            fl = Image.new("RGBA", (W, H))
            fig_area(fl, p["box"], fig, cfg)
            ANIM_T = None
        else:
            if "fl" not in p:
                p["fl"] = Image.new("RGBA", (W, H))
                fig_area(p["fl"], p["box"], fig, cfg)
            fl = p["fl"]
        fm, bm = fig_mask(fig, p["box"], tc, tch), bullets_mask(p["bul_rects"], tc, tch)
        img = Image.alpha_composite(Image.alpha_composite(p["base"], masked(p["bul"], bm)), masked(fl, fm))
        if not live and fm is None and bm is None:
            settled[ci] = img  # これ以上変化しない章は、使い回す
            return img, ("S", ci)
        return img, ("F", ci, round(tc * FPS))

    fi = 0
    for n, ((ci, li, spk, disp, say), v) in enumerate(zip(lines, voices)):
        dur = durs[n]
        ex = expression(spk, disp, tags[n])
        pages = subtitle_pages(disp)
        bounds = np.cumsum([0] + pages) / sum(pages) * (dur - 0.3)  # ページの切り替え時刻
        overlays = {}
        prev_key, prev_bytes = None, None
        nfr = int(round((starts[n] + dur) * FPS)) - fi
        for k in range(nfr):
            tt = k / FPS
            # 口の開きは、そのコマの間の声の大きさ（RMS = 二乗平均の平方根）で3段階に分ける
            page = max(0, min(len(pages) - 1, int(np.searchsorted(bounds, tt, side="right")) - 1))
            seg = v[int(max(0, tt - 0.1) * SR): int(max(0, tt - 0.1 + 1 / FPS) * SR)]
            rms = float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0
            mouth = (0 if rms < 0.025 else (1 if rms < 0.07 else 2)) if portraits(spk) else 0
            blink = tuple(c for c in SPK if portraits(c) and blinking(c, starts[n] + tt))
            okey = (page, mouth, blink)
            if okey not in overlays:
                overlays[okey] = line_overlay(spk, disp, ex, mouth, page, blink)
            sl, skey = slide_frame(ci, starts[n] - chapter_starts[ci] + tt)
            key = (skey, okey)
            if key != prev_key:
                prev_bytes = Image.alpha_composite(sl, overlays[okey]).convert("RGB").tobytes()
                prev_key = key
            proc.stdin.write(prev_bytes)
        fi += nfr
        if n % 10 == 0:
            print(f"  frames {fi} / {int(total * FPS)}", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg failed")
    thumbnail(bg, cfg, os.path.join(here, "thumbnail.png"))
    with open(os.path.join(here, "chapters.txt"), "w") as f:
        for ci, st in chapter_starts.items():
            f.write(f"{int(st // 60)}:{int(st % 60):02d} {cfg.CHAPTERS[ci]['title']}\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
