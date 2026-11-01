#!/usr/bin/env python3
"""MLBレジェンド紹介ショート（スポーツ中継の成績テロップ風）: ベーブ・ルース

シーン: タイトル → 通算打撃成績 → 通算投手成績 → 獲得タイトル → 最も輝いた年(1921) → 締め
各行が順番にスライドイン、数字は0から目標値までカウントアップ。字幕つき（無音視聴対策）。
音声: voicevox/ の 001〜006 を使用（voicevox_synth.py で生成）
"""
import importlib.util
import math
import os
import subprocess
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("base", os.path.join(HERE, "..", "shorts_honey", "make_short.py"))
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

W, H, FPS, SR = 1080, 1920, 30, 48000
JP = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
JPB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
NUM = "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"
GOLD, NAVY, RED, WHITE = (255, 200, 60), (10, 18, 48), (215, 40, 55), (255, 255, 255)


def jp(size, bold=False):
    return ImageFont.truetype(JPB if bold else JP, size, index=0)


def num(size):
    return ImageFont.truetype(NUM, size)


# ---- 台本と表示データ -------------------------------------------------------
SCENES = [
    dict(kind="title", caption="大谷翔平より100年前の二刀流、ベーブ・ルースの成績を見ていくのだ！"),
    dict(kind="board", head="通算打撃成績", eng="CAREER BATTING",
         caption="通算打率.342、714本塁打。OPSはなんと1.164なのだ！",
         rows=[("打率", ".342"), ("本塁打", "714"), ("打点", "2,214"),
               ("出塁率", ".474"), ("長打率", ".690"), ("OPS", "1.164")], hl=5),
    dict(kind="board", head="通算投手成績", eng="CAREER PITCHING",
         caption="投手としても94勝46敗、防御率2.28なのだ。",
         rows=[("登板", "163"), ("勝利", "94"), ("敗戦", "46"), ("勝率", ".671"), ("防御率", "2.28")], hl=4),
    dict(kind="titles", head="獲得タイトル", eng="AWARDS & TITLES",
         caption="本塁打王12回、打点王6回。首位打者に最優秀防御率、MVPまで！",
         rows=[("本塁打王", "12", "回"), ("打点王", "6", "回"), ("首位打者", "1", "回 1924"),
               ("最優秀防御率", "1", "回 1916"), ("MVP", "1", "回 1923"), ("世界一", "7", "回")]),
    dict(kind="board", head="最も輝いた年", eng="BEST SEASON", year="1921",
         caption="最も輝いたのは1921年。59本塁打、171打点、OPS1.359！",
         rows=[("打率", ".378"), ("本塁打", "59"), ("打点", "171"), ("得点", "177"),
               ("出塁率", ".512"), ("長打率", ".846"), ("OPS", "1.359")], hl=6),
    dict(kind="outro", caption="打っても投げても歴史に残る、それがベーブ・ルースなのだ！"),
]
SOURCE = "Stats: 野球殿堂 / MLB.com / Baseball-Reference / SABR"
CREDIT = "VOICEVOX:ずんだもん"
SHOW_CAPTION = False  # 字幕（ナレーションの文字起こし）を出す場合は True


# ---- 数値フォーマット（カウントアップ用） ---------------------------------------
def fmt(target, p):
    """target 文字列の書式を保ったまま、割合 p (0..1) の値を返す"""
    t = target.replace(",", "")
    dec = len(t.split(".")[1]) if "." in t else 0
    v = float(t) * p
    s = f"{v:.{dec}f}" if dec else f"{int(round(v)):,}" if "," in target else str(int(round(v)))
    if target.startswith(".") and s.startswith("0"):
        s = s[1:]
    return s


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


# ---- 背景・共通パーツ ----------------------------------------------------------
def make_bg():
    y = np.linspace(0, 1, H)[:, None]
    top, bot = np.array([16, 30, 78]), np.array([4, 8, 24])
    g = (top * (1 - y) + bot * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    img = Image.fromarray(g.astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(lay)
    for x in range(-H, W, 46):  # 斜めの細線
        d.line((x, H, x + H, 0), fill=(255, 255, 255, 10), width=3)
    # 下から赤いグロー
    glow = Image.new("RGBA", (W, H))
    ImageDraw.Draw(glow).ellipse((-300, 1500, W + 300, 2600), fill=RED + (90,))
    img = Image.alpha_composite(img, lay)
    return Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(120)))


