"""ふしぎな絶景の科学 昭和新山（30秒・全画面の型）

事実の根拠（国土交通省 観光庁 多言語解説）:
- 1943〜45年の活動で、海抜120〜150mの畑が海抜250mほどの「屋根山」に盛り上がり、その中央から溶岩が出てきた
- 成長が止まった1945年9月の標高は406.9m
- 壮瞥郵便局長の三松正夫が、2年近く山の成長を線画で記録した（ミマツダイヤグラム）
- 1957年に国の特別天然記念物
"""
import math
import os

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

import longform as L

FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 150, 80)
PLACE = dict(name="昭和新山", pref="北海道壮瞥町", lat=42.5425, lon=140.864)
MAP_CREDITS = ["航空写真（現在・1961〜69年）・陰影起伏: 出典 国土地理院（地理院タイルを加工して作成）"]

SW, SH = 1080, 1920
_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
_P = Image.open(os.path.join(_M, "photo_z15.jpg")).convert("RGB")
_O = Image.open(os.path.join(_M, "old1961_z15.jpg")).convert("RGB")
_H = Image.open(os.path.join(_M, "hillshade_z15.png")).convert("RGB")
_HS = Image.blend(_H, Image.new("RGB", _H.size, "white"), 0.35)
_REAL = ImageChops.multiply(_P, _HS)
_FLAT = ImageChops.multiply(_P, _HS.filter(ImageFilter.GaussianBlur(40)))  # 起伏をならした（平らに見える）版
DOME = (730, 575)  # 昭和新山の頂上付近（航空写真の上の位置）
GOLD, LAVA = (255, 214, 120), (255, 110, 40)


def _crop(im, scale, cx=None, cy=None):
    cx, cy = cx or DOME[0], cy or DOME[1] + 60
    w, h = 560 * scale, 995 * scale
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    return box, im.crop(tuple(int(v) for v in box)).resize((SW, SH), Image.BILINEAR)


def _scr(box, x, y):
    return (x - box[0]) * SW / (box[2] - box[0]), (y - box[1]) * SH / (box[3] - box[1])


def _glow(base, lay, blur=12):
    return ImageChops.add(ImageChops.add(base, lay.filter(ImageFilter.GaussianBlur(blur))), lay)


def hook(t, lt):
    _, im = _crop(_REAL, 1.15 - 0.2 * min(1, lt / 4))
    return im


def rise(t, lt):
    """平らな畑 → 起伏が浮かび上がる（地面が盛り上がる）。頂上が光る"""
    k = min(1.0, lt / 4.0)
    box, flat = _crop(_FLAT, 0.8)
    _, real = _crop(_REAL, 0.8)
    im = Image.blend(flat, real, k)
    lay = Image.new("RGB", (SW, SH))
    d = ImageDraw.Draw(lay)
    x, y = _scr(box, *DOME)
    r = 60 + 160 * k
    d.ellipse((x - r, y - r, x + r, y + r), outline=tuple(int(v * (0.4 + 0.6 * k)) for v in GOLD), width=6)
    return _glow(im, lay)


_rng = __import__("random").Random(4)
_EMB = [(_rng.random(), _rng.uniform(-1, 1)) for _ in range(50)]


def magma(t, lt):
    """地下から上がってきたマグマ：頂上の下がやわらかく赤く光り、火の粉が立ちのぼる"""
    box, im = _crop(_REAL, 0.6)
    im = ImageEnhance.Brightness(im).enhance(0.75)
    lay = Image.new("RGB", (SW, SH))
    d = ImageDraw.Draw(lay)
    x, y = _scr(box, *DOME)
    k = min(1.0, lt / 2.5)
    a = 0.75 + 0.25 * math.sin(t * 3)
    r = 230 * (0.4 + 0.6 * k)
    d.ellipse((x - r, y - r * 0.75, x + r, y + r * 0.75), fill=tuple(int(v * 0.55 * a) for v in LAVA))
    lay = lay.filter(ImageFilter.GaussianBlur(70))
    d = ImageDraw.Draw(lay)
    for i, (off, sx) in enumerate(_EMB):  # 火の粉（ばらばらに立ちのぼる）
        ph = (t * 0.5 + off) % 1
        ex = x + sx * 150 * (0.3 + ph)
        ey = y - ph * 420 * k
        rr = 5 * (1 - ph) + 1
        d.ellipse((ex - rr, ey - rr, ex + rr, ey + rr), fill=tuple(int(v * (1 - ph)) for v in GOLD))
    return ImageChops.add(im, lay)


