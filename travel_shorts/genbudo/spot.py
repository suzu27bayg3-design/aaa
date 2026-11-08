"""ふしぎな絶景の科学 #1 玄武洞（兵庫県豊岡市）

事実の根拠:
- 約160万年前の火山活動でできた玄武岩の柱状節理 … 産総研 地質ニュース / 環境省
- 洞くつは江戸時代などに石を切り出した跡（採石場）… 豊岡市資料
- 「玄武洞」は1807年に柴野栗山が命名。1884年に小藤文次郎がここの石を「玄武岩」と命名 … 豊岡市資料
- 松山基範が、玄武洞の岩が今と逆向きに磁化していることを発見（1926年発見・1929年発表とする資料あり）… 環境省 / 神戸新聞
- 柱状節理：厚い溶岩が冷えて縮むとき、表面に割れ目ができ、六角形に近い柱になる（5〜7角形もまじる）
"""
import math

from PIL import Image, ImageDraw

import longform as L

TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 190, 90)
MAP_CREDITS = ["航空写真・陰影起伏: 出典 国土地理院（地理院タイルを加工して作成）",
               "地質図: 出典 産総研地質調査総合センター 20万分の1日本シームレス地質図V2（CC BY 4.0、玄武岩の範囲を抽出して加工）"]
PLACE = dict(name="玄武洞", pref="兵庫県豊岡市", lat=35.594, lon=134.808)


def _label(d, xy, s, size=34, fill=L.WHITE):
    d.text(xy, s, font=L.jp(size, True), fill=fill, anchor="mm", stroke_width=5,
           stroke_fill=L.WHITE if fill == L.NAVY else L.NAVY)


def _hex_centers(w, h, a):
    pts = []
    for row in range(-1, int(h / (a * 1.5)) + 2):
        for col in range(-1, int(w / (a * math.sqrt(3))) + 2):
            pts.append((col * a * math.sqrt(3) + (a * math.sqrt(3) / 2 if row % 2 else 0), row * a * 1.5))
    return pts


def cooling(t, lt):
    """上から見た溶岩：熱い（オレンジ）→ 冷えて灰色に。縮むにつれて六角形の割れ目が広がる"""
    W, H = 900, 640
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    k = min(1.0, lt / 3.0)  # 冷え方
    hot, cold = (255, 120, 40), (90, 95, 105)
    col = tuple(int(hot[i] * (1 - k) + cold[i] * k) for i in range(3))
    box = (40, 40, W - 40, H - 120)
    d.rounded_rectangle(box, 26, fill=col)
    cracks = Image.new("RGBA", (W, H))
    full = d
    d = ImageDraw.Draw(cracks)
    a = 70
    gap = 2 + 9 * k  # 縮むほど割れ目が広がる
    for cx, cy in _hex_centers(box[2] - box[0], box[3] - box[1], a):
        x, y = cx + box[0], cy + box[1]
        r = a - gap
        poly = [(x + r * math.cos(math.radians(60 * i + 30)), y + r * math.sin(math.radians(60 * i + 30))) for i in range(6)]
        if k > 0.15:
            d.polygon(poly, outline=(30, 30, 40), width=int(2 + 5 * k))
            # 中心へ向かう小さな矢印（縮む向き）
            if k < 0.95:
                for i in (0, 2, 4):
                    p = poly[i]
                    q = (p[0] + (x - p[0]) * 0.35, p[1] + (y - p[1]) * 0.35)
                    d.line([p, q], fill=(255, 255, 255, int(200 * k)), width=4)
    mask = Image.new("L", (W, H))
    ImageDraw.Draw(mask).rounded_rectangle(box, 26, fill=255)
    im.paste(cracks, (0, 0), Image.composite(cracks.split()[3], Image.new("L", (W, H)), mask))
    d = full
    _label(d, (W / 2, H - 70), "熱い溶岩 → 冷えて縮む → 六角形に割れる" if k < 1 else "割れ目が下へのびて、柱になる", 36,
           (255, 220, 120))
    return im


