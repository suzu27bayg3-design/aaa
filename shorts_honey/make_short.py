#!/usr/bin/env python3
"""YouTube Shorts 雑学動画ジェネレーター「はちみつはなぜ腐らない？」（ずんだもん版）

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
TITLE = "はちみつは なぜ腐らない？"
SCENES = [
    ("3000年前のはちみつ、まだ食べられるって、知ってた？",
     "3000年前の\nはちみつ\n食べられる！？", "", "🍯", (255, 200, 40)),
    ("古代エジプトのお墓から、食べられる状態で見つかったと言われています。",
     "古代エジプトの\n墓から発見", "数千年たっても保存状態良好", "🏺", (255, 170, 60)),
    ("理由その1。水分が20%以下で、糖がとても濃いからです。",
     "理由①\n水分が少ない", "水分20%以下（国際規格）", "💧", (90, 200, 255)),
    ("濃い糖が、浸透圧で菌の水分をうばうので、菌は増えられません。",
     "浸透圧で\n菌がカラカラに", "水は糖の濃い側へ移動する", "@osmosis", (140, 230, 120)),
    ("理由その2と3。酸性で、しかもミツバチの酵素が、殺菌作用のある過酸化水素を作ります。",
     "理由②③\n酸性＋過酸化水素", "pH約3〜4.5 / ハチの酵素", "🐝", (255, 220, 60)),
    ("ただし、1歳未満の赤ちゃんには、絶対に与えないでください。",
     "注意！\n1歳未満には\n与えない", "乳児ボツリヌス症の予防", "👶", (255, 100, 100)),
    ("だから、数千年前のはちみつでも、腐っていないんです。",
     "だから\n数千年でも\n腐らない", "フォローで毎日雑学！", "🍯", (255, 200, 40)),
]
SOURCE_NOTE = "出典: Smithsonian Magazine / Codex Alimentarius / 厚生労働省"


# ショート向けの声の設計:
#   hook  = 明るい声(mei_happy)・やや高め … 冒頭/驚き/オチで感情を乗せる
#   talk  = 通常の声(mei_normal)・抑揚強め … 説明は聞き取りやすく
#   -r: 話速, -fm: ピッチ(半音), -jf: 抑揚(F0変動)の強さ, -a: 声質(大きいほど明るく若い)
VOICE_PRESETS = {
    "hook": ("mei_happy.htsvoice", ["-r", "1.20", "-fm", "0.5", "-jf", "1.25", "-a", "0.56"]),
    "talk": ("mei_normal.htsvoice", ["-r", "1.22", "-fm", "2.0", "-jf", "1.35", "-a", "0.56"]),
}
# 各シーンの声（SCENES と同じ順番）
VOICE_STYLE = ["hook", "talk", "talk", "talk", "talk", "hook", "hook"]


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
    """はちみつ色グラデーション + ハニカム模様"""
    y = np.linspace(0, 1, H)[:, None]
    top, bot = np.array([60, 30, 5]), np.array([25, 10, 2])
    grad = (top * (1 - y) + bot * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    img = Image.fromarray(grad.astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(lay)
    r = 70
    for row in range(-1, int(H / (r * 1.5)) + 2):
        for col in range(-1, int(W / (r * math.sqrt(3))) + 2):
            cx = col * r * math.sqrt(3) + (row % 2) * r * math.sqrt(3) / 2
            cy = row * r * 1.5
            pts = [(cx + r * math.cos(math.radians(60 * k + 30)),
                    cy + r * math.sin(math.radians(60 * k + 30))) for k in range(6)]
            d.polygon(pts, outline=(255, 180, 40, 38), width=4)
    return Image.alpha_composite(img, lay)


def osmosis_img(size):
    """浸透圧の図: 左=菌(細胞)、右=濃いはちみつ。水(青い粒)が膜を通って右へ出ていく"""
    w, h = int(size * 1.6), size
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, int(size * 0.09))
    # はちみつ側
    d.rounded_rectangle((w * 0.52, h * 0.08, w * 0.98, h * 0.82), 30, fill=(230, 150, 20, 235))
    for i in range(14):  # 糖(白い四角)
        x, y = w * (0.58 + 0.09 * (i % 5)), h * (0.18 + 0.15 * (i // 5))
        d.rounded_rectangle((x, y, x + 34, y + 34), 6, fill=(255, 245, 220))
    # 菌(細胞)と膜
    d.ellipse((w * 0.03, h * 0.14, w * 0.43, h * 0.76), fill=(120, 200, 110), outline=(30, 80, 30), width=8)
    d.line((w * 0.475, h * 0.08, w * 0.475, h * 0.82), fill=(255, 255, 255), width=6)
    # 水の粒と矢印(菌→はちみつ)
    for j, yy in enumerate((0.3, 0.45, 0.6)):
        y = h * yy
        d.ellipse((w * 0.2 - 18, y - 18, w * 0.2 + 18, y + 18), fill=(80, 170, 255))
        d.line((w * 0.27, y, w * 0.55, y), fill=(80, 170, 255), width=10)
        d.polygon([(w * 0.55, y - 20), (w * 0.55, y + 20), (w * 0.6, y)], fill=(80, 170, 255))
    for x, label in ((0.23, "菌"), (0.75, "はちみつ")):
        bb = d.textbbox((0, 0), label, font=f)
        d.text((w * x - (bb[2] - bb[0]) / 2, h * 0.85), label, font=f, fill=(255, 255, 255),
               stroke_width=5, stroke_fill=(0, 0, 0))
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
                     stroke_width=stroke, stroke_fill=(20, 8, 0))
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
    d.rounded_rectangle((60, 150, W - 60, 290), 40, fill=(255, 190, 0, 235))
    title = TITLE
    bb = d.textbbox((0, 0), title, font=tf)
    d.text(((W - (bb[2] - bb[0])) / 2, 185), title, font=tf, fill=(40, 15, 0, 255))
    # 出典
    nf = ImageFont.truetype(FONT, 30)
    bb = d.multiline_textbbox((0, 0), SOURCE_NOTE, font=nf, align="center")
    d.multiline_text(((W - (bb[2] - bb[0])) / 2, H - 260), SOURCE_NOTE, font=nf, align="center",
                     fill=(255, 230, 180, 170))
    return layer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice-dir", default=HERE,
                    help="mei_normal.htsvoice と mei_happy.htsvoice があるフォルダ")
    ap.add_argument("--voice-files", default=None,
                    help="VOICEVOX等で書き出したシーン別音声のフォルダ（指定するとOpen JTalkの代わりに使う）")
    ap.add_argument("--credit", default="",
                    help="画面下に出すクレジット 例: 'VOICEVOX:ずんだもん'")
    ap.add_argument("--out", default=os.path.join(HERE, "honey_short.mp4"))
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
    emojis = [osmosis_img(560) if e == '@osmosis' else emoji_img(e, 380)
              for (*_x, e, _c) in SCENES]
    glow = Image.new("RGBA", (W, H))
    ImageDraw.Draw(glow).ellipse((W / 2 - 330, 400, W / 2 + 330, 960), fill=(255, 200, 60, 90))
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
        d.rectangle((0, H - 18, int(W * t / total), H), fill=(255, 200, 0, 255))
        ff.stdin.write(frame.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", args.out)


if __name__ == "__main__":
    main()