def eras(t, lt):
    """1960年代（白黒）→ 今（緑の森）"""
    k = min(1.0, max(0.0, (lt - 1.2) / 1.2))
    _, old = _crop(_O, 0.8)
    _, now = _crop(_P, 0.8)
    im = Image.blend(old, now, k).convert("RGBA")
    d = ImageDraw.Draw(im)
    lab = "1961〜69年" if k < 0.5 else "現在"
    d.rounded_rectangle((60, 1300, 460, 1400), 30, fill=(0, 0, 0, 170))
    d.text((260, 1350), lab, font=L.jp(56, True), fill=GOLD, anchor="mm")
    return im


FIGS = {"hook": hook, "rise": rise, "magma": magma, "eras": eras}

SCENES = [
    dict(spk="Z", ex="panic", say="この山、畑から生えてきたのだ！？",
         read="この、やま、はたけから、はえてきたのだ！？",
         head="畑から\n山が生えた！？", show=("fig", "hook")),
    dict(spk="M", say="北海道の昭和新山。1943年から、畑だった土地がどんどん盛り上がったの。",
         read="ほっかいどうの、しょうわしんざん。せんきゅうひゃくよんじゅうさんねんから、はたけだった、とちが、どんどん、もりあがったの。",
         head="畑が\n盛り上がった", show=("fig", "rise")),
    dict(spk="M", say="地下から上がってきたマグマが押し上げて、2年ほどで高さ約400メートルの山になったのよ。",
         read="ちかから、あがってきた、マグマが、おしあげて、にねんほどで、たかさ、やく、よんひゃくメートルの、やまに、なったのよ。",
         head="2年で\n約400m", show=("fig", "magma")),
    dict(spk="M", say="1960年代はまだ岩がむき出し。今は森におおわれ始めているわ。",
         read="せんきゅうひゃくろくじゅうねんだいは、まだ、いわが、むきだし。いまは、もりに、おおわれはじめているわ。",
         head="昔と今", show=("fig", "eras")),
    dict(spk="Z", say="畑が、山になったのだ！",
         read="はたけが、やまに、なったのだ！",
         head="畑が山に！", show=("fig", "hook")),
]

META = dict(
    title="畑から山が生えた！？昭和新山 #shorts #絶景 #科学",
    alt_titles=["2年で畑が400mの山に！昭和新山 #shorts #火山", "郵便局長が記録した山の誕生 #shorts #北海道"],
    lead="北海道壮瞥町の昭和新山は、1943〜45年に畑だった土地が盛り上がってできた火山です。",
    points=["1943〜45年の活動で、海抜120〜150mの畑が海抜250mほどの屋根山に盛り上がり、その中央から溶岩が出てきた",
            "成長が止まった1945年9月の標高は406.9m",
            "壮瞥郵便局長の三松正夫が、2年近く山の成長を記録した（ミマツダイヤグラム）。1957年に国の特別天然記念物"],
    principle=("地下から上がってきたマグマが地表近くで止まると、その上の地面を押し上げて盛り上げます（潜在円頂丘・屋根山）。"
               "さらにねばりけの強いマグマが地表に押し出されると、流れ広がらずにその場で積み重なり、ドームの形の山（溶岩ドーム）になります。"
               "昭和新山は、この両方が2年ほどのうちに起きて生まれました。"),
    sources=[("国土交通省 観光庁 多言語解説（昭和新山）", "https://www.mlit.go.jp/tagengo-db/common/001641465.pdf"),
             ("国土交通省 観光庁 多言語解説（Mount Showa Shinzan and the Mimatsu Diagram）", "https://www.mlit.go.jp/tagengo-db/en/H30-00070.html"),
             ("内閣府 防災（有珠山の災害教訓）", "https://www.bousai.go.jp/kyoiku/kyokun/usuzan/database/01/01/02/uzn010102_07.htm")],
    tags=["昭和新山", "しょうわしんざん", "有珠山", "溶岩ドーム", "屋根山", "三松正夫", "ミマツダイヤグラム", "壮瞥町", "洞爺湖",
          "北海道", "火山", "絶景", "ふしぎな絶景", "地学", "科学", "航空写真", "shorts"],
    hashtags=["#絶景", "#科学", "#昭和新山", "#火山", "#shorts"],
    pinned="当時の郵便局長・三松正夫さんは、2年近く山の成長を描き続けました。次はどこのふしぎな絶景が見たい？",
    notes=["「約400メートル」は、1945年9月の標高406.9m（国土交通省資料）にもとづく。今の標高は浸食などで少しちがう。",
           "「平らな畑 → 盛り上がる」の場面は、陰影起伏をならした絵から本物の起伏へ切りかえる演出で、当時の写真ではない。",
           "昔の航空写真は1961〜69年のもの（1940年代の写真はこの場所にない）。",
           "ミマツダイヤグラムの図は著作権の確認ができないため使っていない。"],
)
