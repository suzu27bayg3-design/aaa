#!/usr/bin/env python3
"""毎日の雑学ショート（1080x1920）を、1つの台本ファイルから作る。

使い方:
  bash tools/voicevox_engine.sh
  python3 tools/trivia_short.py trivia_daily/2026-11-05_octopus/topic.py
  → 同じフォルダに short.mp4 / cover.png / metadata.md（タイトル・説明欄・タグ・ハッシュタグ・固定コメント）

台本ファイル（topic.py）に書くもの:
  TITLE   … 画面上の帯に出す短い題（12文字前後）
  SCENES  … [dict(spk="Z"|"M", say="セリフ", read="読み（任意）", ex="表情（任意）",
               head="大見出し（\\n で改行）", sub="小さな補足（任意）", fig="🐙" または関数名), ...]
            最後のセリフが冒頭の問いかけにつながる「ループ構成」にすると、くり返し再生されやすい
  FIGS    … {関数名: draw(t, local_t) -> RGBA画像} 動く図（任意）
  META    … 投稿用メタデータ（title, alt_titles, lead, points, principle, sources, tags, hashtags, pinned）

しくみ:
  1. VOICEVOX でセリフごとに音声を作る（読みは log に出るので、読み間違いを確かめて read で直す）
  2. 音声の長さに合わせて、1秒に FPS 枚のコマを描く。図は経過時間で動き、立ち絵は声の大きさ（RMS）で口が動く
  3. BGM は声が鳴っている間だけ下げ（ダッキング）、-14 LUFS にそろえて ffmpeg で MP4 にする
"""
import argparse
import importlib.util
import math
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import longform as L  # noqa: E402

SW, SH = 1080, 1920
FPS = 15
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
GAP = 0.25
MIRROR = {"Z"}  # 左右反転する話者（ずんだもんは左にいるので、右のめたんの方を向かせる）


def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (200, 200))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((size, int(size * im.height / im.width)), Image.LANCZOS)


def background(c1, c2):
    y = np.linspace(0, 1, SH)[:, None, None]
    g = (np.array(c1) * (1 - y) + np.array(c2) * y).repeat(SW, 1)
    im = Image.fromarray(g.astype(np.uint8)).convert("RGBA")
    dots = Image.new("RGBA", (SW, SH))
    d = ImageDraw.Draw(dots)
    for gy in range(0, SH, 90):
        for gx in range((gy // 90) % 2 * 45, SW, 90):
            d.ellipse((gx - 5, gy - 5, gx + 5, gy + 5), fill=(255, 255, 255, 18))
    im = Image.alpha_composite(im, dots)
    glow = Image.new("RGBA", (SW, SH))
    ImageDraw.Draw(glow).ellipse((SW / 2 - 380, 330, SW / 2 + 380, 1030), fill=(255, 255, 255, 40))
    return Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(70)))


def top_band(title, accent):
    lay = Image.new("RGBA", (SW, SH))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((50, 120, SW - 50, 250), 40, fill=accent + (240,))
    f = L.jp(66) if d.textlength(title, font=L.jp(66)) < SW - 160 else L.jp(54)
    d.text((SW / 2, 185), title, font=f, fill=L.NAVY, anchor="mm")
    return lay


def head_layer(head, sub, color):
    lay = Image.new("RGBA", (SW, SH))
    d = ImageDraw.Draw(lay)
    lines = head.split("\n")
    size = 128
    while size > 70 and max(d.textlength(s, font=L.jp(size)) for s in lines) > SW - 100:
        size -= 6
    f = L.jp(size)
    lh = size * 1.18
    y0 = 1185 - lh * (len(lines) - 1) / 2
    for i, s in enumerate(lines):
        d.text((SW / 2, y0 + i * lh), s, font=f, fill=color, anchor="mm", stroke_width=12, stroke_fill=L.NAVY)
    if sub:
        sf = L.jp(46, True)
        tw = d.textlength(sub, font=sf)
        y = y0 + lh * (len(lines) - 1) + size * 0.6 + 40
        d.rounded_rectangle((SW / 2 - tw / 2 - 36, y, SW / 2 + tw / 2 + 36, y + 84), 28, fill=(0, 0, 0, 150))
        d.text((SW / 2, y + 42), sub, font=sf, fill=L.WHITE, anchor="mm")
    return lay


