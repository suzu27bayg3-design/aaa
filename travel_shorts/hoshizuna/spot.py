"""ふしぎな絶景の科学 星の砂（30秒・全画面型）

事実の根拠:
- 竹富島のカイジ浜は星砂で知られる。星砂は、海藻などについていた有孔虫（ホシズナ Baculogypsina sphaerulata）の
  遺骸が砂浜に打ち上げられたもの … 国土交通省 観光庁 多言語解説
- 砂浜の星の砂は、ホシスナが死んだあと打ち上がったカラ。波にもまれてトゲが折れたりけずられたりして丸くなる … 沖縄美ら島財団
- 有孔虫は炭酸カルシウムなどの殻を作るので、死後も堆積物の中に残る … 講談社ブルーバックス（有孔虫全般の説明）
- 星砂の本場は八重山諸島で、なかでも竹富島のものが有名 … 地質調査所（現 産総研）地質ニュース
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from aerial_full import Aerial  # noqa: E402

FULL = True
PHOTO_FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (255, 225, 140)
PLACE = dict(name="カイジ浜", pref="沖縄県竹富町", lat=24.3225, lon=124.0745)
MAP_CREDITS = ["航空写真: 出典 国土地理院（地理院タイルを加工して作成）"]

_M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")
A15 = Aerial(os.path.join(_M, "photo_z15.jpg"), base_w=700)
A17 = Aerial(os.path.join(_M, "photo_z17.jpg"), base_w=620)
ISLAND = (640, 640)
BEACH15 = (440, 630)
BEACH17 = (720, 700)
SAND = (300, 600)  # 浜の沖の白い砂だまり
WAVE = [(150, 1100), (300, 900), (480, 800), (640, 730), (745, 690)]


def island(t, lt):
    k = min(1.0, lt / 4.0)
    c = (ISLAND[0] + (BEACH15[0] + 150 - ISLAND[0]) * k, ISLAND[1] + (BEACH15[1] + 100 - ISLAND[1]) * k)
    return A15.ring(lt, t, c, at=BEACH15, scale=0.85 - 0.15 * k, color=(255, 240, 180), size=150)


def waves(t, lt):
    """サンゴ礁の海から浜へ、波が殻を運ぶ（光の粒）"""
    return A17.flow(lt, t, (560, 800), WAVE, scale=1.0, color=(255, 245, 210), speed=100, spread=40, dark=0.9, size=5)


FIGS = {"island": island, "waves": waves}

SCENES = [
    dict(spk="Z", ex="panic", say="この砂、ぜんぶ星の形をしてるのだ！",
         read="この、すな、ぜんぶ、ほしの、かたちを、してるのだ！",
         head="この砂\nぜんぶ星形！？", show=("photo", "Star_sand_Iriomote.jpg", "in"), head_y=560),
    dict(spk="M", say="じつはこれ、石じゃなくて、小さな生き物の殻なの。",
         read="じつは、これ、いしじゃなくて、ちいさな、いきものの、からなの。",
         head="石じゃなくて\n生き物の殻", show=("photo", "Baculogypsina_sphaerulata.jpg", "in", "card"), head_y=1230),
    dict(spk="M", say="有孔虫のホシズナ。海藻などにくっついてくらす、とても小さな生き物よ。",
         read="ゆうこうちゅうの、ほしずな。かいそうなどに、くっついて、くらす、とても、ちいさな、いきものよ。",
         head="有孔虫ホシズナ", show=("photo", "Baculogypsina_sphaerulata.jpg", "out", "card"), head_y=1230),
    dict(spk="M", say="沖縄の竹富島、カイジ浜。まわりのサンゴ礁の海に、たくさんすんでいるの。",
         read="おきなわの、たけとみじま、カイジ浜。まわりの、さんごしょうの、うみに、たくさん、すんでいるの。",
         head="竹富島\nカイジ浜", show=("fig", "island")),
    dict(spk="M", say="死んだあとの殻が、波に運ばれて浜に打ち上げられ、星の砂になるのよ。",
         read="しんだ、あとの、からが、なみに、はこばれて、はまに、うちあげられ、ほしの、すなに、なるのよ。",
         head="波が浜へ運ぶ", show=("fig", "waves")),
    dict(spk="M", say="波にもまれるうちに、トゲが折れて、だんだん丸くなっていくの。",
         read="なみに、もまれる、うちに、とげが、おれて、だんだん、まるく、なっていくの。",
         head="トゲが折れて\n丸くなる", show=("photo", "Taketomi_kaiji_hama_2022_1.jpg", "right")),
    dict(spk="Z", say="星の砂は、海の生き物の贈り物だったのだ！",
         read="ほしの、すなは、うみの、いきものの、おくりものだったのだ！",
         head="海の生き物の\n贈り物！", show=("photo", "Kaiji_beach_Taketomi_.jpg", "out")),
]

META = dict(
    title="この砂ぜんぶ星形！？星の砂の正体は生き物の殻 #shorts #沖縄 #科学",
    alt_titles=["星の砂は石じゃない！？ #shorts #竹富島", "小さな生き物が作る星 #shorts #科学 #沖縄"],
    lead="沖縄県竹富島のカイジ浜には、星の形をした「星の砂」があります。正体は石ではなく、有孔虫という小さな生き物の殻です。",
    points=["星の砂は、海藻などにくっついてくらす有孔虫「ホシズナ」の殻",
            "死んだあとの殻が波に運ばれて砂浜に打ち上げられる",
            "波にもまれてトゲが折れたりけずられたりして、だんだん丸くなる",
            "星の砂の本場は八重山諸島で、なかでも竹富島のものが有名"],
    principle=("有孔虫は、ひとつの細胞でできた小さな生き物です。海水にとけているカルシウムなどを取りこんで、炭酸カルシウムの殻を"
               "自分で作ります。ホシズナの殻は、まわりにトゲが出た星のような形をしています。生き物が死んだあとも、かたい殻は"
               "とけずに残り、波に運ばれて浜に集まります。サンゴ礁の海の砂浜には、このように生き物の殻や骨がくだけてできた砂が"
               "多くふくまれています。"),
    sources=[("国土交通省 観光庁 多言語解説（Kaiji Hama: Star Sand and Subtropical Foliage）", "https://www.mlit.go.jp/tagengo-db/en/R1-03055.html"),
             ("沖縄美ら島財団（ホシスナ）", "https://www.churashima.okinawa/userfiles/files/topics/event/2013/h25-hoshizuna.pdf"),
             ("産総研 地質調査総合センター 地質ニュース（星砂）", "https://www.gsj.jp/data/chishitsunews/76_10_05.pdf"),
             ("講談社ブルーバックス 付録（有孔虫の殻）", "https://bluebacks.kodansha.co.jp/files/9784065216903/appendix/attachments/chikyubook_column10.pdf")],
    tags=["星の砂", "星砂", "ほしずな", "有孔虫", "ホシズナ", "竹富島", "カイジ浜", "八重山", "沖縄", "サンゴ礁",
          "炭酸カルシウム", "生き物", "絶景", "ふしぎな絶景", "生物", "科学", "shorts"],
    hashtags=["#沖縄", "#絶景", "#科学", "#星の砂", "#shorts"],
    pinned="星の砂は持ち帰らず、その場で見て楽しんでね。次はどこのふしぎな絶景が見たい？",
    notes=["2・3場面目のホシズナの拡大写真は電子顕微鏡写真（330px と小さいため、全画面にせずカードで表示した）。",
           "1場面目の写真は西表島の星の砂（竹富島のものではない）。動画では場所を言わずに見せた。",
           "炭酸カルシウムの殻は、有孔虫全般についての資料にもとづき、説明欄だけで述べた。",
           "光の粒は、波が殻を浜へ運ぶようすを表した演出。",
           "大きさの数字は公的な資料で確認できなかったため言っていない。"],
)
