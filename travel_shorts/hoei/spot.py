"""ふしぎな絶景の科学 富士山の宝永火口（30秒・全画面・立体）

事実の根拠:
- 1707年12月16日に噴火が始まり、16日間断続的に続いた（宝永噴火）。富士山の最後の噴火 … 気象庁
- 南東斜面の標高約2100〜3150mに、3つの大きな火口ができた … 内閣府 防災
- 噴火の日のうちに江戸にも多量の灰が降った（川崎で厚さ5cm） … 気象庁
- 総噴出量 約17億m³ … 内閣府 防災
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

import longform as L

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
import terrain3d as T3  # noqa: E402

FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 150, 80)
PLACE = dict(name="宝永火口", pref="静岡県", lat=35.351, lon=138.745)
MAP_CREDITS = ["標高（地理院タイル DEM10B）・陰影起伏: 出典 国土地理院。標高に合わせて色をつけて立体表示に加工"]

SW, SH = 1080, 1920
_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
_DEM = np.load(os.path.join(_M, "dem_z13.npy"))
_TEX = np.array(Image.open(os.path.join(_M, "tex_z13.jpg")).convert("RGB"))
_MPP = 156543.03 * math.cos(math.radians(35.35)) / 2 ** 13
CRATER = (1080.2, 1039.8)
SUMMIT = (977.7, 971.3)
GOLD, LAVA = (255, 214, 120), (255, 110, 40)
_R = random.Random(7)
_ASH = [(_R.random(), _R.uniform(-1, 1), _R.uniform(0.6, 1.4)) for _ in range(160)]


def _r3(target, az, el, dist):
    return T3.render(_DEM, _TEX, _MPP, target, az=az, el=el, dist=dist, exag=1.0, size=(720, 1280)).resize((SW, SH), Image.BILINEAR)


def hook(t, lt):
    """富士山を南東からまわりこむ"""
    return _r3(SUMMIT, az=-75 + 7 * lt, el=22, dist=17000 - 300 * lt)


def zoom(t, lt):
    """宝永火口に寄って、火口のまわりをやさしく光らせる"""
    k = min(1.0, lt / 3.0)
    im = _r3(CRATER, az=-45, el=25, dist=12000 - 5000 * k)
    lay = Image.new("RGB", (SW, SH))
    d = ImageDraw.Draw(lay)
    x, y = SW / 2, SH / 2
    a = 0.6 + 0.4 * math.sin(t * 3)
    r = 170 + 40 * k
    d.ellipse((x - r, y - r * 1.3, x + r, y + r * 1.1), outline=tuple(int(v * a * k) for v in GOLD), width=7)
    return ImageChops.add(im, lay.filter(ImageFilter.GaussianBlur(6)))


def erupt(t, lt):
    """火口から灰と火の粉が立ちのぼり、東（画面の右上）へ流れていく"""
    im = _r3(CRATER, az=-45, el=25, dist=9000)
    lay = Image.new("RGB", (SW, SH))
    d = ImageDraw.Draw(lay)
    x, y = SW / 2, SH / 2
    d.ellipse((x - 120, y - 80, x + 120, y + 80), fill=tuple(int(v * (0.7 + 0.3 * math.sin(t * 5))) for v in LAVA))
    glow = lay.filter(ImageFilter.GaussianBlur(50))
    d = ImageDraw.Draw(glow)
    k = min(1.0, lt / 2.0)
    for off, sx, sp in _ASH:
        ph = (t * 0.35 * sp + off) % 1
        if ph > k:
            continue
        ex = x + sx * 60 + ph ** 1.6 * 700  # 上に上がりながら東へ流される
        ey = y - ph * 900
        rr = 4 + 30 * ph
        c = int(200 * (1 - ph) * (0.5 + 0.5 * sp / 1.4))
        d.ellipse((ex - rr, ey - rr, ex + rr, ey + rr), fill=(c, c, c))
        if ph < 0.25:
            d.ellipse((ex - 4, ey - 4, ex + 4, ey + 4), fill=GOLD)
    return ImageChops.add(im, glow.filter(ImageFilter.GaussianBlur(3)))


def last(t, lt):
    """引いて、富士山全体（右の山腹に宝永火口）"""
    k = min(1.0, lt / 4.0)
    return _r3(SUMMIT, az=-50, el=20, dist=12000 + 5000 * k)


FIGS = {"hook": hook, "zoom": zoom, "erupt": erupt, "last": last}

SCENES = [
    dict(spk="Z", ex="panic", say="富士山の横に、大きな穴があいてるのだ！？",
         read="ふじさんの、よこに、おおきな、あなが、あいてるのだ！？",
         head="富士山の横に\n穴！？", show=("fig", "hook")),
    dict(spk="M", say="これは宝永火口。南東の山腹に、大きな火口が3つ並んでいるの。",
         read="これは、ほうえいかこう。なんとうの、さんぷくに、おおきな、かこうが、みっつ、ならんでいるの。",
         head="宝永火口", show=("fig", "zoom")),
    dict(spk="M", say="1707年の噴火で、ここから16日間も火山灰が噴き出したの。灰は江戸にまで降ったわ。",
         read="せんななひゃくななねんの、ふんかで、ここから、じゅうろくにちの、あいだ、かざんばいが、ふきだしたの。はいは、えどにまで、ふったわ。",
         head="灰は江戸まで", show=("fig", "erupt")),
    dict(spk="M", say="これが、今のところ富士山の最後の噴火なのよ。",
         read="これが、いまのところ、ふじさんの、さいごの、ふんかなのよ。",
         head="富士山\n最後の噴火", show=("fig", "last")),
    dict(spk="Z", say="富士山にも、穴があいていたのだ！",
         read="ふじさんにも、あなが、あいていたのだ！",
         head="富士山に穴！", show=("fig", "hook")),
]

META = dict(
    title="富士山の横に穴！？宝永火口 #shorts #絶景 #科学",
    alt_titles=["灰は江戸まで降った！富士山の最後の噴火 #shorts #富士山", "富士山にある3つの火口 #shorts #火山"],
    lead="富士山の南東の山腹には、大きくえぐれた「宝永火口」があります。1707年の宝永噴火でできた火口です。",
    points=["1707年12月16日に噴火が始まり、16日間断続的に続いた（宝永噴火）。これが今のところ富士山の最後の噴火",
            "南東の山腹、標高約2100〜3150mに大きな火口が3つできた",
            "噴火の日のうちに江戸にも灰が降った（川崎で厚さ5cm）。総噴出量は約17億m³"],
    principle=("富士山は、山頂の火口だけでなく、山腹の割れ目からも噴火します。宝永噴火では、地下のマグマが南東の山腹から"
               "噴き出し、ガスを多く含んだマグマが細かく砕けて大量の火山灰や軽石になりました。噴き上がった灰は上空の西風に流されて"
               "東へ運ばれ、遠く江戸（今の東京）にまで降り積もりました。"),
    sources=[("気象庁「富士山 有史以降の火山活動」", "https://www.data.jma.go.jp/vois/data/tokyo/314_Fujisan/314_history.html"),
             ("内閣府 防災「1707 富士山宝永噴火 報告書」", "https://www.bousai.go.jp/kyoiku/kyokun/kyoukunnokeishou/rep/1707_houei_fujisan_funka/pdf/1707-houei-fujisanFUNKA_06_chap2.pdf"),
             ("内閣府 防災（富士山の降灰の想定）", "https://www.bousai.go.jp/kazan/kouikikouhaiworking/pdf/20181207siryo3.pdf")],
    tags=["富士山", "宝永火口", "宝永噴火", "宝永山", "1707年", "火山灰", "江戸", "静岡県", "山梨県", "火山",
          "絶景", "ふしぎな絶景", "地学", "科学", "立体地図", "shorts"],
    hashtags=["#絶景", "#科学", "#富士山", "#火山", "#shorts"],
    pinned="宝永火口は登山道（富士宮ルート）から近くまで歩いて行けます。次はどこのふしぎな絶景が見たい？",
    notes=["立体は国土地理院の10m標高データ（DEM10B）を使用。山頂付近の航空写真タイルが欠けていたため、色は標高に合わせてつけた（実際の色とはちがう）。",
           "「最後の噴火」は「今のところ」と言い、将来の噴火がないとは言っていない。",
           "火口のまわりの光、灰と火の粉の流れは演出。灰が東へ流れたのは、上空の西風に流されたという説明にもとづく。",
           "噴火の始まりの時刻は資料によって差がある（午前10時ごろ／正午前ごろ）ため、時刻は言っていない。"],
)