def speakers(spk, ex, mouth, blink):
    """下に2人の立ち絵。話している人を明るく大きく、もう1人は少し暗く"""
    lay = Image.new("RGBA", (SW, SH))
    for k, x in (("Z", 10), ("M", SW - 330)):
        talking = k == spk
        e = ex if talking else "happy"
        im = L.face(k, e, k in blink, mouth if talking else 0)
        if k in MIRROR:  # 左右反転して、2人が向き合うようにする
            im = ImageOps.mirror(im)
        w = 330 if talking else 290
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        if not talking:
            r, g, b, al = im.split()
            im = Image.merge("RGBA", [c.point(lambda v: int(v * 0.68)) for c in (r, g, b)] + [al])
        im = im.crop((0, 0, w, min(im.height, 380)))
        lay.alpha_composite(im, (-25 if k == "Z" else SW - w - 10, SH - 60 - im.height))  # ずんだもんの切り抜き端は画面の外へ
    return lay


CAP_W = 380


def caption_lines(text):
    return L.wrap(ImageDraw.Draw(Image.new("RGB", (8, 8))), text, L.jp(42, True), CAP_W)


def caption(text, spk, color, page=0):
    """話している言葉を、立ち絵の間の吹き出しに出す（音を消して見る人向け）。長いときは3行ずつページ送り"""
    lay = Image.new("RGBA", (SW, SH))
    d = ImageDraw.Draw(lay)
    f = L.jp(42, True)
    ls = caption_lines(text)[page * 3: page * 3 + 3]
    x0, x1 = 345, SW - 345
    y1 = SH - 120
    y0 = y1 - 40 - 56 * len(ls)
    d.rounded_rectangle((x0, y0, x1, y1), 26, fill=(255, 255, 255, 235), outline=color, width=6)
    tail = [(x0, y1 - 60), (x0 - 30, y1 - 40), (x0, y1 - 30)] if spk == "Z" else \
           [(x1, y1 - 60), (x1 + 30, y1 - 40), (x1, y1 - 30)]
    d.polygon(tail, fill=color)
    for i, s in enumerate(ls):
        d.text((SW / 2, y0 + 20 + 28 + i * 56), s, font=f, fill=L.NAVY, anchor="mm")
    return lay


