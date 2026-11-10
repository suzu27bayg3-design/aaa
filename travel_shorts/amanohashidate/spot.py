"""ふしぎな絶景の科学 #3 天橋立（京都府宮津市）

事実の根拠:
- 宮津市江尻から南の文珠まで、長さ約3.6km・幅20〜150mで、宮津湾と阿蘇海を分ける砂州 … 京都府
- 南へ向かう沿岸漂砂（丹後半島東岸の川から出た土砂が波で運ばれる）がたまってできた … 京都府
- 8〜9千年前の海面上昇が止まったころに、でき始めた可能性 … 京都府
- 昭和初期から砂浜がやせ始め、突堤などをつくった。1986年（昭和61年）から、宮津港周辺にたまった砂を江尻側の付け根に入れ、
  波の力で砂浜を戻す「サンドバイパス」を行っている … 京都府
- 名前は、丹後国風土記の「イザナギが天へ通うために立てたはしごが倒れた」という伝説から … 京都府丹後広域振興局
"""
import math
import os

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

import longform as L

TITLE = "ふしぎな絶景の科学"
ACCENT = (120, 210, 230)
PLACE = dict(name="天橋立", pref="京都府宮津市", lat=35.570, lon=135.191)
MAP_CREDITS = ["航空写真（現在・1961〜69年・1974〜78年）: 出典 国土地理院（地理院タイルを加工して作成）"]

_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
_WIDE = Image.open(os.path.join(_M, "photo_z14.jpg")).convert("RGB")
CROP = (180, 560, 1080, 1280)  # 色のそろった範囲（北の海岸〜天橋立）
GOLD = (255, 214, 120)


def _label(d, xy, s, size=34, fill=L.WHITE):
    d.text(xy, s, font=L.jp(size, True), fill=fill, anchor="mm", stroke_width=5,
           stroke_fill=L.WHITE if fill == L.NAVY else L.NAVY)


# 砂の通り道（海岸線の少し海側。航空写真 z14 の座標）
COAST = [(780, 560), (700, 640), (662, 720), (632, 790), (592, 845), (548, 885)]
BAR = [(548, 885), (505, 950), (466, 1018), (436, 1078), (410, 1130)]
PATH = COAST + BAR[1:]
_SEG = [math.dist(PATH[i], PATH[i + 1]) for i in range(len(PATH) - 1)]
_TOT = sum(_SEG)
_RNG = np.random.default_rng(3)
_P = [(_RNG.uniform(0, 1), _RNG.normal(0, 7), _RNG.uniform(0.8, 1.2)) for _ in range(160)]


def _at(s):
    s = max(0.0, min(_TOT - 0.01, s))
    for i, l in enumerate(_SEG):
        if s <= l:
            f = s / l
            return PATH[i][0] + (PATH[i + 1][0] - PATH[i][0]) * f, PATH[i][1] + (PATH[i + 1][1] - PATH[i][1]) * f, i
        s -= l
    return PATH[-1][0], PATH[-1][1], len(PATH) - 2


def _darken(im, k=0.55):
    return ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.75)).enhance(k)


def _glow_frame(t, settle=False):
    """光る粒（砂）が海岸にそって南へ流れる。settle=True なら天橋立の上で止まって積もる"""
    base = _darken(_WIDE)
    glow = Image.new("RGB", _WIDE.size)
    d = ImageDraw.Draw(glow)
    for u, off, sp in _P:
        s0 = (u * _TOT + t * 110 * sp) % _TOT
        if settle and s0 > sum(_SEG[:len(COAST) - 1]):  # 天橋立に入った粒はゆっくり
            s0 = sum(_SEG[:len(COAST) - 1]) + (s0 - sum(_SEG[:len(COAST) - 1])) * 0.6
        for j in range(8):
            x, y, i = _at(s0 - j * 7)
            nx, ny = -(PATH[i + 1][1] - PATH[i][1]), PATH[i + 1][0] - PATH[i][0]
            nl = math.hypot(nx, ny) or 1
            x, y = x + off * nx / nl, y + off * ny / nl
            c = 1 - j / 8
            r = 3.4 - j * 0.32
            d.ellipse((x - r, y - r, x + r, y + r), fill=tuple(int(v * c) for v in GOLD))
    if settle:  # 積もった砂州を光らせる
        a = 0.5 + 0.5 * math.sin(t * 2)
        d.line(BAR, fill=tuple(int(v * (0.35 + 0.25 * a)) for v in GOLD), width=18, joint="curve")
    out = ImageChops.add(ImageChops.add(base, glow.filter(ImageFilter.GaussianBlur(6))), glow)
    return out.crop(CROP)


def _frame_box(im, notes):
    im = im.convert("RGBA")
    d = ImageDraw.Draw(im)
    for text, xy, size, col in notes:
        _label(d, xy, text, size, col)
    d.text((im.width - 12, im.height - 14), "出典：国土地理院", font=L.jp(20, True), fill=(220, 230, 240), anchor="rm")
    return im


