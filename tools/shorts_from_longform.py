#!/usr/bin/env python3
"""長尺解説動画の台本から、縦長ショート（1080x1920）を作る。

使い方:
  bash tools/voicevox_engine.sh
  python3 tools/shorts_from_longform.py longform_quantum5/script.py   # → longform_quantum5/short.mp4

台本に SHORT = dict(fig_from=章番号, hook=("1行目", "2行目"), lines=[(話者, 表示, 読み or None, 表情), ...])
を書いておくと、その章の動く図を真ん中に置き、上に大きな問いかけ、下に立ち絵と字幕を出す。
最後に「▶ 続きは本編」の帯を出す（投稿時に、関連動画のリンクを本編に設定する）。

しくみは横長の解説動画と同じ: 1秒に FPS 枚のコマを描いて ffmpeg に流し込む。図は経過時間で動き、
立ち絵は声の大きさ（RMS）で口が動く。
"""
import argparse
import importlib.util
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import longform as L  # noqa: E402

SW, SH = 1080, 1920
FIG_SIZE = {"tower": (900, 620), "dial": (900, 560), "platform": (900, 520), "bars": (900, 600),
            "period": (900, 520), "bb84": (900, 600), "pair": (900, 560), "landscape": (900, 560),
            "repeater": (900, 560), "pipeline": (900, 560), "tiles": (900, 640)}


def vbg():
    im = Image.new("RGBA", (SW, SH))
    d = ImageDraw.Draw(im)
    for y in range(SH):
        k = y / SH
        d.line((0, y, SW, y), fill=(int(20 * (1 - k) + 6 * k), int(30 * (1 - k) + 10 * k), int(72 * (1 - k) + 28 * k), 255))
    return im


def outlined(d, xy, text, font, fill, sw=8):
    d.text(xy, text, font=font, fill=fill, anchor="mm", stroke_width=sw, stroke_fill=L.NAVY)


def portrait(spk, ex, size, mouth=0, blink=False):
    im = L.face(spk, ex, blink, mouth)
    return im.resize((size, int(im.height * size / im.width)), Image.LANCZOS)


def base_frame(hook, tag, cta):
    im = vbg()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 60, 420, 120), 30, fill=(66, 133, 244))
    d.text((230, 90), tag, font=L.jp(34, True), fill=L.WHITE, anchor="mm")
    f1 = L.jp(84) if d.textlength(hook[0], font=L.jp(84)) < SW - 80 else L.jp(70)
    f2 = L.jp(96) if d.textlength(hook[1], font=L.jp(96)) < SW - 80 else L.jp(78)
    outlined(d, (SW / 2, 250), hook[0], f1, L.WHITE, 7)
    outlined(d, (SW / 2, 370), hook[1], f2, L.GOLD, 8)
    pan = Image.new("RGBA", (SW, SH))
    ImageDraw.Draw(pan).rounded_rectangle((30, 470, SW - 30, 1250), 36, fill=(255, 255, 255, 18),
                                          outline=(110, 150, 255, 120), width=3)
    im = Image.alpha_composite(im, pan)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((SW / 2 - 330, 1270, SW / 2 + 330, 1340), 35, fill=(230, 60, 80))
    d.text((SW / 2, 1305), cta, font=L.jp(34, True), fill=L.WHITE, anchor="mm")
    return im


def fig_layer(fig, cfg, t, scale=1.12):
    bw, bh = FIG_SIZE.get(fig["kind"], (900, 580))
    lay = Image.new("RGBA", (bw + 40, bh + 40))
    L.ANIM_T = t if fig["kind"] in L.LIVE_KINDS else None
    L.fig_area(lay, (20, 20, bw + 20, bh + 20), fig, cfg)
    L.ANIM_T = None
    lay = lay.resize((int(lay.width * scale), int(lay.height * scale)), Image.LANCZOS)
    out = Image.new("RGBA", (SW, SH))
    out.alpha_composite(lay, (int((SW - lay.width) / 2), int(860 - lay.height / 2)))
    return out


