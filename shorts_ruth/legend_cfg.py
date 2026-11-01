# ベーブ・ルース（tools/legend_short.py 用の設定）
NAME_EN, NAME_JP, YEARS = "BABE RUTH", "ベーブ・ルース", "1914–1935"
SOURCE = "Stats: 野球殿堂 / MLB.com / Baseball-Reference / SABR"
OUT = "ruth_short.mp4"
THUMB = dict(text="大谷より\\n100年前の\\n二刀流")

SCENES = [
    dict(kind="hook", photo="00_title_c1922.jpg", voice="hook",
         text=["大谷より", "100年前の", "二刀流"],
         narration="大谷翔平より100年前に、二刀流で歴史を作った男がいるのだ。"),
    dict(kind="board", photo="01_swing_c1927.png", head="通算打撃成績", eng="CAREER BATTING", hl=4,
         rows=[("打率", ".342", None), ("安打", "2,873", None), ("本塁打", "714", None),
               ("長打率", ".690", None), ("OPS", "1.164", None)],
         narration="ベーブ・ルース。通算2873安打、714本塁打。オーピーエスは、いってんいちろくよん、なのだ。"),
    dict(kind="big", photo="00_title_c1922.jpg", value="2,062", label="四球", voice="hook",
         sub=["投手に勝負を避けられた証", "2001年まで歴代最多"],
         narration="投手に恐れられて、四球は2062個。2001年まで歴代最多なのだ！"),
    dict(kind="board", photo="02_pitching_1914-19.jpg", head="通算投手成績", eng="CAREER PITCHING", hl=2,
         rows=[("勝利", "94", None), ("敗戦", "46", None), ("防御率", "2.28", "1916年 タイトル")],
         narration="しかも投手として、94勝、防御率2.28なのだ。"),
    dict(kind="titles", photo="03_redsox_1919.jpg", head="獲得タイトル", eng="AWARDS & TITLES", voice="hook",
         rows=[("本塁打王", "12", "回"), ("打点王", "6", "回"), ("MVP", "1", "回 1923"), ("世界一", "7", "回")],
         narration="本塁打王12回、ワールドシリーズ制覇は7回！"),
    dict(kind="board", photo="04_1921.jpg", head="最も輝いた年", year="1921", hl=3,
         rows=[("本塁打", "59", "当時の新記録"), ("打点", "171", None), ("得点", "177", None), ("OPS", "1.359", None)],
         narration="最も輝いた1921年は、59本塁打、171打点なのだ！"),
    dict(kind="loop", photo="05_outro_c1922.jpg", voice="hook",
         text=["打って、投げて。", "100年前の", "二刀流"],
         narration="打って、投げて。100年前の二刀流、それがベーブ・ルースなのだ。"),
]
