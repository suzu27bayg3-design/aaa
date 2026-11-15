"""ふしぎな絶景の科学 西之島（30秒・全画面）

事実の根拠:
- 2013年11月20日、西之島の南南東約500mの海で噴火が始まり、新しい島が見つかった … 気象庁 / 海上保安庁
- 新しい島は溶岩で広がり、2013年12月26日に元の西之島とつながった … 気象庁
- 噴火は約2年続き、島は噴火前の約12倍の広さになった … 海上保安庁
- その後の噴火でも陸地が広がり、2019年に地形図と海図が改められ、日本の管轄海域が約50km²広がった … 国土地理院
"""
import os

from PIL import Image, ImageDraw

import longform as L

FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 160, 90)
PLACE = dict(name="西之島", pref="東京都小笠原村", lat=27.247, lon=140.874)
MAP_CREDITS = ["航空写真（現在・1970年代）: 出典 国土地理院（地理院タイルを加工して作成。写真のない海の部分は海の色でうめた）"]

SW, SH = 1080, 1920
_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
PAD = 700  # 写真のまわりを海の色で広げる（切り出しが写真の外に出ても黒くならないように）


def _padded(name):
    im = Image.open(os.path.join(_M, name)).convert("RGB")
    out = Image.new("RGB", (im.width + 2 * PAD, im.height + 2 * PAD), (28, 62, 92))
    m = Image.new("L", im.size, 255).filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(0))
    out.paste(im, (PAD, PAD), m)
    return out


_NOW = _padded("photo_fill.jpg")
_OLD = _padded("old1974_fill.jpg")
C = (540 + PAD, 470 + PAD)


def _view(im, scale):
    w, h = 640 * scale, 640 * scale * SH / SW
    b = (C[0] - w / 2, C[1] - h / 2, C[0] + w / 2, C[1] + h / 2)
    return im.crop(tuple(int(v) for v in b)).resize((SW, SH), Image.BILINEAR)


def _label(im, text):
    im = im.convert("RGBA")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 1250, 520, 1350), 30, fill=(0, 0, 0, 170))
    d.text((290, 1300), text, font=L.jp(52, True), fill=(255, 214, 120), anchor="mm")
    return im


def now(t, lt):
    return _view(_NOW, 1.0 - 0.15 * min(1, lt / 4))


def before(t, lt):
    return _label(_view(_OLD, 0.9), "1970年代")


def grow(t, lt):
    k = min(1.0, max(0.0, (lt - 0.8) / 2.5))
    im = Image.blend(_view(_OLD, 0.9), _view(_NOW, 0.9), k)
    return _label(im, "1970年代" if k < 0.5 else "現在")


FIGS = {"now": now, "before": before, "grow": grow}

SCENES = [
    dict(spk="Z", ex="panic", say="この島、10年ちょっとで何倍にも大きくなったのだ！？",
         read="この、しま、じゅうねん、ちょっとで、なんばいにも、おおきく、なったのだ！？",
         head="島が\n大きくなった！？", show=("fig", "now")),
    dict(spk="M", say="東京都の西之島。前は、こんなに小さな島だったの。",
         read="とうきょうとの、にしのしま。まえは、こんなに、ちいさな、しまだったの。",
         head="前は小さな島", show=("fig", "before")),
    dict(spk="M", say="2013年、すぐ近くの海で噴火が始まり、新しい島が生まれて、元の島とつながったのよ。",
         read="にせんじゅうさんねん、すぐ、ちかくの、うみで、ふんかが、はじまり、あたらしい、しまが、うまれて、もとの、しまと、つながったのよ。",
         head="新しい島が\n生まれてつながった", show=("fig", "grow")),
    dict(spk="M", say="流れ出た溶岩が海をうめて、島は噴火前の約12倍の広さになったの。",
         read="ながれでた、ようがんが、うみを、うめて、しまは、ふんかまえの、やく、じゅうにばいの、ひろさに、なったの。",
         head="約12倍に", show=("fig", "now")),
    dict(spk="M", say="噴火は約2年も続いて、溶岩がどんどん海に流れこんだの。",
         head="約2年の噴火", show=("fig", "grow")),
    dict(spk="M", say="島が広がったおかげで、2019年には地図が書きかえられて、日本の海も広がったのよ。",
         head="日本の海が\n広がった", show=("fig", "now")),
    dict(spk="Z", say="今も、地球が島を作っているのだ！",
         read="いまも、ちきゅうが、しまを、つくっているのだ！",
         head="地球が\n島を作ってる！", show=("fig", "now")),
]

META = dict(
    title="島が12倍に！？今も成長する西之島 #shorts #絶景 #科学",
    alt_titles=["噴火で生まれた新しい島 #shorts #西之島", "日本の島が大きくなった！ #shorts #科学 #小笠原"],
    lead="東京都小笠原村の西之島は、2013年に始まった噴火で新しい島が生まれ、元の島とつながって大きくなりました。",
    points=["噴火は約2年続いた。2019年に地形図と海図が改められ、日本の管轄海域が約50km²広がった",
            "2013年11月20日、西之島の南南東約500mの海で噴火が始まり、新しい島が見つかった",
            "新しい島は溶岩で広がり、2013年12月26日に元の西之島とつながった",
            "噴火は約2年続き、島は噴火前の約12倍の広さに。その後の噴火でも広がり、2019年に地図と海図が改められた"],
    principle=("海の中で火山が噴火すると、流れ出た溶岩が海水で冷やされて固まり、海底から積み重なっていきます。やがて海面より上に"
               "出ると新しい島になり、さらに溶岩が流れ出るたびに、固まった溶岩が海をうめて陸地が広がります。"),
    sources=[("気象庁 火山活動解説資料（西之島 2013年）", "https://www.data.jma.go.jp/vois/data/report/monthly_v-act_doc/tokyo/2013y/326_13y.pdf"),
             ("海上保安庁（西之島の噴火と拡大）", "https://www1.kaiho.mlit.go.jp/kenkyu/report/rhr55/rhr55-00.pdf"),
             ("国土地理院「西之島の地形図と海図を改版」", "https://www.gsi.go.jp/kanri/kanri61003.html")],
    tags=["西之島", "にしのしま", "新島", "海底火山", "噴火", "溶岩", "小笠原", "小笠原諸島", "東京都", "火山",
          "絶景", "ふしぎな絶景", "地学", "科学", "航空写真", "shorts"],
    hashtags=["#絶景", "#科学", "#西之島", "#火山", "#shorts"],
    pinned="島が広がると、日本の海の範囲も広がります。次はどこのふしぎな絶景が見たい？コメントで教えてください！",
    notes=["「前は小さな島」の写真は国土地理院の1970年代の空中写真。2013年の噴火直前とは時期がちがう。",
           "「約12倍」は海上保安庁の報告（噴火が約2年続いたあとの面積）にもとづく。",
           "西之島は今も活動中の火山で、上陸などは規制されている。"],
)
