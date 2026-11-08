"""ふしぎな絶景の科学 #1 玄武洞（兵庫県豊岡市）

事実の根拠:
- 約160万年前の火山活動でできた玄武岩の柱状節理 … 産総研 地質ニュース / 環境省
- 洞くつは江戸時代などに石を切り出した跡（採石場）… 豊岡市資料
- 「玄武洞」は1807年に柴野栗山が命名。1884年に小藤文次郎がここの石を「玄武岩」と命名 … 豊岡市資料
- 松山基範が、玄武洞の岩が今と逆向きに磁化していることを発見（1926年発見・1929年発表とする資料あり）… 環境省 / 神戸新聞
- 柱状節理：厚い溶岩が冷えて縮むとき、表面に割れ目ができ、六角形に近い柱になる（5〜7角形もまじる）
"""
import math

from PIL import Image, ImageDraw

import longform as L

TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 190, 90)
MAP_CREDITS = ["航空写真・陰影起伏: 出典 国土地理院（地理院タイルを加工して作成）",
               "地質図: 出典 産総研地質調査総合センター 20万分の1日本シームレス地質図V2（CC BY 4.0、玄武岩の範囲を抽出して加工）"]
PLACE = dict(name="玄武洞", pref="兵庫県豊岡市", lat=35.594, lon=134.808)


def _label(d, xy, s, size=34, fill=L.WHITE):
    d.text(xy, s, font=L.jp(size, True), fill=fill, anchor="mm", stroke_width=5,
           stroke_fill=L.WHITE if fill == L.NAVY else L.NAVY)


def _hex_centers(w, h, a):
    pts = []
    for row in range(-1, int(h / (a * 1.5)) + 2):
        for col in range(-1, int(w / (a * math.sqrt(3))) + 2):
            pts.append((col * a * math.sqrt(3) + (a * math.sqrt(3) / 2 if row % 2 else 0), row * a * 1.5))
    return pts


def cooling(t, lt):
    """上から見た溶岩：熱い（オレンジ）→ 冷えて灰色に。縮むにつれて六角形の割れ目が広がる"""
    W, H = 900, 640
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    k = min(1.0, lt / 3.0)  # 冷え方
    hot, cold = (255, 120, 40), (90, 95, 105)
    col = tuple(int(hot[i] * (1 - k) + cold[i] * k) for i in range(3))
    box = (40, 40, W - 40, H - 120)
    d.rounded_rectangle(box, 26, fill=col)
    cracks = Image.new("RGBA", (W, H))
    full = d
    d = ImageDraw.Draw(cracks)
    a = 70
    gap = 2 + 9 * k  # 縮むほど割れ目が広がる
    for cx, cy in _hex_centers(box[2] - box[0], box[3] - box[1], a):
        x, y = cx + box[0], cy + box[1]
        r = a - gap
        poly = [(x + r * math.cos(math.radians(60 * i + 30)), y + r * math.sin(math.radians(60 * i + 30))) for i in range(6)]
        if k > 0.15:
            d.polygon(poly, outline=(30, 30, 40), width=int(2 + 5 * k))
            # 中心へ向かう小さな矢印（縮む向き）
            if k < 0.95:
                for i in (0, 2, 4):
                    p = poly[i]
                    q = (p[0] + (x - p[0]) * 0.35, p[1] + (y - p[1]) * 0.35)
                    d.line([p, q], fill=(255, 255, 255, int(200 * k)), width=4)
    mask = Image.new("L", (W, H))
    ImageDraw.Draw(mask).rounded_rectangle(box, 26, fill=255)
    im.paste(cracks, (0, 0), Image.composite(cracks.split()[3], Image.new("L", (W, H)), mask))
    d = full
    _label(d, (W / 2, H - 70), "熱い溶岩 → 冷えて縮む → 六角形に割れる" if k < 1 else "割れ目が下へのびて、柱になる", 36,
           (255, 220, 120))
    return im


def columns(t, lt):
    """横から見た図：割れ目が冷えた面から内側へのびて、柱が並ぶ"""
    W, H = 900, 640
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    top, bot = 60, 500
    d.rectangle((40, top, W - 40, bot), fill=(95, 100, 110))
    grow = min(1.0, lt / 2.0)
    for i in range(1, 12):
        x = 40 + i * (W - 80) / 12
        y1 = top + (bot - top) * grow
        d.line([(x, top), (x + 6 * math.sin(i), y1)], fill=(25, 25, 35), width=7)
    d.rectangle((40, top - 30, W - 40, top), fill=(120, 170, 255))
    _label(d, (W / 2, top - 15), "冷たい空気（ここから冷える）", 28)
    _label(d, (W / 2, 560), "割れ目が下へのびる ＝ 柱状節理", 36, (255, 220, 120))
    return im


