"""ふしぎな絶景の科学 阿蘇カルデラ（30秒・全画面の型）

旧版（travel_shorts/aso/）と「視聴を継続」の割合を比べるための新しい型。
- 25〜35秒、驚き1つ＋理由1つ
- 1秒目から全画面の本物の航空写真、題名の帯なし、最後は冒頭の絵に戻ってループ
事実の根拠は旧版と同じ（熊本県・国土交通省・産総研・内閣府）。
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

import longform as L

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
import gsi_tiles as G  # noqa: E402

FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 170, 90)
PLACE = dict(name="阿蘇カルデラ", pref="熊本県", lat=32.957, lon=131.074)
MAP_CREDITS = ["航空写真・陰影起伏: 出典 国土地理院（地理院タイルを加工して作成）",
               "地質図: 出典 産総研地質調査総合センター 20万分の1日本シームレス地質図V2（CC BY 4.0、大規模火砕流の範囲を抽出して加工）"]

SW, SH = 1080, 1920
_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "aso", "maps")
GOLD, LAVA = (255, 214, 120), (255, 120, 60)

# ---- カルデラ（ズーム12の航空写真×陰影起伏、縦長に切り出し） ----
_P = Image.open(os.path.join(_M, "photo_z12.jpg")).convert("RGB")
_H = Image.open(os.path.join(_M, "hill_z12.png")).convert("RGB")
_CAL = ImageChops.multiply(_P, Image.blend(_H, Image.new("RGB", _H.size, "white"), 0.4))
CX, CY = G.to_px(32.957, 131.074, 12, (3536, 1647))
CX -= 65  # 航空写真の外輪山に合わせて西へ寄せる
_MPX = 156543.03 * math.cos(math.radians(32.957)) / 2 ** 12
RX, RY = 9000 / _MPX, 12500 / _MPX


def _view(scale):
    """カルデラ中心の縦長（9:16）の範囲を切り出して全画面に。scale が小さいほど寄る"""
    w, h = 900 * scale, 1600 * scale
    box = (CX - w / 2, CY - h / 2 + 60 * scale, CX + w / 2, CY + h / 2 + 60 * scale)
    return box, _CAL.crop(tuple(int(v) for v in box)).resize((SW, SH), Image.BILINEAR)


def _to_screen(box, x, y):
    return (x - box[0]) * SW / (box[2] - box[0]), (y - box[1]) * SH / (box[3] - box[1])


def _glow(base, lay, blur=8):
    return ImageChops.add(ImageChops.add(base, lay.filter(ImageFilter.GaussianBlur(blur))), lay)


def hook(t, lt):
    """本物の航空写真でカルデラにゆっくり寄っていく"""
    _, im = _view(1.05 - 0.15 * min(1, lt / 4))
    return im


def rim(t, lt):
    box, base = _view(0.9)
    lay = Image.new("RGB", (SW, SH))
    d = ImageDraw.Draw(lay)
    k = min(1.0, lt / 2.0)
    pts = [_to_screen(box, CX + RX * math.cos(a), CY + RY * math.sin(a))
           for a in np.linspace(-math.pi / 2, -math.pi / 2 + 2 * math.pi * k, 120)]
    d.line(pts, fill=GOLD, width=9, joint="curve")
    hx, hy = pts[-1]
    d.ellipse((hx - 14, hy - 14, hx + 14, hy + 14), fill=(255, 255, 255))
    return _glow(base, lay)


def sink(t, lt):
    box, base = _view(0.9)
    m = Image.new("L", (SW, SH))
    (x0, y0), (x1, y1) = _to_screen(box, CX - RX, CY - RY), _to_screen(box, CX + RX, CY + RY)
    ImageDraw.Draw(m).ellipse((x0, y0, x1, y1), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(40))
    k = min(1.0, lt / 2.5)
    im = Image.composite(ImageEnhance.Brightness(base).enhance(1 - 0.5 * k), base, m)
    lay = Image.new("RGB", (SW, SH))
    ImageDraw.Draw(lay).ellipse((x0, y0, x1, y1), outline=LAVA, width=8)
    return _glow(im, ImageEnhance.Brightness(lay).enhance(0.7 + 0.3 * math.sin(t * 3)), 14)


# ---- 九州（ズーム9）：火砕流の地層が阿蘇から広がる ----
_P9 = Image.open(os.path.join(_M, "photo_z9.jpg")).convert("RGB")
_G9 = np.array(Image.open(os.path.join(_M, "geo_z9.png")).convert("RGB")).astype(int)
AX, AY = G.to_px(32.957, 131.074, 9, (440, 204))
_MASK = np.zeros(_G9.shape[:2], bool)
for c in ((255, 208, 215), (255, 217, 210), (255, 226, 205), (227, 181, 156)):
    _MASK |= (abs(_G9[:, :, 0] - c[0]) < 10) & (abs(_G9[:, :, 1] - c[1]) < 10) & (abs(_G9[:, :, 2] - c[2]) < 10)
_YY, _XX = np.mgrid[0:_G9.shape[0], 0:_G9.shape[1]]
_R = np.hypot(_XX - AX, _YY - AY)
_KM = 156543.03 * math.cos(math.radians(32.957)) / 2 ** 9 / 1000
_MASK &= _R * _KM < 190
YAMA = G.to_px(34.15, 131.55, 9, (440, 204))
BOX9 = (AX - 340, AY - 625, AX + 340, AY + 584)  # 縦長：阿蘇から山口県まで入る範囲


def spread(t, lt):
    base = ImageEnhance.Brightness(ImageEnhance.Color(_P9).enhance(0.7)).enhance(0.55)
    k = min(1.0, lt / 3.5)
    reach = 190 / _KM * k
    lay = np.zeros(_G9.shape, np.uint8)
    lay[_MASK & (_R < reach)] = LAVA
    im = _glow(base, Image.fromarray(lay), 5)
    d = ImageDraw.Draw(im)
    d.ellipse((AX - reach, AY - reach, AX + reach, AY + reach), outline=GOLD, width=3)
    d.ellipse((AX - 9, AY - 9, AX + 9, AY + 9), fill=(255, 255, 255))
    im = im.crop(tuple(int(v) for v in BOX9)).resize((SW, SH), Image.BILINEAR).convert("RGBA")
    d = ImageDraw.Draw(im)
    sx = lambda x, y: ((x - BOX9[0]) * SW / (BOX9[2] - BOX9[0]), (y - BOX9[1]) * SH / (BOX9[3] - BOX9[1]))  # noqa: E731
    ax, ay = sx(AX, AY)
    d.text((ax + 80, ay + 10), "阿蘇", font=L.jp(52, True), fill=L.WHITE, anchor="mm", stroke_width=6, stroke_fill=L.NAVY)
    if k > 0.6:
        yx, yy = sx(*YAMA)
        d.text((yx, yy), "山口県", font=L.jp(52, True), fill=GOLD, anchor="mm", stroke_width=6, stroke_fill=L.NAVY)
    return im


FIGS = {"hook": hook, "rim": rim, "spread": spread, "sink": sink}

SCENES = [
    dict(spk="Z", ex="panic", say="この丸いくぼ地、ぜんぶ火山なのだ！？",
         read="この、まるい、くぼち、ぜんぶ、火山なのだ！？",
         head="この穴\nぜんぶ火山！？", show=("fig", "hook")),
    dict(spk="M", say="熊本の阿蘇カルデラ。南北25キロもある、巨大なくぼ地よ。",
         read="くまもとの、あそカルデラ。なんぼく、にじゅうごキロもある、きょだいな、くぼちよ。",
         head="南北25km", show=("fig", "rim")),
    dict(spk="M", say="9万年前の大噴火では、火砕流が山口県まで届いたの。",
         read="きゅうまんねん前の、だいふんかでは、かさいりゅうが、やまぐちけんまで、とどいたの。",
         head="火砕流が\n山口県まで", show=("fig", "spread")),
    dict(spk="M", say="マグマが一気に抜けて、地面が落ちこんでできたのよ。",
         read="マグマが、いっきに抜けて、地面が、落ちこんで、できたのよ。",
         head="地面が\n落ちこんだ", show=("fig", "sink")),
    dict(spk="Z", say="その穴の中に、町があるのだ！",
         read="その、あなの中に、まちが、あるのだ！",
         head="穴の中に町！", show=("fig", "hook")),
]

META = dict(
    title="この丸い穴、ぜんぶ火山！？阿蘇カルデラ #shorts #絶景 #科学",
    alt_titles=["9万年前の大噴火は山口まで届いた！ #shorts #阿蘇", "穴の中に町がある！？阿蘇カルデラ #shorts #火山"],
    lead="熊本県の阿蘇には、南北約25km・東西約18kmの巨大なくぼ地「カルデラ」があり、その中に町や田んぼが広がっています。",
    points=["約27万〜9万年前に4回の大噴火があり、最後の「阿蘇4」の火砕流は山口県中部（約170km）まで届いた",
            "地下のマグマが一度に大量に出たため、支えを失った地面が落ちこんでカルデラができた"],
    principle=("地下のマグマだまりのマグマが大噴火で一度に大量に噴き出すと、その上の地面は支えを失って落ちこみ、"
               "大きなくぼ地（カルデラ）になります。噴火で起きる火砕流は、高温のガスと火山灰・軽石がまざって地面をはうように"
               "高速で流れるもので、阿蘇4噴火の火砕流は山口県まで届きました。"),
    sources=[("熊本県（阿蘇カルデラの大きさ・面積）", "https://www.pref.kumamoto.jp/uploaded/attachment/24429.pdf"),
             ("国土交通省 観光庁 多言語解説（阿蘇カルデラの形成史）", "https://www.mlit.go.jp/tagengo-db/common/001555893.pdf"),
             ("産総研 地質調査総合センター（阿蘇4火砕流堆積物分布図）", "https://www.gsj.jp/data/gcn/gsj_cn_vol13.no4_p63-68.pdf"),
             ("内閣府 防災「日本の火山 阿蘇山」", "https://www.bousai.go.jp/kohou/kouhoubousai/h21/03/volcano.html")],
    tags=["阿蘇", "阿蘇山", "阿蘇カルデラ", "カルデラ", "火砕流", "阿蘇4", "大噴火", "外輪山", "熊本県", "九州", "火山",
          "絶景", "ふしぎな絶景", "地学", "科学", "航空写真", "shorts"],
    hashtags=["#絶景", "#科学", "#阿蘇", "#火山", "#shorts"],
    pinned="この火砕流は、山口県の秋吉台にも地層を残しています。次はどこのふしぎな絶景が見たい？",
    notes=["30秒・全画面の型の試作。旧版（46秒）と「視聴を継続」の割合を比べる。",
           "九州の地図で光る範囲は、地質図の「大規模火砕流」の地層のうち阿蘇から190km以内の部分（目安）。",
           "カルデラのふちの光る線は、東西18km・南北25kmのだ円で示した目安。"],
)
