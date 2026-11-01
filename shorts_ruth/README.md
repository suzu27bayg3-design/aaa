# YouTube Shorts：100年前の二刀流 ベーブ・ルース（MLBレジェンド紹介）

- 動画: `ruth_short.mp4`（1080×1920 縦型 / 30fps / 約48秒 / H.264 + AAC）
- デザイン: スポーツ中継の成績テロップ風（`make_ruth.py`）。行が順にスライドイン、数字は0からカウントアップ、字幕つき
- 声: VOICEVOX:ずんだもん。`bash ../tools/voicevox_engine.sh` → `python3 voicevox_synth.py && python3 make_ruth.py`
- 構成: タイトル → 通算打撃成績（打率/本塁打/打点/出塁率/長打率/OPS）→ 通算投手成績 → 獲得タイトル → 最も輝いた年（1921年）→ 締め
- 最後の0.4秒にサムネイル用コマ（`thumb.png`）
- 旧版（絵文字＋カード形式）は `make_short.py`（Gitの履歴に動画も残っています）

## 素材について（重要）
- **試合映像・プレー動画は使っていません。** MLBの映像は権利管理が厳しく、無断で使うと著作権侵害の申し立て（削除・ストライク）の対象になります。
- **写真:** Wikimedia Commons で Public domain 表示の写真のみ使用（出典・撮影者は `photos/SOURCES.md`）。
- 成績（数字）は事実なので自由に使えます。映像は図・数字アニメーションで構成しています。

## 投稿用メタデータ

**タイトル**
```
大谷翔平より100年前の二刀流 ベーブ・ルース #shorts #MLB #野球
```

**説明欄**
```
大谷翔平より100年前の二刀流、ベーブ・ルースの成績まとめ。

【通算打撃成績】打率.342 / 714本塁打 / 2,214打点 / 出塁率.474 / 長打率.690 / OPS 1.164
【通算投手成績】163登板 / 94勝46敗 / 勝率.671 / 防御率2.28
【獲得タイトル】本塁打王12回 / 打点王6回 / 首位打者(1924) / 最優秀防御率(1916) / MVP(1923) / ワールドシリーズ制覇7回
【最も輝いた年 1921年】打率.378 / 59本塁打 / 171打点 / 177得点 / 出塁率.512 / 長打率.846 / OPS 1.359
※打点は資料により2,213〜2,214、1921年のOPSは1.358〜1.359と表記に差があります

出典:
アメリカ野球殿堂 Babe Ruth
https://baseballhall.org/hall-of-famers/ruth-babe
MLB.com Babe Ruth
https://www.mlb.com/player/121578
Baseball-Reference Babe Ruth
https://www.baseball-reference.com/players/r/ruthba01.shtml
Wikipedia「List of career achievements by Babe Ruth」（タイトル一覧）
https://en.wikipedia.org/wiki/List_of_career_achievements_by_Babe_Ruth
SABR「Babe Ruth in 1921: Recrowning Baseball's Greatest Slugging Season」
https://sabr.org/research/article/babe-ruth-in-1921-recrowning-baseballs-greatest-slugging-season/
Baseball-Reference Bullpen 1921 American League
https://www.baseball-reference.com/bullpen/1921_AL

VOICEVOX:ずんだもん

#MLB #野球 #ベーブルース #大谷翔平 #二刀流 #shorts
```

**固定コメント案**
```
次に紹介してほしい昔のMLB選手をコメントで教えてください！
```

## サムネイル
動画の**最後の0.4秒**にサムネイル専用のコマ（`thumb.png`）。YouTubeアプリの投稿画面でサムネイルの鉛筆アイコン →
コマ選択バーを**右端まで**動かして選択。
