"""毎日の科学の雑学 2026-11-06「空はなぜ青い？夕焼けはなぜ赤い？」（物理）

事実の根拠:
- 空気の分子による散乱（レイリー散乱）は、波長が短い光ほど強い（波長の4乗に反比例）… Met Office / 香港天文台
- 夕方は光が大気を長く通るので、青い光は途中で散らばって減り、赤い光が残る … Met Office / Royal Museums Greenwich
- 紫がもっと散らばるのに空が紫に見えないのは、太陽の光に紫が少なく、目が紫に鈍いから … 香港天文台
- 青(450nm)と赤(700nm)の散らばりやすさの比: (700/450)^4 ≈ 5.9
"""
import math

from PIL import Image, ImageDraw

import longform as L

TITLE = "空の色の秘密"
ACCENT = (120, 200, 255)
BG = ((20, 60, 140), (8, 16, 50))
SOURCE_NOTE = "出典: Met Office / 香港天文台 / Royal Museums Greenwich"

BLUE, RED, SUN = (80, 160, 255), (255, 90, 70), (255, 220, 90)


def _label(d, xy, s, size=32, fill=L.WHITE):
    d.text(xy, s, font=L.jp(size, True), fill=fill, anchor="mm", stroke_width=5, stroke_fill=L.NAVY)


def scatter(t, lt):
    """太陽の光（赤と青の粒）が空気の分子に当たる。青はあちこちへ散らばり、赤はほぼまっすぐ進む"""
    W, H = 840, 600
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    mx, my = 420, 300
    d.ellipse((20, my - 70, 160, my + 70), fill=SUN)
    _label(d, (90, my + 105), "太陽の光", 34)
    d.ellipse((mx - 44, my - 44, mx + 44, my + 44), fill=(200, 210, 230), outline=L.WHITE, width=4)
    _label(d, (mx, my + 80), "空気の分子", 32)
    n = 36
    for i in range(n):
        ph = (t * 0.55 + i / n) % 1.0
        blue = i % 2 == 0
        col = BLUE if blue else RED
        scattered = blue or i % 12 == 1  # 赤も少しは散らばる（約1/6）
        if ph < 0.5:
            x, y = 170 + (mx - 170) * ph / 0.5, my + (i % 5 - 2) * 6
        else:
            s = (ph - 0.5) / 0.5
            if scattered:
                a = math.radians((i * 137.5) % 360)
                x, y = mx + math.cos(a) * 330 * s, my + math.sin(a) * 260 * s
            else:
                x, y = mx + 390 * s, my + (i % 5 - 2) * 6
        r = 14
        d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    _label(d, (W - 130, 70), "青：よく散らばる", 32, BLUE)
    _label(d, (W - 130, H - 40), "赤：まっすぐ進む", 32, RED)
    return im


def sunset(t, lt):
    """地球と大気。昼の光は短い道のり、夕方の光は長い道のりで、途中で青が抜けて赤くなる"""
    W, H = 840, 600
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    cx, cy, R = 420, 1180, 900
    d.ellipse((cx - R - 140, cy - R - 140, cx + R + 140, cy + R + 140), fill=(110, 170, 255, 70))  # 大気
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(60, 140, 90))  # 地面
    ox, oy = 420, cy - R  # 見ている人
    d.ellipse((ox - 14, oy - 34, ox + 14, oy - 6), fill=L.WHITE)
    prog = min(1.0, lt / 1.2)
    # 昼：真上から（短い）
    top = (ox, oy - 140 - 40)
    d.line([top, (ox, top[1] + (oy - 40 - top[1]) * prog)], fill=(255, 255, 240), width=12)
    _label(d, (ox + 110, top[1] - 10), "昼：短い道のり", 30)
    # 夕方：横から（長い）。進むほど青が抜けて赤くなる
    sx, sy = 70, oy - 150
    steps = 30
    for k in range(int(steps * prog)):
        f0, f1 = k / steps, (k + 1) / steps
        p0 = (sx + (ox - 30 - sx) * f0, sy + (oy - 30 - sy) * f0)
        p1 = (sx + (ox - 30 - sx) * f1, sy + (oy - 30 - sy) * f1)
        c = (255, int(250 - 160 * f0), int(230 - 200 * f0))
        d.line([p0, p1], fill=c, width=12)
        if k % 5 == 2:  # 抜けていく青い光
            a = math.radians(200 + k * 23 + t * 40)
            q = (p0[0] + 40 * math.cos(a), p0[1] + 40 * math.sin(a))
            d.line([p0, q], fill=BLUE, width=5)
    d.ellipse((sx - 40, sy - 40, sx + 40, sy + 40), fill=(255, 150, 60))
    _label(d, (190, sy - 80), "夕方：長い道のり", 30, (255, 170, 90))
    return im


FIGS = {"scatter": scatter, "sunset": sunset}

