"""ふしぎな絶景の科学 大涌谷の黒たまご（30秒・全画面型・立体地形）

事実の根拠:
- 約80度の温泉池で生卵をゆでると、気泡（小さな穴）の多い殻に温泉の成分の鉄分がつき、そこへ硫化水素が反応して黒くなる
  … ANA Japan Travel Planner（大涌谷）
- 鉄が硫化水素と反応して黒い硫化鉄になる … ウェザーニュース
- 箱根山の水蒸気噴火は過去約3500年間に5回以上あり、確認された5回はすべて大涌谷周辺が火口 … 神奈川県
- 2015年に大涌谷で小規模な水蒸気噴火があった … nippon.com ほか
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
import terrain3d as T3  # noqa: E402

FULL = True
PHOTO_FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 210, 90)
PLACE = dict(name="大涌谷", pref="神奈川県箱根町", lat=35.2427, lon=139.0197)
MAP_CREDITS = ["立体地形: 出典 国土地理院（標高タイル・航空写真を加工して作成）"]

SW, SH = 1080, 1920
_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
_DEM = np.load(os.path.join(_M, "dem_z14.npy"))
for _ in range(20):
    _n = np.isnan(_DEM)
    if not _n.any():
        break
    _p = np.pad(_DEM, 1, mode="edge")
    _DEM[_n] = np.nanmean(np.stack([_p[:-2, 1:-1], _p[2:, 1:-1], _p[1:-1, :-2], _p[1:-1, 2:]]), 0)[_n]
_TEX = np.array(Image.open(os.path.join(_M, "photo_z14.jpg")).convert("RGB"))
_MPP = 156543.03 * math.cos(math.radians(35.24)) / 2 ** 14
OWK = (1009, 810)
_MARK = np.zeros_like(_TEX)
yy, xx = np.ogrid[:_TEX.shape[0], :_TEX.shape[1]]
_MARK[(xx - OWK[0]) ** 2 + (yy - OWK[1]) ** 2 < 10 ** 2] = 255
_ZERO = np.zeros_like(_TEX)
GOLD = (255, 214, 120)
_R = __import__("random").Random(5)
_STEAM = [(_R.random(), _R.uniform(-1, 1), _R.uniform(0.6, 1.4)) for _ in range(120)]


def _r(target, az, el, dist, tex=_TEX):
    return T3.render(_DEM, tex, _MPP, target, az=az, el=el, dist=dist, exag=1.0, size=(540, 960),
                     fill_gaps=True).resize((SW, SH), Image.BICUBIC)


def _spot(target, args):
    m = np.array(_r(target, tex=_MARK, **args).convert("L")).astype(int) - np.array(_r(target, tex=_ZERO, **args).convert("L")).astype(int)
    ys, xs = np.nonzero(m > 100)
    return (xs.mean(), ys.mean()) if len(xs) else None


def hakone(t, lt):
    """箱根の山を回りこみながら、大涌谷に寄って光の輪"""
    k = min(1.0, lt / 5.0)
    k = 0.5 - 0.5 * math.cos(math.pi * k)
    args = dict(az=195 + 10 * k, el=24 + 4 * k, dist=8000 - 3500 * k)
    im = _r(OWK, **args)
    p = _spot(OWK, args)
    if p:
        lay = Image.new("RGB", (SW, SH))
        d = ImageDraw.Draw(lay)
        for i in range(3):
            ph = (t * 0.7 + i / 3) % 1
            r = 20 + 140 * ph
            d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), outline=tuple(int(v * (1 - ph) * k) for v in GOLD), width=7)
        im = ImageChops.add(ImageChops.add(im, lay.filter(ImageFilter.GaussianBlur(8))), lay)
    return im


def steam(t, lt):
    """大涌谷から白い噴気が立ちのぼる（演出）"""
    args = dict(az=205, el=28, dist=4500)
    im = _r(OWK, **args)
    p = _spot(OWK, args) or (SW / 2, SH / 2)
    lay = Image.new("RGB", (SW, SH))
    d = ImageDraw.Draw(lay)
    for off, sx, sp in _STEAM:
        ph = (t * 0.25 * sp + off) % 1
        x = p[0] + sx * 80 + ph * 160
        y = p[1] - ph * 700
        r = 10 + 70 * ph
        c = int(150 * (1 - ph))
        d.ellipse((x - r, y - r, x + r, y + r), fill=(c, c, c))
    return ImageChops.add(im, lay.filter(ImageFilter.GaussianBlur(18)))


FIGS = {"hakone": hakone, "steam": steam}

EGG = "Black_egg___Owakudani___Hakone__10621176696_.jpg"
SCENES = [
    dict(spk="Z", ex="panic", say="ゆでたら、卵が真っ黒になったのだ！",
         read="ゆでたら、たまごが、まっくろに、なったのだ！",
         head="ゆでたら\n真っ黒！？", show=("photo", EGG, "in"), head_y=560),
    dict(spk="M", say="箱根の大涌谷の名物、黒たまご。ここは、今も火山ガスが噴き出す谷なの。",
         read="ハコネの、おおわくだにの、めいぶつ、くろたまご。ここは、いまも、かざんガスが、ふきだす、たになの。",
         head="大涌谷の\n黒たまご", show=("photo", "A_view_of_Owakudani_-_a_volcanic_valley_with_active_sulphur_vents_and_hot_springs_in_Hakone__Japan.jpg", "right")),
    dict(spk="M", say="箱根火山の中にあって、2015年にも小さな噴火が起きた場所なのよ。",
         read="ハコネかざんの、なかに、あって、にせんじゅうごねんにも、ちいさな、ふんかが、おきた、ばしょなのよ。",
         head="今も生きている\n火山", show=("fig", "hakone")),
    dict(spk="M", say="卵を温泉の池でゆでると、殻の小さな穴に、温泉の鉄分がくっつくの。",
         read="たまごを、おんせんの、いけで、ゆでると、からの、ちいさな、あなに、おんせんの、てつぶんが、くっつくの。",
         head="殻の穴に\n鉄分がつく", show=("photo", "Owakudani__Hakone_July_2018.jpg", "in")),
    dict(spk="M", say="そこへ火山ガスの硫化水素が反応して、黒い硫化鉄に変わるのよ。",
         read="そこへ、かざんガスの、りゅうかすいそが、はんのうして、くろい、りゅうかてつに、かわるのよ。",
         head="鉄＋硫化水素\n→黒い硫化鉄", show=("fig", "steam")),
    dict(spk="M", say="だから黒いのは殻だけ。中は、ふつうのゆで卵なの。",
         read="だから、くろいのは、からだけ。なかは、ふつうの、ゆでたまごなの。",
         head="黒いのは\n殻だけ", show=("photo", "Hakone_black_egg_dsc05310.jpg", "in")),
    dict(spk="Z", say="火山が黒くそめた卵だったのだ！",
         read="かざんが、くろく、そめた、たまごだったのだ！",
         head="火山が\nそめた卵！", show=("photo", EGG, "out")),
]

META = dict(
    title="ゆでたら真っ黒！？大涌谷の黒たまごは火山がそめた #shorts #箱根 #科学",
    alt_titles=["卵が黒くなる谷 大涌谷のひみつ #shorts #箱根", "黒たまごはなぜ黒い？ #shorts #科学 #火山"],
    lead="神奈川県箱根町の大涌谷では、温泉の池でゆでた卵の殻が真っ黒になります。今も火山ガスが噴き出す、箱根火山の谷です。",
    points=["約80度の温泉池でゆでると、小さな穴の多い殻に温泉の鉄分がつく",
            "そこへ火山ガスの硫化水素が反応して、黒い硫化鉄になる（黒いのは殻だけ）",
            "箱根山の水蒸気噴火は過去約3500年に5回以上あり、確認された5回はすべて大涌谷のまわりが火口。2015年にも小さな噴火があった"],
    principle=("卵の殻は炭酸カルシウムでできていて、目に見えない小さな穴がたくさんあいています。大涌谷の温泉の池には、地下からとけ出した"
               "鉄などの成分がふくまれていて、ゆでている間に殻の穴やすき間にくっつきます。そこへ、火山ガスにふくまれる硫化水素が反応すると、"
               "鉄と硫黄が結びついた黒い「硫化鉄」ができ、殻が黒く色づきます。地下のマグマに温められた水や火山ガスが地表に出てくる"
               "場所だからこそ起きる、火山の化学反応です。"),
    sources=[("ANA Japan Travel Planner（大涌谷・黒たまご）", "https://www.ana.co.jp/ja/jp/japan-travel-planner/kanagawa/0000003.html"),
             ("ウェザーニュース（黒たまごが黒くなるしくみ）", "https://weathernews.jp/soramagazine/201707/05/"),
             ("大涌谷くろたまご館（白身の黒い点の説明）", "https://owakudani.com/2025/09/28/blackegg_20250928"),
             ("神奈川県（箱根山の火山砂防計画）", "https://www.pref.kanagawa.jp/documents/95886/02_saboukeikaku_yosoukuikizu_1.pdf"),
             ("nippon.com（箱根・大涌谷）", "https://www.nippon.com/ja/guide-to-japan/gu900158/")],
    tags=["大涌谷", "黒たまご", "くろたまご", "箱根", "箱根山", "火山", "硫化水素", "硫化鉄", "温泉", "化学反応",
          "神奈川県", "箱根町", "絶景", "ふしぎな絶景", "化学", "科学", "shorts"],
    hashtags=["#箱根", "#絶景", "#科学", "#黒たまご", "#shorts"],
    pinned="大涌谷は火山ガスの状況で立ち入りが規制されることがあります。行く前に箱根町の情報を確認してね。次はどこのふしぎな絶景が見たい？",
    notes=["黒くなるしくみ（鉄分＋硫化水素→硫化鉄）は観光案内と気象情報サイトの説明。公的機関の解説は見つからなかったので、出典にそのことがわかるよう名前を書いた。",
           "白い噴気の粒は、大涌谷から噴気が立ちのぼるようすを表した演出。",
           "立体地形は、国土地理院の標高タイルに航空写真を貼って描いたもの（高さは強調していない）。",
           "「中はふつうのゆで卵」は、黒いのが殻の表面だけという説明にもとづく。白身に黒い点が出ることがあるが、食べても問題ないと大涌谷くろたまご館が案内している。"],
)
