#!/usr/bin/env python3
"""YouTube Shorts 雑学動画ジェネレーター「100年前の二刀流 ベーブ・ルース」（MLBレジェンド紹介）

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
TITLE = "100年前の二刀流！？"
# 絵文字の代わりに "@count:数値:単位"（数字カウントアップ）, "@stat:左|右"（成績カード）, "@vs"（比較）
SCENES = [
    ("大谷翔平より100年以上前に、二刀流をやった男がいるって、知ってた？",
     "大谷より\n100年前の\n二刀流！？", "", "⚾", (255, 255, 255)),
    ("その名は、ベーブ・ルース。最初は、レッドソックスのエース投手でした。",
     "ベーブ・ルース", "1914年 レッドソックスでデビュー", "🧢", (255, 90, 90)),
    ("1918年には、投げて13勝、打って11本塁打。",
     "1918年\n投げて打って", "レッドソックス時代", "@stat:13勝|11本", (255, 210, 80)),
    ("ヤンキースに移ると打者に専念して、1927年には、シーズン60本塁打。",
     "1927年\nシーズン60本", "34年間破られなかった記録", "@count:60:本", (120, 190, 255)),
    ("通算714本塁打。この記録は、39年間も破られませんでした。",
     "通算714本塁打", "1974年まで歴代1位", "@count:714:本", (255, 210, 80)),
    ("1934年には日本にも来て、全米チームの主砲として、大歓迎されました。",
     "1934年\n日本にも来た！", "日米野球 全米チームの一員", "🇯🇵", (255, 255, 255)),
    ("2022年、大谷が10勝10本を達成して、ルース以来104年ぶりと話題になりました。",
     "2022年\n大谷が並んだ", "同じシーズンに10勝＆10本塁打", "@vs", (255, 90, 90)),
    ("100年以上前の二刀流、それが、ベーブ・ルースです。",
     "100年前の\n二刀流\nベーブ・ルース", "フォローで毎日雑学！", "⚾", (255, 255, 255)),
]
SOURCE_NOTE = "出典: 野球殿堂 / MLB.com / SABR（成績は公式記録より）"


# ショート向けの声の設計:
#   hook  = 明るい声(mei_happy)・やや高め … 冒頭/驚き/オチで感情を乗せる
#   talk  = 通常の声(mei_normal)・抑揚強め … 説明は聞き取りやすく
#   -r: 話速, -fm: ピッチ(半音), -jf: 抑揚(F0変動)の強さ, -a: 声質(大きいほど明るく若い)
VOICE_PRESETS = {
    "hook": ("mei_happy.htsvoice", ["-r", "1.20", "-fm", "0.5", "-jf", "1.25", "-a", "0.56"]),
    "talk": ("mei_normal.htsvoice", ["-r", "1.22", "-fm", "2.0", "-jf", "1.35", "-a", "0.56"]),
}
# 各シーンの声（SCENES と同じ順番）
VOICE_STYLE = ["hook", "talk", "talk", "hook", "talk", "talk", "talk", "hook"]


VOICE_FX = ("highpass=f=90,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=4,"
            "acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2")


def load_audio(path, fx):
    """任意の音声ファイル(wav/mp3等)を 48kHz モノラル float に読み込む（ffmpeg経由）"""
    cmd = ["ffmpeg", "-loglevel", "error", "-i", path]
    if fx:
        cmd += ["-af", fx]
    cmd += ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)
    # 書き出し時に付く前後の無音を詰める（-45dBより小さい部分）
    idx = np.where(np.abs(a) > 10 ** (-45 / 20))[0]
    return a[max(0, idx[0] - int(0.03 * SR)): idx[-1] + int(0.08 * SR)] if len(idx) else a


def external_voices(folder):
    """VOICEVOX等で書き出した音声を名前順に返す（001_..., 002_... の連番を想定）"""
    exts = (".wav", ".mp3", ".m4a", ".ogg", ".flac")
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith(exts))
    assert len(files) == len(SCENES), f"{folder} の音声は {len(files)} 個、シーンは {len(SCENES)} 個です"
    for f, (narr, *_r) in zip(files, SCENES):
        print(f"  {f}  ←  {narr[:20]}…")
    return [load_audio(os.path.join(folder, f), VOICE_FX) for f in files]


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
    """紺のグラデーション + 縦じま（ピンストライプ）"""
    y = np.linspace(0, 1, H)[:, None]
    top, bot = np.array([20, 32, 70]), np.array([6, 10, 26])
    grad = (top * (1 - y) + bot * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    img = Image.fromarray(grad.astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(lay)
    for x in range(30, W, 70):
        d.line((x, 0, x, H), fill=(255, 255, 255, 22), width=4)
    return Image.alpha_composite(img, lay)


def _card(d, box, big, small, color, fbig, fsmall):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 36, fill=(255, 255, 255, 235), outline=color, width=10)
    bb = d.textbbox((0, 0), big, font=fbig)
    d.text(((x0 + x1 - (bb[2] - bb[0])) / 2, y0 + 30), big, font=fbig, fill=(15, 25, 60))
    if small:
        bb = d.textbbox((0, 0), small, font=fsmall)
        d.text(((x0 + x1 - (bb[2] - bb[0])) / 2, y1 - 95), small, font=fsmall, fill=color)


def stat_img(spec):
    """成績カード（左|右）"""
    left, right = spec.split("|")
    w, h = 960, 460
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    fb, fs = ImageFont.truetype(FONT, 150), ImageFont.truetype(FONT, 64)
    _card(d, (0, 20, 460, 440), left, "投手で", (220, 60, 60), fb, fs)
    _card(d, (500, 20, 960, 440), right, "打者で", (40, 90, 200), fb, fs)
    return im


def vs_img():
    """1918年ルース vs 2022年大谷（同一シーズン2桁勝利＆2桁本塁打）"""
    w, h = 920, 540
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    fy, fn, fs = ImageFont.truetype(FONT, 56), ImageFont.truetype(FONT, 80), ImageFont.truetype(FONT, 60)
    for x0, year, name, st, col in ((0, "1918年", "ルース", "13勝・11本", (220, 60, 60)),
                                    (480, "2022年", "大谷", "15勝・34本", (40, 90, 200))):
        d.rounded_rectangle((x0, 0, x0 + 440, h), 36, fill=(255, 255, 255, 235), outline=col, width=10)
        for txt, f, yy, c in ((year, fy, 40, col), (name, fn, 150, (15, 25, 60)), (st, fs, 330, col)):
            bb = d.textbbox((0, 0), txt, font=f)
            d.text((x0 + (440 - (bb[2] - bb[0])) / 2, yy), txt, font=f, fill=c)
    fv = ImageFont.truetype(FONT, 90)
    d.ellipse((w / 2 - 70, h / 2 - 70, w / 2 + 70, h / 2 + 70), fill=(255, 210, 60), outline=(0, 0, 0), width=6)
    bb = d.textbbox((0, 0), "VS", font=fv)
    d.text((w / 2 - (bb[2] - bb[0]) / 2, h / 2 - 58), "VS", font=fv, fill=(0, 0, 0))
    return im


_COUNT_CACHE = {}


def count_img(value, unit, color):
    """カウントアップする大きな数字"""
    key = (value, unit, color)
    if key not in _COUNT_CACHE:
        im = Image.new("RGBA", (1000, 460))
        d = ImageDraw.Draw(im)
        fn, fu = ImageFont.truetype(FONT, 330), ImageFont.truetype(FONT, 140)
        num = str(value)
        bn = d.textbbox((0, 0), num, font=fn, stroke_width=14)
        bu = d.textbbox((0, 0), unit, font=fu, stroke_width=10)
        tw = (bn[2] - bn[0]) + 20 + (bu[2] - bu[0])
        x = (1000 - tw) / 2
        d.text((x, 40), num, font=fn, fill=color, stroke_width=14, stroke_fill=(0, 0, 0))
        d.text((x + (bn[2] - bn[0]) + 20, 230), unit, font=fu, fill=(255, 255, 255),
               stroke_width=10, stroke_fill=(0, 0, 0))
        _COUNT_CACHE[key] = im
    return _COUNT_CACHE[key]


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
                     stroke_width=stroke, stroke_fill=(5, 8, 25))
    return bbox[3] - bbox[1]


def scene_layer(head, sub, color, idx):
    """見出しと字幕のレイヤー（透明背景）"""
    layer = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(layer)
    lines = head.split("\n")
    size = 150 if len(lines) <= 2 else 118
    while True:  # 画面幅(左右60pxの余白)に収まるまで縮める
        hf = ImageFont.truetype(FONT, size)
        bb = d.multiline_textbbox((0, 0), head, font=hf, spacing=18, align="center", stroke_width=12)
        if bb[2] - bb[0] <= W - 120 or size <= 70:
            break
        size -= 6
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
    d.rounded_rectangle((60, 150, W - 60, 290), 40, fill=(220, 50, 60, 240))
    title = TITLE
    bb = d.textbbox((0, 0), title, font=tf)
    d.text(((W - (bb[2] - bb[0])) / 2, 185), title, font=tf, fill=(255, 255, 255, 255))
    # 出典
    nf = ImageFont.truetype(FONT, 30)
    bb = d.multiline_textbbox((0, 0), SOURCE_NOTE, font=nf, align="center")
    d.multiline_text(((W - (bb[2] - bb[0])) / 2, H - 260), SOURCE_NOTE, font=nf, align="center",
                     fill=(220, 225, 255, 170))
    return layer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice-dir", default=os.path.join(HERE, "..", "shorts_honey"),
                    help="mei_normal.htsvoice と mei_happy.htsvoice があるフォルダ")
    ap.add_argument("--voice-files", default=None,
                    help="VOICEVOX等で書き出したシーン別音声のフォルダ（指定するとOpen JTalkの代わりに使う）")
    ap.add_argument("--credit", default="",
                    help="画面下に出すクレジット 例: 'VOICEVOX:ずんだもん'")
    ap.add_argument("--out", default=os.path.join(HERE, "ruth_short.mp4"))
    args = ap.parse_args()
    if args.voice_files is None and os.path.isdir(os.path.join(HERE, "voicevox")) and any(
            f.lower().endswith((".wav", ".mp3")) for f in os.listdir(os.path.join(HERE, "voicevox"))):
        args.voice_files = os.path.join(HERE, "voicevox")
        if not args.credit:
            args.credit = "VOICEVOX:ずんだもん"  # 規約で必須のクレジット
    if args.credit:
        global SOURCE_NOTE
        SOURCE_NOTE = SOURCE_NOTE + "\n" + args.credit

    tmp = tempfile.mkdtemp()
    gap = 0.22  # 間を詰めてテンポよく
    assert len(VOICE_STYLE) == len(SCENES)
    if args.voice_files:
        print("外部音声を使用:", args.voice_files)
        voices = external_voices(args.voice_files)
    else:
        voices = [tts(narr, os.path.join(tmp, f"v{i}.wav"), args.voice_dir, VOICE_STYLE[i])
                  for i, (narr, *_rest) in enumerate(SCENES)]
    durs = [len(a) / SR + gap for a in voices]
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
    emojis = [stat_img(e[6:]) if e.startswith('@stat:') else vs_img() if e == '@vs'
              else None if e.startswith('@count:') else emoji_img(e, 380)
              for (*_x, e, _c) in SCENES]
    glow = Image.new("RGBA", (W, H))
    ImageDraw.Draw(glow).ellipse((W / 2 - 330, 400, W / 2 + 330, 960), fill=(120, 160, 255, 70))
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
        if em is None:  # 数字カウントアップ（最初の1.2秒で0→目標値、イーズアウト）
            _, target, unit = SCENES[si][3].split(":")
            p = min(1.0, lt / 1.2)
            val = int(round(int(target) * (1 - (1 - p) ** 3)))
            em = count_img(val, unit, SCENES[si][4])
            scale = 1.0 + (0.08 * math.sin(min(1.0, (lt - 1.2) / 0.3) * math.pi) if 1.2 < lt < 1.5 else 0)
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
        d.rectangle((0, H - 18, int(W * t / total), H), fill=(220, 50, 60, 255))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", args.out)


if __name__ == "__main__":
    main()
