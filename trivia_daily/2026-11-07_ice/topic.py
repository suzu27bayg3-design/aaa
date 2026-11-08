"""毎日の科学の雑学 2026-11-07「氷はなぜ水に浮く？」（化学）

事実の根拠:
- 凍ると水素結合で分子がすき間の多い六角形の結晶に並び、液体より密度が小さくなる（氷 約0.92 g/cm3、水 約1.00 g/cm3）
  … Britannica / University of Leeds
- 同じ重さなら氷は水より約1割（約9%）体積が大きい … 0.917 → 1/0.917 ≈ 1.09
- 淡水は約4℃で最も重くなるため、湖は上から凍り、底には約4℃の水が残る … University of Illinois / University of Leeds / Britannica
"""
import math

from PIL import Image, ImageDraw

import longform as L

TITLE = "氷が浮く秘密"
ACCENT = (150, 220, 255)
BG = ((20, 70, 130), (6, 18, 48))
SOURCE_NOTE = "出典: Britannica / University of Leeds / University of Illinois"

O, H = (235, 80, 90), (245, 245, 255)


def _label(d, xy, s, size=34, fill=L.WHITE):
    stroke = L.WHITE if fill == L.NAVY else L.NAVY  # 暗い文字は白ぶち、明るい文字は紺ぶち
    d.text(xy, s, font=L.jp(size, True), fill=fill, anchor="mm", stroke_width=5, stroke_fill=stroke)


def _mol(d, x, y, a, s=1.0):
    """水分子：赤い酸素に白い水素が2つ（約104度の角度）"""
    for da in (-52, 52):
        r = math.radians(a + da)
        hx, hy = x + math.cos(r) * 20 * s, y + math.sin(r) * 20 * s
        d.ellipse((hx - 9 * s, hy - 9 * s, hx + 9 * s, hy + 9 * s), fill=H)
    d.ellipse((x - 15 * s, y - 15 * s, x + 15 * s, y + 15 * s), fill=O)


def molecules(t, lt):
    """左：液体の水（ぎゅっと詰まって動き回る）／右：氷（六角形に並び、すき間が多い）"""
    W, Hh = 860, 600
    im = Image.new("RGBA", (W, Hh))
    d = ImageDraw.Draw(im)
    for x0, name in ((20, "水（液体）"), (450, "氷（固体）")):
        d.rounded_rectangle((x0, 60, x0 + 390, 520), 30, fill=(255, 255, 255, 25), outline=(180, 220, 255), width=4)
        _label(d, (x0 + 195, 555), name)
    k = 0
    for gy in range(7):
        for gx in range(6):
            k += 1
            x = 60 + gx * 62 + 12 * math.sin(t * 3 + k * 1.7)
            y = 100 + gy * 60 + 12 * math.cos(t * 2.6 + k * 2.3)
            _mol(d, x, y, (k * 77 + t * 90) % 360, 0.9)
    # 氷：六角形（ハチの巣）の頂点に分子。線は水素結合
    cx, cy, a = 645, 290, 62
    pts = []
    for row in range(-3, 4):
        for col in range(-2, 3):
            hx = cx + col * a * 1.5
            hy = cy + row * a * math.sqrt(3) + (a * math.sqrt(3) / 2 if col % 2 else 0)
            for v in range(6):
                ang = math.radians(60 * v)
                pts.append((round(hx + a * math.cos(ang)), round(hy + a * math.sin(ang))))
    pts = sorted(set(p for p in pts if 470 < p[0] < 820 and 80 < p[1] < 500))
    for i, p in enumerate(pts):
        for q in pts[i + 1:]:
            if abs(math.dist(p, q) - a) < 4:
                d.line([p, q], fill=(140, 200, 255, 160), width=4)
    for i, p in enumerate(pts):
        _mol(d, p[0], p[1], 90 + 60 * (i % 3), 0.75)
    return im


def volume(t, lt):
    """同じ重さの水と氷。氷は約1割大きい"""
    W, Hh = 860, 600
    im = Image.new("RGBA", (W, Hh))
    d = ImageDraw.Draw(im)
    grow = min(1.0, lt / 1.5)
    base = 500
    for x0, h, name, col in ((120, 300, "水 100", (90, 160, 255)), (500, 300 * (1 + 0.09 * grow), "氷 109", (200, 235, 255))):
        d.rectangle((x0, base - h, x0 + 240, base), fill=col, outline=L.WHITE, width=5)
        _label(d, (x0 + 120, base - h / 2), name, 48, L.NAVY if "氷" in name else L.WHITE)
    d.line((90, base - 300, 790, base - 300), fill=(255, 220, 90), width=4)
    _label(d, (430, 60), "同じ重さで比べると…", 36)
    _label(d, (430, 550), "氷は約1割大きい ＝ 水より軽い", 36, (255, 220, 90))
    return im


def lake(t, lt):
    """冬の湖の断面：上に氷のふた、底には約4℃の重い水。魚が泳ぐ"""
    W, Hh = 860, 600
    im = Image.new("RGBA", (W, Hh))
    d = ImageDraw.Draw(im)
    top, bot = 120, 540
    for y in range(top, bot):  # 上ほど冷たい（白っぽい）、底ほど4℃（青）
        f = (y - top) / (bot - top)
        d.line((40, y, W - 40, y), fill=(int(170 - 120 * f), int(210 - 90 * f), int(250 - 40 * f)))
    d.rectangle((40, 80, W - 40, top), fill=(235, 248, 255), outline=L.WHITE, width=4)
    _label(d, (W / 2, 100), "氷（0℃）＝ふた", 34, L.NAVY)
    _label(d, (W - 150, 200), "0℃に近い", 30)
    _label(d, (W - 150, 500), "約4℃（一番重い）", 30, (255, 220, 90))
    for i in range(3):
        x = 120 + ((t * 70 + i * 260) % 620)
        y = 330 + i * 55 + 12 * math.sin(t * 2 + i)
        d.ellipse((x - 40, y - 18, x + 30, y + 18), fill=(255, 170, 80))
        d.polygon([(x - 38, y), (x - 70, y - 20), (x - 70, y + 20)], fill=(255, 140, 60))
        d.ellipse((x + 12, y - 8, x + 20, y), fill=L.NAVY)
    return im


