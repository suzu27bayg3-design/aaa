#!/usr/bin/env python3
"""MLBレジェンド紹介ショート（スポーツ中継の成績テロップ風）: ルー・ゲーリッグ

シーン: タイトル → 通算打撃成績 → 鉄人の記録 → 獲得タイトル → 最も輝いた年(1927) → 締め
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
NAME_EN, NAME_JP, YEARS = "LOU GEHRIG", "ルー・ゲーリッグ", "1923–1939"
SCENES = [
    dict(kind="title", caption="2130試合連続出場。鉄の馬と呼ばれた男、ルー・ゲーリッグの成績を見ていくのだ！"),
    dict(kind="board", head="通算打撃成績", eng="CAREER BATTING",
         caption="通算打率.340、493本塁打、1,995打点。OPSは1.080なのだ！",
         rows=[("打率", ".340"), ("本塁打", "493"), ("打点", "1,995"),
               ("出塁率", ".447"), ("長打率", ".632"), ("OPS", "1.080")], hl=5),
    dict(kind="board", head="鉄人の記録", eng="THE IRON HORSE",
         caption="約14年間休まず2,130試合連続出場。満塁本塁打は23本なのだ。",
         rows=[("連続試合出場", "2,130"), ("満塁本塁打", "23"), ("1931年の打点", "184")], hl=0),
    dict(kind="titles", head="獲得タイトル", eng="AWARDS & TITLES",
         caption="MVP2回、1934年には三冠王。ワールドシリーズも6回制覇！",
         rows=[("MVP", "2", "回 27・36"), ("三冠王", "1", "回 1934"), ("本塁打王", "3", "回"),
               ("打点王", "5", "回"), ("首位打者", "1", "回 1934"), ("世界一", "6", "回")]),
    dict(kind="board", head="最も輝いた年", eng="BEST SEASON", year="1927",
         caption="最も輝いたのは1927年。打率.373、47本塁打、175打点でMVP！",
         rows=[("打率", ".373"), ("本塁打", "47"), ("打点", "175"), ("得点", "149"),
               ("安打", "218"), ("塁打", "447"), ("OPS", "1.240")], hl=6),
    dict(kind="outro", caption="引退のとき「地球上で最も幸運な男」と語った、それがルー・ゲーリッグなのだ。"),
]
SOURCE = "Stats: 野球殿堂 / MLB.com / Baseball-Reference / SABR"
CREDIT = "VOICEVOX:ずんだもん"


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
    d.text((60, 235), NAME_EN, font=num(118), fill=WHITE)
    d.text((66, 375), f"{NAME_JP}  {YEARS}", font=jp(40, True), fill=GOLD)
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
    off = int(300 * (1 - a))
    d.text((60 - off, 600), "LOU", font=num(250), fill=WHITE)
    d.text((60 + off, 850), "GEHRIG", font=num(210), fill=GOLD)
    d.text((70, 1110), NAME_JP, font=jp(96), fill=WHITE)
    if lt > 0.5:
        for i, (t, c, wdt) in enumerate((("YANKEES", (40, 70, 160), 300), ("#4", RED, 150), ("1923–1939", (120, 120, 140), 380))):
            x = 70 + sum(w_ + 25 for _, _, w_ in ((None, None, 300), (None, None, 150))[:i])
            d.rounded_rectangle((x, 1260, x + wdt, 1340), 16, fill=c)
            tw = d.textlength(t, font=num(46))
            d.text((x + (wdt - tw) / 2, 1272), t, font=num(46), fill=WHITE)
    d.polygon([(0, 150), (W, 150), (W, 400), (0, 440)], fill=RED)
    d.text((60, 175), "2,130試合連続出場", font=jp(80), fill=WHITE)
    d.text((60, 280), "鉄の馬", font=jp(110), fill=GOLD)
    d.text((420, 315), "THE IRON HORSE", font=num(64), fill=WHITE)


def draw_outro(img, lt):
    d = ImageDraw.Draw(img)
    a = ease(lt / 0.4)
    d.text((60, 600), "1939年 引退スピーチ", font=jp(64, True), fill=GOLD)
    d.text((60, 720), "「地球上で", font=jp(120), fill=WHITE)
    d.text((60, 880), "　最も幸運な男」", font=jp(120), fill=WHITE)
    d.text((70, 1060), "the luckiest man on the face of the earth", font=num(36), fill=(200, 210, 240))
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
    sweep = sweep_layer()
    out = os.path.join(HERE, "gehrig_short.mp4")
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
        caption(d, sc["caption"])
        d.text((W - 60, 1665), CREDIT, font=jp(26, True), fill=(220, 225, 255), anchor="ra")
        d.rectangle((0, H - 16, int(W * t / total), H), fill=GOLD)
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", out)


if __name__ == "__main__":
    main()