def speaker_layer(spk, ex, text, mouth, blink, page):
    lay = Image.new("RGBA", (SW, SH))
    other = "M" if spk == "Z" else "Z"
    p1 = portrait(spk, ex, 360, mouth, spk in blink)
    p2 = portrait(other, "happy", 280, 0, other in blink)
    p2 = Image.alpha_composite(p2, Image.new("RGBA", p2.size, (0, 0, 0, 90)))
    xs = (20, SW - 300) if spk == "Z" else (SW - 380, 20)
    lay.alpha_composite(p2.crop((0, 0, p2.width, 300)), (xs[1], 1360))
    lay.alpha_composite(p1.crop((0, 0, p1.width, 300)), (xs[0], 1355))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((40, 1640, SW - 40, 1860), 30, fill=(255, 255, 255, 240), outline=L.SPK[spk][1], width=8)
    f = L.jp(50, True)
    ls = L.wrap(d, text, f, SW - 140)[page * 3: page * 3 + 3]
    for i, ln in enumerate(ls):
        d.text((70, 1752 - len(ls) * 32 + i * 64), ln, font=f, fill=L.NAVY)
    return lay


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--no-tts", action="store_true")
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("cfg", a.script)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    here = os.path.dirname(os.path.abspath(a.script))
    sh = cfg.SHORT
    fig = cfg.CHAPTERS[sh["fig_from"]]["fig"]
    vdir = os.path.join(here, "voicevox_short")
    os.makedirs(vdir, exist_ok=True)
    lines = sh["lines"]
    if not a.no_tts:
        for n, row in enumerate(lines):
            kana = L.tts(row[2] or row[1], row[0], os.path.join(vdir, f"{n:02d}_{row[0]}.wav"))
            print(f"{n:02d} {L.SPK[row[0]][0]}: {kana}")
    voices = [L.base.load_audio(os.path.join(vdir, f"{n:02d}_{r[0]}.wav"), L.base.VOICE_FX) for n, r in enumerate(lines)]
    durs = [len(v) / L.SR + 0.3 for v in voices]
    durs[-1] += 1.5  # 最後に「続きは本編」を見せる時間
    total = sum(durs) + 0.3
    starts = np.cumsum([0.3] + durs[:-1])

    # 音声: セリフ + 小さめのBGM（声の間は下げる）
    music = L.base.bgm(total) * 0.5
    vo = np.zeros_like(music)
    for v, st in zip(voices, starts):
        s0 = int(st * L.SR)
        vo[s0:s0 + len(v)] += v[: max(0, len(vo) - s0)]
    env = np.convolve(np.abs(vo), np.ones(int(0.05 * L.SR)) / int(0.05 * L.SR), "same")
    act = np.convolve((env > 0.01).astype(float), np.ones(int(0.25 * L.SR)) / int(0.25 * L.SR), "same")
    music *= 1 - 0.6 * np.clip(act * 1.5, 0, 1)
    mix = np.clip((vo * 0.9 + music) / max(1.0, np.abs(vo * 0.9 + music).max() / 0.95), -1, 1)
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "mix.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(L.SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

    tag = getattr(cfg, "THUMB_TAG", "量子解説")
    cta = "▶ 続きは本編（" + cfg.TITLE[:14] + "）"
    base = base_frame(sh["hook"], tag, cta)
    out = os.path.join(here, "short.mp4")
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{SW}x{SH}", "-r", str(L.FPS), "-i", "-", "-i", wav,
                             "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                             "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000",
                             "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                            stdin=subprocess.PIPE)
    live = fig["kind"] in L.LIVE_KINDS
    static_fig = None if live else fig_layer(fig, cfg, 0)
    nfr = int(total * L.FPS)
    cache = {}
    for k in range(nfr):
        t = k / L.FPS
        n = max(0, int(np.searchsorted(starts, t, side="right")) - 1)
        spk, disp = lines[n][0], lines[n][1]
        ex = lines[n][3] if len(lines[n]) > 3 else L.expression(spk, disp)
        tt = t - starts[n]
        v = voices[n]
        seg = v[int(max(0, tt - 0.1) * L.SR): int(max(0, tt - 0.1 + 1 / L.FPS) * L.SR)]
        rms = float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0
        mouth = 0 if rms < 0.025 else (1 if rms < 0.07 else 2)
        blink = tuple(c for c in L.SPK if L.blinking(c, t))
        npg = max(1, (len(L.wrap(ImageDraw.Draw(base), disp, L.jp(50, True), SW - 140)) + 2) // 3)
        page = min(npg - 1, int(tt / max(0.1, durs[n] - 0.3) * npg))
        key = (n, mouth, blink, page)
        if key not in cache:
            cache.clear()
            cache[key] = speaker_layer(spk, ex, disp, mouth, blink, page)
        fl = fig_layer(fig, cfg, t + 1.0) if live else static_fig
        img = Image.alpha_composite(Image.alpha_composite(base, fl), cache[key])
        d = ImageDraw.Draw(img)
        d.rectangle((0, SH - 20, SW * (t / total), SH), fill=L.GOLD)
        proc.stdin.write(img.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg failed")
    print("wrote", out, f"{total:.1f}s")


if __name__ == "__main__":
    main()