FIGS = {"molecules": molecules, "volume": volume, "lake": lake}

SCENES = [
    dict(spk="Z", ex="think", say="ふつう固体は液体に沈むのに、氷はどうして水に浮くのだ？",
         read="ふつう、こたいは、えきたいに沈むのに、氷は、どうして水に浮くのだ？",
         head="氷はなぜ\n浮く？", fig="🧊"),
    dict(spk="M", ex="explain", say="水の分子は、水素結合という手で、となりの分子とつながっているの。",
         read="水の分子は、すいそけつごう、という手で、となりの分子と、つながっているの。",
         head="分子が\n手をつなぐ", sub="水素結合", fig="molecules"),
    dict(spk="M", ex="smug", say="凍ると六角形にきっちり並んで、すき間の多い形になるの。同じ重さでも、体積が約1割大きくなるのよ。",
         read="こおると、ろっかっけいに、きっちり並んで、すき間の多い形になるの。同じ重さでも、体積が、やく、いちわり大きくなるのよ。",
         head="すき間で\n約1割ふくらむ", sub="だから水より軽い", fig="volume"),
    dict(spk="Z", ex="panic", say="もし氷が沈んだら、どうなるのだ！？", head="もし氷が\n沈んだら？", fig="🐟"),
    dict(spk="M", ex="explain", say="湖は底から凍ってしまうわ。実際は氷が上でふたになって、底には4度くらいの水が残るの。",
         read="湖は、底から凍ってしまうわ。実際は、氷が上で、ふたになって、底には、よんどくらいの水が残るの。",
         head="氷がふたになる", sub="淡水は約4℃で一番重い", fig="lake"),
    dict(spk="Z", ex="happy", say="すき間のおかげで、魚も冬をこせるのだ！だから氷は浮くのだ！",
         read="すき間のおかげで、魚も、冬をこせるのだ！だから、氷は浮くのだ！",
         head="すき間が\n命を守る", fig="lake"),
]

META = dict(
    title="氷はなぜ水に浮く？すき間が命を守っていた #shorts #科学 #雑学",
    alt_titles=["固体なのに浮く！氷が水より軽いのはなぜ？ #shorts #科学",
                "もし氷が沈んだら湖の魚は…？水のふしぎ #shorts #雑学"],
    lead="ふつう固体は液体より重いのに、氷は水に浮きます。その理由は、凍るときにできる「すき間」にあります。",
    points=["水の分子は「水素結合」でとなりの分子と引き合っている",
            "凍ると分子が六角形に並び、すき間の多い結晶になる（同じ重さで体積が約1割大きい）",
            "淡水は約4℃で一番重いので、湖は上から凍り、底に約4℃の水が残って魚が冬を越せる"],
    principle=("水の分子（H₂O）は、酸素がわずかにマイナス、水素がわずかにプラスの電気を帯びているため、となりの分子の酸素と"
               "水素が引き合います（水素結合）。液体ではこの結びつきが切れたりつながったりしながら分子が詰まっていますが、凍ると"
               "1つの分子が4つの分子と決まった角度で結びつき、六角形のすき間の多い結晶になります。そのため氷の密度は約0.92 g/cm³と"
               "水（約1.00 g/cm³）より小さく、アルキメデスの原理で浮きます。また淡水は約4℃で最も密度が大きくなるので、冬の湖では"
               "冷たい水が上に残って表面から凍り、氷がふたの役目をして下の水が凍りにくくなります。"),
    sources=[("Britannica「Why Does Water Freeze from the Top Down?」",
              "https://www.britannica.com/story/why-does-water-freeze-from-the-top-down"),
             ("University of Leeds「Properties of water」",
              "https://see.leeds.ac.uk/enviroweb/hydrosphere/2_properties_of_water/waterp3.php"),
             ("University of Illinois Physics Van「Water at 4 deg C」",
              "https://van.physics.illinois.edu/ask/listing/1736")],
    tags=["氷はなぜ浮く", "氷が浮く理由", "氷", "水", "水素結合", "密度", "4℃", "湖が凍る", "化学", "理科",
          "科学", "雑学", "豆知識", "ずんだもん", "四国めたん", "VOICEVOX", "shorts"],
    hashtags=["#科学", "#雑学", "#化学", "#ずんだもん", "#shorts"],
    pinned="冬に水道管が破れることがあるのも、凍ると水がふくらむから。ほかに知りたい「水のふしぎ」があればコメントで！🧊",
    notes=["「約1割」は氷0.917 g/cm³・水1.00 g/cm³から 1/0.917 ≈ 1.09。資料によって氷の密度に少し差がある（0.92前後）。",
           "「約4℃で一番重い」は淡水の話。海水は凍る直前まで重くなり続けるので、湖の話に限定した。",
           "「浅い湖は底まで凍ることもある」ため、「湖は凍らない」とは言っていない。"],
)
