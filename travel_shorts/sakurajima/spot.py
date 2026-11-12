"""ふしぎな絶景の科学 桜島（30秒・全画面の型）

事実の根拠:
- 1914年1月12日に噴火が始まり、13日に溶岩が流れ出し、1月29日に瀬戸海峡をふさいで大隅半島と陸続きに … 内閣府 防災
- 噴火前の瀬戸海峡は幅300〜400m、深さ70〜80m … 鹿児島県（大正噴火100周年記念誌）
"""
import math
import os

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

import longform as L

FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 150, 80)
PLACE = dict(name="桜島", pref="鹿児島県", lat=31.585, lon=130.66)
MAP_CREDITS = ["航空写真・陰影起伏: 出典 国土地理院（地理院タイルを加工して作成）"]  # 古い地図と写真は photos/credits.json

SW, SH = 1080, 1920
_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
_P = Image.open(os.path.join(_M, "photo_z13.jpg")).convert("RGB")
_H = Image.open(os.path.join(_M, "hill_z13.png")).convert("RGB")
_BASE = ImageChops.multiply(_P, Image.blend(_H, Image.new("RGB", _H.size, "white"), 0.45))
BOX = (300, 0, 1308, 1792)  # 縦長（9:16）の範囲：桜島と大隅半島がつながる所まで
LAVA, GOLD = (255, 110, 40), (255, 214, 120)
# 東の山腹から瀬戸海峡（つながった所）までの溶岩の通り道（目安）
FLOW = [(975, 1050), (1005, 1082), (1035, 1115), (1060, 1145), (1080, 1166), (1092, 1176)]
STRAIT = (1080, 1166)  # 地形図で大正溶岩と大隅半島がつながる所（国道224号と220号の合流付近）


def _view(scale, cx=None, cy=None):
    cx = cx or (BOX[0] + BOX[2]) / 2
    cy = cy or (BOX[1] + BOX[3]) / 2
    w, h = (BOX[2] - BOX[0]) * scale, (BOX[3] - BOX[1]) * scale
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    return box, _BASE.crop(tuple(int(v) for v in box)).resize((SW, SH), Image.BILINEAR)


def _scr(box, x, y):
    return (x - box[0]) * SW / (box[2] - box[0]), (y - box[1]) * SH / (box[3] - box[1])


def _glow(base, lay, blur=10):
    return ImageChops.add(ImageChops.add(base, lay.filter(ImageFilter.GaussianBlur(blur))), lay)


def hook(t, lt):
    _, im = _view(1.0 - 0.12 * min(1, lt / 4))
    return im


def joint(t, lt):
    """つながった所（瀬戸）に寄って、光の輪で示す"""
    k = min(1.0, lt / 2.5)
    s = 1.0 - 0.45 * k
    cx = (BOX[0] + BOX[2]) / 2 + (STRAIT[0] - (BOX[0] + BOX[2]) / 2) * k
    cy = (BOX[1] + BOX[3]) / 2 + (STRAIT[1] - (BOX[1] + BOX[3]) / 2) * k
    box, base = _view(s, cx, cy)
    lay = Image.new("RGB", (SW, SH))
    d = ImageDraw.Draw(lay)
    x, y = _scr(box, *STRAIT)
    for i in range(3):
        ph = (t * 0.7 + i / 3) % 1
        r = 30 + 150 * ph
        d.ellipse((x - r, y - r, x + r, y + r), outline=tuple(int(v * (1 - ph)) for v in GOLD), width=7)
    return _glow(base, lay)


_RNG = np.random.default_rng(5)
_PTS = [(_RNG.uniform(0, 1), _RNG.normal(0, 5), _RNG.uniform(0.7, 1.3)) for _ in range(120)]
_SEG = [math.dist(FLOW[i], FLOW[i + 1]) for i in range(len(FLOW) - 1)]
_TOT = sum(_SEG)


def _at(s):
    s = max(0.0, min(_TOT - 0.01, s))
    for i, l in enumerate(_SEG):
        if s <= l:
            f = s / l
            return FLOW[i][0] + (FLOW[i + 1][0] - FLOW[i][0]) * f, FLOW[i][1] + (FLOW[i + 1][1] - FLOW[i][1]) * f
        s -= l
    return FLOW[-1]


