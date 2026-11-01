# サイ・ヤング（tools/legend_short.py 用の設定）
NAME_EN, NAME_JP, YEARS = "CY YOUNG", "サイ・ヤング", "1890–1911"
SOURCE = "Stats: 野球殿堂 / Baseball-Reference / Britannica / StatMuse"
OUT = "young_short.mp4"
THUMB = dict(text="サイ・ヤング賞\\nの由来の\\n投手")

SCENES = [
    dict(kind="hook", photo="00_title_1902.jpg", voice="hook",
         text=["サイ・ヤング賞の", "サイ・ヤングって", "誰？"],
         narration="毎年発表されるサイ・ヤング賞。その名前の由来になった投手を、知ってるのだ？"),
    dict(kind="big", photo="02_thompson_1909.jpg", value="511", label="通算勝利",
         sub=["1890年〜1911年", "MLB歴代最多"],
         narration="サイ・ヤング。通算511勝は、メジャー歴代最多なのだ！"),
    dict(kind="board", photo="01_conlon_1911.jpg", head="通算投手成績", eng="CAREER PITCHING", hl=0,
         rows=[("勝利", "511", "歴代最多"), ("防御率", "2.63", None), ("完投", "749", None),
               ("投球回", "7,356", None), ("奪三振", "2,803", None)],
         narration="防御率2.63。完投は749回、投げたイニングは7356なのだ。"),
    dict(kind="titles", photo="03_1908.jpg", head="記録とタイトル", eng="RECORDS & TITLES",
         rows=[("投手三冠", "1", "回 1901"), ("完全試合", "1", "回 1904", "20世紀初")],
         narration="1901年には投手三冠。1904年には、20世紀初の完全試合なのだ。"),
    dict(kind="board", photo="04_1899.jpg", head="最も輝いた年", year="1901", hl=2, voice="hook",
         rows=[("勝利", "33", "リーグ1位"), ("敗戦", "10", None), ("防御率", "1.62", "リーグ1位"),
               ("奪三振", "158", "リーグ1位")],
         narration="最も輝いた1901年は、33勝10敗、防御率1.62で、投手三冠なのだ！"),
    dict(kind="loop", photo="05_1950.jpg", voice="hook",
         text=["1956年", "サイ・ヤング賞", "誕生"],
         narration="亡くなった翌年の1956年、彼の名前をつけたサイ・ヤング賞が生まれたのだ。"),
]