def sweep_layer():
    """斜めに流れる光の帯（毎フレーム位置をずらす）"""
    band = Image.new("RGBA", (W * 3, H))
    d = ImageDraw.Draw(band)
    d.polygon([(W, 0), (W + 160, 0), (W + 160 - 700, H), (W - 700, H)], fill=(255, 255, 255, 16))
    return band.filter(ImageFilter.GaussianBlur(30))


def header(d):
    """上部: MLB LEGENDS リボン + 選手名"""
    d.polygon([(0, 150), (420, 150), (380, 220), (0, 220)], fill=RED)
    d.text((40, 158), "MLB LEGENDS", font=num(48), fill=WHITE)
    d.text((60, 235), "BABE RUTH", font=num(118), fill=WHITE)
    d.text((66, 375), "ベーブ・ルース  1914–1935", font=jp(40, True), fill=GOLD)
    d.text((60, 90), SOURCE, font=jp(24, True), fill=(200, 210, 240))


def section(d, head, eng, lt, year=None):
    """セクション見出し（左からスライドイン）"""
    off = int(-600 * (1 - ease(lt / 0.35)))
    y = 470
    d.polygon([(off, y), (off + 1000, y), (off + 960, y + 130), (off, y + 130)], fill=GOLD)
    d.text((off + 60, y + 8), head, font=jp(84), fill=NAVY)
    hb = d.textbbox((0, 0), head, font=jp(84))
    x = off + 60 + hb[2] + 24
    if year:
        d.text((x, y + 65), year, font=num(108), fill=RED, anchor="lm")
    else:
        d.text((x, y + 88), eng, font=num(34), fill=NAVY, anchor="ls")


def caption(d, text):
    """字幕（無音視聴向け）: 2行まで、下部のUIと重ならない位置"""
    import re
    f = jp(46, True)
    # 英数字・小数点のかたまりは途中で改行しない。句読点は行頭に来ないようにする
    tokens = re.findall(r"[0-9A-Za-z.,]+|.", text)
    lines, cur = [], ""
    for tok in tokens:
        if d.textlength(cur + tok, font=f) > 900 and cur and tok not in "、。！？":
            lines.append(cur)
            cur = tok
        else:
            cur += tok
    lines.append(cur)
    y = 1500
    box_h = 70 * len(lines) + 30
    d.rounded_rectangle((60, y - 15, W - 60, y - 15 + box_h), 24, fill=(0, 0, 0, 170))
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        d.text(((W - tw) / 2, y + i * 70), ln, font=f, fill=WHITE)




# ---- 写真（photos/ フォルダに置くと自動で使う） ---------------------------------
from PIL import ImageOps


