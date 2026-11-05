#!/usr/bin/env python3
"""チャンネルのアイコン（800x800）とバナー（2560x1440）を作る。

使い方: python3 tools/channel_art.py "ずんだもんの" "なるほど研究所"   → channel_art/icon.png, banner.png

YouTube の推奨サイズ:
  アイコン 800x800（表示は円形・小さいと98x98）→ 大事なものは中央の円の中に、文字は入れすぎない
  バナー 2560x1440 → テレビでは全体、PCは横長の帯、スマホは中央 1546x423 だけが見える。名前と顔はこの中に入れる
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import longform as L  # noqa: E402
import trivia_short as T  # noqa: E402

CH = os.path.join(L.ROOT, "assets", "characters")
OUT = os.path.join(L.ROOT, "channel_art")
GREEN, PINK = (110, 200, 90), (235, 95, 160)


def char(name, ex="happy", mirror=False):
    im = Image.open(os.path.join(CH, name, f"{ex}__o1.png")).convert("RGBA")
    im = im.crop(im.getbbox())
    return ImageOps.mirror(im) if mirror else im


def grad(w, h, c1, c2):
    y = np.linspace(0, 1, h)[:, None, None]
    return Image.fromarray((np.array(c1) * (1 - y) + np.array(c2) * y).repeat(w, 1).astype(np.uint8)).convert("RGBA")


def sparkles(im, n, seed=1, box=None):
    """きらきら。半透明は別の層に描いてから重ねる（直接描くと透明度が無視される）"""
    rng = np.random.default_rng(seed)
    lay = Image.new("RGBA", im.size)
    d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = box or (0, 0, im.width, im.height)
    for _ in range(n):
        x, y, r = rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(4, 12)
        d.polygon([(x, y - r * 2), (x + r * 0.5, y - r * 0.5), (x + r * 2, y), (x + r * 0.5, y + r * 0.5),
                   (x, y + r * 2), (x - r * 0.5, y + r * 0.5), (x - r * 2, y), (x - r * 0.5, y - r * 0.5)],
                  fill=(255, 255, 255, 110))
    im.alpha_composite(lay)


def icon(path):
    S = 800
    im = grad(S, S, (40, 70, 160), (12, 20, 60))
    sparkles(im, 30, 3)
    glow = Image.new("RGBA", (S, S))
    ImageDraw.Draw(glow).ellipse((120, 140, 680, 700), fill=(255, 230, 120, 90))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(60)))
    bulb = T.emoji_img("💡", 190)
    im.alpha_composite(bulb, (S // 2 - bulb.width // 2, 70))
    z = char("zundamon", "happy", mirror=True)
    m = char("metan", "happy")
    for c, x, w in ((m, 380, 430), (z, -20, 450)):
        c = c.resize((w, int(c.height * w / c.width)), Image.LANCZOS)
        im.alpha_composite(c.crop((0, 0, w, min(c.height, S - 230))), (x, 230))
    # 円形に切り抜いたときの見え方も保存（確認用）
    mask = Image.new("L", (S, S))
    ImageDraw.Draw(mask).ellipse((0, 0, S, S), fill=255)
    im.convert("RGB").save(path)
    prev = Image.new("RGBA", (S, S), (255, 255, 255, 255))
    prev.paste(im, (0, 0), mask)
    prev.convert("RGB").resize((200, 200), Image.LANCZOS).save(path.replace(".png", "_preview_circle.png"))


def banner(path, l1, l2, tagline):
    BW, BH = 2560, 1440
    im = grad(BW, BH, (34, 60, 150), (10, 16, 52))
    grid = Image.new("RGBA", (BW, BH))
    d = ImageDraw.Draw(grid)
    for gx in range(0, BW, 120):  # うすい方眼（研究所らしさ）
        d.line((gx, 0, gx, BH), fill=(255, 255, 255, 16), width=2)
    for gy in range(0, BH, 120):
        d.line((0, gy, BW, gy), fill=(255, 255, 255, 16), width=2)
    im.alpha_composite(grid)
    sparkles(im, 90, 7)
    sx0, sy0 = (BW - 1546) // 2, (BH - 423) // 2  # スマホでも見える範囲
    glow = Image.new("RGBA", (BW, BH))
    ImageDraw.Draw(glow).rounded_rectangle((sx0 + 230, sy0 + 10, sx0 + 1316, sy0 + 413), 80, fill=(255, 255, 255, 40))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(im)
    cx = BW / 2
    d.text((cx, sy0 + 90), l1, font=L.jp(72), fill=GREEN, anchor="mm", stroke_width=8, stroke_fill=L.NAVY)
    d.text((cx, sy0 + 200), l2, font=L.jp(118), fill=L.WHITE, anchor="mm", stroke_width=12, stroke_fill=L.NAVY)
    f = L.jp(36, True)
    tw = d.textlength(tagline, font=f)
    d.rounded_rectangle((cx - tw / 2 - 40, sy0 + 300, cx + tw / 2 + 40, sy0 + 370), 40, fill=L.GOLD)
    d.text((cx, sy0 + 335), tagline, font=f, fill=L.NAVY, anchor="mm")
    z = char("zundamon", "happy", mirror=True)
    m = char("metan", "explain")
    for c, x in ((z, sx0 - 60), (m, sx0 + 1546 - 230)):
        c = c.resize((290, int(c.height * 290 / c.width)), Image.LANCZOS)
        c = c.crop((0, 0, c.width, min(c.height, 423 + 40)))
        im.alpha_composite(c, (int(x), sy0 - 20))
    im.convert("RGB").save(path)
    # スマホで見える範囲に枠を描いた確認用
    chk = im.copy()
    ImageDraw.Draw(chk).rectangle((sx0, sy0, sx0 + 1546, sy0 + 423), outline=(255, 60, 60), width=6)
    chk.convert("RGB").resize((1280, 720), Image.LANCZOS).save(path.replace(".png", "_safe_area.png"))


def main():
    l1, l2 = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("ずんだもんの", "なるほど研究所")
    tag = sys.argv[3] if len(sys.argv) > 3 else "毎日21時 雑学ショート ／ 量子技術をやさしく解説"
    os.makedirs(OUT, exist_ok=True)
    icon(os.path.join(OUT, "icon.png"))
    banner(os.path.join(OUT, "banner.png"), l1, l2, tag)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
