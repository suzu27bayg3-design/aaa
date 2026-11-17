"""ふしぎな絶景の科学 エンジェルロード（30秒・全画面）

事実の根拠:
- 香川県土庄町。弁天島から中余島・小余島・大余島へ続く島々の間に、1日2回の干潮のときだけ砂の道（砂州・トンボロ）が現れる。
  長さは約500m … 香川県観光協会 ほか
- 渡れるのは干潮の前後数時間（資料により2〜3時間）。大余島は私有地で、歩けるのは手前まで … 観光案内
- 潮の満ち引きは、月の引力（と太陽の引力）がもとになる「起潮力」で海面が盛り上がり、地球の自転でその下を通るため、
  ふつう1日に2回ずつ満潮と干潮が来る … 気象庁
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from aerial_full import Aerial  # noqa: E402

FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (120, 220, 230)
PLACE = dict(name="エンジェルロード", pref="香川県小豆島", lat=34.474, lon=134.188)
MAP_CREDITS = ["航空写真: 出典 国土地理院（地理院タイルを加工して作成）"]

_D = os.path.dirname(os.path.abspath(__file__))
A = Aerial(os.path.join(_D, "maps", "photo_z17.jpg"), base_w=700)
ROAD = [(680, 120), (665, 250), (660, 360), (655, 450), (660, 520), (645, 600), (640, 680), (648, 780), (660, 880)]
C = (650, 640)
_PH = {c["file"] for c in json.load(open(os.path.join(_D, "photos", "credits.json")))} if os.path.exists(
    os.path.join(_D, "photos", "credits.json")) else set()


def hook(t, lt):
    return A.view(lt, C, s0=1.0, s1=0.8, dur=4.5)


def road(t, lt):
    return A.flow(lt, t, C, ROAD, scale=0.85, color=(255, 236, 180), speed=70, spread=4, dark=0.75, size=6)


def tide(t, lt):
    """潮が満ちていくように、砂の道をうすい水色でおおっていく（演出）"""
    from PIL import Image, ImageDraw
    b, im = A.frame(C, 0.85)
    lay = Image.new("RGBA", im.size)
    d = ImageDraw.Draw(lay)
    k = min(1.0, lt / 3.0)
    pts = [A.scr(b, x, y) for x, y in ROAD]
    d.line(pts, fill=(40, 90, 120, int(200 * k)), width=70, joint="curve")
    out = im.convert("RGBA")
    out.alpha_composite(lay)
    return out


def ring(t, lt):
    return A.ring(lt, t, C, at=(655, 450), scale=0.85, color=(255, 236, 180), size=180)


FIGS = {"hook": hook, "road": road, "tide": tide, "ring": ring}


def _shot(name, fallback, move="in"):
    return ("photo", name, move) if name in _PH else ("fig", fallback)


def _hy(name):
    return 1230 if name in _PH else 330


SCENES = [
    dict(spk="Z", ex="panic", say="海の中に、島へ続く砂の道があるのだ！？",
         head="海の中に\n砂の道！？", show=_shot("Angel_Road_Shodoshima_Japan.jpg", "hook"), head_y=_hy("Angel_Road_Shodoshima_Japan.jpg")),
    dict(spk="M", say="香川県小豆島のエンジェルロード。島と島をつなぐ、長さ約500メートルの砂の道なの。",
         head="長さ 約500m", show=("fig", "road")),
    dict(spk="M", say="でも、この道が見えるのは、潮が引いている時間だけ。満ち潮になると、海にしずんでしまうのよ。",
         head="潮が引いた\n時だけ", show=("fig", "tide")),
    dict(spk="M", say="潮の満ち引きは、月の引力で海の水が引っぱられて、海面がもり上がるから起きるの。",
         head="月が海を\n引っぱる", show=("fig", "ring")),
    dict(spk="M", say="地球が回るから、1日にふつう2回、満ち潮と引き潮がやってくるのよ。",
         head="1日に2回", show=_shot("Angel_Road_Shodo_Island_Japan07s3.jpg", "road", "right"), head_y=_hy("Angel_Road_Shodo_Island_Japan07s3.jpg")),
    dict(spk="M", say="道ができるのは、島のかげで波が弱まって、砂がたまりやすいからと考えられているわ。",
         head="島のかげに\n砂がたまる", show=("fig", "road")),
    dict(spk="Z", say="月が作る、1日2回だけの道なのだ！",
         head="月が作る道！", show=_shot("Angel_Road_Shodoshima_Japan.jpg", "hook", "out"), head_y=_hy("Angel_Road_Shodoshima_Japan.jpg")),
]

META = dict(
    title="潮が引いた時だけ現れる道！エンジェルロード #shorts #絶景 #科学",
    alt_titles=["月が作る1日2回だけの道 #shorts #小豆島", "海の中に砂の道！？ #shorts #科学 #香川"],
    lead="香川県小豆島のエンジェルロードは、潮が引いたときだけ海の中に現れて、島へ歩いて渡れる砂の道です。",
    points=["土庄町の弁天島から沖の島々へ続く、長さ約500mの砂の道（砂州・トンボロ）",
            "道が見えるのは干潮の前後数時間だけ。満潮になると海にしずむ",
            "潮の満ち引きは、月の引力（と太陽の引力）で海面がもり上がり、地球が回ることで、ふつう1日2回ずつ起こる",
            "島のかげで波が弱まり、砂がたまりやすいため道ができると考えられている"],
    principle=("月の引力は、月に近い側の海水をより強く、遠い側の海水をより弱く引っぱります。この差（起潮力）によって、地球の"
               "月に向いた側と反対側の2か所で海面がもり上がります。地球が1日に1回自転するあいだに、ある場所はこの2つのもり上がりの下を"
               "通るので、ふつう1日に2回ずつ満潮と干潮が来ます。エンジェルロードは、干潮で海面が下がったときだけ、浅い海底にたまった砂の道が"
               "海の上に出てきます。"),
    sources=[("気象庁「潮汐・海面水位の知識」", "https://ds.data.jma.go.jp/gmd/kaiyou/db/tide/knowledge/tide/choseki.html"),
             ("気象庁 福岡管区気象台（潮の満ち引きのしくみ）", "https://www.data.jma.go.jp/fukuoka/chosa/files/harerun0082.pdf"),
             ("香川県観光協会 うどん県旅ネット（エンジェルロード）", "https://www.my-kagawa.jp/files/user/site/07b9350b88b621b92955dbcf176c3db4e82ce1fb.pdf")],
    tags=["エンジェルロード", "小豆島", "土庄町", "トンボロ", "砂州", "干潮", "潮の満ち引き", "潮汐", "月の引力", "香川県",
          "瀬戸内海", "絶景", "ふしぎな絶景", "科学", "航空写真", "shorts"],
    hashtags=["#絶景", "#科学", "#エンジェルロード", "#小豆島", "#shorts"],
    pinned="渡れる時間は日によってちがいます。行く前に潮見表でチェック！次はどこのふしぎな絶景が見たい？",
    notes=["渡れる時間は資料によって「干潮の前後2時間」「前後3時間」とちがうため、動画では「潮が引いている時間だけ」と言った。",
           "「1日に2回」は「ふつう」をつけた（場所や日によって1日1回のこともある）。",
           "砂の道が島のかげにできるしくみ（トンボロ）は一般的な説明で、エンジェルロード固有の研究は確認できていないため「考えられている」とした。",
           "潮が満ちる場面は、砂の道を水色でおおう演出。"],
)
