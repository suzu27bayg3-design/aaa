#!/usr/bin/env python3
"""ショート動画の最後に「サムネイル専用のコマ」を追加する。

YouTubeアプリでは、ショートのサムネイルを動画内のコマから選ぶ。
一覧で縮小されても読めるよう、特大の文字＋大きな絵文字のコマを作り、動画の最後に数フレーム足す。
投稿時にサムネイル選択バーを右端まで動かすと、このコマを選べる。

使い方:
  python3 tools/add_thumb_frame.py VIDEO.mp4 --text "うんちが\\n四角い\\n動物！？" --emoji 💩 \\
      --color "#ffd23c" --bg "#1a3a12" [--sec 0.4] [--png thumb.png]
  元の動画は VIDEO.mp4 のまま上書き（元ファイルは make_short.py で再生成できる）。
"""
import argparse
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((size, int(size * im.height / im.width)), Image.LANCZOS)


def make_thumb(text, emoji, color, bg, tag):
    c, b = hex2rgb(color), hex2rgb(bg)
    # 背景: 中央が明るい放射状グラデーション（主役を目立たせる）
    img = Image.new("RGB", (W, H), b)
    glow = Image.new("RGBA", (W, H))
    gd = ImageDraw.Draw(glow)
    for i in range(12):
        r = 900 - i * 60
        a = 10 + i * 6
        gd.ellipse((W / 2 - r, 900 - r, W / 2 + r, 900 + r), fill=c + (a,))
    img = Image.alpha_composite(img.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(40)))
    # 集中線（半透明で重ねる）
    import math
    lines_layer = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(lines_layer)
    for k in range(48):
        th = 2 * math.pi * k / 48
        d.polygon([(W / 2, 900), (W / 2 + 1800 * math.cos(th), 900 + 1800 * math.sin(th)),
                   (W / 2 + 1800 * math.cos(th + 0.035), 900 + 1800 * math.sin(th + 0.035))],
                  fill=(255, 255, 255, 22))
    img.alpha_composite(lines_layer)
    # 文字の背後を少し暗くして読みやすく
    shade = Image.new("RGBA", (W, H))
    ImageDraw.Draw(shade).rounded_rectangle((20, 640, W - 20, 1480), 60, fill=(0, 0, 0, 90))
    img.alpha_composite(shade.filter(ImageFilter.GaussianBlur(30)))
    # 絵文字（上部・高さ380px以内に収める）
    em = emoji_img(emoji, 420)
    if em.height > 380:
        em = em.resize((int(em.width * 380 / em.height), 380), Image.LANCZOS)
    sh = Image.new("RGBA", em.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 120), mask=em.split()[3])
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (W // 2 - em.width // 2 + 10, 230 + 14))
    img.alpha_composite(em, (W // 2 - em.width // 2, 230))
    # 特大テキスト（画面中央より上〜中央に配置。下端・右端はUIと重なるので避ける）
    d = ImageDraw.Draw(img)
    lines = text.split("\n")
    size = 210
    while True:
        f = ImageFont.truetype(FONT, size)
        bb = d.multiline_textbbox((0, 0), text, font=f, spacing=10, align="center", stroke_width=18)
        if bb[2] - bb[0] <= W - 80 or size <= 90:
            break
        size -= 8
    tw, th_ = bb[2] - bb[0], bb[3] - bb[1]
    y = max(700, 230 + em.height + 60)
    # 行ごとに色を変える（最終行を強調色に）
    yy = y
    for i, ln in enumerate(lines):
        lb = d.textbbox((0, 0), ln, font=f, stroke_width=18)
        fill = c if i == len(lines) - 1 else (255, 255, 255)
        d.text(((W - (lb[2] - lb[0])) / 2, yy), ln, font=f, fill=fill,
               stroke_width=18, stroke_fill=(0, 0, 0))
        yy += (lb[3] - lb[1]) + 18
    # 左上のタグ
    tf = ImageFont.truetype(FONT, 64)
    tb = d.textbbox((0, 0), tag, font=tf)
    d.rounded_rectangle((50, 80, 50 + tb[2] - tb[0] + 60, 80 + 110), 28, fill=c)
    d.text((80, 100), tag, font=tf, fill=(0, 0, 0))
    return img.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--text", required=True, help='改行は "\\n"')
    ap.add_argument("--emoji", required=True)
    ap.add_argument("--color", default="#ffd23c", help="強調色")
    ap.add_argument("--bg", default="#101820", help="背景色")
    ap.add_argument("--tag", default="1分雑学")
    ap.add_argument("--sec", type=float, default=0.4)
    ap.add_argument("--png", default=None, help="サムネイル画像も保存する場合のパス")
    a = ap.parse_args()

    thumb = make_thumb(a.text.replace("\\n", "\n"), a.emoji, a.color, a.bg, a.tag)
    tmp = tempfile.mkdtemp()
    png = a.png or os.path.join(tmp, "thumb.png")
    thumb.save(png)
    # サムネイルのコマを無音で a.sec 秒の動画にし、元動画の後ろに連結（同じ規格で再エンコード）
    out = os.path.join(tmp, "out.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", a.video,
        "-loop", "1", "-framerate", "30", "-t", str(a.sec), "-i", png,
        "-f", "lavfi", "-t", str(a.sec), "-i", "anullsrc=r=48000:cl=mono",
        "-filter_complex",
        "[1:v]scale=1080:1920,format=yuv420p,setsar=1[t];[0:v]setsar=1[v0];"
        "[v0][0:a][t][2:a]concat=n=2:v=1:a=1[v][a]",
        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out],
        check=True)
    os.replace(out, a.video)
    print("added thumbnail frame:", a.video, "(png:", png, ")")


if __name__ == "__main__":
    main()