SCENES = [
    dict(spk="Z", ex="think", say="空って、どうして青いのだ？", head="空はなぜ\n青い？", fig="🌤"),
    dict(spk="M", ex="explain", say="太陽の光には、いろいろな色がまざっているの。空気の分子に当たると、光は四方に散らばるわ。",
         read="太陽の光には、いろいろな色が、まざっているの。空気の分子に当たると、光は、しほうに散らばるわ。",
         head="光が\n散らばる", sub="レイリー散乱", fig="scatter"),
    dict(spk="M", ex="smug", say="青い光は波が短いから、赤い光より5倍以上も散らばりやすいの。だから空全体から青が届くのよ。",
         read="青い光は、波が短いから、赤い光より、ごばい以上も散らばりやすいの。だから、空全体から、青が届くのよ。",
         head="青は赤より\n5倍以上散らばる", sub="波長が短いほど散らばる", fig="scatter"),
    dict(spk="Z", ex="panic", say="じゃあ、夕焼けが赤いのはどうしてなのだ！？", head="夕焼けは\nなぜ赤い？", fig="🌇"),
    dict(spk="M", ex="explain", say="夕方は、光が空気の中を長く通るの。青は途中で散らばって減り、残った赤い光が目に届くのよ。",
         read="夕方は、光が、空気の中を長く通るの。青は、途中で散らばって、へってしまい、残った赤い光が、目に届くのよ。",
         head="長い道のりで\n青が抜ける", sub="残った赤が届く", fig="sunset"),
    dict(spk="Z", ex="happy", say="同じ散らばり方で、昼は青、夕方は赤になるのだ！空が青いわけ、もう言えるのだ！",
         read="同じ散らばり方で、昼は青、夕方は赤になるのだ！空が青いわけ、もう言えるのだ！",
         head="昼は青\n夕方は赤", fig="🌍"),
]

META = dict(
    title="空はなぜ青い？夕焼けはなぜ赤い？ #shorts #科学 #雑学",
    alt_titles=["夕焼けが赤い本当の理由、説明できる？ #shorts #科学",
                "青い光は赤い光の約6倍散らばる！空の色のしくみ #shorts #雑学"],
    lead="空が青いのも、夕焼けが赤いのも、じつは同じしくみ。光が空気の分子に当たって散らばる「レイリー散乱」で説明できます。",
    points=["太陽の光にはいろいろな色がまざっていて、空気の分子に当たると四方に散らばる",
            "波長が短い青い光ほど散らばりやすい（波長の4乗に反比例。青450nmと赤700nmで約6倍）",
            "夕方は光が大気を長く通るので、青い光が途中で抜けて、残った赤やオレンジが届く"],
    principle=("光は波で、色によって波の長さ（波長）がちがいます。空気の分子のように光の波長よりずっと小さい粒に光が当たると、"
               "光は四方へ散らばり、その強さは波長の4乗に反比例します（レイリー散乱）。そのため波長の短い青い光が空全体から"
               "目に届き、空は青く見えます。紫はさらに散らばりますが、太陽の光に紫が少なく、人の目も紫に鈍いため、青く見えます。"
               "夕方は太陽が低く、光が大気を通る道のりが長くなるので、青い光は途中で散らばってしまい、赤やオレンジが残ります。"),
    sources=[("Met Office「Why is the sky blue?」（英国気象庁）",
              "https://weather.metoffice.gov.uk/learn-about/weather/optical-effects/why-is-the-sky-blue"),
             ("Hong Kong Observatory「Why is the sky blue?」（香港天文台）",
              "https://www.hko.gov.hk/en/education/earth-science/optical-phenomena/00364-why-is-the-sky-blue.html"),
             ("Royal Museums Greenwich「Why is the sky blue?」",
              "https://www.rmg.co.uk/stories/space-astronomy/why-sky-blue")],
    tags=["空はなぜ青い", "空が青い理由", "夕焼け", "夕焼けが赤い理由", "レイリー散乱", "光の散乱", "波長", "物理",
          "科学", "理科", "雑学", "豆知識", "ずんだもん", "四国めたん", "VOICEVOX", "shorts"],
    hashtags=["#科学", "#雑学", "#物理", "#ずんだもん", "#shorts"],
    pinned="火星では反対に、夕焼けが青っぽくなるって知ってた？ 気になる人がいたら次の雑学にします🌇 ほかに知りたい「なぜ？」もコメントで！",
    notes=["「約6倍」は青450nm・赤700nmとしたときの (700/450)^4 ≈ 5.9。セリフでは「5倍以上」と控えめに言った。",
           "空が紫に見えない理由は、太陽光の紫が少ないことと目の感度で説明（香港天文台）。酸素による吸収説は弱いので使っていない。",
           "固定コメントの「火星の夕焼けは青っぽい」は Royal Museums Greenwich の記述に基づく。"],
)
