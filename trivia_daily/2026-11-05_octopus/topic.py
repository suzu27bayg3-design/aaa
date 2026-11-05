"""毎日の雑学ショート 2026-11-05「タコの心臓は3つ」

事実の根拠:
- 心臓は3つ（えら心臓2つ＋体の心臓1つ）、血はヘモシアニン（銅）で酸素と結びつくと青い … Smithsonian / Britannica
- ジェット推進で泳ぐと体の心臓が止まる。長くは泳ぎ続けられない … Wells et al. (1987) J. Exp. Biol. 131, 175–187
"""
import math

from PIL import Image, ImageDraw

import longform as L

TITLE = "タコのからだの秘密"
ACCENT = (120, 200, 255)
BG = ((30, 40, 110), (6, 12, 40))
SOURCE_NOTE = "出典: Wells et al. J. Exp. Biol. (1987) / Smithsonian / Britannica"

RED, BLUE, GRAY = (235, 70, 90), (70, 140, 255), (120, 125, 140)


def _heart(d, cx, cy, r, color, outline=(255, 255, 255)):
    """ハート形（2つの円＋三角形）"""
    d.ellipse((cx - r, cy - r * 0.9, cx, cy + r * 0.1), fill=color)
    d.ellipse((cx, cy - r * 0.9, cx + r, cy + r * 0.1), fill=color)
    d.polygon([(cx - r * 0.98, cy - r * 0.25), (cx + r * 0.98, cy - r * 0.25), (cx, cy + r)], fill=color)


def _body(stopped=False, t=0.0, lt=0.0):
    W, H = 820, 620
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    # タコの頭（外とう膜）と足を、うすい線で描く
    d.ellipse((210, 20, 610, 400), fill=(255, 140, 120, 60), outline=(255, 170, 150, 200), width=6)
    for i in range(8):
        x = 230 + i * 52
        pts = [(x + 18 * math.sin(t * 2 + i + k / 3), 380 + k * 22) for k in range(10)]
        d.line(pts, fill=(255, 170, 150, 180), width=14, joint="curve")
    beat = 0.5 + 0.5 * math.sin(t * 2 * math.pi * 1.3)
    # えら心臓（左右）：えらに血を送る
    for cx in (290, 530):
        r = 58 + 10 * beat
        _heart(d, cx, 250, r, BLUE)
    # 体の心臓（まん中）：体じゅうに血を送る
    if stopped and lt > 0.8:
        _heart(d, 410, 150, 62, GRAY)
        d.line((350, 90, 470, 210), fill=RED, width=14)
        d.line((470, 90, 350, 210), fill=RED, width=14)
    else:
        _heart(d, 410, 150, 62 + 12 * beat, RED)
    f = L.jp(34, True)
    for cx in (290, 530):
        d.text((cx, 335), "えら心臓", font=f, fill=L.WHITE, anchor="mm", stroke_width=5, stroke_fill=L.NAVY)
    d.text((410, 232), "体の心臓", font=f, fill=L.WHITE if not (stopped and lt > 0.8) else (255, 120, 120),
           anchor="mm", stroke_width=5, stroke_fill=L.NAVY)
    if stopped:
        # ジェット噴射の水しぶき
        for k in range(6):
            y = 470 + ((lt * 300 + k * 40) % 150)
            d.ellipse((650 + k * 18, y, 676 + k * 18, y + 26), fill=(160, 220, 255, 200))
    return im


def hearts(t, lt):
    return _body(False, t, lt)


def jet(t, lt):
    return _body(True, t, lt)


def blood(t, lt):
    W, H = 820, 560
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    for i, (cx, col, who, metal, name) in enumerate(((220, RED, "ヒト", "鉄 Fe", "ヘモグロビン"),
                                                       (600, BLUE, "タコ", "銅 Cu", "ヘモシアニン"))):
        if i == 1 and lt < 0.5:
            continue
        d.polygon([(cx, 60), (cx - 120, 290), (cx + 120, 290)], fill=col)
        d.ellipse((cx - 125, 200, cx + 125, 450), fill=col)
        d.text((cx, 330), metal, font=L.jp(56), fill=L.WHITE, anchor="mm", stroke_width=6, stroke_fill=L.NAVY)
        d.text((cx, 500), f"{who}：{name}", font=L.jp(38, True), fill=L.WHITE, anchor="mm",
               stroke_width=5, stroke_fill=L.NAVY)
    return im


FIGS = {"hearts": hearts, "jet": jet, "blood": blood}