def magnet(t, lt):
    """今の地球の磁石と、玄武洞の岩に残った磁石の向きをくらべる"""
    W, H = 900, 640
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    flip = min(1.0, max(0.0, (lt - 0.8) / 0.8))
    for cx, name, ang in ((230, "今の地球", -90), (670, "玄武洞の岩", -90 + 180 * flip)):
        d.ellipse((cx - 170, 140, cx + 170, 480), fill=(240, 240, 245), outline=L.WHITE, width=6)
        r = math.radians(ang)
        tip = (cx + 140 * math.cos(r), 310 + 140 * math.sin(r))
        tail = (cx - 140 * math.cos(r), 310 - 140 * math.sin(r))
        n = (math.cos(r + math.pi / 2) * 28, math.sin(r + math.pi / 2) * 28)
        d.polygon([tip, (cx + n[0], 310 + n[1]), (cx - n[0], 310 - n[1])], fill=(230, 50, 60))
        d.polygon([tail, (cx + n[0], 310 + n[1]), (cx - n[0], 310 - n[1])], fill=(60, 90, 200))
        _label(d, (cx, 530), name, 40)
        _label(d, (cx, 110), "北", 34, (255, 220, 120))
    _label(d, (W / 2, 600), "N極とS極が入れかわっていた！", 38, (255, 220, 120))
    return im


import json
import os

from PIL import ImageFilter

_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
_AER = Image.open(os.path.join(_M, "aerial.jpg")).convert("RGBA")
_MASK = Image.open(os.path.join(_M, "basalt_mask.png")).convert("L")
_INFO = json.load(open(os.path.join(_M, "aerial.json")))
CROP = (250, 380, 1650, 1780)  # 航空写真（1792px四方）から使う範囲


def _px(lat, lon):
    z, (ox, oy) = _INFO["z"], _INFO["origin"]
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return (x - ox) * 256, (y - oy) * 256


def realmap(t, lt):
    """国土地理院の航空写真（陰影起伏を重ねて立体感）に、産総研の地質図から取り出した
    約160万年前の玄武岩の分布（むらさき）を重ねる。円山川の両岸に同じ溶岩がある"""
    S = 900
    x0, y0, x1, y1 = CROP
    z = 1.0 - 0.06 * min(1, lt / 6)  # ゆっくりズーム
    cw = (x1 - x0) * z
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    box = (cx - cw / 2, cy - cw / 2, cx + cw / 2, cy + cw / 2)
    sc = S / cw
    base = _AER.crop(tuple(int(v) for v in box)).resize((S, S), Image.BILINEAR)
    a = min(1.0, max(0.0, (lt - 1.0) / 0.8))
    if a > 0:
        m = _MASK.crop(tuple(int(v) for v in box)).resize((S, S), Image.BILINEAR).point(lambda v: int(v * 0.55 * a))
        base = Image.composite(Image.new("RGBA", (S, S), (210, 70, 210, 255)), base, m)
    im = Image.new("RGBA", (S, S + 60))
    im.paste(base, (0, 0))
    d = ImageDraw.Draw(im)
    to = lambda lat, lon: ((_px(lat, lon)[0] - box[0]) * sc, (_px(lat, lon)[1] - box[1]) * sc)  # noqa: E731
    # 円山川
    rx, ry = to(35.598, 134.803)
    _label(d, (rx - 40, ry - 40), "円山川", 32, (150, 210, 255))
    # 西岸の溶岩（二見山付近）
    if a > 0.5:
        wx, wy = to(35.5797, 134.7882)
        _label(d, (wx, wy - 10), "二見山付近", 34)
        _label(d, (wx, wy + 32), "（西岸の溶岩）", 28)
    # 流れの向き（推定）
    k = min(1.0, max(0.0, (lt - 2.4) / 1.0))
    if k > 0:
        sx, sy = to(35.5835, 134.7955)
        ex, ey = to(35.5925, 134.8045)
        mx, my = sx + (ex - sx) * k, sy + (ey - sy) * k
        d.line([(sx, sy), (mx, my)], fill=(255, 210, 80), width=10)
        if k >= 1:
            ang = math.atan2(ey - sy, ex - sx)
            d.polygon([(ex, ey), (ex - 30 * math.cos(ang - 0.5), ey - 30 * math.sin(ang - 0.5)),
                       (ex - 30 * math.cos(ang + 0.5), ey - 30 * math.sin(ang + 0.5))], fill=(255, 210, 80))
    # 玄武洞のピン
    gx, gy = to(35.594, 134.808)
    d.ellipse((gx - 18, gy - 58, gx + 18, gy - 22), fill=(230, 50, 60))
    d.polygon([(gx - 15, gy - 34), (gx + 15, gy - 34), (gx, gy)], fill=(230, 50, 60))
    _label(d, (gx + 95, gy - 40), "玄武洞", 36)
    # 凡例と出典
    if a > 0:
        d.rounded_rectangle((16, 16, 470, 70), 16, fill=(0, 0, 0, 170))
        d.rectangle((30, 30, 60, 56), fill=(210, 70, 210))
        d.text((74, 43), "約160万年前の玄武岩の溶岩", font=L.jp(28, True), fill=L.WHITE, anchor="lm")
    d.text((S / 2, S + 30), "出典：国土地理院（航空写真・陰影起伏）／産総研（シームレス地質図V2）を加工",
           font=L.jp(22, True), fill=(220, 230, 240), anchor="mm")
    return im



