#!/usr/bin/env python3
"""YouTube Shorts 雑学動画ジェネレーター「はちみつはなぜ腐らない？」

構成:
  1. Open JTalk (HTS音声合成) で各シーンのナレーションWAVを生成
  2. WAVの長さに合わせてPillowで 1080x1920 / 30fps のフレームを描画
  3. numpyで簡単なBGMを合成し、ナレーションとミックス
  4. ffmpeg で H.264 + AAC の MP4 に書き出し

必要: ffmpeg, open_jtalk, naist-jdic, mei_normal.htsvoice, Pillow, numpy
使い方: python3 make_short.py [--voice path/to/mei_normal.htsvoice]
"""
import argparse
import math
import os
import subprocess
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, SR = 1080, 1920, 30, 48000
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
DIC = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
HERE = os.path.dirname(os.path.abspath(__file__))

# (ナレーション読み上げ文, 画面の見出し, 画面の字幕, 絵文字, 強調色)
SCENES = [
    ("3000年前のはちみつ、まだ食べられるって、知ってた？",
     "3000年前の\nはちみつ\n食べられる！？", "", "🍯", (255, 196, 0)),
    ("古代エジプトの墓から見つかったはちみつは、今でも食べられる状態だったと言われています。",
     "古代エジプトの\n墓から発見", "数千年たっても保存状態良好", "🏺", (255, 170, 60)),
    ("腐らない理由、その1。水分が20%以下と少なく、糖がとても濃いから。",
     "理由①\n水分が少ない", "水分20%以下・糖分約80%", "💧", (90, 200, 255)),
    ("濃い糖が、浸透圧で菌の水分をうばうので、菌は増えられません。",
     "浸透圧で\n菌がカラカラに", "糖の濃い側へ水が引っぱられる", "🦠", (140, 230, 120)),
    ("理由、その2。ピーエイチが3から4.5ほどの酸性で、菌が苦手な環境なんです。",
     "理由②\n酸性", "pH 約3〜4.5", "🍋", (255, 235, 80)),
    ("理由、その3。ミツバチの酵素が、殺菌作用のある過酸化水素を、つくり出します。",
     "理由③\nハチの酵素が\n過酸化水素を生成", "グルコースオキシダーゼ → H2O2", "🐝", (255, 200, 40)),
    ("ただし、1歳未満の赤ちゃんには、乳児ボツリヌス症のおそれがあるので、与えないでください。",
     "注意！\n1歳未満には\n与えない", "乳児ボツリヌス症の予防", "👶", (255, 90, 90)),
    ("保存は、フタをしっかり閉めて。湿気を吸うと、発酵することもあります。フォローで、毎日雑学！",
     "フタを閉めて\n保存しよう", "フォローで毎日雑学！", "✅", (120, 230, 160)),
]
SOURCE_NOTE = "出典: Smithsonian Magazine / Codex Alimentarius / 厚生労働省"


def tts(text, path, voice):
    subprocess.run(["open_jtalk", "-x", DIC, "-m", voice, "-r", "1.12",
                    "-fm", "1.5", "-ow", path], input=text.encode(), check=True)
    with wave.open(path) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    # 48kHz へ線形補間でリサンプル
    n = int(len(a) * SR / sr)
    return np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a)


def bgm(seconds):
    """ペンタトニックの軽いアルペジオ + パッド（ADSR風の減衰付き正弦波）"""
    t = np.arange(int(seconds * SR)) / SR
    out = np.zeros_like(t)
    bpm, base = 112, 261.63  # C4
    beat = 60 / bpm / 2  # 8分音符
    penta = [0, 2, 4, 7, 9, 12, 9, 7]
    chords = [0, -3, 5, 7]  # C, Am, F, G のルート移動（半音）
    note_len = int(beat * SR)
    for i in range(int(seconds / beat)):
        root = chords[(i // 16) % 4]
        f = base * 2 ** ((root + penta[i % 8]) / 12)
        s = i * note_len
        tt = np.arange(min(note_len * 3, len(t) - s)) / SR
        env = np.exp(-tt * 6)
        out[s:s + len(tt)] += 0.10 * env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt))
    for k in range(int(seconds / (beat * 16)) + 1):
        root = chords[k % 4]
        s = int(k * beat * 16 * SR)
        L = min(int(beat * 16 * SR), len(t) - s)
        if L <= 0:
            break
        tt = np.arange(L) / SR
        env = np.minimum(1, tt * 4) * np.minimum(1, (L / SR - tt) * 4)
        for iv in (0, 4, 7):
            f = base / 2 * 2 ** ((root + iv) / 12)
            out[s:s + L] += 0.035 * env * np.sin(2 * np.pi * f * tt)
    fade = np.minimum(1, np.minimum(t / 0.5, (seconds - t) / 1.0))
    return out * fade


