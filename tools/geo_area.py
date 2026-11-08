#!/usr/bin/env python3
"""絶景ショート用の地図素材をまとめて作る（国土地理院の航空写真＋産総研の地質図）。

使い方:
  python3 tools/geo_area.py travel_shorts/akiyoshido 34.236 131.302 0,100,233
      → maps/zoom_z{5,8,11,14}.jpg（日本全体からのズーム用）
         maps/aerial.jpg（航空写真×陰影起伏）, maps/mask.png（地質図で指定した色の範囲）, maps/aerial.json

しくみ:
  ・ズーム用には、ズーム段階ごとに中心のまわりの航空写真をつないでおき、動画ではその間を拡大しながらつなぐ
  ・地質図はズーム13までなので、ズーム15の航空写真の位置に合わせて4倍に引きのばし、指定した色の所だけ取り出す
  ・地質図の文字で抜けた穴は、ふくらませて縮める処理（クロージング）で埋める
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageChops, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsi_tiles as G  # noqa: E402

ZOOMS = (5, 8, 11, 14)


def main(spot, lat, lon, rgb):
    out = os.path.join(spot, "maps")
    os.makedirs(out, exist_ok=True)
    for z in ZOOMS:
        im, org = G.mosaic("photo", lat, lon, z, 2)
        x, y = G.to_px(lat, lon, z, org)
        im.crop((int(x) - 512, int(y) - 512, int(x) + 512, int(y) + 512)).convert("RGB").save(
            os.path.join(out, f"zoom_z{z}.jpg"), quality=90)
    ph, o15 = G.mosaic("photo", lat, lon, 15, 3)
    hs, _ = G.mosaic("hillshade", lat, lon, 15, 3)
    aer = ImageChops.multiply(ph.convert("RGB"), Image.blend(hs.convert("RGB"), Image.new("RGB", hs.size, "white"), 0.45))
    aer.save(os.path.join(out, "aerial.jpg"), quality=92)
    geo, o13 = G.mosaic("geology", lat, lon, 13, 2)
    g = np.array(geo.convert("RGB")).astype(int)
    m13 = ((abs(g[:, :, 0] - rgb[0]) < 12) & (abs(g[:, :, 1] - rgb[1]) < 12) & (abs(g[:, :, 2] - rgb[2]) < 12)).astype(np.uint8) * 255
    N = aer.size[0]
    ys, xs = np.mgrid[0:N, 0:N]
    sx = ((o15[0] * 256 + xs) / 4 - o13[0] * 256).astype(int)
    sy = ((o15[1] * 256 + ys) / 4 - o13[1] * 256).astype(int)
    ok = (sx >= 0) & (sx < m13.shape[1]) & (sy >= 0) & (sy < m13.shape[0])
    m = np.zeros((N, N), np.uint8)
    m[ok] = m13[sy[ok], sx[ok]]
    mi = Image.fromarray(m).filter(ImageFilter.GaussianBlur(6)).point(lambda v: 255 if v > 128 else 0)
    for f in (ImageFilter.MaxFilter(41), ImageFilter.MaxFilter(41), ImageFilter.MinFilter(41), ImageFilter.MinFilter(41)):
        mi = mi.filter(f)
    mi.filter(ImageFilter.GaussianBlur(3)).save(os.path.join(out, "mask.png"))
    json.dump(dict(z=15, origin=o15, size=N, center=[lat, lon]), open(os.path.join(out, "aerial.json"), "w"))
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), [int(v) for v in sys.argv[4].split(",")])
