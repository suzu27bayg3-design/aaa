"""ふしぎな絶景の科学 青木ヶ原樹海と西湖・精進湖（30秒・全画面）

事実の根拠:
- 864年の貞観噴火で富士山の北西のふもとから流れ出た青木ヶ原溶岩が、「せの海（剗の海）」と呼ばれる湖の大部分を埋め、
  残った部分が西湖と精進湖になった … 国土交通省 観光庁 多言語解説・日本地球惑星科学連合 2003年大会要旨・山梨県
- 溶岩の上にできた森で、千年たっても土の層は薄く養分が少ない。木は根を苔むした地面にむき出しに広げて育つ
  … 国土交通省 観光庁 多言語解説（Forests of Mt. Fuji）・山梨県（土の厚さは十数cm）
- 産総研シームレス地質図：樹海の範囲は完新世の玄武岩の溶岩
"""
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from aerial_full import Aerial, SW, SH  # noqa: E402

FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 150, 90)
PLACE = dict(name="青木ヶ原樹海", pref="山梨県富士河口湖町", lat=35.468, lon=138.635)
MAP_CREDITS = ["航空写真: 出典 国土地理院（地理院タイルを加工して作成）",
               "地質: 出典 産総研地質調査総合センター（20万分の1日本シームレス地質図V2）を加工して作成"]

_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
A = Aerial(os.path.join(_M, "photo_z14.jpg"), base_w=620)
_MASK = Image.open(os.path.join(_M, "lava_mask.png")).convert("L")
SAIKO, SHOJI = (1440, 735), (545, 860)
C_ALL = (930, 980)
C_LAVA = (960, 1010)
LAVA_PATH = [(1150, 1760), (1050, 1450), (960, 1200), (930, 1000), (950, 870)]
WATER, LAVA = (150, 220, 255), (255, 130, 50)


def _rings(d, b, t, pts, color, size=110):
    for p in pts:
        x, y = A.scr(b, *p)
        for i in range(3):
            ph = (t * 0.7 + i / 3) % 1
            r = 15 + size * ph
            d.ellipse((x - r, y - r, x + r, y + r), outline=tuple(int(v * (1 - ph)) for v in color), width=6)


def lakes(t, lt):
    """西湖と精進湖の両方に光の輪"""
    k = min(1.0, lt / 5.0)
    k = 0.5 - 0.5 * math.cos(math.pi * k)
    c = (SHOJI[0] + 120 + (SAIKO[0] - 120 - SHOJI[0] - 120) * k, 900)
    b, im = A.frame(c, 1.1)
    lay = Image.new("RGB", (SW, SH))
    _rings(ImageDraw.Draw(lay), b, t, [SAIKO, SHOJI], WATER)
    return Aerial.glow(im, lay)


def lava(t, lt):
    """地質図の溶岩の範囲がオレンジに染まり、富士山の方から光の粒が流れこむ"""
    k = min(1.0, lt / 3.0)
    flow = A.flow(lt, t, C_LAVA, LAVA_PATH, scale=1.2, color=LAVA, speed=100, spread=30, dark=1.0, size=5)
    b = A.box(C_LAVA, 1.2)
    m = _MASK.crop(tuple(int(v) for v in b)).resize((SW, SH), Image.BILINEAR)
    a = (0.2 + 0.05 * math.sin(t * 3)) * k
    return Image.composite(Image.new("RGB", (SW, SH), LAVA), flow, m.point(lambda v: int(v * a)))


def forest(t, lt):
    """溶岩の上の森に寄っていく（溶岩の範囲はうすく）"""
    k = min(1.0, lt / 4.0)
    s = 1.2 - 0.5 * k
    c = (C_ALL[0] + (900 - C_ALL[0]) * k, C_ALL[1] + (1150 - C_ALL[1]) * k)
    b, im = A.frame(c, s)
    m = _MASK.crop(tuple(int(v) for v in b)).resize((SW, SH), Image.BILINEAR)
    return Image.composite(Image.new("RGB", (SW, SH), LAVA), im, m.point(lambda v: int(v * 0.18 * (1 - k))))


FIGS = {"lakes": lakes, "lava": lava, "forest": forest}

