"""ふしぎな絶景の科学 那智の滝（30秒・全画面）

事実の根拠:
- 一段で落ちる滝として日本一の落差。幅13mの滝口から133m下の滝つぼへ落ちる。熊野那智大社の別宮・飛瀧神社の御神体。
  国の名勝。熊野那智大社は世界遺産「紀伊山地の霊場と参詣道」の一部 … 国土交通省 観光庁 多言語解説・和歌山県
- 滝の固い岩盤は、約1400万年前のマグマだまりが冷えて固まったもの。まわりのもろい地層がけずられて岩棚が残った … 国土交通省 観光庁 多言語解説
- 固く浸食に強い火成岩と、やわらかく浸食を受けやすい地層の境目にできた滝 … 和歌山県
- 産総研シームレス地質図：滝の場所は中新世（ランギアン期〜サーラバリアン期）の花崗岩類（熊野酸性岩類）、東どなりは砂岩泥岩互層
"""
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from aerial_full import Aerial, SW, SH  # noqa: E402

FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (150, 220, 255)
PLACE = dict(name="那智の滝", pref="和歌山県那智勝浦町", lat=33.6756, lon=135.8875)
MAP_CREDITS = ["航空写真: 出典 国土地理院（電子国土基本図（オルソ画像）を加工して作成）",
               "地質: 出典 産総研地質調査総合センター（20万分の1日本シームレス地質図V2）を加工して作成"]

_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
A16 = Aerial(os.path.join(_M, "ort_z16.jpg"), base_w=620)
A15 = Aerial(os.path.join(_M, "ort_z15.jpg"), base_w=680)
FALL16 = (914, 975)
FALL15 = (969, 872)
GEO_C = (1060, 960)
RIVER = [(969, 872), (1000, 930), (1060, 975), (1200, 1000), (1300, 1040), (1400, 1090), (1440, 1130)]
_MASK = Image.open(os.path.join(_M, "mask.png")).convert("L")
_EDGE = _MASK.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(5))
WARM, GOLD = (255, 150, 200), (255, 214, 120)


def spot(t, lt):
    """滝の場所に寄って、光の輪"""
    k = min(1.0, lt / 4.0)
    return A16.ring(lt, t, FALL16, at=FALL16, scale=1.15 - 0.3 * k, color=(170, 230, 255), size=170)


def geo(t, lt):
    """固い岩（花崗岩類）の広がりをやさしく色づけ、境目を光らせ、滝に輪"""
    b, im = A15.frame(GEO_C, 1.0)
    box = tuple(int(v) for v in b)
    m = _MASK.crop(box).resize((SW, SH), Image.BILINEAR)
    e = _EDGE.crop(box).resize((SW, SH), Image.BILINEAR)
    k = min(1.0, lt / 1.5)
    a = (0.26 + 0.06 * math.sin(t * 3)) * k
    im = Image.composite(Image.new("RGB", (SW, SH), WARM), im, m.point(lambda v: int(v * a)))
    lay = Image.composite(Image.new("RGB", (SW, SH), GOLD), Image.new("RGB", (SW, SH)), e.point(lambda v: int(v * k)))
    d = ImageDraw.Draw(lay)
    x, y = A15.scr(b, *FALL15)
    for i in range(3):
        ph = (t * 0.7 + i / 3) % 1
        r = 20 + 120 * ph
        d.ellipse((x - r, y - r, x + r, y + r), outline=tuple(int(v * (1 - ph)) for v in (170, 230, 255)), width=6)
    return Aerial.glow(im, lay)


def river(t, lt):
    """滝から下流へ、川の流れにそって光の粒（やわらかい地層の谷をけずる）"""
    return A15.flow(lt, t, (1125, 1000), RIVER, scale=0.9, color=(110, 190, 255), speed=90, spread=3, dark=0.8, size=5)


FIGS = {"spot": spot, "geo": geo, "river": river}

