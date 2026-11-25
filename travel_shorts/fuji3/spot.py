"""ふしぎな絶景の科学 富士山は火山の重ね着（30秒・全画面・写真は全画面型）

事実の根拠:
- 富士山は小御岳・古富士の両火山の上にできた成層火山（体積約400km³は小御岳・古富士・新富士を含む） … 気象庁
- 富士山は小御岳火山のふもとに約10万年前に誕生し、古富士火山・新富士火山の2世代の噴火で今の円錐形になった … 静岡県
- 今の山体は小御岳・古富士の上にできた新富士火山 … 内閣府 防災
- 富士スバルライン五合目の小御嶽神社がある平らな台地は、小御岳火山の山頂部。ほとんどは富士山の溶岩におおわれた
  … 国土交通省 観光庁 多言語解説（Komitake-Jinja Shrine）
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
ACCENT = (255, 200, 110)
PLACE = dict(name="富士山", pref="静岡県・山梨県", lat=35.3606, lon=138.7274)
MAP_CREDITS = ["立体地形: 出典 国土地理院（標高タイル・航空写真を加工して作成）"]

SW, SH = 1080, 1920
_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hoei", "maps")
_DEM = np.load(os.path.join(_M, "dem_z13.npy"))
for _ in range(20):  # 標高の欠け（NaN）をまわりの値でうめる（白い線のノイズ対策）
    _n = np.isnan(_DEM)
    if not _n.any():
        break
    _p = np.pad(_DEM, 1, mode="edge")
    _nb = np.stack([_p[:-2, 1:-1], _p[2:, 1:-1], _p[1:-1, :-2], _p[1:-1, 2:]])
    _DEM[_n] = np.nanmean(_nb, 0)[_n]
_TEX = np.array(Image.open(os.path.join(_M, "photo_z13.jpg")).convert("RGB"))
_MPP = 156543.03 * math.cos(math.radians(35.35)) / 2 ** 13
SUMMIT = (977.7, 971.3)
KOMI = (1010, 723)  # 小御嶽神社（富士スバルライン五合目）
_MARK = np.zeros_like(_TEX)
yy, xx = np.ogrid[:_TEX.shape[0], :_TEX.shape[1]]
_MARK[(xx - KOMI[0]) ** 2 + (yy - KOMI[1]) ** 2 < 14 ** 2] = 255
_ZERO = np.zeros_like(_TEX)
GOLD = (255, 214, 120)


def _r(target, az, el, dist, tex=_TEX):
    return T3.render(_DEM, tex, _MPP, target, az=az, el=el, dist=dist, exag=1.0, size=(540, 960), fill_gaps=True).resize((SW, SH), Image.BICUBIC)


def orbit(t, lt):
    """北からゆっくり回りこむ"""
    return _r(SUMMIT, az=165 + 4 * lt, el=14, dist=12500 - 200 * lt)


def komi(t, lt):
    """北側の五合目（小御岳の山頂）に寄って、光の輪"""
    k = min(1.0, lt / 4.0)
    k = 0.5 - 0.5 * math.cos(math.pi * k)
    tgt = (SUMMIT[0] + (990 - SUMMIT[0]) * k, SUMMIT[1] + (800 - SUMMIT[1]) * k)
    args = dict(az=185, el=16 + 8 * k, dist=12500 - 3000 * k)
    im = _r(tgt, **args)
    m = np.array(_r(tgt, tex=_MARK, **args).convert("L")).astype(int) - np.array(_r(tgt, tex=_ZERO, **args).convert("L")).astype(int)
    ys, xs = np.nonzero(m > 100)
    if len(xs):
        x, y = xs.mean(), ys.mean()
        lay = Image.new("RGB", (SW, SH))
        d = ImageDraw.Draw(lay)
        for i in range(3):
            ph = (t * 0.7 + i / 3) % 1
            r = 20 + 130 * ph
            d.ellipse((x - r, y - r, x + r, y + r), outline=tuple(int(v * (1 - ph) * k) for v in GOLD), width=7)
        im = ImageChops.add(ImageChops.add(im, lay.filter(ImageFilter.GaussianBlur(8))), lay)
    return im


def grow(t, lt):
    """平らな地面から富士山が盛り上がる（高さを0→1に）"""
    k = min(1.0, lt / 4.5)
    k = 0.5 - 0.5 * math.cos(math.pi * k)
    return T3.render(_DEM, _TEX, _MPP, SUMMIT, az=200, el=14, dist=13000, hscale=0.05 + 0.95 * k, exag=1.0,
                     size=(540, 960), fill_gaps=True).resize((SW, SH), Image.BICUBIC)


FIGS = {"orbit": orbit, "komi": komi, "grow": grow}

P = "Mount_Fuji_20120203_a.jpg"
SCENES = [
    dict(spk="Z", ex="panic", say="富士山の中に、古い火山が2つも埋まってるのだ！",
         read="ふじさんの、なかに、ふるい、かざんが、ふたつも、うまってるのだ！",
         head="富士山の中に\n古い火山が2つ！？", show=("fig", "orbit"), head_y=560),
    dict(spk="M", say="じつは富士山は、古い火山の上に、新しい火山が重なってできた山なの。",
         read="じつは、ふじさんは、ふるい、かざんの、うえに、あたらしい、かざんが、かさなって、できた、やまなの。",
         head="火山の重ね着", show=("photo", P, "right")),
    dict(spk="M", say="いちばん下が小御岳火山、その上に古富士火山、そしていちばん上が今の新富士火山よ。",
         read="いちばん、したが、こみたけかざん、その、うえに、こふじかざん。そして、いちばん、うえが、いまの、しんふじかざんよ。",
         head="小御岳→古富士\n→新富士", show=("photo", "ISS-46_Mount_Fuji__Japan.jpg", "in")),
    dict(spk="M", say="北側の五合目には、いちばん古い小御岳火山の山頂が、少しだけ顔を出しているの。",
         read="きたがわの、ごごうめには、いちばん、ふるい、こみたけ、かざんの、さんちょうが、すこしだけ、かおを、だしているの。",
         head="五合目に\n古い火山の山頂", show=("fig", "komi")),
    dict(spk="M", say="そこには小御嶽神社が建っていて、まわりはほとんど新しい溶岩におおわれているのよ。",
         read="そこには、こみたけじんじゃが、たっていて、まわりは、ほとんど、あたらしい、ようがんに、おおわれているのよ。",
         head="小御嶽神社", show=("fig", "komi")),
    dict(spk="M", say="噴火をくり返して古い山をおおい、今のきれいな円すい形に育ったのよ。",
         read="ふんかを、くりかえして、ふるい、やまを、おおい、いまの、きれいな、えんすいけいに、そだったのよ。",
         head="噴火をくり返して\n育った", show=("fig", "grow")),
    dict(spk="Z", say="富士山は、火山の重ね着だったのだ！",
         read="ふじさんは、かざんの、かさねぎだったのだ！",
         head="火山の重ね着\nだった！", show=("photo", "038_Mount_Fuji_and_Aokigahara_forest__Japan__at_sunrise_Photo_by_Giles_Laurent.jpg", "out")),
]

META = dict(
    title="富士山の中に古い火山が2つ！？富士山は火山の重ね着 #shorts #富士山 #科学",
    alt_titles=["五合目に古い火山の山頂が！？ #shorts #富士山", "富士山は3代目だった！？ #shorts #科学 #火山"],
    lead="日本一の山・富士山は、ひとつの火山ではありません。古い「小御岳火山」「古富士火山」の上に、今の「新富士火山」が重なってできています。",
    points=["富士山は、小御岳火山と古富士火山の上にできた成層火山（気象庁）",
            "小御岳火山のふもとで約10万年前に生まれ、古富士火山・新富士火山の噴火で今の円すい形になった（静岡県）",
            "富士スバルライン五合目の小御嶽神社がある台地は、小御岳火山の山頂部。ほとんどは新しい溶岩におおわれた"],
    principle=("火山は、噴火のたびに溶岩や火山灰を積み重ねて大きくなります（成層火山）。山頂の火口から噴き出したものが"
               "まわりに同じように積もると、すそ野の広い円すい形になります。富士山では、古い火山（小御岳・古富士）の上に"
               "新しい噴火の溶岩や火山灰が何万年もかけて積み重なり、古い山をすっぽりおおいました。そのため、いちばん古い"
               "小御岳火山は、北側の五合目でほんの少し顔を出しているだけです。"),
    sources=[("気象庁「富士山」", "https://www.data.jma.go.jp/vois/data/tokyo/314_Fujisan/314_index.html"),
             ("気象庁 日本活火山総覧「富士山」", "https://www.data.jma.go.jp/vois/data/filing/souran/main/55_Fujisan.pdf"),
             ("静岡県（富士山の成り立ち）", "https://www.pref.shizuoka.jp/kankosports/kanko/mtfuji/1002802/1019031.html"),
             ("内閣府 防災「日本の火山 富士山」", "https://www.bousai.go.jp/kohou/kouhoubousai/h24/70/volcano.html"),
             ("国土交通省 観光庁 多言語解説（Komitake-Jinja Shrine）", "https://www.mlit.go.jp/tagengo-db/en/R1-00155.html")],
    tags=["富士山", "小御岳", "古富士", "新富士", "小御嶽神社", "五合目", "富士スバルライン", "成層火山", "火山", "静岡県",
          "山梨県", "世界遺産", "絶景", "ふしぎな絶景", "地学", "科学", "shorts"],
    hashtags=["#富士山", "#絶景", "#科学", "#火山", "#shorts"],
    pinned="富士スバルライン五合目の小御嶽神社は、いちばん古い火山のてっぺん。行ったことある？次はどこのふしぎな絶景が見たい？",
    notes=["立体の富士山は、国土地理院の標高タイルに航空写真を貼って描いたもの（高さは強調していない）。",
           "「盛り上がる」場面は、高さを少しずつ上げて見せた演出で、実際の成長のしかたや順番を表したものではない。",
           "年代は資料により差がある（新富士の活動開始は約1万1千年前・約2万年前など）ため、動画では言っていない。",
           "小御岳火山の山頂が五合目に「顔を出している」は、国土交通省の多言語解説（台地が小御岳の山頂部）と観光案内にもとづく。",
           "Wikimedia Commons が混み合っていて新しい写真を取得できず、写真は以前の動画で使ったもの（NASA、Batholith、Giles Laurent）を使った。"],
)