SCENES = [
    dict(spk="Z", ex="think", say="タコの心臓って、いくつあるか知ってるのだ？",
         head="タコの心臓は\nいくつ？", fig="🐙"),
    dict(spk="M", ex="explain", say="正解は3つ。えらに血を送る心臓が2つと、体じゅうに送る心臓が1つよ。",
         read="正解は、みっつ。えらに血を送る心臓が、ふたつと、からだじゅうに送る心臓が、ひとつよ。",
         head="心臓が3つ！", sub="えら心臓×2 ＋ 体の心臓×1", fig="hearts"),
    dict(spk="Z", ex="panic", say="しかも、血が青いって本当なのだ！？",
         head="血が青い！？", fig="blood"),
    dict(spk="M", ex="explain", say="酸素を運ぶのが、鉄ではなく銅をふくむヘモシアニンだから。酸素と結びつくと青くなるの。",
         read="酸素を運ぶのが、てつではなく、どうをふくむ、ヘモシアニンだから。酸素と結びつくと、青くなるの。",
         head="銅で青くなる", sub="ヘモシアニン＝銅をふくむ", fig="blood"),
    dict(spk="M", ex="smug", say="しかも、勢いよく泳ぐと、体に血を送る心臓が止まってしまうの。",
         read="しかも、いきおいよく泳ぐと、からだに血を送る心臓が、止まってしまうの。",
         head="泳ぐと\n心臓が止まる", sub="1987年の実験で確認", fig="jet"),
    dict(spk="Z", ex="happy", say="だから長く泳ぐのは苦手なのだ。心臓が3つでも、たいへんなのだ！",
         read="だから、長く泳ぐのは苦手なのだ。心臓が、みっつでも、たいへんなのだ！",
         head="長く泳ぐのは\n苦手", fig="🐙"),
]

META = dict(
    title="タコの心臓は3つ！しかも血は青い #shorts #雑学",
    alt_titles=["タコは泳ぐと心臓が止まる！？ #shorts #雑学 #タコ",
                "タコの血はなぜ青い？心臓が3つある理由 #shorts #雑学"],
    lead="タコには心臓が3つあり、血は青色。しかも勢いよく泳ぐと、心臓の1つが止まってしまいます。",
    points=["心臓は3つ：えらに血を送る「えら心臓」が2つ＋体じゅうに送る「体の心臓」が1つ",
            "血が青いのは、酸素を運ぶ物質が鉄（ヘモグロビン）ではなく銅をふくむヘモシアニンだから",
            "ジェット噴射で泳ぐと「体の心臓」が止まる。だから長い距離を泳ぎ続けるのは苦手（1987年の実験）"],
    principle=("ヒトの血の赤は、ヘモグロビンの鉄が酸素と結びついた色。タコのヘモシアニンは銅が酸素と結びつくと青く、"
               "酸素がはなれるとほぼ無色になります。えらの細い血管に血を通すには強い力が必要なので、えら専用のポンプ"
               "（えら心臓）があり、体の心臓は酸素をもらった血を全身へ送ります。泳ぐときは体（外とう膜）を強くしめて水を"
               "噴き出すため、体の中の圧力が上がって血が心臓に戻りにくくなり、体の心臓が止まると考えられています。"),
    sources=[("Wells et al. (1987)「Blood flow and pressure changes in exercising octopuses」J. Exp. Biol. 131, 175–187",
              "https://doi.org/10.1242/jeb.131.1.175"),
             ("Smithsonian Magazine「Ten Wild Facts About Octopuses」",
              "https://www.smithsonianmag.com/science-nature/ten-wild-facts-about-octopuses-they-have-three-hearts-big-brains-and-blue-blood-7625828/"),
             ("Britannica「Hemocyanin」", "https://www.britannica.com/science/hemocyanin")],
    tags=["タコ", "蛸", "octopus", "タコの心臓", "心臓が3つ", "青い血", "ヘモシアニン", "生き物の雑学", "動物",
          "雑学", "豆知識", "科学", "海の生き物", "ずんだもん", "四国めたん", "VOICEVOX", "shorts"],
    hashtags=["#雑学", "#タコ", "#生き物", "#ずんだもん", "#shorts"],
    pinned="ほかにも「えっ、そうなの！？」な生き物の体の秘密、知ってたらコメントで教えてください！明日の雑学の参考にします🐙",
    notes=["「泳ぐと心臓が止まる」は Wells ほか(1987) の要旨「ジェット推進には心停止がともなう」に基づく。"
           "止まるのは体の心臓で、一時的なもの。",
           "「歩くほうが好き」とは言わず、論文にある「長くは泳ぎ続けられない」の範囲で表現した。"],
)