_PILE = [(_RNG.normal(0, 1), _RNG.normal(0, 1), _RNG.uniform(0, 1)) for _ in range(260)]


def _lava_frame(t, k, counter=None):
    """溶岩の粒が東へ流れ、つながった所に少しずつ積もって海峡をふさぐ"""
    box, base = _view(0.55, STRAIT[0] - 60, STRAIT[1] - 40)
    base = ImageEnhance.Brightness(base).enhance(0.75)
    lay = Image.new("RGB", (SW, SH))
    d = ImageDraw.Draw(lay)
    for u, off, sp in _PTS:
        s0 = (u * _TOT + t * 60 * sp) % (_TOT * min(1, k * 1.6) + 1)
        for j in range(7):
            x, y = _at(s0 - j * 4)
            X, Y = _scr(box, x, y + off)
            r = 7 - j * 0.8
            c = 1 - j / 7
            d.ellipse((X - r, Y - r, X + r, Y + r), fill=tuple(int(v * c) for v in LAVA))
    X0, Y0 = _scr(box, *STRAIT)
    n = int(len(_PILE) * max(0.0, (k - 0.3) / 0.7))
    for gx, gy, br in _PILE[:n]:  # 積もった溶岩（粒の集まり）
        x, y = X0 + gx * 55, Y0 + gy * 32
        r = 5 + 3 * br
        c = 0.55 + 0.45 * br * (0.7 + 0.3 * math.sin(t * 4 + gx * 3))
        d.ellipse((x - r, y - r, x + r, y + r), fill=tuple(int(v * c) for v in LAVA))
    im = _glow(base, lay, 12).convert("RGBA")
    if counter is not None:
        dd = ImageDraw.Draw(im)
        dd.text((SW / 2, SH * 0.62), counter, font=L.jp(150), fill=GOLD, anchor="mm", stroke_width=10, stroke_fill=L.NAVY)
    return im


def lava(t, lt):
    return _lava_frame(t, min(1.0, lt / 3.5))


def days(t, lt):
    k = min(1.0, lt / 2.5)
    return _lava_frame(t, 1.0, f"{int(round(17 * k))}日目")


_OLD = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos",
                               "Sakurajima_southeast_map_before_1914.png")).convert("RGB")


def oldmap(t, lt):
    """噴火前の地図（全体を見せる）。海峡の場所を光の輪で示す"""
    W = 1000
    sc = W / _OLD.width
    m = _OLD.resize((W, int(_OLD.height * sc)), Image.LANCZOS)
    z = 1.0 + 0.25 * min(1, lt / 5)  # 海峡に向かってゆっくり寄る
    fx, fy = 395 / 500, 205 / 310  # 地図の上の海峡の位置（割合）
    mw, mh = int(W / z), int(m.height / z)
    x0 = int(min(max(0, fx * W - mw / 2), W - mw))
    y0 = int(min(max(0, fy * m.height - mh / 2), m.height - mh))
    m = m.crop((x0, y0, x0 + mw, y0 + mh)).resize((W, int(W * mh / mw)), Image.LANCZOS)
    out = Image.new("RGB", (SW, SH), (14, 18, 30))
    X, Y = (SW - W) // 2, 700 - m.height // 2
    out.paste(m, (X, Y))
    lay = Image.new("RGB", (SW, SH))
    d = ImageDraw.Draw(lay)
    cx = X + (fx * _OLD.width * sc - x0) * W / mw
    cy = Y + (fy * _OLD.height * sc - y0) * W / mw
    for i in range(3):
        ph = (t * 0.7 + i / 3) % 1
        r = 25 + 110 * ph
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=tuple(int(v * (1 - ph)) for v in GOLD), width=7)
    out = _glow(out, lay).convert("RGBA")
    ImageDraw.Draw(out).text((SW / 2, Y + m.height + 30), "地図：大日本帝国陸軍 陸地測量部（噴火前）/ Public domain / Wikimedia Commons",
                             font=L.jp(22, True), fill=(220, 230, 240), anchor="mm")
    return out


FIGS = {"oldmap": oldmap, "hook": hook, "joint": joint, "lava": lava, "days": days}