def load_photos(folder):
    """photos/ の画像を読み込み、紺〜クリームのデュオトーンに加工して返す（名前順）。
    1枚目=タイトル用（人物の顔が分かるもの推奨）。クレジットは photos/credits.txt に1行で書く。"""
    if not os.path.isdir(folder):
        return [], ""
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
    out = []
    for f in files:
        im = Image.open(os.path.join(folder, f)).convert("L")
        im = ImageOps.autocontrast(im, cutoff=1)
        im = ImageOps.colorize(im, black=(8, 14, 40), white=(245, 232, 205), mid=(110, 110, 120))
        # 1.12倍の余白をつけて画面を覆うサイズに（パン・ズーム用）
        s = max(W * 1.12 / im.width, H * 1.12 / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        out.append(im.convert("RGBA"))
    cpath = os.path.join(folder, "credits.txt")
    credit = open(cpath, encoding="utf-8").read().strip() if os.path.exists(cpath) else ""
    return out, credit


def photo_frame(ph, lt, dur, darkness, seed=0):
    """ケン・バーンズ効果: ゆっくりズームしながら少しパン"""
    p = max(0.0, min(1.0, lt / max(dur, 0.1)))
    z = 1.0 + 0.08 * p                      # 1.00 → 1.08
    cw, ch = ph.width / z, ph.height / z
    cw, ch = min(cw, ph.width), min(ch, ph.height)
    # 縦横比を画面に合わせる
    if cw / ch > W / H:
        cw = ch * W / H
    else:
        ch = cw * H / W
    dx = (ph.width - cw) * (0.5 + 0.3 * math.sin(seed + p * 1.2))
    dy = (ph.height - ch) * (0.35 + 0.15 * p)
    img = ph.crop((int(dx), int(dy), int(dx + cw), int(dy + ch))).resize((W, H), Image.BILINEAR)
    shade = Image.new("RGBA", (W, H), (6, 10, 30, int(255 * darkness)))
    return Image.alpha_composite(img, shade)


# ---- シーン描画 -----------------------------------------------------------------
def draw_board(img, sc, lt):
    d = ImageDraw.Draw(img)
    section(d, sc["head"], sc["eng"], lt, sc.get("year"))
    rows = sc["rows"]
    rh = 118 if len(rows) >= 7 else 130
    y0 = 640
    for i, row in enumerate(rows):
        t0 = 0.35 + 0.16 * i
        if lt < t0:
            continue
        a = ease((lt - t0) / 0.25)
        x = int(80 * (1 - a))
        y = y0 + i * rh
        lay = Image.new("RGBA", (W, H))
        ld = ImageDraw.Draw(lay)
        hl = sc.get("hl") == i
        fill = GOLD + (235,) if hl else ((255, 255, 255, 26) if i % 2 == 0 else (255, 255, 255, 12))
        ld.rounded_rectangle((60 + x, y, W - 60 + x, y + rh - 14), 18, fill=fill)
        ld.rectangle((60 + x, y, 72 + x, y + rh - 14), fill=RED if not hl else NAVY)
        tc = NAVY if hl else WHITE
        ld.text((105 + x, y + (rh - 14) / 2), row[0], font=jp(58), fill=tc, anchor="lm")
        p = ease((lt - t0 - 0.1) / 0.7)
        val = fmt(row[1], p)
        vc = NAVY if hl else GOLD
        if sc["kind"] == "titles":
            unit = row[2]
            uf = jp(40, True)
            uw = ld.textlength(unit, font=uf)
            ld.text((W - 90 + x - uw, y + (rh - 14) / 2 + 8), unit, font=uf, fill=WHITE, anchor="lm")
            ld.text((W - 110 + x - uw, y + (rh - 14) / 2), val, font=num(96), fill=vc, anchor="rm")
        else:
            ld.text((W - 95 + x, y + (rh - 14) / 2), val, font=num(100), fill=vc, anchor="rm")
        alpha = lay.split()[3].point(lambda v: int(v * a))
        lay.putalpha(alpha)
        img.alpha_composite(lay)


def draw_title(img, lt):
    d = ImageDraw.Draw(img)
    a = ease(lt / 0.4)
    # 巨大な名前
    off = int(300 * (1 - a))
    d.text((60 - off, 560), "BABE", font=num(270), fill=WHITE)
    d.text((60 + off, 820), "RUTH", font=num(270), fill=GOLD)
    d.text((70, 1110), "ベーブ・ルース", font=jp(96), fill=WHITE)
    if lt > 0.5:
        for i, (t, c) in enumerate((("RED SOX", RED), ("YANKEES", (40, 70, 160)), ("BRAVES", (120, 120, 140)))):
            x = 70 + i * 315
            d.rounded_rectangle((x, 1260, x + 290, 1340), 16, fill=c)
            tw = d.textlength(t, font=num(46))
            d.text((x + (290 - tw) / 2, 1272), t, font=num(46), fill=WHITE)
    # フック
    d.polygon([(0, 150), (W, 150), (W, 400), (0, 440)], fill=RED)
    d.text((60, 175), "大谷より100年前の", font=jp(80), fill=WHITE)
    d.text((60, 280), "二刀流", font=jp(110), fill=GOLD)
    d.text((440, 330), "1914–1935", font=num(70), fill=WHITE)


def draw_outro(img, lt):
    d = ImageDraw.Draw(img)
    a = ease(lt / 0.4)
    d.text((60, 600), "打っても", font=jp(130), fill=WHITE)
    d.text((60, 780), "投げても", font=jp(130), fill=WHITE)
    d.text((60, 960), "歴史に残る。", font=jp(130), fill=GOLD)
    if lt > 0.6:
        d.rounded_rectangle((60, 1200, W - 60, 1360), 30, fill=RED)
        d.text((W / 2, 1280), "次は誰を紹介する？ コメントで！", font=jp(56), fill=WHITE, anchor="mm")
    d.rectangle((0, int(560 - 20 * (1 - a)), int(W * a), 572), fill=GOLD)


# ---- メイン ---------------------------------------------------------------------
def main():
    folder = os.path.join(HERE, "voicevox")
    files = sorted(f for f in os.listdir(folder) if f.endswith(".wav"))
    assert len(files) == len(SCENES), f"音声 {len(files)} / シーン {len(SCENES)}"
    voices = [base.load_audio(os.path.join(folder, f), base.VOICE_FX) for f in files]
    gap = 0.3
    durs = [len(a) / SR + gap + (0.6 if SCENES[i]["kind"] in ("board", "titles") else 0)
            for i, a in enumerate(voices)]
    total = sum(durs) + 0.4
    print(f"total {total:.1f}s")
    assert total < 60

    music = base.bgm(total)
    vo = np.zeros_like(music)
    starts = np.cumsum([0.15] + durs[:-1])
    for a, s0 in zip(voices, starts):
        s = int(s0 * SR)
        vo[s:s + len(a)] += a[: len(vo) - s]
    env = np.convolve(np.abs(vo), np.ones(int(0.05 * SR)) / int(0.05 * SR), "same")
    active = np.convolve((env > 0.01).astype(float), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
    music *= 1 - 0.55 * np.clip(active * 1.5, 0, 1)
    mix = vo * 0.9 + music * 1.3
    mix = np.clip(mix / max(1.0, np.abs(mix).max() / 0.95), -1, 1)
    tmp = tempfile.mkdtemp()
    wav_path = os.path.join(tmp, "mix.wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

    bg = make_bg()
    photos, photo_credit = load_photos(os.path.join(HERE, "photos"))
    print(f"photos: {len(photos)}")
    sweep = sweep_layer()
    out = os.path.join(HERE, "ruth_short.mp4")
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
        sc = SCENES[si]
        if photos:
            if sc["kind"] == "title":
                ph, dk = photos[0], 0.25
            elif sc["kind"] == "outro":
                ph, dk = photos[-1], 0.45
            else:
                mid = photos[1:-1] if len(photos) >= 3 else photos  # 先頭=タイトル, 最後=締め
                ph, dk = mid[(si - 1) % len(mid)], 0.70
            frame = photo_frame(ph, lt, durs[si], dk, seed=si)
            if sc["kind"] == "title":  # 文字の読みやすさのため下半分を暗く
                g = Image.new("RGBA", (W, H))
                gd = ImageDraw.Draw(g)
                for yy in range(500, H, 8):
                    gd.rectangle((0, yy, W, yy + 8), fill=(6, 10, 30, int(min(220, (yy - 500) * 0.32))))
                frame = Image.alpha_composite(frame, g)
        else:
            frame = bg.copy()
        cx = int((t * 260) % (W * 2))
        frame.alpha_composite(sweep.crop((cx, 0, cx + W, H)))
        if sc["kind"] == "title":
            draw_title(frame, lt)
        elif sc["kind"] == "outro":
            header(ImageDraw.Draw(frame))
            draw_outro(frame, lt)
        else:
            header(ImageDraw.Draw(frame))
            draw_board(frame, sc, lt)
        d = ImageDraw.Draw(frame)
        if SHOW_CAPTION:
            caption(d, sc["caption"])
        d.text((W - 60, 1665), CREDIT, font=jp(26, True), fill=(220, 225, 255), anchor="ra")
        if photos and photo_credit:
            d.text((60, 1705), "Photo: " + photo_credit, font=jp(22, True), fill=(220, 225, 255))
        d.rectangle((0, H - 16, int(W * t / total), H), fill=GOLD)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", out)


if __name__ == "__main__":
    main()
