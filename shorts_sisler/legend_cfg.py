# ジョージ・シスラー（tools/legend_short.py 用の設定）
NAME_EN, NAME_JP, YEARS = "GEORGE SISLER", "ジョージ・シスラー", "1915–1930"
SOURCE = "Stats: 野球殿堂 / Baseball-Reference / Britannica / SABR"
OUT = "sisler_short.mp4"
THUMB = dict(text="イチローが\\n抜いた\\n安打記録")

SCENES = [
    dict(kind="hook", photo="00_title_1924.jpg", voice="hook",
         text=["イチローが抜いた", "84年前の", "安打記録"],
         narration="イチローが2004年に抜いた、84年前の安打記録。元の持ち主を、知ってるのだ？"),
    dict(kind="big", photo="02_card_1921.jpg", value="257", label="シーズン安打（1920年）",
         sub=["84年間 破られなかった記録", "2004年 イチローが262安打で更新"],
         narration="ジョージ・シスラー。1920年に257安打。この記録は84年間破られなかったのだ。"),
    dict(kind="board", photo="01_stlouis_1924.jpg", head="通算打撃成績", eng="CAREER BATTING", hl=1,
         rows=[("打率", ".340", None), ("安打", "2,812", None), ("本塁打", "102", None),
               ("打点", "1,178", None), ("盗塁", "375", "盗塁王4回")],
         narration="通算打率、さんわりよんぶ、2812安打。足も速くて、盗塁王を4回とったのだ。"),
    dict(kind="titles", photo="03_handshake_1924.jpg", head="獲得タイトル", eng="AWARDS & TITLES",
         rows=[("首位打者", "2", "回 20・22"), ("盗塁王", "4", "回"), ("MVP", "1", "回 1922")],
         narration="首位打者2回、盗塁王4回。1922年にはMVPなのだ。"),
    dict(kind="board", photo="04_may_1924.jpg", head="最も輝いた年", year="1922", hl=0, voice="hook",
         rows=[("打率", ".420", "MVP"), ("盗塁", "51", "盗塁王"), ("連続試合安打", "41", "当時ア・リーグ記録")],
         narration="最も輝いた1922年は、打率、よんわりにぶ。41試合連続安打で、MVPなのだ！"),
    dict(kind="loop", photo="05_three_stars_1924.jpg", voice="hook",
         text=["イチローが追いかけた", "安打製造機", "ジョージ・シスラー"],
         narration="イチローが追いかけた、84年前の安打製造機。それがジョージ・シスラーなのだ。"),
]
