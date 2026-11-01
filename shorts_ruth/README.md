# YouTube Shorts：大谷より100年前の二刀流 ベーブ・ルース（MLBレジェンド紹介）

- 動画: `ruth_short.mp4`（1080×1920 縦型 / 30fps / H.264 + AAC）
- 生成: `bash ../tools/voicevox_engine.sh` → `python3 ../tools/legend_short.py legend_cfg.py`（台本・成績・写真の割り当ては `legend_cfg.py`）
- 構成（約44秒）: 写真＋問いかけ「大谷より100年前の二刀流」→ 通算打撃（安打を含む5項目）→ 四球2,062（カウントアップ）→ 通算投手 → 獲得タイトル → 最も輝いた年1921 → 冒頭に戻るループ
- 写真: Wikimedia Commons の Public domain 写真（`photos/SOURCES.md`）。試合映像は不使用
- 最後の0.4秒にサムネイル用コマ（`thumb.png`）
- 旧版のスクリプト（`make_ruth.py` / `make_short.py`）も残しています

---

## 投稿用メタデータ

### タイトル（候補。1つ選ぶ）
```
大谷翔平より100年前の「二刀流」ベーブ・ルースがエグすぎた #shorts
```
```
【MLB伝説】100年前の二刀流 ベーブ・ルースの成績 #shorts #大谷翔平
```
- 「大谷翔平」を入れると検索・関連表示に乗りやすくなります。タイトルは40字前後までに。

### 説明欄（`../docs/description_guide.md` の型）
```
【大谷翔平より100年前の二刀流】ベーブ・ルースの成績がすごすぎる
投手で94勝、打者で714本塁打。メジャーリーグ最初の“二刀流スター”を40秒でまとめました。

▼ベーブ・ルース 成績まとめ
・通算打撃：打率.342 / 2,873安打 / 714本塁打 / 長打率.690 / OPS 1.164
・四球：2,062個（投手に勝負を避けられた証。2001年まで歴代最多）
・通算投手：94勝46敗 / 防御率2.28（1916年 最優秀防御率）
・タイトル：本塁打王12回 / 打点王6回 / MVP（1923）/ ワールドシリーズ制覇7回
・最も輝いた年（1921年）：59本塁打（当時の新記録）/ 171打点 / 177得点 / OPS 1.359

💬 大谷とルース、二刀流としてすごいのはどっち？ コメントで教えてください！
▶ MLBレジェンド図鑑：ルー・ゲーリッグ / ジョージ・シスラー / サイ・ヤング も公開中

※記録は資料により差があります（安打2,873〜2,874、打点2,213〜2,214、1921年OPS 1.358〜1.359）
出典：アメリカ野球殿堂 https://baseballhall.org/hall-of-famers/ruth-babe
MLB.com https://www.mlb.com/player/121578
Baseball-Reference https://www.baseball-reference.com/players/r/ruthba01.shtml
SABR（1921年）https://sabr.org/research/article/babe-ruth-in-1921-recrowning-baseballs-greatest-slugging-season/
MLB.com（四球記録）https://www.mlb.com/news/rickey-henderson-passes-babe-ruth-walk-record
写真：Wikimedia Commons（Public domain）Underwood & Underwood, Charles M. Conlon, George G. Bain ほか
音声：VOICEVOX:ずんだもん

#大谷翔平 #ベーブルース #メジャーリーグ #MLB #二刀流
```
- ハッシュタグは3〜5個に絞り、内容と関係あるものだけにします。

### 固定コメント
```
大谷とルース、二刀流としてすごいのはどっち？ コメントで教えてください！
次に紹介してほしい昔のMLB選手も募集中！
```
- 2択の質問は答えやすく、コメントが付きやすくなります。

### 投稿時の設定
- **関連動画**: ルー・ゲーリッグ編を設定（ショートから別の動画へ誘導できるリンク）
- **サムネイル**: コマ選択バーを右端まで動かし、最後の特大文字のコマを選ぶ
- **公開日時**: 同じシリーズは同じ曜日・時間にそろえると、続けて見てもらいやすい

## サムネイル
動画の最後の0.4秒にサムネイル専用のコマ（`thumb.png`）。YouTubeアプリの投稿画面でサムネイルの鉛筆アイコン → コマ選択バーを右端へ。