def hexagon_bg():
    """はちみつ色グラデーション + ハニカム模様"""
    y = np.linspace(0, 1, H)[:, None]
    top, bot = np.array([60, 30, 5]), np.array([25, 10, 2])
    grad = (top * (1 - y) + bot * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    img = Image.fromarray(grad.astype(np.uint8))
    d = ImageDraw.Draw(img, "RGBA")
    r = 70
    for row in range(-1, int(H / (r * 1.5)) + 2):
        for col in range(-1, int(W / (r * math.sqrt(3))) + 2):
            cx = col * r * math.sqrt(3) + (row % 2) * r * math.sqrt(3) / 2
            cy = row * r * 1.5
            pts = [(cx + r * math.cos(math.radians(60 * k + 30)),
                    cy + r * math.sin(math.radians(60 * k + 30))) for k in range(6)]
            d.polygon(pts, outline=(255, 180, 40, 38), width=4)
    return img


def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((size, int(size * im.height / im.width)), Image.LANCZOS)


def draw_text_center(d, text, y, font, fill, stroke=10, spacing=18):
    bbox = d.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align="center")
    x = (W - (bbox[2] - bbox[0])) / 2
    d.multiline_text((x, y), text, font=font, fill=fill, spacing=spacing, align="center",
                     stroke_width=stroke, stroke_fill=(20, 8, 0))
    return bbox[3] - bbox[1]


def scene_layer(head, sub, color, idx):
    """見出しと字幕のレイヤー（透明背景）"""
    layer = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(layer)
    lines = head.split("\n")
    size = 150 if max(len(s) for s in lines) <= 7 and len(lines) <= 2 else 118
    hf = ImageFont.truetype(FONT, size)
    th = draw_text_center(d, head, 0, hf, (0, 0, 0, 0), 0)  # 高さ計測
    layer = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(layer)
    y0 = 1230 - th / 2
    draw_text_center(d, head, y0, hf, color + (255,), 12)
    if sub:
        sf = ImageFont.truetype(FONT, 58)
        bb = d.textbbox((0, 0), sub, font=sf)
        tw = bb[2] - bb[0]
        bx, by = (W - tw) / 2 - 40, y0 + th + 90
        d.rounded_rectangle((bx, by, bx + tw + 80, by + 110), 30, fill=(0, 0, 0, 150))
        d.text((bx + 40, by + 22), sub, font=sf, fill=(255, 255, 255, 255))
    # 上部タイトル帯
    tf = ImageFont.truetype(FONT, 64)
    d.rounded_rectangle((60, 150, W - 60, 290), 40, fill=(255, 190, 0, 235))
    title = "はちみつは なぜ腐らない？"
    bb = d.textbbox((0, 0), title, font=tf)
    d.text(((W - (bb[2] - bb[0])) / 2, 185), title, font=tf, fill=(40, 15, 0, 255))
    # 出典
    nf = ImageFont.truetype(FONT, 30)
    bb = d.textbbox((0, 0), SOURCE_NOTE, font=nf)
    d.text(((W - (bb[2] - bb[0])) / 2, H - 260), SOURCE_NOTE, font=nf, fill=(255, 230, 180, 170))
    return layer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default=os.path.join(HERE, "mei_normal.htsvoice"))
    ap.add_argument("--out", default=os.path.join(HERE, "honey_short.mp4"))
    args = ap.parse_args()

    tmp = tempfile.mkdtemp()
    gap = 0.35
    voices, durs = [], []
    for i, (narr, *_rest) in enumerate(SCENES):
        a = tts(narr, os.path.join(tmp, f"v{i}.wav"), args.voice)
        voices.append(a)
        durs.append(len(a) / SR + gap)
    total = sum(durs) + 0.5
    print(f"total {total:.1f}s")
    assert total < 60, "Shortsは60秒以内に"

    # 音声ミックス
    mix = bgm(total)
    pos = 0.15
    for a, du in zip(voices, durs):
        s = int(pos * SR)
        mix[s:s + len(a)] += a * 0.95
        pos += du
    mix = np.clip(mix / max(1.0, np.abs(mix).max() / 0.95), -1, 1)
    wav_path = os.path.join(tmp, "mix.wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

    bg = hexagon_bg().convert("RGBA")
    layers = [scene_layer(h, s, c, i) for i, (_, h, s, _e, c) in enumerate(SCENES)]
    emojis = [emoji_img(e, 380) for (*_x, e, _c) in SCENES]
    glow = Image.new("RGBA", (W, H))
    ImageDraw.Draw(glow).ellipse((W / 2 - 330, 400, W / 2 + 330, 960), fill=(255, 200, 60, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    base = Image.alpha_composite(bg, glow)

    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav_path,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", args.out],
        stdin=subprocess.PIPE)
    starts = np.cumsum([0.15] + durs[:-1])
    nframes = int(total * FPS)
    for fi in range(nframes):
        t = fi / FPS
        si = max(0, int(np.searchsorted(starts, t, side="right")) - 1)
        lt = t - starts[si]
        frame = base.copy()
        # 絵文字: ポップイン（オーバーシュート付き）+ ふわふわ上下
        k = min(1, lt / 0.35)
        scale = max(0.2, 0.5 + 0.5 * k + 0.15 * math.sin(k * math.pi))
        em = emojis[si]
        em2 = em.resize((int(em.width * scale), int(em.height * scale)))
        bob = 14 * math.sin(t * 2.4)
        frame.alpha_composite(em2, (int(W / 2 - em2.width / 2), int(680 - em2.height / 2 + bob)))
        # 見出し: 下からスライドイン
        ly = int(60 * (1 - min(1, lt / 0.25)) ** 2)
        lay = layers[si]
        if ly:
            frame.alpha_composite(lay.crop((0, 0, W, H - ly)), (0, ly))
        else:
            frame.alpha_composite(lay)
        # 進捗バー
        d = ImageDraw.Draw(frame)
        d.rectangle((0, H - 18, int(W * t / total), H), fill=(255, 200, 0, 255))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", args.out)


if __name__ == "__main__":
    main()