def columns(t, lt):
    """横から見た図：割れ目が冷えた面から内側へのびて、柱が並ぶ"""
    W, H = 900, 640
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    top, bot = 60, 500
    d.rectangle((40, top, W - 40, bot), fill=(95, 100, 110))
    grow = min(1.0, lt / 2.0)
    for i in range(1, 12):
        x = 40 + i * (W - 80) / 12
        y1 = top + (bot - top) * grow
        d.line([(x, top), (x + 6 * math.sin(i), y1)], fill=(25, 25, 35), width=7)
    d.rectangle((40, top - 30, W - 40, top), fill=(120, 170, 255))
    _label(d, (W / 2, top - 15), "冷たい空気（ここから冷える）", 28)
    _label(d, (W / 2, 560), "割れ目が下へのびる ＝ 柱状節理", 36, (255, 220, 120))
    return im


def magnet(t, lt):
    """今の地球の磁石と、玄武洞の岩に残った磁石の向きをくらべる"""
    W, H = 900, 640
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    flip = min(1.0, max(0.0, (lt - 0.8) / 0.8))
    for cx, name, ang in ((230, "今の地球", -90), (670, "玄武洞の岩", -90 + 180 * flip)):
        d.ellipse((cx - 170, 140, cx + 170, 480), fill=(240, 240, 245), outline=L.WHITE, width=6)
        r = math.radians(ang)
        tip = (cx + 140 * math.cos(r), 310 + 140 * math.sin(r))
        tail = (cx - 140 * math.cos(r), 310 - 140 * math.sin(r))
        n = (math.cos(r + math.pi / 2) * 28, math.sin(r + math.pi / 2) * 28)
        d.polygon([tip, (cx + n[0], 310 + n[1]), (cx - n[0], 310 - n[1])], fill=(230, 50, 60))
        d.polygon([tail, (cx + n[0], 310 + n[1]), (cx - n[0], 310 - n[1])], fill=(60, 90, 200))
        _label(d, (cx, 530), name, 40)
        _label(d, (cx, 110), "北", 34, (255, 220, 120))
    _label(d, (W / 2, 600), "N極とS極が入れかわっていた！", 38, (255, 220, 120))
    return im


import json
import os

from PIL import ImageFilter

_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
_AER = Image.open(os.path.join(_M, "aerial.jpg")).convert("RGBA")
_MASK = Image.open(os.path.join(_M, "basalt_mask.png")).convert("L")
_INFO = json.load(open(os.path.join(_M, "aerial.json")))
CROP = (250, 380, 1650, 1780)  # 航空写真（1792px四方）から使う範囲


def _px(lat, lon):
    z, (ox, oy) = _INFO["z"], _INFO["origin"]
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return (x - ox) * 256, (y - oy) * 256


def realmap(t, lt):
    """国土地理院の航空写真（陰影起伏を重ねて立体感）に、産総研の地質図から取り出した
    約160万年前の玄武岩の分布（むらさき）を重ねる。円山川の両岸に同じ溶岩がある"""
    S = 900
    x0, y0, x1, y1 = CROP
    z = 1.0 - 0.06 * min(1, lt / 6)  # ゆっくりズーム
    cw = (x1 - x0) * z
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    box = (cx - cw / 2, cy - cw / 2, cx + cw / 2, cy + cw / 2)
    sc = S / cw
    base = _AER.crop(tuple(int(v) for v in box)).resize((S, S), Image.BILINEAR)
    a = min(1.0, max(0.0, (lt - 1.0) / 0.8))
    if a > 0:
        m = _MASK.crop(tuple(int(v) for v in box)).resize((S, S), Image.BILINEAR).point(lambda v: int(v * 0.55 * a))
        base = Image.composite(Image.new("RGBA", (S, S), (210, 70, 210, 255)), base, m)
    im = Image.new("RGBA", (S, S + 60))
    im.paste(base, (0, 0))
    d = ImageDraw.Draw(im)
    to = lambda lat, lon: ((_px(lat, lon)[0] - box[0]) * sc, (_px(lat, lon)[1] - box[1]) * sc)  # noqa: E731
    # 円山川
    rx, ry = to(35.598, 134.803)
    _label(d, (rx - 40, ry - 40), "円山川", 32, (150, 210, 255))
    # 西岸の溶岩（二見山付近）
    if a > 0.5:
        wx, wy = to(35.5797, 134.7882)
        _label(d, (wx, wy - 10), "二見山付近", 34)
        _label(d, (wx, wy + 32), "（西岸の溶岩）", 28)
    # 流れの向き（推定）
    k = min(1.0, max(0.0, (lt - 2.4) / 1.0))
    if k > 0:
        sx, sy = to(35.5835, 134.7955)
        ex, ey = to(35.5925, 134.8045)
        mx, my = sx + (ex - sx) * k, sy + (ey - sy) * k
        d.line([(sx, sy), (mx, my)], fill=(255, 210, 80), width=10)
        if k >= 1:
            ang = math.atan2(ey - sy, ex - sx)
            d.polygon([(ex, ey), (ex - 30 * math.cos(ang - 0.5), ey - 30 * math.sin(ang - 0.5)),
                       (ex - 30 * math.cos(ang + 0.5), ey - 30 * math.sin(ang + 0.5))], fill=(255, 210, 80))
    # 玄武洞のピン
    gx, gy = to(35.594, 134.808)
    d.ellipse((gx - 18, gy - 58, gx + 18, gy - 22), fill=(230, 50, 60))
    d.polygon([(gx - 15, gy - 34), (gx + 15, gy - 34), (gx, gy)], fill=(230, 50, 60))
    _label(d, (gx + 95, gy - 40), "玄武洞", 36)
    # 凡例と出典
    if a > 0:
        d.rounded_rectangle((16, 16, 470, 70), 16, fill=(0, 0, 0, 170))
        d.rectangle((30, 30, 60, 56), fill=(210, 70, 210))
        d.text((74, 43), "約160万年前の玄武岩の溶岩", font=L.jp(28, True), fill=L.WHITE, anchor="lm")
    d.text((S / 2, S + 30), "出典：国土地理院（航空写真・陰影起伏）／産総研（シームレス地質図V2）を加工",
           font=L.jp(22, True), fill=(220, 230, 240), anchor="mm")
    return im


