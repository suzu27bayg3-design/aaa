# 解説動画：量子コンピュータは、いつ役に立つのか？（ずんだもん×四国めたん）

- 動画: `quantum_longform.mp4`（1920×1080 横長 / 約6分04秒 / H.264 + AAC）
- ショート: `short.mp4`（1080×1920 縦長 / 約0分22秒）。投稿時に「関連動画」を本編に設定する
- 構成: 冒頭の予告（約10秒）→ 本編 → まとめ → 次回予告（最後の約20秒。終了画面で次回の動画を表示）
- サムネイル: `thumbnail.png`（1280×720。通常動画はカスタムサムネイルをアップロード可能）
- 生成: `bash ../tools/voicevox_engine.sh` → `python3 ../tools/longform.py script.py`（台本・図は `script.py`）
- チャプター: `chapters.txt`（説明欄に貼るとYouTubeのチャプターになる）
- 形式: ずんだもん（質問役）× 四国めたん（解説役）の掛け合い。章ごとに箇条書き＋図、下部に話者テロップ
- 立ち絵: 坂本アヒルさんのPSD素材から書き出したパーツ（`../assets/characters/`）。話している方は明るく、
  声の大きさ（0.1秒ごとのRMS）で口を3段階に動かす口パク、数秒ごとのまばたき付き。聞いている方は暗くなる

---

## 投稿用メタデータ

### タイトル（候補。おすすめ順）
```
量子コンピュータはいつ使える？最大の壁「エラー」突破の最前線【ずんだもん解説】
```
```
Google Willow・ノーベル賞・日本の256量子ビット 量子コンピュータの今が6分でわかる【ずんだもん】
```
```
量子コンピュータで暗号は破られる？実用化の目安は2030年前後【ずんだもん解説】
```
- 先頭に検索語「量子コンピュータ」。誰もが持つ疑問「いつ使える？」をそのままタイトルにし、答えの鍵（エラー）を予告する

### 説明欄
```
「量子コンピュータって、結局いつ役に立つの？」
その答えに、ここ1〜2年の研究で大きく近づきました。実用化を阻む最大の壁「エラー」を、どうやって乗り越え始めたのかを、ずんだもんと四国めたんが約6分で解説します。

・量子ビットの「重ね合わせ」と「もつれ」とは？（何でも一気に試せるわけではない）
・エラーを減らす「量子誤り訂正」を多数決のたとえで解説
・Google Willow：量子ビットを増やすほどエラーが約半分に（2024年）
・2025年ノーベル物理学賞と、日本の256量子ビット機（理研×富士通）
・本格的な機械は2030年前後が目標？ 今の暗号は大丈夫？

▼チャプター
0:00 予告・オープニング
0:28 量子ビットってなに？
1:06 最大の壁「エラー」
1:29 誤り訂正のしくみ（多数決）
2:17 突破口① Google「Willow」(2024)
2:50 突破口② 2025年ノーベル物理学賞
3:16 日本の研究：理研×富士通
3:47 いろいろな方式
4:19 いつ役に立つ？ IBMのロードマップ
4:49 今の暗号は破られる？
5:32 まとめ
5:49 次回予告

▼この動画で紹介した研究
・Google「Willow」（2024年12月, Nature）：符号距離3→5→7で論理エラー率がおよそ半分ずつに（しきい値以下の誤り訂正）
・2025年ノーベル物理学賞：J. クラーク / M. デヴォレ / J. マルティニス（電気回路での巨視的量子トンネル効果とエネルギー量子化）
・理研×富士通：256量子ビット超伝導量子コンピュータ（2025年4月）、2026年度に1000量子ビット級を目標
・IBMのロードマップ：2029年 Starling（論理200量子ビット・1億演算）、2033年 Blue Jay（論理2000量子ビット）※企業の計画
・RSA-2048の解読に必要な量子ビット数の試算：2019年 約2000万 → 2025年 100万未満（Gidney, arXiv:2505.15917）
・NIST 耐量子暗号の標準（2024年8月, FIPS 203/204/205）

💬 量子コンピュータで一番楽しみな使い道は？ コメントで教えてください！
▶ 第2回「量子コンピュータが得意な計算」も公開中（URLを貼る）

出典:
Google Quantum AI「Quantum error correction below the surface code threshold」(Nature, 2024) 解説: APS Physics https://physics.aps.org/articles/v17/176
Scimex（Willow）https://www.scimex.org/newsfeed/googles-new-quantum-chip-hits-error-correction-target
NobelPrize.org（2025年物理学賞）https://www.nobelprize.org/prizes/physics/2025/summary/
The Quantum Insider（ノーベル賞）https://thequantuminsider.com/2025/10/07/clarke-devoret-and-martinis-win-2025-nobel-prize-in-physics-for-revealing-quantum-effects-in-macroscopic-circuits/
富士通（256量子ビット）https://global.fujitsu/ja-jp/technology/research/quantum/fujitsu-superconducting-quantum-computer-lp
MONOist（256量子ビット・1000量子ビット目標）https://monoist.itmedia.co.jp/mn/articles/2504/28/news064.html
DatacenterDynamics（IBM Starling）https://www.datacenterdynamics.com/en/news/ibm-updates-quantum-computing-roadmap-to-deliver-starling-system-by-2029/
arXiv:2505.15917（Gidney 2025）https://arxiv.org/abs/2505.15917
Cloud Security Alliance（NIST FIPS 203/204/205）https://cloudsecurityalliance.org/articles/nist-fips-203-204-and-205-finalized-an-important-step-towards-a-quantum-safe-future

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子コンピュータ #ずんだもん #科学解説
```

### 固定コメント
```
量子コンピュータで一番楽しみな使い道は？ 次に解説してほしいテーマもコメントで！
```