SCENES = [
    dict(spk="Z", ex="panic", say="高さ133メートルを、まっすぐ落ちる滝なのだ！？",
         read="たかさ、ひゃくさんじゅうさんメートルを、まっすぐ、おちる、たきなのだ！？",
         head="133mを\nまっすぐ落ちる！？", show=("photo", "Nachi_Falls_2025-10-13.jpg", "in"), head_y=1230),
    dict(spk="M", say="和歌山県の那智の滝。一段で落ちる滝では、日本一の落差なの。",
         read="わかやまけんの、なちのたき。いちだんで、おちる、たきでは、にっぽんいちの、らくさなの。",
         head="那智の滝\n落差133m", show=("fig", "spot")),
    dict(spk="M", say="滝の岩は、約1400万年前に地下のマグマが冷えて固まった、とても固い岩なの。",
         read="たきの、いわは、やく、せんよんひゃくまんねんまえに、ちかの、マグマが、ひえて、かたまった、とても、かたい、いわなの。",
         head="マグマが固まった\n固い岩", show=("fig", "geo")),
    dict(spk="M", say="となりの砂岩や泥岩はやわらかいから、川にけずられて低くなったの。",
         read="となりの、さがんや、でいがんは、やわらかいから、かわに、けずられて、ひくく、なったの。",
         head="やわらかい地層は\nけずられた", show=("fig", "river")),
    dict(spk="M", say="固い岩だけが崖になって残り、そこから水が一気に落ちるのよ。",
         read="かたい、いわだけが、がけに、なって、のこり、そこから、みずが、いっきに、おちるのよ。",
         head="固い岩の崖から\n一気に落ちる", show=("photo", "Nachikatsuura_Nachi_Falls_05.jpg", "right"), head_y=1230),
    dict(spk="M", say="滝そのものが神様としてまつられていて、世界遺産の一部なのよ。",
         read="たき、そのものが、かみさまとして、まつられていて、せかいいさんの、いちぶなのよ。",
         head="滝が\nご神体", show=("photo", "Three-storied_Pagoda_of_Seiganto-ji_and_Nachi_Falls_201808.jpg", "in"), head_y=1230),
    dict(spk="Z", say="岩の固さのちがいが、作った滝なのだ！",
         read="いわの、かたさの、ちがいが、つくった、たきなのだ！",
         head="岩の固さが\n作った滝！", show=("photo", "Nachi_Falls__51929861348_.jpg", "out"), head_y=1230),
]

META = dict(
    title="133mをまっすぐ落ちる！那智の滝は岩の固さが作った #shorts #絶景 #科学",
    alt_titles=["日本一の落差の滝のひみつ #shorts #那智の滝", "マグマが作った滝！？那智の滝 #shorts #和歌山 #科学"],
    lead="和歌山県那智勝浦町の那智の滝は、幅13mの滝口から133m下の滝つぼへ一気に落ちる、一段の滝として日本一の落差をもつ滝です。",
    points=["一段で落ちる滝として日本一の落差（133m）。滝そのものが飛瀧神社の御神体で、国の名勝",
            "滝の岩は、約1400万年前に地下のマグマだまりが冷えて固まった固い岩（地質図では花崗岩類）",
            "となりのやわらかい砂岩や泥岩の地層は川にけずられ、固い岩との境目に崖ができて滝になった",
            "熊野那智大社は世界遺産「紀伊山地の霊場と参詣道」の一部"],
    principle=("川の水は、流れながら少しずつ岩をけずります。やわらかい岩は早くけずれ、固い岩はなかなかけずれません。"
               "そのため固い岩とやわらかい岩がとなり合う所では、やわらかい側だけが低くなり、固い岩の端が急な崖として残ります。"
               "川がその崖を越えるところで、水が一気に落ちて滝になります（差別侵食）。那智の滝では、地下のマグマが"
               "ゆっくり冷えて固まった固い花崗岩類が、まわりの砂岩・泥岩よりけずられにくかったため、133mの崖が残りました。"),
    sources=[("国土交通省 観光庁 多言語解説（那智の滝のでき方）", "https://www.mlit.go.jp/tagengo-db/R1-02350.html"),
             ("国土交通省 観光庁 多言語解説（世界文化遺産 那智大滝・飛瀧神社）", "https://www.mlit.go.jp/tagengo-db/R2-00209.html"),
             ("和歌山県（那智の滝と地質）", "https://www.pref.wakayama.lg.jp/prefg/000200/nagomi/p50/p08_09.pdf"),
             ("和歌山県（那智大滝）", "https://www.pref.wakayama.lg.jp/prefg/081300/d00215008.html"),
             ("産総研 地質調査総合センター 20万分の1日本シームレス地質図V2", "https://gbank.gsj.jp/seamless/")],
    tags=["那智の滝", "那智大滝", "飛瀧神社", "熊野那智大社", "青岸渡寺", "熊野古道", "世界遺産", "名勝", "那智勝浦町",
          "和歌山県", "滝", "差別侵食", "花崗岩", "絶景", "ふしぎな絶景", "地学", "科学", "shorts"],
    hashtags=["#絶景", "#科学", "#那智の滝", "#和歌山", "#shorts"],
    pinned="東尋坊も「固い岩だけが残った」絶景。くらべてみてね。次はどこのふしぎな絶景が見たい？",
    notes=["岩の名前は、動画では「マグマが冷えて固まった固い岩」とだけ言った。地質図では花崗岩類（熊野酸性岩類）。滝の崖の岩を花崗斑岩とする資料もあるため、細かい名前は言っていない。",
           "地質図の色づけ（ピンク）は、地質図の花崗岩類の範囲を航空写真に重ねたもの。地質図は20万分の1なので、境目は目安。",
           "光る粒は滝から下流（那智川）へ流れる向きの演出。",
           "年代は資料により約1400万〜1500万年前と幅がある。動画では国土交通省の資料の約1400万年前を使った。"],
)
