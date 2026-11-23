"""ふしぎな絶景の科学 華厳の滝と中禅寺湖（30秒・全画面）

事実の根拠:
- 男体山から流れ出た溶岩が大谷川をせき止めて中禅寺湖ができた … 国土交通省 観光庁 多言語解説
  （年代は資料により約2万年前・約1万5000年前などの差があるため、動画では言わない）
- 湖の水が流れ出るのは大谷川ただ一つ。中禅寺湖から東に流れ出て、華厳の滝で97m下る … 国土交通省 観光庁 多言語解説
- 滝の壁は、溶岩が五角形や六角形の柱の形に固まった柱状節理の岩盤がほとんど … 栃木県の学校の探究資料・観光案内
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from aerial_full import Aerial, SW, SH  # noqa: E402

FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 170, 90)
PLACE = dict(name="華厳の滝", pref="栃木県日光市", lat=36.7380, lon=139.5026)
MAP_CREDITS = ["航空写真: 出典 国土地理院（地理院タイルを加工して作成。撮影時期のちがう写真の色をそろえ、湖は地理院地図の範囲で色づけ）"]

_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
A14 = Aerial(os.path.join(_M, "norm_z14.jpg"), base_w=620)
A16 = Aerial(os.path.join(_M, "norm_z16.jpg"), base_w=620)
FALL14, NANTAI = (1259, 1037), (1119, 640)
FALL16 = (940, 819)
OUT16 = [(560, 735), (680, 758), (760, 775), (850, 800), (940, 819)]
LAVA = [(1119, 640), (1150, 760), (1190, 880), (1230, 980), (1255, 1030)]
_a = np.array(A14.im).astype(int)
_LAKE = Image.fromarray(((_a[..., 2] > _a[..., 1] + 8) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
LAVA_C, WATER_C = (255, 120, 40), (150, 220, 255)


def outflow(t, lt):
    """湖から流れ出る川にそって光の粒、滝に光の輪"""
    b, im = A16.frame((800, 800), 1.0 - 0.1 * min(1, lt / 4))
    lay = A16.flow(lt, t, (800, 800), OUT16, scale=1.0 - 0.1 * min(1, lt / 4), color=WATER_C, speed=80, spread=3, dark=1.0, size=5)
    d_im = Image.new("RGB", (SW, SH))
    d = ImageDraw.Draw(d_im)
    x, y = A16.scr(b, *FALL16)
    for i in range(3):
        ph = (t * 0.7 + i / 3) % 1
        r = 20 + 130 * ph
        d.ellipse((x - r, y - r, x + r, y + r), outline=tuple(int(v * (1 - ph)) for v in WATER_C), width=6)
    return Aerial.glow(lay, d_im)


def lava(t, lt):
    """男体山の頂上から、溶岩の光が流れ下って谷をふさぐ"""
    return A14.flow(lt, t, (1150, 860), LAVA, scale=1.0, color=LAVA_C, speed=80, spread=10, dark=0.8, size=6)


def dam(t, lt):
    """せき止められた水がたまる：湖をやさしく光らせ、せき止めた所に輪"""
    k = min(1.0, lt / 2.0)
    b, im = A14.frame((1000, 900), 1.3)
    box = tuple(int(v) for v in b)
    m = _LAKE.crop(box).resize((SW, SH), Image.BILINEAR)
    a = (0.15 + 0.06 * math.sin(t * 3)) * k
    im = Image.composite(Image.new("RGB", (SW, SH), (80, 170, 255)), im, m.point(lambda v: int(v * a)))
    lay = Image.new("RGB", (SW, SH))
    d = ImageDraw.Draw(lay)
    x, y = A14.scr(b, 1225, 1000)
    for i in range(3):
        ph = (t * 0.7 + i / 3) % 1
        r = 15 + 100 * ph
        d.ellipse((x - r, y - r, x + r, y + r), outline=tuple(int(v * (1 - ph)) for v in LAVA_C), width=6)
    return Aerial.glow(im, lay)


FIGS = {"outflow": outflow, "lava": lava, "dam": dam}

P_LAKE = "Japan__Tochigi_-_Nikko_lake_Ch_zenji_Kegon_waterfall_2015.jpg"
SCENES = [
    dict(spk="Z", ex="panic", say="湖のすぐ先から、97メートルも落ちる滝なのだ！？",
         read="みずうみの、すぐさきから、きゅうじゅうななメートルも、おちる、たきなのだ！？",
         head="湖の先が\nいきなり滝！？", show=("photo", P_LAKE, "in"), head_y=1230),
    dict(spk="M", say="栃木県日光の華厳の滝。中禅寺湖の水が、ここから流れ落ちるの。",
         read="とちぎけん、にっこうの、けごんのたき。ちゅうぜんじこの、みずが、ここから、ながれおちるの。",
         head="華厳の滝", show=("fig", "outflow")),
    dict(spk="M", say="となりの男体山が噴火したとき、流れ出た溶岩が、谷をせき止めたの。",
         read="となりの、なんたいさんが、ふんかしたとき、ながれでた、ようがんが、たにを、せきとめたの。",
         head="溶岩が\n谷をせき止めた", show=("fig", "lava")),
    dict(spk="M", say="行き場をなくした水がたまって、中禅寺湖ができたのよ。",
         read="いきばを、なくした、みずが、たまって、ちゅうぜんじこが、できたのよ。",
         head="水がたまって\n湖に", show=("fig", "dam")),
    dict(spk="M", say="あふれた水が、固まった溶岩の崖から、一気に落ちているのが華厳の滝なの。",
         read="あふれた、みずが、かたまった、ようがんの、がけから、いっきに、おちているのが、けごんのたきなの。",
         head="溶岩の崖から\n落ちる", show=("photo", "Lake_chuzenji_and_kegon_waterfall.jpg", "in"), head_y=1230),
    dict(spk="M", say="崖には、溶岩が冷えて縮んでできた、柱の形の割れ目も見られるのよ。",
         read="がけには、ようがんが、ひえて、ちぢんで、できた、はしらの、かたちの、われめも、みられるのよ。",
         head="柱の形の割れ目", show=("photo", "Kegon_Falls_-_Nikko_National_Park.jpg", "in"), head_y=1230),
    dict(spk="Z", say="噴火が作った、湖と滝だったのだ！",
         read="ふんかが、つくった、みずうみと、たきだったのだ！",
         head="噴火が作った\n湖と滝！", show=("photo", "Kegon_Falls__51988140443_.jpg", "out"), head_y=1230),
]

META = dict(
    title="湖の先がいきなり滝！？華厳の滝は噴火が作った #shorts #絶景 #科学",
    alt_titles=["97mの滝と湖のひみつ #shorts #華厳の滝", "溶岩が作った湖と滝！？ #shorts #日光 #科学"],
    lead="栃木県日光市の華厳の滝は、中禅寺湖からあふれた水が97m下へ落ちる滝です。湖も滝も、男体山の噴火で生まれました。",
    points=["男体山から流れ出た溶岩が大谷川の谷をせき止め、水がたまって中禅寺湖ができた",
            "湖の水が流れ出る川は大谷川ただ一つ。その出口近くで、水が97m下に落ちるのが華厳の滝",
            "滝の壁の多くは、溶岩が冷えて縮み、柱の形に割れた岩（柱状節理）"],
    principle=("水は高い所から低い所へ流れ、谷にそって集まります。その谷を溶岩がふさぐと、水は行き場をなくして"
               "せき止められた所にたまり、湖になります（せき止め湖）。湖の水がいっぱいになると、いちばん低い所からあふれ出て"
               "新しい川になります。中禅寺湖では、その出口のすぐ先が固まった溶岩の高い崖になっているため、"
               "水が一気に落ちて華厳の滝になっています。溶岩は冷えて固まるときに縮むので、柱の形に割れることがあります（柱状節理）。"),
    sources=[("国土交通省 観光庁 多言語解説（中禅寺湖・華厳の滝）", "https://www.mlit.go.jp/tagengo-db/common/001556132.pdf"),
             ("国土交通省 観光庁 多言語解説（日光）", "https://www.mlit.go.jp/tagengo-db/common/001551864.pdf"),
             ("nippon.com（華厳の滝）", "https://www.nippon.com/ja/guide-to-japan/gu900200/")],
    tags=["華厳の滝", "中禅寺湖", "男体山", "日光", "日光国立公園", "大谷川", "せき止め湖", "溶岩", "柱状節理", "栃木県",
          "滝", "火山", "絶景", "ふしぎな絶景", "地学", "科学", "shorts"],
    hashtags=["#絶景", "#科学", "#華厳の滝", "#日光", "#shorts"],
    pinned="和歌山の那智の滝は「固い岩が残った」滝、華厳の滝は「溶岩がせき止めた湖」の滝。でき方のちがいをくらべてみてね。",
    notes=["湖ができた年代は資料により約2万年前・約1万5000年前などの差があるため、動画では言っていない。",
           "溶岩の光の流れは、男体山からせき止めた所までを表した演出で、実際の溶岩の流れた道すじそのものではない。",
           "航空写真は、撮影時期のちがう写真がつぎはぎで色がばらばらだったため、明るさの細かいもようだけを残して色をそろえ、湖は地理院地図の範囲で青く色づけした。",
           "柱状節理は、国土交通省の資料ではなく学校の探究資料・観光案内の説明にもとづく。動画では「見られる」と言うにとどめた。",
           "産総研の地質図は、作成時にメンテナンス中で使えなかった。"],
)
