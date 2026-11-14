#!/usr/bin/env python3
"""全画面（1080x1920）の航空写真の場面を作る部品。spot.py から使う。

  A = Aerial(path_to_photo_jpg)                        # 国土地理院の航空写真（つないだもの）
  A.view(lt, center=(x, y), s0=1.0, s1=0.8, dur=5)    # ゆっくりズーム
  A.ring(lt, t, center, at=(x, y))                     # 指定した場所に、広がる光の輪
  A.flow(lt, t, center, path=[(x,y),...])              # 道すじにそって光る粒が流れる
座標はすべて航空写真の画像の上のピクセル。
"""
import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

SW, SH = 1080, 1920
GOLD = (255, 214, 120)


class Aerial:
    def __init__(self, path, base_w=560):
        self.im = Image.open(path).convert("RGB")
        self.bw = base_w  # scale=1 のときに切り出す幅（px）
        r = random.Random(3)
        self.pts = [(r.random(), r.gauss(0, 1), r.uniform(0.7, 1.3)) for _ in range(140)]

    def box(self, center, scale):
        w, h = self.bw * scale, self.bw * scale * SH / SW
        return (center[0] - w / 2, center[1] - h / 2, center[0] + w / 2, center[1] + h / 2)

    def scr(self, box, x, y):
        return (x - box[0]) * SW / (box[2] - box[0]), (y - box[1]) * SH / (box[3] - box[1])

    def frame(self, center, scale, dark=1.0):
        b = self.box(center, scale)
        im = self.im.crop(tuple(int(v) for v in b)).resize((SW, SH), Image.BILINEAR)
        if dark != 1.0:
            im = ImageEnhance.Brightness(im).enhance(dark)
        return b, im

    def view(self, lt, center, s0=1.0, s1=0.85, dur=5.0):
        k = min(1.0, lt / dur)
        k = 0.5 - 0.5 * math.cos(math.pi * k)
        return self.frame(center, s0 + (s1 - s0) * k)[1]

    @staticmethod
    def glow(base, lay, blur=10):
        return ImageChops.add(ImageChops.add(base, lay.filter(ImageFilter.GaussianBlur(blur))), lay)

    def ring(self, lt, t, center, at, scale=0.8, color=GOLD, size=150):
        b, im = self.frame(center, scale)
        lay = Image.new("RGB", (SW, SH))
        d = ImageDraw.Draw(lay)
        x, y = self.scr(b, *at)
        for i in range(3):
            ph = (t * 0.7 + i / 3) % 1
            r = 25 + size * ph
            d.ellipse((x - r, y - r, x + r, y + r), outline=tuple(int(v * (1 - ph)) for v in color), width=7)
        return self.glow(im, lay)

    def flow(self, lt, t, center, path, scale=0.8, color=GOLD, speed=90, spread=8, dark=0.7, size=6):
        b, im = self.frame(center, scale, dark)
        seg = [math.dist(path[i], path[i + 1]) for i in range(len(path) - 1)]
        tot = sum(seg)

        def at(s):
            s = max(0.0, min(tot - 0.01, s))
            for i, l in enumerate(seg):
                if s <= l:
                    f = s / l
                    return path[i][0] + (path[i + 1][0] - path[i][0]) * f, path[i][1] + (path[i + 1][1] - path[i][1]) * f, i
                s -= l
            return path[-1][0], path[-1][1], len(seg) - 1

        lay = Image.new("RGB", (SW, SH))
        d = ImageDraw.Draw(lay)
        for u, off, sp in self.pts:
            s0 = (u * tot + t * speed * sp) % tot
            for j in range(7):
                x, y, i = at(s0 - j * 5)
                nx, ny = -(path[i + 1][1] - path[i][1]), path[i + 1][0] - path[i][0]
                nl = math.hypot(nx, ny) or 1
                X, Y = self.scr(b, x + off * spread * nx / nl, y + off * spread * ny / nl)
                r = size - j * 0.7
                c = 1 - j / 7
                d.ellipse((X - r, Y - r, X + r, Y + r), fill=tuple(int(v * c) for v in color))
        return self.glow(im, lay)