def flow(t, lt):
    im = _glow_frame(t)
    return _frame_box(im, [("丹後半島の川から出た砂", (640, 40), 30, GOLD),
                           ("波で南へ運ばれる ↓", (640, 90), 30, GOLD),
                           ("宮津湾", (700, 520), 34, L.WHITE), ("阿蘇海", (150, 520), 34, L.WHITE)])


def grow(t, lt):
    im = _glow_frame(t, settle=True)
    return _frame_box(im, [("湾の入口にたまって", (640, 40), 30, GOLD), ("細長くのびた", (640, 90), 30, GOLD),
                           ("天橋立", (180, 380), 40, L.WHITE), ("宮津湾", (700, 520), 34, L.WHITE)])


ERAS = [("1961〜69年", "old1961_z15.jpg"), ("1974〜78年", "old1974_z15.jpg"), ("現在", "photo_z15.jpg")]
_ERA_IMS = [Image.open(os.path.join(_M, f)).convert("RGB").crop((120, 120, 680, 680)).resize((880, 880)) for _, f in ERAS]


def eras(t, lt):
    """同じ場所の航空写真を、昔から今へ切りかえる"""
    seg = 1.6
    i = min(2, int(lt / seg))
    f = min(1.0, max(0.0, (lt - i * seg) / 0.5)) if i > 0 else 1.0
    im = _ERA_IMS[i] if f >= 1 else Image.blend(_ERA_IMS[i - 1], _ERA_IMS[i], f)
    im = im.convert("RGBA")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, 330, 90), 20, fill=(0, 0, 0, 170))
    d.text((175, 55), ERAS[i][0], font=L.jp(40, True), fill=GOLD, anchor="mm")
    d.text((im.width - 12, im.height - 14), "出典：国土地理院（空中写真）", font=L.jp(20, True), fill=(220, 230, 240), anchor="rm")
    return im


def bypass(t, lt):
    """今の守り方：港のまわりにたまった砂を、天橋立の付け根（江尻）に入れる → 波が南へ運んで砂浜にもどす"""
    base = _darken(_WIDE, 0.6)
    glow = Image.new("RGB", _WIDE.size)
    d = ImageDraw.Draw(glow)
    seg = [math.dist(BAR[i], BAR[i + 1]) for i in range(len(BAR) - 1)]
    tot = sum(seg)
    for u, off, sp in _P[:90]:
        s0 = (u * tot + t * 70 * sp) % tot
        for j in range(7):
            ss = max(0.0, s0 - j * 7)
            for i, l in enumerate(seg):
                if ss <= l:
                    f = ss / l
                    x = BAR[i][0] + (BAR[i + 1][0] - BAR[i][0]) * f + off * 0.8
                    y = BAR[i][1] + (BAR[i + 1][1] - BAR[i][1]) * f
                    break
                ss -= l
            c = 1 - j / 7
            r = 3.2 - j * 0.35
            d.ellipse((x - r, y - r, x + r, y + r), fill=tuple(int(v * c) for v in GOLD))
    rx, ry = BAR[0]
    for k in range(3):  # 付け根で砂を入れる（広がる輪）
        ph = (t * 0.8 + k / 3) % 1
        rr = 10 + 50 * ph
        d.ellipse((rx - rr, ry - rr, rx + rr, ry + rr), outline=tuple(int(v * (1 - ph)) for v in GOLD), width=4)
    out = ImageChops.add(ImageChops.add(base, glow.filter(ImageFilter.GaussianBlur(5))), glow).crop(CROP)
    return _frame_box(out, [("サンドバイパス（1986年〜）", (640, 40), 32, GOLD),
                            ("港のまわりの砂を付け根へ", (rx - CROP[0] + 200, ry - CROP[1] - 30), 28, GOLD),
                            ("↓ 波が南へ運ぶ", (rx - CROP[0] + 150, ry - CROP[1] + 110), 28, L.WHITE),
                            ("宮津湾", (700, 520), 34, L.WHITE)])


FIGS = {"flow": flow, "grow": grow, "eras": eras, "bypass": bypass}

