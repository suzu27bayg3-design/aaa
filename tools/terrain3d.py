#!/usr/bin/env python3
"""国土地理院の標高タイル（DEM）に航空写真を貼って、斜めから見た立体の地形を描く。

しくみ:
  - 標高タイル（dem5a_png / dem_png）は、色(R,G,B)に高さが入っている：x = R*65536 + G*256 + B、
    x < 2^23 なら 高さ = x*0.01 m、x > 2^23 なら (x - 2^24)*0.01 m、(128,0,0) はデータなし
  - 地面の1点1点を、カメラから見た画面の位置に投影し、遠い点から順に塗っていく（手前の点が上書きする＝隠れる）
  - 点と点のすき間ができないよう、各点を縦長の小さな線として塗る
  - hscale で高さを0→1に変えると、地面が平らな状態から盛り上がる様子を描ける
"""
import io
import math
import os
import sys
import time
import urllib.request

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsi_tiles as G  # noqa: E402

UA = G.UA


def dem_mosaic(lat, lon, z, r, kind="dem5a_png"):
    cx, cy = G.tile_xy(lat, lon, z)
    x0, y0 = int(cx) - r, int(cy) - r
    n = 2 * r + 1
    H = np.full((n * 256, n * 256), np.nan, np.float32)
    for i in range(n):
        for j in range(n):
            u = f"https://cyberjapandata.gsi.go.jp/xyz/{kind}/{z}/{x0 + i}/{y0 + j}.png"
            try:
                a = np.array(Image.open(io.BytesIO(urllib.request.urlopen(
                    urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30).read())).convert("RGB")).astype(np.int64)
            except Exception:
                continue
            x = a[:, :, 0] * 65536 + a[:, :, 1] * 256 + a[:, :, 2]
            h = np.where(x < 2 ** 23, x * 0.01, (x - 2 ** 24) * 0.01).astype(np.float32)
            h[(a[:, :, 0] == 128) & (a[:, :, 1] == 0) & (a[:, :, 2] == 0)] = np.nan
            H[j * 256:(j + 1) * 256, i * 256:(i + 1) * 256] = h
            time.sleep(0.05)
    return H, (x0, y0)


def render(H, tex, mpp, target, az, el, dist, hscale=1.0, exag=1.5, size=(540, 960), fov=50, bg=(14, 22, 48),
           local=None):
    """H: 標高(m)の2次元配列, tex: 同じ大きさの航空写真(RGB配列), mpp: 1pxあたりのm
    target: 注目点 (px, py), az: カメラの方位(度, 0=南から北を見る), el: 見下ろす角度(度), dist: カメラまでの距離(m)
    local: (cx, cy, radius_px, k) なら、その円の中だけ高さを k 倍（盛り上がる演出）"""
    h, w = H.shape
    Hs = np.nan_to_num(H, nan=0.0).copy()
    base = np.nanmin(H)
    Hs = (Hs - base)
    if local is not None:
        cx, cy, rad, k = local
        yy, xx = np.mgrid[0:h, 0:w]
        rr = np.hypot(xx - cx, yy - cy) / rad
        wgt = np.clip(1 - rr, 0, 1) ** 1.5  # 中心ほど強く
        ground = np.percentile(Hs[rr > 1.2], 50) if (rr > 1.2).any() else 0
        Hs = Hs - (Hs - ground).clip(0) * wgt * (1 - k)
    Hs = Hs * hscale * exag
    step = 2
    ys, xs = np.mgrid[0:h:step, 0:w:step]
    X = (xs - target[0]) * mpp
    Y = -(ys - target[1]) * mpp
    Z = Hs[ys, xs]
    C = tex[ys, xs]
    a = math.radians(az)
    e = math.radians(el)
    # カメラ座標：カメラは注目点から dist だけ離れ、方位 az（0なら南側）から el の角度で見下ろす
    xr = X * math.cos(a) - Y * math.sin(a)
    yr = X * math.sin(a) + Y * math.cos(a)  # 奥行き方向（正が奥）
    zr = Z - Hs[int(target[1]), int(target[0])] if 0 <= int(target[1]) < h and 0 <= int(target[0]) < w else Z
    depth = yr * math.cos(e) - zr * math.sin(e) + dist  # 奥ほど遠く、高い所ほどカメラに近い
    up = yr * math.sin(e) + zr * math.cos(e)  # 奥ほど・高いほど画面の上
    W, Hh = size
    f = (W / 2) / math.tan(math.radians(fov / 2))
    ok = depth > 50
    sx = (W / 2 + f * xr / depth).astype(np.int32)
    sy = (Hh / 2 - f * up / depth).astype(np.int32)
    ok &= (sx >= 0) & (sx < W) & (sy > -400) & (sy < Hh)
    idx = np.argsort(-depth[ok], kind="stable")  # 遠い順
    sx, sy, C, dep = sx[ok][idx], sy[ok][idx], C[ok][idx], depth[ok][idx]
    img = np.zeros((Hh, W, 3), np.uint8)
    g = np.linspace(0, 1, Hh)[:, None]  # 空：上は青、地平線に近いほど白っぽく
    sky = (np.array([70, 120, 190]) * (1 - g) + np.array([215, 228, 240]) * g).astype(np.uint8)
    img[:] = sky[:, None, :]
    span = np.clip((f * step * mpp / dep * 2.6).astype(np.int32), 2, 70)  # 縦の大きさ（近いほど大きい）
    wid = np.clip((f * step * mpp / dep * 1.2).astype(np.int32), 2, 30)  # 横の大きさ
    for dy in range(0, 71):
        m = span > dy
        if not m.any():
            break
        yy = sy[m] + dy
        v = (yy >= 0) & (yy < Hh)
        ww = wid[m][v]
        for dx in range(0, int(ww.max()) if len(ww) else 0):
            mm = ww > dx
            xx = np.clip(sx[m][v][mm] + dx, 0, W - 1)
            img[yy[v][mm], xx] = C[m][v][mm]
    # 空のグラデーション（地面がない上の方）
    return Image.fromarray(img)
