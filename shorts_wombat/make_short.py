#!/usr/bin/env python3
"""YouTube Shorts 雑学動画ジェネレーター「ウォンバットのうんちはなぜ四角い？」

構成:
  1. Open JTalk (HTS音声合成) で各シーンのナレーションWAVを生成
  2. WAVの長さに合わせてPillowで 1080x1920 / 30fps のフレームを描画
  3. numpyで簡単なBGMを合成し、ナレーションとミックス
  4. ffmpeg で H.264 + AAC の MP4 に書き出し

必要: ffmpeg, open_jtalk, naist-jdic, mei_normal.htsvoice + mei_happy.htsvoice, Pillow, numpy
使い方: python3 make_short.py [--voice-dir 声モデルのあるフォルダ]
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

# (ナレーション読み上げ文, 画面の見出し, 画面の字幕, 絵文字 or "@図", 強調色)
# 最後のシーンが冒頭につながる「ループ構成」
TITLE = "うんちが四角い動物！？"
SCENES = [
    ("サイコロみたいな、四角いうんちをする動物が、いるって知ってた？",
     "四角い\nうんち！？", "", "@cube", (255, 200, 120)),
    ("正体は、オーストラリアに住む、ウォンバット。",
     "正体は\nウォンバット", "オーストラリアの有袋類", "🇦🇺", (255, 220, 90)),
    ("お尻の穴が、四角いの？いいえ、穴は丸いんです。",
     "お尻の穴は\n丸い", "「四角い穴」説はハズレ", "⭕", (255, 110, 110)),
    ("秘密は、腸の壁。硬いところと、やわらかいところが、交互に並んでいます。",
     "腸の壁に\n硬い所と\n柔らかい所", "腸の断面イメージ", "@gut", (120, 220, 255)),
    ("腸の終わりのほうで、水分が抜けて固まるとき、腸の動きで押されて、角ができるんです。",
     "乾きながら\n角ができる", "腸の終盤で形が決まる", "💧", (140, 230, 140)),
    ("この研究は、2019年、イグノーベル賞を受賞しました。",
     "イグノーベル賞\n受賞！", "2019年 物理学賞", "🏆", (255, 210, 60)),
    ("だから、ウォンバットのうんちは、四角いんです。",
     "だから\nうんちが四角い", "フォローで毎日雑学！", "@cube", (255, 200, 120)),
]
SOURCE_NOTE = "出典: Yang et al. Soft Matter (2021) / タスマニア大学 / Ig Nobel 2019"


# ショート向けの声の設計:
#   hook  = 明るい声(mei_happy)・やや高め … 冒頭/驚き/オチで感情を乗せる
#   talk  = 通常の声(mei_normal)・抑揚強め … 説明は聞き取りやすく
#   -r: 話速, -fm: ピッチ(半音), -jf: 抑揚(F0変動)の強さ, -a: 声質(大きいほど明るく若い)
VOICE_PRESETS = {
    "hook": ("mei_happy.htsvoice", ["-r", "1.20", "-fm", "0.5", "-jf", "1.25", "-a", "0.56"]),
    "talk": ("mei_normal.htsvoice", ["-r", "1.22", "-fm", "2.0", "-jf", "1.35", "-a", "0.56"]),
}
# 各シーンの声（SCENES と同じ順番）
VOICE_STYLE = ["hook", "talk", "hook", "talk", "talk", "hook", "hook"]


def tts(text, path, voice_dir, style="talk"):
    model, opts = VOICE_PRESETS[style]
    subprocess.run(["open_jtalk", "-x", DIC, "-m", os.path.join(voice_dir, model), *opts,
                    "-ow", path], input=text.encode(), check=True)
    # 声の音質処理: 低域カット / こもり(250Hz)を軽く削る / 明瞭度(3kHz)を持ち上げる / コンプで音量を揃える
    proc = path.replace(".wav", "_fx.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-af",
                    "highpass=f=90,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=4,"
                    "acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2",
                    proc], check=True)
    path = proc
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


def grid_bg():
    """草原色グラデーション + 斜めの四角タイル（キューブがテーマ）"""
    y = np.linspace(0, 1, H)[:, None]
    top, bot = np.array([38, 62, 30]), np.array([14, 26, 12])
    grad = (top * (1 - y) + bot * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    img = Image.fromarray(grad.astype(np.uint8)).convert("RGBA")
    pat = Image.new("RGBA", (W * 2, H * 2))
    d = ImageDraw.Draw(pat)
    s = 120
    for gx in range(0, W * 2, s):
        for gy in range(0, H * 2, s):
            d.rounded_rectangle((gx + 12, gy + 12, gx + s - 12, gy + s - 12), 18,
                                outline=(200, 255, 160, 30), width=4)
    pat = pat.rotate(15, resample=Image.BICUBIC).crop((W // 2, H // 2, W // 2 + W, H // 2 + H))
    return Image.alpha_composite(img, pat)


def cube_img(size):
    """茶色のキューブ（四角いうんち）を3段積みで描く"""
    im = Image.new("RGBA", (size, size))
    d = ImageDraw.Draw(im)
    def cube(cx, cy, a):
        top = [(cx, cy - a), (cx + a, cy - a / 2), (cx, cy), (cx - a, cy - a / 2)]
        left = [(cx - a, cy - a / 2), (cx, cy), (cx, cy + a), (cx - a, cy + a / 2)]
        right = [(cx, cy), (cx + a, cy - a / 2), (cx + a, cy + a / 2), (cx, cy + a)]
        d.polygon(top, fill=(176, 120, 72), outline=(60, 35, 15), width=6)
        d.polygon(left, fill=(120, 76, 40), outline=(60, 35, 15), width=6)
        d.polygon(right, fill=(146, 96, 52), outline=(60, 35, 15), width=6)
    a = size * 0.2
    cube(size * 0.30, size * 0.62, a)
    cube(size * 0.70, size * 0.62, a)
    cube(size * 0.50, size * 0.30, a)
    return im.crop(im.getbbox())


def gut_img(size):
    """腸の断面: 硬い壁(濃い太線)と柔らかい壁(淡い線)が交互、中に角ばった便"""
    im = Image.new("RGBA", (size, size))
    d = ImageDraw.Draw(im)
    c, R = size / 2, size * 0.33
    for k in range(4):
        a0 = 45 + 90 * k
        d.arc((c - R, c - R, c + R, c + R), a0 - 22, a0 + 22, fill=(240, 90, 90), width=40)
        d.arc((c - R, c - R, c + R, c + R), a0 + 22, a0 + 68, fill=(255, 190, 190), width=20)
    r = R * 0.62
    pts = []
    for i in range(360):
        th = math.radians(i)
        # 角の丸い四角（スーパー楕円）
        x = abs(math.cos(th)) ** 0.5 * (1 if math.cos(th) >= 0 else -1)
        yv = abs(math.sin(th)) ** 0.5 * (1 if math.sin(th) >= 0 else -1)
        pts.append((c + r * x, c + r * yv))
    d.polygon(pts, fill=(146, 96, 52), outline=(60, 35, 15), width=6)
    f = ImageFont.truetype(FONT, int(size * 0.13))
    d.text((c + R * 0.55, c - R * 1.12), "硬", font=f, fill=(255, 255, 255), stroke_width=5, stroke_fill=(0, 0, 0))
    d.text((c + R * 1.0, c - R * 0.16), "柔", font=f, fill=(255, 255, 255), stroke_width=5, stroke_fill=(0, 0, 0))
    return im


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
                     stroke_width=stroke, stroke_fill=(10, 20, 5))
    return bbox[3] - bbox[1]


def scene_layer(head, sub, color, idx):
    """見出しと字幕のレイヤー（透明背景）"""
    layer = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(layer)
    lines = head.split("\n")
    size = 150 if max(len(s) for s in lines) <= 6 and len(lines) <= 2 else 118
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
    d.rounded_rectangle((60, 150, W - 60, 290), 40, fill=(120, 200, 80, 235))
    title = TITLE
    bb = d.textbbox((0, 0), title, font=tf)
    d.text(((W - (bb[2] - bb[0])) / 2, 185), title, font=tf, fill=(15, 35, 5, 255))
    # 出典
    nf = ImageFont.truetype(FONT, 30)
    bb = d.textbbox((0, 0), SOURCE_NOTE, font=nf)
    d.text(((W - (bb[2] - bb[0])) / 2, H - 260), SOURCE_NOTE, font=nf, fill=(220, 255, 200, 170))
    return layer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice-dir", default=os.path.join(HERE, "..", "shorts_honey"),
                    help="mei_normal.htsvoice と mei_happy.htsvoice があるフォルダ")
    ap.add_argument("--out", default=os.path.join(HERE, "wombat_short.mp4"))
    args = ap.parse_args()

    tmp = tempfile.mkdtemp()
    gap = 0.22  # 間を詰めてテンポよく
    voices, durs = [], []
    assert len(VOICE_STYLE) == len(SCENES)
    for i, (narr, *_rest) in enumerate(SCENES):
        a = tts(narr, os.path.join(tmp, f"v{i}.wav"), args.voice_dir, VOICE_STYLE[i])
        voices.append(a)
        durs.append(len(a) / SR + gap)
    total = sum(durs) + 0.5
    print(f"total {total:.1f}s")
    assert total < 60, "Shortsは60秒以内に"

    # 音声ミックス
    music = bgm(total)
    vo = np.zeros_like(music)
    pos = 0.15
    for a, du in zip(voices, durs):
        s = int(pos * SR)
        vo[s:s + len(a)] += a
        pos += du
    # ダッキング: 声が鳴っている間はBGMを下げる（声の包絡線を平滑化してゲインに）
    env = np.convolve(np.abs(vo), np.ones(int(0.05 * SR)) / int(0.05 * SR), "same")
    active = np.convolve((env > 0.01).astype(float), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
    music *= 1 - 0.55 * np.clip(active * 1.5, 0, 1)
    mix = vo * 0.9 + music * 1.3
    mix = np.clip(mix / max(1.0, np.abs(mix).max() / 0.95), -1, 1)
    wav_path = os.path.join(tmp, "mix.wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

    bg = grid_bg().convert("RGBA")
    layers = [scene_layer(h, s, c, i) for i, (_, h, s, _e, c) in enumerate(SCENES)]
    emojis = [cube_img(440) if e == '@cube' else gut_img(560) if e == '@gut' else emoji_img(e, 380)
              for (*_x, e, _c) in SCENES]
    glow = Image.new("RGBA", (W, H))
    ImageDraw.Draw(glow).ellipse((W / 2 - 330, 400, W / 2 + 330, 960), fill=(220, 255, 150, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    base = Image.alpha_composite(bg, glow)

    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav_path,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", args.out],
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
        d.rectangle((0, H - 18, int(W * t / total), H), fill=(140, 220, 90, 255))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", args.out)


if __name__ == "__main__":
    main()