def write_metadata(cfg, here, total):
    m = cfg.META
    src = "\n".join(f"{lab}\n{url}" for lab, url in m["sources"])
    desc = (m["lead"] + "\n\n" + "\n".join("・" + p for p in m["points"]) + "\n\n"
            + "【しくみ】" + m["principle"] + "\n\n"
            + "📅 毎日1本、雑学ショートを投稿中。フォローで明日の雑学も！\n\n"
            + "出典:\n" + src + "\n\n"
            + "音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん\n立ち絵: 坂本アヒル\n\n"
            + " ".join(m["hashtags"]))
    tags = ", ".join(dict.fromkeys(m["tags"]))
    assert len(tags) <= 500
    code = lambda s: "```\n" + s + "\n```\n"  # noqa: E731
    md = [f"# {m['title'].split(' #')[0]}（{total:.0f}秒）\n",
          f"- 動画: `short.mp4`（1080×1920 縦長 / 約{total:.0f}秒）/ 表紙候補: `cover.png`\n"
          f"- 作り直し: `bash tools/voicevox_engine.sh` → `python3 tools/trivia_short.py {os.path.relpath(here, L.ROOT)}/topic.py`\n",
          "\n**タイトル**\n", code(m["title"])]
    if m.get("alt_titles"):
        md += ["**ほかの候補**\n"] + [code(t) for t in m["alt_titles"]]
    md += ["**説明欄**\n", code(desc), "**タグ**（タグ欄に貼る）\n", code(tags),
           "**固定コメント**\n", code(m["pinned"]),
           "**設定**：カテゴリ「教育」/ 再生リスト「毎日雑学ショート」/ ショートの説明欄のURLは押せないので、"
           "長尺につなぐときは「関連動画」で設定する\n"]
    if m.get("notes"):
        md += ["\n**事実確認のメモ**\n"] + [f"- {n}\n" for n in m["notes"]]
    with open(os.path.join(here, "metadata.md"), "w", encoding="utf-8") as f:
        f.write("".join(md))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--no-tts", action="store_true")
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("topic", a.topic)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    here = os.path.dirname(os.path.abspath(a.topic))
    sc = cfg.SCENES
    vdir = os.path.join(here, "voicevox")
    os.makedirs(vdir, exist_ok=True)
    if not a.no_tts:
        for n, s in enumerate(sc):
            kana = L.tts(s.get("read") or s["say"], s["spk"], os.path.join(vdir, f"{n:02d}_{s['spk']}.wav"))
            print(f"{n:02d} {L.SPK[s['spk']][0]}: {kana}")
    voices = [L.base.load_audio(os.path.join(vdir, f"{n:02d}_{s['spk']}.wav"), L.base.VOICE_FX) for n, s in enumerate(sc)]
    durs = [len(v) / L.SR + GAP for v in voices]
    durs[-1] += 0.6
    starts = np.cumsum([0.2] + durs[:-1])
    total = float(starts[-1] + durs[-1])
    assert total < 60, f"{total:.1f}s: ショートは60秒以内に"

    music = L.base.bgm(total) * 0.9
    vo = np.zeros_like(music)
    for v, st in zip(voices, starts):
        s0 = int(st * L.SR)
        vo[s0:s0 + len(v)] += v[: max(0, len(vo) - s0)]
    env = np.convolve(np.abs(vo), np.ones(int(0.05 * L.SR)) / int(0.05 * L.SR), "same")
    act = np.convolve((env > 0.01).astype(float), np.ones(int(0.25 * L.SR)) / int(0.25 * L.SR), "same")
    music *= 1 - 0.6 * np.clip(act * 1.5, 0, 1)
    mix = vo * 0.9 + music
    mix = np.clip(mix / max(1.0, np.abs(mix).max() / 0.95), -1, 1)
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, "mix.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(L.SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())

    accent = getattr(cfg, "ACCENT", (255, 200, 60))
    bg = Image.alpha_composite(background(*getattr(cfg, "BG", ((20, 40, 90), (8, 14, 40)))), top_band(cfg.TITLE, accent))
    nf = L.jp(26, True)
    ImageDraw.Draw(bg).text((SW / 2, 290), getattr(cfg, "SOURCE_NOTE", ""), font=nf, fill=(255, 255, 255, 170), anchor="mm")
    heads = [head_layer(s["head"], s.get("sub", ""), s.get("color", accent)) for s in sc]
    figs = getattr(cfg, "FIGS", {})
    emo = {s["fig"]: emoji_img(s["fig"], 360) for s in sc if s.get("fig") and s["fig"] not in figs}
    npgs = [max(1, (len(caption_lines(s["say"])) + 2) // 3) for s in sc]

    out = os.path.join(here, "short.mp4")
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{SW}x{SH}", "-r", str(FPS), "-i", "-", "-i", wav,
                             "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                             "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000",
                             "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                            stdin=subprocess.PIPE)
    cache = {}
    cover = None
    for k in range(int(total * FPS)):
        t = k / FPS
        n = max(0, int(np.searchsorted(starts, t, side="right")) - 1)
        s = sc[n]
        lt = t - starts[n]
        v = voices[n]
        seg = v[int(max(0, lt - 0.1) * L.SR): int(max(0, lt - 0.1 + 1 / FPS) * L.SR)]
        rms = float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0
        mouth = 0 if rms < 0.025 else (1 if rms < 0.07 else 2)
        blink = tuple(c for c in L.SPK if L.blinking(c, t))
        ex = s.get("ex") or L.expression(s["spk"], s["say"])
        page = min(npgs[n] - 1, int(lt / max(0.1, durs[n] - GAP) * npgs[n]))
        key = (n, mouth, blink, page)
        if key not in cache:
            cache.clear()
            cache[key] = Image.alpha_composite(speakers(s["spk"], ex, mouth, blink),
                                               caption(s["say"], s["spk"], L.SPK[s["spk"]][1], page))
        frame = bg.copy()
        # 図: 関数なら経過時間で描き直す。絵文字ならポップイン＋ふわふわ
        f = s.get("fig")
        if f in figs:
            im = figs[f](t, lt)
        elif f:
            im = emo[f]
        else:
            im = None
        if im is not None:
            kk = min(1, lt / 0.3)
            scl = 0.6 + 0.4 * kk + 0.12 * math.sin(kk * math.pi) if f not in figs or n == 0 or sc[n - 1].get("fig") != f else 1
            if scl != 1:
                im = im.resize((max(1, int(im.width * scl)), max(1, int(im.height * scl))))
            bob = 0 if f in figs else 12 * math.sin(t * 2.4)
            frame.alpha_composite(im, (int(SW / 2 - im.width / 2), int(690 - im.height / 2 + bob)))
        # 見出し: 下から少しスライドして出る
        dy = int(50 * (1 - min(1, lt / 0.25)) ** 2)
        frame.alpha_composite(heads[n].crop((0, 0, SW, SH - dy)), (0, dy))
        frame.alpha_composite(cache[key])
        ImageDraw.Draw(frame).rectangle((0, SH - 16, SW * t / total, SH), fill=accent)
        if n == 0 and cover is None and lt > 0.6:
            cover = frame.copy()
        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg failed")
    cover.convert("RGB").save(os.path.join(here, "cover.png"))
    write_metadata(cfg, here, total)
    print("wrote", out, f"{total:.1f}s")


if __name__ == "__main__":
    main()