# ---- 六角の柱ができるまで（段階ごとの図） ---------------------------------------------
import numpy as np  # noqa: E402

HOT, COLD = (255, 110, 40), (92, 96, 108)


def _mix(c1, c2, k):
    return tuple(int(c1[i] * (1 - k) + c2[i] * k) for i in range(3))


def pond(t, lt):
    """横から見た溶岩の池：上（空気）と下（地面）から冷えて、冷えた部分（灰色）が内側へ進む"""
    W, H = 900, 760
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    top, bot = 150, 610
    k = min(1.0, lt / 5.0)
    d.rectangle((60, top - 70, W - 60, top), fill=(150, 200, 245))
    d.rectangle((60, bot, W - 60, bot + 60), fill=(150, 120, 90))
    d.rectangle((60, top, W - 60, bot), fill=HOT)
    # 冷えた層：上からは速く、下からはゆっくり
    ct, cb = (bot - top) * 0.45 * k, (bot - top) * 0.25 * k
    for i in range(int(ct)):
        d.line((60, top + i, W - 60, top + i), fill=_mix(COLD, HOT, i / max(1, ct) * 0.5))
    for i in range(int(cb)):
        d.line((60, bot - i, W - 60, bot - i), fill=_mix(COLD, HOT, i / max(1, cb) * 0.5))
    for x in range(140, W - 100, 160):  # 熱が逃げる矢印
        ph = (t * 0.8 + x / 300) % 1
        d.line((x, top - 10 - 40 * ph, x, top - 50 - 40 * ph), fill=(255, 255, 255), width=6)
        d.line((x, bot + 10 + 20 * ph, x, bot + 40 + 20 * ph), fill=(255, 230, 200), width=6)
    _label(d, (W / 2, top - 105), "空気で冷える", 34)
    _label(d, (W / 2, bot + 100), "地面で冷える", 34)
    _label(d, (W / 2, (top + bot) / 2), "まだ熱い溶岩", 40)
    _label(d, (W - 150, top + ct / 2 + 10), "固まった部分", 28, (220, 230, 255))
    _label(d, (130, (top + bot) / 2 - 150), "厚さ\n約100m", 30, (255, 220, 120))
    return im


_rng = np.random.default_rng(7)
_HC = []
for _r in range(-1, 9):
    for _c in range(-1, 11):
        _HC.append(((_c + (0.5 if _r % 2 else 0)) * 92, _r * 92 * math.sqrt(3) / 2))
_HC = np.array(_HC)
_JIT = _rng.normal(0, 30, _HC.shape)


