# ルー・ゲーリッグ（tools/legend_short.py 用の設定）
NAME_EN, NAME_JP, YEARS = "LOU GEHRIG", "ルー・ゲーリッグ", "1923–1939"
SOURCE = "Stats: 野球殿堂 / MLB.com / Baseball-Reference / SABR"
OUT = "gehrig_short.mp4"
THUMB = dict(text="衣笠が抜いた\\n鉄の馬の\\n記録")

SCENES = [
    dict(kind="hook", photo="00_title_1923.jpg", voice="hook",
         text=["衣笠が抜いた", "「鉄の馬」の", "記録"],
         narration="衣笠祥雄が抜いた、2130試合連続出場。元の記録の持ち主を、知ってるのだ？"),
    dict(kind="big", photo="02_game_1925.jpg", value="2,130", label="試合連続出場",
         sub=["1925年〜1939年", "1987年 衣笠祥雄が更新"],
         narration="ルー・ゲーリッグ。約14年間、1試合も休まなかったのだ。"),
    dict(kind="board", photo="01_game_1928.jpg", head="通算打撃成績", eng="CAREER BATTING", hl=3,
         rows=[("打率", ".340", None), ("本塁打", "493", None), ("打点", "1,995", None), ("OPS", "1.080", None)],
         narration="通算493本塁打、1995打点の強打者なのだ。"),
    dict(kind="titles", photo="03_portrait_1923.jpg", head="記録とタイトル", eng="RECORDS & TITLES",
         rows=[("満塁本塁打", "23", "本", "2013年まで最多"), ("MVP", "2", "回"),
               ("三冠王", "1", "回 1934"), ("世界一", "6", "回")],
         narration="満塁ホームラン23本、MVP2回、1934年には三冠王なのだ。"),
    dict(kind="board", photo="04_elgrafico_1927.jpg", head="最も輝いた年", year="1927", hl=3, voice="hook",
         rows=[("打率", ".373", None), ("本塁打", "47", None), ("打点", "175", "当時の新記録"), ("OPS", "1.240", "MVP")],
         narration="最も輝いた1927年は、打率、さんわりななぶさんりん、175打点でMVPなのだ！"),
    dict(kind="loop", photo="05_farewell_1939.jpg", voice="hook",
         text=["衣笠が追いかけた", "「鉄の馬」", "ルー・ゲーリッグ"],
         narration="引退のとき、自分は地球上で最も幸運な男だと語った、鉄の馬なのだ。"),
]