SCENES = [
    dict(spk="Z", ex="panic", say="海の上に、松の道が続いてるのだ！？",
         head="海の上に\n松の道！？", show=("photo", "Amanohashidate_-_Amanohashidate7584.jpg", "in")),
    dict(spk="M", say="京都府宮津市の天橋立。日本三景のひとつで、長さ約3.6キロの砂の道なの。",
         read="きょうとふ、みやづしの、あまのはしだて。にほんさんけいの、ひとつで、長さ、やく、さんてんろくキロの、砂の道なの。",
         head="天橋立", sub="長さ 約3.6km", show=("zoom",), head_y=1340),
    dict(spk="M", say="丹後半島の川から海に出た砂が、波で少しずつ南へ運ばれていくの。",
         read="たんごはんとうの、川から海に出た砂が、波で少しずつ、南へ運ばれていくの。",
         head="① 砂が\n南へ運ばれる", show=("fig", "flow"), head_y=1230),
    dict(spk="M", say="その砂が湾の入口にたまって、細長くのびたのが天橋立。8千年ほど前から、でき始めたと考えられているわ。",
         read="その砂が、湾の入口にたまって、細長くのびたのが、あまのはしだて。はっせんねんほど前から、でき始めたと、考えられているわ。",
         head="② たまって\n細長くのびた", sub="砂州", show=("fig", "grow"), head_y=1190),
    dict(spk="Z", say="昔と今の航空写真をくらべると、海側の砂浜の形が変わっているのだ！",
         read="昔と今の、こうくうしゃしんを、くらべると、海側の砂浜の形が、変わっているのだ！",
         head="昔と今を\nくらべると", show=("fig", "eras"), head_y=1270),
    dict(spk="M", say="昭和のはじめから砂がやせてきたの。今は、港にたまった砂を付け根に運んで、波の力で砂浜をもどしているのよ。",
         read="しょうわの、はじめから、砂が、やせてきたの。今は、港にたまった砂を、付け根に運んで、波の力で、砂浜をもどしているのよ。",
         head="③ 人が砂を運んで\n守っている", show=("fig", "bypass"), head_y=1230),
    dict(spk="Z", say="神様のはしごが倒れてできた、という伝説もあるのだ！行ってみたいのだ？",
         read="かみさまの、はしごが倒れてできた、という伝説もあるのだ！行ってみたいのだ？",
         head="行ってみたい？", show=("photo", "Amanohashidate_-_Amanohashidate7592.jpg", "out")),
]

META = dict(
    title="海の上に松の道！天橋立は砂が作った #shorts #絶景 #科学",
    alt_titles=["天橋立はどうやってできた？砂の流れを航空写真で見る #shorts #日本三景",
                "やせていく天橋立を人が守っている！？ #shorts #科学 #京都"],
    lead="京都府宮津市の天橋立は、長さ約3.6km、幅20〜150mの細長い砂の道（砂州）です。海の流れが運んだ砂がたまってできました。",
    points=["① 丹後半島の東側の川から海に出た砂が、波によって少しずつ南へ運ばれる（沿岸漂砂）",
            "② 砂が宮津湾の入口にたまって細長くのび、宮津湾と阿蘇海を分ける砂州になった。8〜9千年前ごろからでき始めた可能性がある",
            "③ 昭和のはじめから砂浜がやせ、1986年からは港のまわりにたまった砂を天橋立の付け根に入れて、波の力で砂浜をもどす「サンドバイパス」を行っている",
            "名前は、イザナギが天へ通うために立てたはしごが倒れた、という丹後国風土記の伝説から"],
    principle=("波が海岸にななめに打ち寄せると、砂は波に持ち上げられて、少しずつ横へずれながら運ばれます（沿岸漂砂）。"
               "天橋立では、この砂の流れが南向きにそろっていて、流れがゆるむ湾の入口で砂がたまり、細長くのびて砂州になりました。"
               "砂州は、砂が入ってくる量と出ていく量のつり合いで形が保たれます。川から来る砂が減ると、波に削られる量の方が多くなって"
               "やせてしまうため、今は人が砂を運んで流れの上手側に入れ、つり合いを保っています。"),
    sources=[("京都府「海岸（天橋立の砂州と侵食対策）」", "https://www.pref.kyoto.jp/kanri/documents/05-13kaigan.pdf"),
             ("京都府「サンドバイパス事業」", "https://www.pref.kyoto.jp/kowanji/1197619883097.html"),
             ("京都府レッドデータブック（天橋立の地形）", "https://www.pref.kyoto.jp/kankyo/rdb/geo/db/sur0021.html"),
             ("京都府丹後広域振興局（天橋立の名前の由来）", "https://www.pref.kyoto.jp/tango/tango-doboku/documents/hashidatehikitugu.pdf")],
    tags=["天橋立", "あまのはしだて", "日本三景", "砂州", "沿岸漂砂", "サンドバイパス", "宮津", "宮津市", "京都府", "丹後",
          "絶景", "ふしぎな絶景", "地形", "地学", "科学", "観光", "航空写真", "shorts"],
    hashtags=["#絶景", "#科学", "#天橋立", "#日本三景", "#shorts"],
    pinned="股のぞきで見ると、天にかかる橋のように見えるとか。次はどこのふしぎな絶景が見たい？コメントで教えてください！",
    notes=["砂の流れの光る粒は、京都府の「南へ向かう沿岸漂砂」という説明にもとづく演出。粒の通り道は海岸線にそった目安。",
           "「地震で持ち上がった」説は信頼できる資料で確認できなかったので入れていない。",
           "昔の航空写真は国土地理院の1961〜69年・1974〜78年の空中写真。年代ごとに撮影の色や明るさがちがう。",
           "サンドバイパスの場面は、付け根（江尻側）に砂を入れ、波が南へ運ぶことだけを示している（運ぶ道すじは描いていない）。"],
)