FIGS = {"cooling": cooling, "columns": columns, "magnet": magnet, "realmap": realmap}

SCENES = [
    dict(spk="Z", ex="think", say="この六角形の柱、だれが作ったのだ？",
         read="この、ろっかっけいの柱、だれが作ったのだ？",
         head="だれが作った？", show=("photo", "Genbudo_Cave_2018.jpg", "in")),
    dict(spk="M", say="ここは兵庫県豊岡市の玄武洞。約160万年前の溶岩でできた、自然の柱なの。",
         read="ここは、ひょうごけん、とよおかしの、げんぶどう。やく、ひゃくろくじゅうまんねん前の溶岩でできた、自然の柱なの。",
         head="自然が作った柱", sub="約160万年前の溶岩", show=("map",), head_y=1340),
    dict(spk="M", say="むらさきが同じ溶岩よ。円山川の西の、二見山のあたりで噴火して、川の両側に広がっていたと考えられているの。",
         read="むらさきが、同じ溶岩よ。まるやまがわの西の、ふたみやまのあたりで噴火して、川の両側に、広がっていたと考えられているの。",
         head="両岸に同じ溶岩", show=("fig", "realmap"), head_y=1320),
    dict(spk="M", say="厚い溶岩は、冷えて固まるときに縮むの。縮む力でひび割れて、六角形に近い柱に分かれたのよ。",
         read="厚い溶岩は、冷えて固まるときに、ちぢむの。ちぢむ力で、ひび割れて、ろっかっけいに近い柱に、分かれたのよ。",
         head="冷えて縮むと\n割れる", sub="柱状節理", show=("fig", "cooling")),
    dict(spk="Z", say="川がけずった崖から、昔の人が石を切り出して、洞くつになったのだ！",
         read="川が、けずった崖から、昔の人が、石を切り出して、洞くつになったのだ！",
         head="洞くつは\n石切り場のあと", show=("photo", "Genbudo_Cave_2018_2.jpg", "right")),
    dict(spk="M", say="しかもここの岩は、今と逆向きの磁石になっていたの。地球のN極とS極が入れかわっていた証拠になったのよ。",
         read="しかも、ここの岩は、今と逆向きの、磁石になっていたの。地球の、エヌきょくと、エスきょくが、入れかわっていた証拠になったのよ。",
         head="地球の磁石が\n逆だった！", sub="1926年 松山基範が発見", show=("fig", "magnet")),
    dict(spk="Z", say="自然と地球のふしぎがつまった柱なのだ！行ってみたいのだ？",
         head="行ってみたい？", show=("photo", "Genbudo_Cave_2018_3.jpg", "out")),
]

