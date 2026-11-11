"""ふしぎな絶景の科学 #4 阿蘇のカルデラ（熊本県）

事実の根拠:
- カルデラは東西約18km・南北約25km、面積約380km² … 熊本県
- 約27万〜9万年前の4回の大噴火でできた（最後が約9万年前の「阿蘇4」） … 国土交通省（多言語解説）
- 阿蘇4火砕流は熊本・大分・佐賀・福岡のほぼ全域と、長崎・宮崎・山口の一部に分布。北東へ約170kmの山口県中部まで … 産総研
- 火砕流の堆積物は天草や山口県秋吉台でも見られ、火山灰は北海道東部で厚さ10cm以上 … 内閣府 防災
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

import longform as L

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
import gsi_tiles as G  # noqa: E402

TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 170, 90)
PLACE = dict(name="阿蘇カルデラ", pref="熊本県", lat=32.94, lon=131.06)
MAP_CREDITS = ["航空写真・陰影起伏: 出典 国土地理院（地理院タイルを加工して作成）",
               "地質図: 出典 産総研地質調査総合センター 20万分の1日本シームレス地質図V2（CC BY 4.0、大規模火砕流の範囲を抽出して加工）"]

_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
GOLD, LAVA = (255, 214, 120), (255, 120, 60)


def _label(d, xy, s, size=34, fill=L.WHITE):
    d.text(xy, s, font=L.jp(size, True), fill=fill, anchor="mm", stroke_width=5,
           stroke_fill=L.WHITE if fill == L.NAVY else L.NAVY)


def _credit(im, text="出典：国土地理院"):
    ImageDraw.Draw(im).text((im.width - 12, im.height - 14), text, font=L.jp(20, True), fill=(220, 230, 240), anchor="rm")
    return im


# ---- カルデラ（ズーム11の航空写真×陰影起伏） ----
_P11 = Image.open(os.path.join(_M, "photo_z11.jpg")).convert("RGB")
_H11 = Image.open(os.path.join(_M, "hill_z11.png")).convert("RGB")
_CAL = ImageChops.multiply(_P11, Image.blend(_H11, Image.new("RGB", _H11.size, "white"), 0.4))
CX, CY = G.to_px(32.957, 131.074, 11, (1767, 823))  # カルデラの中心付近（航空写真で合わせた）
_MPX = 156543.03 * math.cos(math.radians(32.94)) / 2 ** 11  # 1pxあたりのm
RX, RY = 9000 / _MPX, 12500 / _MPX  # 東西18km・南北25kmの半分
CROP11 = (int(CX - 450), int(CY - 450), int(CX + 450), int(CY + 450))


def _ellipse_pts(n=180, s=1.0):
    return [(CX + RX * s * math.cos(2 * math.pi * i / n) - CROP11[0], CY + RY * s * math.sin(2 * math.pi * i / n) - CROP11[1])
            for i in range(n + 1)]


def rim(t, lt):
    """カルデラのふちを光の線で1周なぞる"""
    base = _CAL.crop(CROP11)
    glow = Image.new("RGB", base.size)
    d = ImageDraw.Draw(glow)
    pts = _ellipse_pts()
    k = min(1.0, lt / 2.5)
    n = max(2, int(len(pts) * k))
    d.line(pts[:n], fill=GOLD, width=6, joint="curve")
    hx, hy = pts[n - 1]
    d.ellipse((hx - 10, hy - 10, hx + 10, hy + 10), fill=(255, 255, 255))
    im = ImageChops.add(ImageChops.add(base, glow.filter(ImageFilter.GaussianBlur(8))), glow).convert("RGBA")
    dd = ImageDraw.Draw(im)
    if k >= 1:
        _label(dd, (450, 450 - RY - 30), "南北 約25km", 32, GOLD)
        _label(dd, (450 + RX + 20, 450), "東西\n約18km", 30, GOLD)
    return _credit(im)


def sink(t, lt):
    """地下のマグマが一度に大量に出て、真ん中が落ちこんだ：カルデラの内側をゆっくり暗く沈ませる"""
    base = _CAL.crop(CROP11)
    m = Image.new("L", base.size)
    ImageDraw.Draw(m).ellipse((CX - RX - CROP11[0], CY - RY - CROP11[1], CX + RX - CROP11[0], CY + RY - CROP11[1]), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(30))
    k = min(1.0, lt / 3.0)
    dark = ImageEnhance.Brightness(base).enhance(1 - 0.45 * k)
    im = Image.composite(dark, base, m)
    glow = Image.new("RGB", base.size)
    ImageDraw.Draw(glow).line(_ellipse_pts(), fill=LAVA, width=5)
    a = 0.5 + 0.5 * math.sin(t * 3)
    im = ImageChops.add(im, ImageEnhance.Brightness(glow.filter(ImageFilter.GaussianBlur(10))).enhance(0.6 + 0.4 * a)).convert("RGBA")
    d = ImageDraw.Draw(im)
    _label(d, (450, 70), "地下のマグマが一気に出て", 32, GOLD)
    _label(d, (450, 120), "真ん中が落ちこんだ ↓", 32, GOLD)
    return _credit(im)


# ---- 九州全体（ズーム8）：大規模火砕流の地層が阿蘇から広がる ----
_P8 = Image.open(os.path.join(_M, "photo_z8.jpg")).convert("RGB")
_G8 = np.array(Image.open(os.path.join(_M, "geo_z8.png")).convert("RGB")).astype(int)
AX, AY = G.to_px(32.94, 131.06, 8, (220, 102))
_MASK = np.zeros(_G8.shape[:2], bool)
for c in ((255, 208, 215), (255, 217, 210), (255, 226, 205), (227, 181, 156)):  # 地質図の「大規模火砕流」の色
    _MASK |= (abs(_G8[:, :, 0] - c[0]) < 10) & (abs(_G8[:, :, 1] - c[1]) < 10) & (abs(_G8[:, :, 2] - c[2]) < 10)
_YY, _XX = np.mgrid[0:_G8.shape[0], 0:_G8.shape[1]]
_R = np.hypot(_XX - AX, _YY - AY)
_KM = 156543.03 * math.cos(math.radians(32.94)) / 2 ** 8 / 1000  # 1pxあたりのkm
_MASK &= _R * _KM < 190  # 阿蘇から190km以内（南九州の別の火山の地層は外す）
YAMA = G.to_px(34.15, 131.55, 8, (220, 102))  # 山口県中部の目安
CROP8 = (int(AX - 360), int(AY - 380), int(AX + 360), int(AY + 340))


def spread(t, lt):
    """火砕流の地層の範囲を、阿蘇から外へ向かって光らせていく"""
    base = ImageEnhance.Brightness(ImageEnhance.Color(_P8).enhance(0.7)).enhance(0.6)
    k = min(1.0, lt / 4.0)
    reach = 190 / _KM * k
    show = _MASK & (_R < reach)
    lay = np.zeros(_G8.shape, np.uint8)
    lay[show] = LAVA
    li = Image.fromarray(lay)
    im = ImageChops.add(ImageChops.add(base, li.filter(ImageFilter.GaussianBlur(4))), ImageEnhance.Brightness(li).enhance(0.6))
    d = ImageDraw.Draw(im)
    rr = reach
    d.ellipse((AX - rr, AY - rr, AX + rr, AY + rr), outline=GOLD, width=3)
    im = im.crop(CROP8).convert("RGBA")
    d = ImageDraw.Draw(im)
    ax, ay = AX - CROP8[0], AY - CROP8[1]
    d.ellipse((ax - 12, ay - 12, ax + 12, ay + 12), fill=(255, 255, 255))
    _label(d, (ax + 70, ay + 30), "阿蘇", 32)
    if k >= 0.9:
        _label(d, (YAMA[0] - CROP8[0], YAMA[1] - CROP8[1] - 10), "山口県まで 約170km", 30, GOLD)
    _label(d, (360, 40), "約9万年前の大噴火の火砕流", 32, GOLD)
    return _credit(im, "出典：国土地理院／産総研（シームレス地質図V2）を加工")


def aerial(t, lt, zoom_in=True):
    """上空から見たカルデラ（本物の航空写真）をゆっくりズーム"""
    k = min(1.0, lt / 6.0)
    z = (0.95 - 0.25 * k) if zoom_in else (0.7 + 0.25 * k)
    w = 900 * z
    box = (int(CX - w / 2), int(CY - w / 2), int(CX + w / 2), int(CY + w / 2))
    im = _CAL.crop(box).resize((900, 900), Image.BILINEAR).convert("RGBA")
    return _credit(im)


def hook(t, lt):
    return aerial(t, lt, True)


def ending(t, lt):
    return aerial(t, lt, False)


FIGS = {"hook": hook, "ending": ending, "rim": rim, "sink": sink, "spread": spread}

SCENES = [
    dict(spk="Z", ex="panic", say="この広い平野、全部が火山の穴の中なのだ！？",
         read="この、ひろい、へいや、全部が、火山の穴の中なのだ！？",
         head="全部\n火山の穴の中！？", show=("fig", "hook"), head_y=1285),
    dict(spk="M", say="熊本県の阿蘇。上から見ると、山がぐるりと輪になっているの。",
         read="くまもとけんの、あそ。上から見ると、山が、ぐるりと、輪になっているの。",
         head="阿蘇", show=("zoom",), head_y=1340),
    dict(spk="M", say="これがカルデラ。南北約25キロ、東西約18キロの、巨大なくぼ地なのよ。",
         read="これが、カルデラ。なんぼく、やく、にじゅうごキロ、とうざい、やく、じゅうはちキロの、巨大な、くぼちなのよ。",
         head="巨大なくぼ地\n＝カルデラ", show=("fig", "rim"), head_y=1285),
    dict(spk="M", say="約27万年前から9万年前に、4回の大噴火があったの。最後の噴火の火砕流は、九州の広い範囲から、山口県まで届いたわ。",
         read="やく、にじゅうななまんねん前から、きゅうまんねん前に、よんかいの、だいふんかが、あったの。最後の噴火の、かさいりゅうは、きゅうしゅうの広い範囲から、やまぐちけんまで、とどいたわ。",
         head="① 4回の\n大噴火", sub="火砕流＝熱いガスと火山灰の流れ", show=("fig", "spread"), head_y=1200),
    dict(spk="M", say="地下のマグマが一気に出たので、支えを失った地面が落ちこんで、このくぼ地ができたのよ。",
         read="地下の、マグマが、いっきに出たので、ささえを失った地面が、落ちこんで、この、くぼちが、できたのよ。",
         head="② 支えを失って\n落ちこんだ", show=("fig", "sink"), head_y=1285),
    dict(spk="Z", say="その中に町や田んぼがあって、人が暮らしているのだ！行ってみたいのだ？",
         read="その中に、町や田んぼがあって、人が暮らしているのだ！行ってみたいのだ？",
         head="行ってみたい？", show=("fig", "ending"), head_y=1285),
]

META = dict(
    title="この平野ぜんぶ火山の穴の中！阿蘇カルデラのでき方 #shorts #絶景 #科学",
    alt_titles=["9万年前の大噴火が九州をおおった！阿蘇カルデラ #shorts #火山",
                "山口県まで届いた火砕流！阿蘇の巨大くぼ地のひみつ #shorts #科学 #熊本"],
    lead="熊本県の阿蘇には、東西約18km・南北約25kmの巨大なくぼ地「カルデラ」があります。その中に町や田んぼが広がり、人が暮らしています。",
    points=["カルデラは東西約18km・南北約25km、面積約380km²",
            "① 約27万〜9万年前に4回の大噴火があった。最後の「阿蘇4」の火砕流は、九州の広い範囲から山口県中部（約170km）まで届いた",
            "② 地下のマグマが一度に大量に出たため、支えを失った地面が落ちこんでカルデラができた",
            "火山灰は北海道東部でも厚さ10cm以上の地層として見つかっている"],
    principle=("地下のマグマだまりにたまったマグマが大噴火で一度に大量に噴き出すと、マグマが占めていた空間の上の地面は"
               "支えを失って落ちこみます。こうしてできる大きなくぼ地がカルデラです。噴火では、高温の火山ガスと火山灰・軽石が"
               "まざって地面をはうように高速で流れる「火砕流」が発生し、阿蘇4噴火の火砕流は海をこえて山口県まで届きました。"),
    sources=[("熊本県（阿蘇カルデラの大きさ・面積）", "https://www.pref.kumamoto.jp/uploaded/attachment/24429.pdf"),
             ("国土交通省 観光庁 多言語解説（阿蘇カルデラの形成史）", "https://www.mlit.go.jp/tagengo-db/common/001555893.pdf"),
             ("産総研 地質調査総合センター（阿蘇4火砕流堆積物分布図）", "https://www.gsj.jp/data/gcn/gsj_cn_vol13.no4_p63-68.pdf"),
             ("内閣府 防災「日本の火山 阿蘇山」", "https://www.bousai.go.jp/kohou/kouhoubousai/h21/03/volcano.html")],
    tags=["阿蘇", "阿蘇山", "阿蘇カルデラ", "カルデラ", "火砕流", "阿蘇4", "大噴火", "外輪山", "大観峰", "熊本県",
          "九州", "火山", "絶景", "ふしぎな絶景", "地学", "科学", "観光", "航空写真", "shorts"],
    hashtags=["#絶景", "#科学", "#阿蘇", "#火山", "#shorts"],
    pinned="阿蘇4噴火の火砕流は、前に紹介した秋吉台にも地層を残しています。次はどこのふしぎな絶景が見たい？コメントで教えてください！",
    notes=["九州の地図で光る範囲は、シームレス地質図の「大規模火砕流」の地層のうち阿蘇から190km以内の部分。阿蘇以外の火山の火砕流の地層もふくむ可能性があり、目安として表示。",
           "カルデラのふちの光る線は、東西18km・南北25kmのだ円で示した目安で、実際の外輪山のふちの形とは少しちがう。",
           "カルデラの中で暮らす人の数は、確かな数字を確認できなかったので言っていない。",
           "阿蘇山（中岳）の今の噴火警戒レベルは変わるため、動画ではふれていない。訪れる前は気象庁の発表を確認すること。"],
)