HOOK = "038_Mount_Fuji_and_Aokigahara_forest__Japan__at_sunrise_Photo_by_Giles_Laurent.jpg"
SCENES = [
    dict(spk="Z", ex="panic", say="富士山のふもとに、木の海が広がってるのだ！？",
         read="ふじさんの、ふもとに、きの、うみが、ひろがってるのだ！？",
         head="富士山のふもとに\n木の海！？", show=("photo", HOOK, "in"), head_y=1230),
    dict(spk="M", say="山梨県の西湖と精進湖。じつは昔、ひとつの大きな湖だったと考えられているの。",
         read="やまなしけんの、さいこと、しょうじこ。じつは、むかし、ひとつの、おおきな、みずうみだったと、かんがえられているの。",
         head="もとは\nひとつの湖", show=("fig", "lakes")),
    dict(spk="M", say="864年、富士山の噴火で流れ出た溶岩が、その湖を埋めて、二つに分けたのよ。",
         read="はっぴゃくろくじゅうよねん、ふじさんの、ふんかで、ながれでた、ようがんが、その、みずうみを、うめて、ふたつに、わけたのよ。",
         head="溶岩が\n湖を分けた", show=("fig", "lava")),
    dict(spk="M", say="その溶岩の上に育ったのが、青木ヶ原樹海なの。",
         read="その、ようがんの、うえに、そだったのが、あおきがはらじゅかいなの。",
         head="溶岩の上の森", show=("fig", "forest")),
    dict(spk="M", say="土はとても薄くて、木の根は溶岩の上をはうように広がっているのよ。",
         read="つちは、とても、うすくて、きの、ねは、ようがんの、うえを、はうように、ひろがっているのよ。",
         head="根が\n溶岩の上をはう", show=("photo", "Aokigahara_Forest__10863169686_.jpg", "in"), head_y=1230),
    dict(spk="M", say="溶岩が流れてから、まだ千年ちょっと。土がゆっくり作られている途中の森なのよ。",
         read="ようがんが、ながれてから、まだ、せんねん、ちょっと。つちが、ゆっくり、つくられている、とちゅうの、もりなのよ。",
         head="千年ちょっとの\n森", show=("photo", "Lake_Sai_and_Aokigahara_from_Koyodai.jpg", "in"), head_y=1230),
    dict(spk="Z", say="湖も森も、噴火が作り変えたのだ！",
         read="みずうみも、もりも、ふんかが、つくりかえたのだ！",
         head="噴火が\n作り変えた！", show=("photo", "Aokigahara_and_Misaka_Mountains.JPG", "out"), head_y=1230),
]

META = dict(
    title="富士山のふもとに木の海！？青木ヶ原樹海は溶岩の上の森 #shorts #絶景 #科学",
    alt_titles=["ひとつの湖が溶岩で2つに！？西湖と精進湖 #shorts #富士山", "千年ちょっとの森のひみつ #shorts #科学 #山梨"],
    lead="富士山の北西のふもとに広がる青木ヶ原樹海は、864年の噴火で流れ出た溶岩の上に育った森です。",
    points=["864年の貞観噴火で流れ出た青木ヶ原溶岩が、「せの海（剗の海）」と呼ばれた湖の大部分を埋めた",
            "埋め残された部分が、今の西湖と精進湖になったと考えられている",
            "溶岩の上の土はとても薄く、木は根を地面の上に広げて育っている"],
    principle=("溶岩は、冷えて固まると岩になります。岩の上には、はじめは土がほとんどありません。コケや草が生えて枯れ、"
               "岩が少しずつくだけて、長い時間をかけて土ができていきます。青木ヶ原では溶岩が流れてから千年ちょっとしかたっていないので、"
               "土の層はまだ十数cmほどと薄く、木は根を深くのばせず、溶岩の上をはうように広げて体を支えています。"
               "また、谷や低い土地に流れこんだ溶岩は、水がたまっていた湖を埋めたり分けたりして、地形そのものを作り変えます。"),
    sources=[("国土交通省 観光庁 多言語解説（西湖と剗の海）", "https://www.mlit.go.jp/tagengo-db/common/001556177.pdf"),
             ("国土交通省 観光庁 多言語解説（Forests of Mt. Fuji）", "https://www.mlit.go.jp/tagengo-db/en/R1-00159.html"),
             ("日本地球惑星科学連合 2003年大会要旨（青木ヶ原溶岩と「せの湖」）", "https://www2.jpgu.org/meeting/2003/pdf/v055/v055-p012.pdf"),
             ("山梨県 富士箱根伊豆国立公園（青木ヶ原樹海）", "https://www.yamanashi-kankou.jp/kokuritsukoen/jp/miryoku/aokigaharajukai.html"),
             ("産総研 地質調査総合センター 20万分の1日本シームレス地質図V2", "https://gbank.gsj.jp/seamless/")],
    tags=["青木ヶ原樹海", "青木ヶ原", "西湖", "精進湖", "せの海", "貞観噴火", "富士山", "溶岩", "富士五湖", "山梨県",
          "富士河口湖町", "森林", "土壌", "絶景", "ふしぎな絶景", "地学", "科学", "shorts"],
    hashtags=["#絶景", "#科学", "#富士山", "#山梨", "#shorts"],
    pinned="樹海のまわりには、溶岩でできた風穴や氷穴もあります。次はどこのふしぎな絶景が見たい？",
    notes=["オレンジの範囲は地質図の「完新世の玄武岩の溶岩」で、青木ヶ原溶岩以外の新しい溶岩もふくむ。動画では「その溶岩」とだけ言った。",
           "光る粒は、富士山の方から溶岩が流れこんだ向きを表した演出で、実際の流れの道すじそのものではない。",
           "せの海の昔の形は推定なので、動画では形を描いていない（両方の湖に光の輪を出すだけ）。",
           "土の厚さは資料により平均3cm・十数cmと差があるため、動画では「とても薄い」と言った。",
           "樹海についての特定の話題（事件など）にはふれていない。写真もそうした名前のついたものは使っていない。"],
)
