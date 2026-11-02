# 解説動画：量子コンピュータは、いつ役に立つのか？（ずんだもん×四国めたん）

- 動画: `quantum_longform.mp4`（1920×1080 横長 / 約5分35秒 / H.264 + AAC）
- サムネイル: `thumbnail.png`（1280×720。通常動画はカスタムサムネイルをアップロード可能）
- 生成: `bash ../tools/voicevox_engine.sh` → `python3 ../tools/longform.py script.py`（台本・図は `script.py`）
- チャプター: `chapters.txt`（説明欄に貼るとYouTubeのチャプターになる）
- 形式: ずんだもん（質問役）× 四国めたん（解説役）の掛け合い。章ごとに箇条書き＋図、下部に話者テロップ
- 立ち絵: 画面下の左右にワイプ表示。話している方は明るく、声の大きさ（0.1秒ごとのRMS）に合わせて弾む。聞いている方は暗くなる。
  ずんだもんは台本の指定・文末記号で表情（happy / smug / shy / panic）を切り替え
- **立ち絵の素材について**: 現在は坂本アヒルさんの立ち絵素材の**ニコニコ静画の見本画像**（`assets/characters/*/preview_*.jpg`）から切り出した簡易版。
  素材本体（PSD）を入手したら `assets/characters/<名前>/<表情>.png` を差し替えるだけで高画質化できる。利用前に素材の規約と東北ずん子プロジェクトのガイドラインを確認すること

---

## 投稿用メタデータ

### タイトル（候補）
```
【ずんだもん解説】量子コンピュータはいつ使える？ 2024〜2025年の最新研究でわかったこと
```
```
量子コンピュータの「最大の壁」がついに突破された？ Google Willow・ノーベル賞・日本の256量子ビットを解説【ずんだもん】
```

### 説明欄
```
【量子コンピュータはいつ役に立つ？】2024〜2025年の最新研究をもとに、ずんだもんと四国めたんが約5分で解説します。
「何でも速くなる夢の機械」ではない量子コンピュータの本当の姿と、実用化に向けた最大の壁「エラー」を乗り越える研究を紹介します。

▼チャプター
0:00 オープニング
0:16 量子ビットってなに？
0:54 最大の壁「エラー」
1:17 誤り訂正のしくみ（多数決）
2:05 突破口① Google「Willow」(2024)
2:36 突破口② 2025年ノーベル物理学賞
3:02 日本の研究：理研×富士通
3:30 いろいろな方式
4:02 いつ役に立つ？ IBMのロードマップ
4:32 今の暗号は破られる？
5:09 まとめ

▼この動画で紹介した研究
・Google「Willow」（2024年12月, Nature）：符号距離3→5→7で論理エラー率がおよそ半分ずつに（しきい値以下の誤り訂正）
・2025年ノーベル物理学賞：J. クラーク / M. デヴォレ / J. マルティニス（電気回路での巨視的量子トンネル効果とエネルギー量子化）
・理研×富士通：256量子ビット超伝導量子コンピュータ（2025年4月）、2026年度に1000量子ビット級を目標
・IBMのロードマップ：2029年 Starling（論理200量子ビット・1億演算）、2033年 Blue Jay（論理2000量子ビット）※企業の計画
・RSA-2048の解読に必要な量子ビット数の試算：2019年 約2000万 → 2025年 100万未満（Gidney, arXiv:2505.15917）
・NIST 耐量子暗号の標準（2024年8月, FIPS 203/204/205）

💬 量子コンピュータで一番楽しみな使い道は？ コメントで教えてください！

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
