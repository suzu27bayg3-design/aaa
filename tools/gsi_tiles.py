#!/usr/bin/env python3
"""国土地理院（地理院タイル）と産総研（シームレス地質図）のタイルをつなげて、指定範囲の地図画像を作る。

使い方: python3 tools/gsi_tiles.py photo 35.594 134.808 15 3 out.jpg   # 種類 緯度 経度 ズーム 半径(タイル数) 出力
  種類: photo（航空写真）/ std（標準地図）/ relief（色別標高）/ hillshade（陰影起伏）/ geology（シームレス地質図）

しくみ: Web地図は地球を256pxの正方形タイルに分けて配っている。緯度経度からタイル番号を計算し、まわりのタイルを並べる。
クレジット: 地理院タイル「出典：国土地理院」/ シームレス地質図「出典：産総研地質調査総合センター（20万分の1日本シームレス地質図V2）」
"""
import io
import math
import sys
import time
import urllib.request

from PIL import Image

UA = "ScienceShortsBot/1.0 (https://github.com/suzu27bayg3-design/aaa)"
URL = {"photo": "https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg",
       "std": "https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png",
       "relief": "https://cyberjapandata.gsi.go.jp/xyz/relief/{z}/{x}/{y}.png",
       "hillshade": "https://cyberjapandata.gsi.go.jp/xyz/hillshademap/{z}/{x}/{y}.png",
       "geology": "https://gbank.gsj.jp/seamless/v2/api/1.2/tiles/{z}/{y}/{x}.png"}


def tile_xy(lat, lon, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def mosaic(kind, lat, lon, z, r):
    cx, cy = tile_xy(lat, lon, z)
    x0, y0 = int(cx) - r, int(cy) - r
    im = Image.new("RGBA", ((2 * r + 1) * 256, (2 * r + 1) * 256), (255, 255, 255, 0))
    for i in range(2 * r + 1):
        for j in range(2 * r + 1):
            u = URL[kind].format(z=z, x=x0 + i, y=y0 + j)
            try:
                data = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30).read()
                im.paste(Image.open(io.BytesIO(data)).convert("RGBA"), (i * 256, j * 256))
            except Exception as e:  # 海などタイルが無い所は空白のまま
                print("miss", u, str(e)[:40])
            time.sleep(0.1)
    return im, (x0, y0)


def to_px(lat, lon, z, origin):
    x, y = tile_xy(lat, lon, z)
    return (x - origin[0]) * 256, (y - origin[1]) * 256


if __name__ == "__main__":
    kind, lat, lon, z, r, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    im, org = mosaic(kind, lat, lon, z, r)
    im.convert("RGB").save(out, quality=92)
    print("wrote", out, im.size, "origin", org)