def _voronoi_edges(centers, w, h, scale=4):
    """点に一番近い場所ごとに色分けし、境目をひびとして取り出す（ボロノイ図）"""
    gw, gh = w // scale, h // scale
    ys, xs = np.mgrid[0:gh, 0:gw]
    px, py = xs * scale, ys * scale
    dist = (px[None] - centers[:, 0, None, None]) ** 2 + (py[None] - centers[:, 1, None, None]) ** 2
    lab = dist.argmin(0)
    e = np.zeros_like(lab, dtype=bool)
    e[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    e[1:, :] |= lab[1:, :] != lab[:-1, :]
    return Image.fromarray((e * 255).astype(np.uint8)).resize((w, h), Image.NEAREST)


def cracks(t, lt):
    """上から見た表面：縮もうとして引っぱられ、ひびが入る。最初はバラバラ → 六角形の網目に整っていく"""
    W, H = 900, 640
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    box = (40, 40, W - 40, H - 120)
    d.rounded_rectangle(box, 26, fill=COLD)
    k = min(1.0, max(0.0, (lt - 1.0) / 3.5))  # 0:バラバラ → 1:六角形
    if lt > 0.4:
        e = _voronoi_edges(_HC + _JIT * (1 - k), box[2] - box[0], box[3] - box[1])
        e = e.filter(ImageFilter.MaxFilter(5))
        lay = Image.new("RGBA", e.size, (25, 25, 35, 255))
        m = Image.new("L", (W, H))
        mk = Image.new("L", e.size)
        mk.paste(e, (0, 0))
        clip = Image.new("L", (W, H))
        ImageDraw.Draw(clip).rounded_rectangle(box, 26, fill=255)
        m.paste(mk, (box[0], box[1]))
        full = Image.new("RGBA", (W, H))
        full.paste(lay, (box[0], box[1]))
        im.paste(full, (0, 0), Image.composite(m, Image.new("L", (W, H)), clip))
    if lt < 1.4:  # 縮む向きの矢印
        for x, y in ((250, 200), (650, 200), (250, 380), (650, 380)):
            cx, cy = W / 2, 290
            d.line([(x, y), (x + (cx - x) * 0.25, y + (cy - y) * 0.25)], fill=(255, 220, 120), width=8)
    _label(d, (W / 2, H - 70), "縮む → 引っぱられて、ひびが入る" if k < 0.5 else "3本のひびが約120度で出会う → 六角形", 34,
           (255, 220, 120))
    return im


def grow(t, lt):
    """横から見た図：固まった部分が内側へ進むたび、ひびも少しずつ内側へのびて長い柱になる"""
    W, H = 900, 700
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    top, bot = 60, 560
    k = min(1.0, lt / 4.5)
    ft, fb = top + (bot - top) * 0.62 * k, bot - (bot - top) * 0.38 * k  # 上と下から進む「冷えた面」
    d.rectangle((60, top, W - 60, bot), fill=HOT)
    d.rectangle((60, top, W - 60, ft), fill=COLD)
    d.rectangle((60, fb, W - 60, bot), fill=COLD)
    for i in range(1, 13):
        x = 60 + i * (W - 120) / 13
        d.line([(x, top), (x + 4 * math.sin(i * 1.7), ft)], fill=(25, 25, 35), width=7)
        d.line([(x + 3 * math.sin(i), fb), (x, bot)], fill=(25, 25, 35), width=7)
    d.line((60, ft, W - 60, ft), fill=(255, 230, 120), width=4)
    d.line((60, fb, W - 60, fb), fill=(255, 230, 120), width=4)
    if k < 1:
        _label(d, (W / 2, (ft + fb) / 2), "まだ熱い", 34)
    _label(d, (W / 2, H - 70), "冷えた面が進むたび、ひびも内側へのびる → 長い柱", 32, (255, 220, 120))
    return im


def starch(t, lt):
    """片栗粉の実験：水でといて乾かすと、縮んでひびが入り、六角形の柱になる"""
    W, H = 900, 680
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    d.ellipse((90, 120, 810, 520), fill=(235, 235, 240), outline=L.WHITE, width=8)  # 皿
    d.ellipse((150, 160, 750, 480), fill=(250, 248, 240))
    k = min(1.0, max(0.0, (lt - 0.6) / 2.5))
    if k > 0:
        e = _voronoi_edges(_HC * 0.6 - 40 + _JIT * 0.6 * (1 - k), 600, 320, scale=3).filter(ImageFilter.MaxFilter(3))
        mk = Image.new("L", (W, H))
        mk.paste(e, (150, 160))
        clip = Image.new("L", (W, H))
        ImageDraw.Draw(clip).ellipse((150, 160, 750, 480), fill=255)
        im.paste(Image.new("RGBA", (W, H), (150, 140, 120, 255)), (0, 0), Image.composite(mk, Image.new("L", (W, H)), clip))
    _label(d, (W / 2, 70), "片栗粉＋水 → 乾かす", 38)
    _label(d, (W / 2, 580), "乾くと縮んで、六角形の柱ができる", 36, (255, 220, 120))
    return im


FIGS = {"cooling": cooling, "columns": columns, "magnet": magnet, "realmap": realmap,
        "pond": pond, "cracks": cracks, "grow": grow, "starch": starch}

SCENES = [
    dict(spk="Z", ex="think", say="この六角形の柱、だれが作ったのだ？",
         read="この、ろっかっけいの柱、だれが作ったのだ？",
         head="だれが作った？", show=("photo", "Genbudo_Cave_2018.jpg", "in")),
    dict(spk="M", say="兵庫県豊岡市の玄武洞。約160万年前の溶岩が作った柱なの。",
         read="ひょうごけん、とよおかしの、げんぶどう。やく、ひゃくろくじゅうまんねん前の溶岩が作った柱なの。",
         head="自然が作った柱", sub="約160万年前の溶岩", show=("map",), head_y=1340),
    dict(spk="M", say="むらさきが同じ溶岩。川の西の二見山あたりで噴火して、両岸に広がったと考えられているの。",
         read="むらさきが、同じ溶岩。川の西の、ふたみやまあたりで噴火して、両岸に広がったと考えられているの。",
         head="両岸に同じ溶岩", show=("fig", "realmap"), head_y=1320),
    dict(spk="M", say="厚さ約100メートルの溶岩は、上と下から、ゆっくり冷えていったの。",
         read="厚さ、やく、ひゃくメートルの溶岩は、上と下から、ゆっくり冷えていったの。",
         head="① 上と下から\n冷える", show=("fig", "pond"), head_y=1300),
    dict(spk="M", say="固まると縮んで、表面にひびが入るの。ひびは約120度で出会う形に落ち着いて、六角形になるのよ。",
         read="固まると、ちぢんで、表面にひびが入るの。ひびは、やく、ひゃくにじゅうどで出会う形に落ち着いて、ろっかっけいになるのよ。",
         head="② 縮んで\n六角形にひび割れ", show=("fig", "cracks"), head_y=1230),
    dict(spk="M", say="固まった部分が内側へ進むたび、ひびものびて、長い柱になったの。",
         read="固まった部分が、内側へ進むたび、ひびも、のびて、長い柱になったの。",
         head="③ ひびがのびて\n長い柱に", show=("fig", "grow"), head_y=1250),
    dict(spk="Z", say="片栗粉を乾かしても、六角形の柱ができるのだ！",
         read="かたくりこを、乾かしても、ろっかっけいの柱ができるのだ！",
         head="片栗粉でも\nできる！", sub="乾いて縮むと同じしくみ", show=("fig", "starch"), head_y=1230),
    dict(spk="M", say="それを川がけずり、人が石を切り出したあとが玄武洞よ。",
         read="それを川がけずり、人が石を切り出したあとが、げんぶどうよ。",
         head="川がけずり\n人が切り出した", show=("photo", "Genbudo_Cave_2018_2.jpg", "right")),
    dict(spk="Z", say="自然が作った六角形の柱なのだ！行ってみたいのだ？",
         read="自然が作った、ろっかっけいの柱なのだ！行ってみたいのだ？",
         head="行ってみたい？", show=("photo", "Genbudo_Cave_2018_3.jpg", "out")),
]

META = dict(
    title="六角形の柱は誰が作った？兵庫・玄武洞のふしぎ #shorts #絶景 #科学",
    alt_titles=["自然が作った六角形の柱！玄武洞はこうしてできた #shorts #ジオパーク",
                "地球の磁石が逆だった証拠が見つかった場所 #shorts #科学 #兵庫"],
    lead="兵庫県豊岡市の玄武洞には、六角形に近い石の柱がずらりと並びます。人が作ったのではなく、約160万年前の溶岩が冷えるときにできた自然の形です。",
    points=["溶岩は円山川の西の二見山付近で噴火し、川の両岸に同じ玄武岩が残っている（産総研の地質図で確認）",
            "① 厚さ約100mの溶岩が、空気にふれる上と地面にふれる下から、ゆっくり冷える",
            "② 固まると縮もうとして表面が引っぱられ、ひびが入る。ひびは約120度で出会う形に落ち着き、六角形が多くなる",
            "③ 固まった部分が内側へ進むたび、ひびも少しずつのびて、冷えた面に垂直な長い柱になる（柱状節理）",
            "片栗粉を水でといて乾かしても、同じしくみで六角形の柱ができる（研究の模型として使われている）",
            "おまけ：ここの岩は今と逆向きに磁化していて、地球のN極とS極の入れかわり（地磁気逆転）の発見につながった"],
    principle=("ものは冷えると縮みます。厚い溶岩は、表面が先に冷えて固まり、縮もうとしますが、まわりとつながっているので"
               "引っぱられる力がたまり、こらえきれなくなった所でひびが入ります。ひびは力をいちばん効率よく逃がせるように、"
               "3本が約120度で出会う形に落ち着きやすく、平面を同じ大きさですき間なく分けると六角形になります（実際は5角形や"
               "7角形もまじります）。冷えて固まった部分は少しずつ内側へ進み、そのたびにひびも内側へのびるので、冷えた面に"
               "垂直な長い柱がならびます。片栗粉を水でといて乾かしても、乾いて縮むことで同じように六角形の柱ができ、"
               "柱状節理を調べる実験の模型として使われています。"),
    sources=[("環境省 山陰海岸国立公園（玄武洞）", "https://www.env.go.jp/nature/nationalparks/try/all/act883.html"),
             ("産総研 地質調査総合センター 地質ニュース", "https://www.gsj.jp/data/chishitsunews/05_11_07.pdf"),
             ("豊岡市 資料（玄武洞の名前と採石の歴史）",
              "https://www.city.toyooka.lg.jp/_res/projects/default_project/_page_/001/002/653/0203.pdf"),
             ("産総研 地質調査総合センター 20万分の1日本シームレス地質図V2", "https://gbank.gsj.jp/seamless/"),
             ("国土地理院 地理院タイル（航空写真・陰影起伏・標準地図）", "https://maps.gsi.go.jp/development/ichiran.html"),
             ("日本の地質案内（玄武洞：アルカリかんらん石玄武岩・層厚約100m）",
              "https://www.web-gis.jp/GS_GeoGuide/GeoDocument/GeoSite_J05-003.html"),
             ("Goehring, Mahadevan, Morris (2009) 柱状節理の大きさが決まるしくみ（片栗粉の実験）PNAS 106, 387",
              "https://pmc.ncbi.nlm.nih.gov/articles/PMC2615021"),
             ("トロント大学「Cracking the Giant's Causeway」（片栗粉で柱状節理を再現）",
              "https://www.physics.utoronto.ca/~nonlin/PNASpress/PNASpress.html"),
             ("神戸新聞（玄武洞と松山基範）", "https://www.kobe-np.co.jp/rentoku/bunkazai/201606/0009237092.shtml")],
    tags=["玄武洞", "げんぶどう", "柱状節理", "玄武岩", "山陰海岸ジオパーク", "ジオパーク", "兵庫県", "豊岡市", "城崎",
          "絶景", "ふしぎな絶景", "地磁気逆転", "松山基範", "地学", "科学", "観光", "ずんだもん", "四国めたん", "shorts"],
    hashtags=["#絶景", "#科学", "#玄武洞", "#ジオパーク", "#shorts"],
    pinned="アイスランドや北アイルランドにも六角形の柱が並ぶ場所があります。次はどこのふしぎな絶景が見たい？コメントで教えてください！",
    notes=["「約120度で出会う」は割れ目の力学からの説明（理想化）で、実際の柱は5〜7角形がまじる。",
           "噴出源は産総研 第四紀火山データベースの「円山川左岸の二見山に噴出源のスコリア丘」に従った。来日岳とする地域資料もある。",
           "地図のむらさきは20万分の1地質図の「第四紀カラブリアン期のアルカリ玄武岩」の範囲。縮尺が小さいので境界はおおよそ。",
           "流れの向きの矢印は、噴出源が西岸にあることからの推定として「考えられている」と表現した。",
           "発見の年は資料によって1926年（発見）と1929年（発表）があるため、見出しは「1926年 発見」とし、説明欄では発表年にふれていない。",
           "「六角形」は「六角形に近い」と言い、5角形や7角形もまじることを説明欄に書いた。",
           "写真は Wikimedia Commons の CC0（著作権放棄）のもの。大きい画像は Commons の自動取得制限で取れず、幅500pxを使用。"],
)
