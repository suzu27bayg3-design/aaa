"""ふしぎな絶景の科学 蔵王の御釜（30秒・全画面）

事実の根拠:
- 噴火のあとの火口に水がたまってできた火口湖。直径約330m、最大水深約30m … 林野庁 東北森林管理局
- 天候などで湖の色がエメラルドグリーンやるり色に変わって見えるので「五色沼」とも呼ばれる … 林野庁 東北森林管理局
- 強い酸性の水 … 東北観光推進機構
- 宮城県と山形県の県境、蔵王連峰の五色岳の中にある … 東北観光推進機構
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from aerial_full import Aerial  # noqa: E402

FULL = True
TITLE = "ふしぎな絶景の科学"
ACCENT = (110, 230, 190)
PLACE = dict(name="御釜", pref="宮城県 蔵王", lat=38.1365, lon=140.4495)
MAP_CREDITS = ["航空写真: 出典 国土地理院（地理院タイルを加工して作成）"]

A = Aerial(os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps", "photo_z16.jpg"), base_w=700)
LAKE = (520, 650)


def hook(t, lt):
    return A.view(lt, LAKE, s0=1.0, s1=0.7, dur=4.5)


def crater(t, lt):
    return A.ring(lt, t, LAKE, at=LAKE, scale=0.55, color=(140, 255, 210), size=230)


def ending(t, lt):
    return A.view(lt, LAKE, s0=0.7, s1=1.0, dur=3.0)


FIGS = {"hook": hook, "crater": crater, "ending": ending}

SCENES = [
    dict(spk="Z", ex="panic", say="山のてっぺんに、エメラルド色の池があるのだ！？",
         read="やまの、てっぺんに、エメラルドいろの、いけが、あるのだ！？",
         head="山頂に\nエメラルドの池！？", show=("fig", "hook")),
    dict(spk="M", say="宮城と山形の県境、蔵王の御釜。火山の火口に水がたまった、火口湖なの。",
         read="みやぎと、やまがたの、けんざかい、ざおうの、おかま。かざんの、かこうに、みずが、たまった、かこうこなの。",
         head="火口にたまった湖", show=("fig", "crater")),
    dict(spk="M", say="直径は約330メートル、いちばん深い所は約30メートルもあるのよ。",
         read="ちょっけいは、やく、さんびゃくさんじゅうメートル、いちばん、ふかい、ところは、やく、さんじゅうメートルも、あるのよ。",
         head="直径 約330m", show=("photo", "Lake_Okama__Zao___Miyagi_05.jpg", "in"), head_y=1230),
    dict(spk="M", say="天気や光の当たり方で色が変わって見えるから、五色沼とも呼ばれているの。",
         read="てんきや、ひかりの、あたりかたで、いろが、かわって、みえるから、ごしきぬまとも、よばれているの。",
         head="色が変わる\n五色沼", show=("photo", "Fall_colors_at_Okama_crater_lake__Mt._Zao__Tohoku_region__Japan_.jpg", "right"), head_y=1230),
    dict(spk="Z", say="火山が作った、宝石みたいな湖なのだ！",
         read="かざんが、つくった、ほうせきみたいな、みずうみなのだ！",
         head="火山が作った\n宝石の湖！", show=("fig", "ending")),
]

META = dict(
    title="山頂にエメラルドの池！？蔵王の御釜 #shorts #絶景 #科学",
    alt_titles=["色が変わる火口湖・御釜 #shorts #蔵王", "火山の火口にたまった湖 #shorts #科学 #宮城"],
    lead="宮城県と山形県の県境、蔵王連峰にある「御釜」は、噴火のあとの火口に水がたまってできた火口湖です。",
    points=["噴火のあとの火口に水がたまってできた火口湖。直径約330m、最大水深約30m",
            "天気などで湖の色がエメラルドグリーンやるり色に変わって見えるため「五色沼」とも呼ばれる",
            "水は強い酸性"],
    principle=("火山の火口は、まわりを壁にかこまれたくぼ地です。そこに雨や雪どけ水がたまると、水の出口がないため湖になります"
               "（火口湖）。湖の色は、水そのものの色だけでなく、空の明るさや太陽の光の向き、見る角度によって、水面で反射する光と"
               "水の中を通ってくる光の割合が変わるため、ちがって見えます。"),
    sources=[("林野庁 東北森林管理局「蔵王御釜」", "https://www.rinya.maff.go.jp/tohoku/introduction/gaiyou_kyoku/annai/midokoro/midokoro_zaouokama.html"),
             ("東北観光推進機構「蔵王御釜」", "https://www.tohokukanko.jp/attractions/detail_1240.html")],
    tags=["御釜", "蔵王", "蔵王の御釜", "火口湖", "五色沼", "蔵王山", "五色岳", "宮城県", "山形県", "東北",
          "絶景", "ふしぎな絶景", "火山", "地学", "科学", "航空写真", "shorts"],
    hashtags=["#絶景", "#科学", "#蔵王", "#御釜", "#shorts"],
    pinned="天気がいい日に行けるとラッキー！次はどこのふしぎな絶景が見たい？コメントで教えてください。",
    notes=["直径は資料によって約330m（林野庁）と約325m（東北観光推進機構）がある。動画は林野庁の数字。",
           "色が変わる理由は、資料では「天候等の条件」とだけ書かれているため、説明欄の原理は光の反射と透過の一般的な説明にとどめた。",
           "蔵王山は活火山で、噴火警戒レベルが変わることがあるため、訪れる前は気象庁の情報を確認すること（動画ではふれていない）。"],
)