META = dict(
    title="六角形の柱は誰が作った？兵庫・玄武洞のふしぎ #shorts #絶景 #科学",
    alt_titles=["自然が作った六角形の柱！玄武洞はこうしてできた #shorts #ジオパーク",
                "地球の磁石が逆だった証拠が見つかった場所 #shorts #科学 #兵庫"],
    lead="兵庫県豊岡市の玄武洞には、六角形に近い石の柱がずらりと並びます。人が作ったのではなく、約160万年前の溶岩が冷えるときにできた自然の形です。",
    points=["溶岩は円山川の西の二見山付近で噴火し、川の両岸に同じ玄武岩が残っている（産総研の地質図で確認）",
            "厚い溶岩は冷えて固まるとき縮み、六角形に近い形にひび割れて柱になる（柱状節理）",
            "川がけずった崖から石を切り出したあとが、今の洞くつ",
            "ここの岩は今と逆向きに磁化していて、地球の磁場（N極とS極）の逆転を示す発見につながった"],
    principle=("ものは冷えると縮みます。厚い溶岩が冷えて固まるとき、縮もうとする力で表面に割れ目ができます。割れ目は"
               "力をいちばん効率よく逃がせる形として、3本が約120度で交わりやすく、全体として六角形に近い網目になります"
               "（実際には5角形や7角形もまじります）。この割れ目が、冷えた面から内側へ少しずつのびていくので、柱が並んだ形"
               "（柱状節理）になります。また、溶岩にふくまれる鉄の鉱物は、冷えて固まるときのまわりの地磁気の向きに磁化します。"
               "玄武洞の岩は今と逆向きに磁化していて、昔は地球のN極とS極が入れかわっていたことを示す証拠になりました。"),
    sources=[("環境省 山陰海岸国立公園（玄武洞）", "https://www.env.go.jp/nature/nationalparks/try/all/act883.html"),
             ("産総研 地質調査総合センター 地質ニュース", "https://www.gsj.jp/data/chishitsunews/05_11_07.pdf"),
             ("豊岡市 資料（玄武洞の名前と採石の歴史）",
              "https://www.city.toyooka.lg.jp/_res/projects/default_project/_page_/001/002/653/0203.pdf"),
             ("産総研 地質調査総合センター 20万分の1日本シームレス地質図V2", "https://gbank.gsj.jp/seamless/"),
             ("国土地理院 地理院タイル（航空写真・陰影起伏・標準地図）", "https://maps.gsi.go.jp/development/ichiran.html"),
             ("日本の地質案内（玄武洞：アルカリかんらん石玄武岩・層厚約100m）",
              "https://www.web-gis.jp/GS_GeoGuide/GeoDocument/GeoSite_J05-003.html"),
             ("神戸新聞（玄武洞と松山基範）", "https://www.kobe-np.co.jp/rentoku/bunkazai/201606/0009237092.shtml")],
    tags=["玄武洞", "げんぶどう", "柱状節理", "玄武岩", "山陰海岸ジオパーク", "ジオパーク", "兵庫県", "豊岡市", "城崎",
          "絶景", "ふしぎな絶景", "地磁気逆転", "松山基範", "地学", "科学", "観光", "ずんだもん", "四国めたん", "shorts"],
    hashtags=["#絶景", "#科学", "#玄武洞", "#ジオパーク", "#shorts"],
    pinned="アイスランドや北アイルランドにも六角形の柱が並ぶ場所があります。次はどこのふしぎな絶景が見たい？コメントで教えてください！",
    notes=["噴出源は産総研 第四紀火山データベースの「円山川左岸の二見山に噴出源のスコリア丘」に従った。来日岳とする地域資料もある。",
           "地図のむらさきは20万分の1地質図の「第四紀カラブリアン期のアルカリ玄武岩」の範囲。縮尺が小さいので境界はおおよそ。",
           "流れの向きの矢印は、噴出源が西岸にあることからの推定として「考えられている」と表現した。",
           "発見の年は資料によって1926年（発見）と1929年（発表）があるため、見出しは「1926年 発見」とし、説明欄では発表年にふれていない。",
           "「六角形」は「六角形に近い」と言い、5角形や7角形もまじることを説明欄に書いた。",
           "写真は Wikimedia Commons の CC0（著作権放棄）のもの。大きい画像は Commons の自動取得制限で取れず、幅500pxを使用。"],
)