SCENES = [
    dict(spk="Z", ex="panic", say="この島、陸とつながってるのだ！？",
         read="この、しま、りくと、つながってるのだ！？",
         head="この島\n陸とつながってる！？", show=("fig", "hook")),
    dict(spk="M", say="噴火の前の地図を見て。ここは海峡で、島と半島は離れていたの。",
         read="ふんかの前の、ちずを見て。ここは、かいきょうで、しまと、はんとうは、はなれていたの。",
         head="1914年より前は\n海だった", show=("fig", "oldmap"), head_y=1240),
    dict(spk="M", say="1914年の大噴火で、溶岩がこの海峡に流れこんだのよ。",
         read="せんきゅうひゃくじゅうよねんの、だいふんかで、ようがんが、この、かいきょうに、ながれこんだのよ。",
         head="溶岩が\n海に流れこむ", show=("photo", "Sakurajima_taisyo_eruption_at_seto_strait.jpg", "in"), head_y=1240),
    dict(spk="M", say="噴火が始まってから、わずか17日で海峡を埋めて、陸続きになったの。",
         read="ふんかが始まってから、わずか、じゅうななにちで、かいきょうを、うめて、りくつづきに、なったの。",
         head="わずか17日", show=("fig", "days")),
    dict(spk="Z", say="今はここで、島が陸になっているのだ！",
         read="いまは、ここで、しまが、りくに、なっているのだ！",
         head="島が陸に！", show=("fig", "joint")),
]

META = dict(
    title="この島、陸とつながってる！？桜島 #shorts #絶景 #科学",
    alt_titles=["溶岩が海を埋めた！17日で島が陸に #shorts #桜島", "桜島はもう島じゃない！？ #shorts #火山"],
    lead="鹿児島の桜島は、もとは鹿児島湾にうかぶ島でした。1914年（大正3年）の大噴火で流れた溶岩が海峡を埋め、大隅半島と陸続きになりました。",
    points=["1914年1月12日に噴火が始まり、13日に溶岩が流れ出した",
            "1月29日、溶岩が瀬戸海峡（幅300〜400m・深さ70〜80m）をふさぎ、大隅半島と陸続きになった"],
    principle=("溶岩は、火口から流れ出したあとも表面が冷えて固まりながら、中の熱い部分が少しずつ前へ進みます。"
               "大量の溶岩が続けて流れこむと、浅い海峡でも先端が海底にたまって積み重なり、やがて海面より高くなって"
               "海をふさぎます。大正噴火では、このようにして幅300〜400m・深さ70〜80mの海峡が埋まりました。"),
    sources=[("内閣府 防災「日本の火山 桜島」", "https://www.bousai.go.jp/kohou/kouhoubousai/h20/05/volcano.html"),
             ("鹿児島県「大正噴火100周年記念誌」", "https://www.pref.kagoshima.jp/aj01/bosai/sonae/sakura100/documents/38032_20140320114753-1.pdf"),
             ("鹿児島市（桜島の火山防災）", "https://www.city.kagoshima.lg.jp/kikikanri/kurashi/bosai/bosai/sakurajima/documents/02kyozaip2.pdf")],
    tags=["桜島", "さくらじま", "大正噴火", "大正大噴火", "溶岩", "陸続き", "瀬戸海峡", "大隅半島", "鹿児島", "鹿児島県",
          "火山", "絶景", "ふしぎな絶景", "地学", "科学", "航空写真", "shorts"],
    hashtags=["#絶景", "#科学", "#桜島", "#火山", "#shorts"],
    pinned="大正噴火では対岸の鹿児島市でも大きな地震の被害がありました。次はどこのふしぎな絶景が見たい？",
    notes=["噴火前の地図は大日本帝国陸軍参謀本部陸地測量部の地図（パブリックドメイン、Wikimedia Commons）。噴火中の写真は鹿児島県の記録写真（パブリックドメイン）。",
           "つながった場所は、地理院地図で大正溶岩の範囲と大隅半島が接する所（国道224号と220号の合流付近）に合わせた。",
           "「17日」は内閣府の「1月12日に噴火開始、1月29日に瀬戸海峡を閉塞」から計算。",
           "「幅400メートル」は鹿児島県の「幅300〜400m」の大きい方。説明欄では幅を正確に書いた。",
           "光る溶岩の流れは、東の山腹から瀬戸までの目安の道すじ。実際の溶岩流の形とはちがう。地質図は大正溶岩だけを分けていないので使っていない。",
           "今の噴火警戒レベルは変わるため、動画ではふれていない。"],
)
