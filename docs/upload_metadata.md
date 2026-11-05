# 投稿用メタデータ一覧（タイトル・説明欄・タグ・ハッシュタグ）
`python3 tools/build_upload_metadata.py` で各 README から作り直せます。「タイトル」「説明欄」「タグ」「固定コメント」はそれぞれコピーしてそのまま貼れます。
## 基本の考え方（なぜこう書くか）
- **タイトルと説明欄の最初の2〜3行がいちばん大事**：YouTube は、タイトル・サムネイル・説明欄などのメタデータから動画の内容を判断して検索や関連動画に出します。検索されやすい言葉（量子コンピュータ、大谷翔平 など）を前のほうに置き、後半で「？」を使って続きが気になる形にしています。（[YouTube ヘルプ：動画のメタデータに関するポリシー](https://support.google.com/youtube/answer/2801973?hl=ja)、[YouTube ヘルプ：パフォーマンスに関するよくある質問](https://support.google.com/youtube/answer/141805?hl=ja)）
- **タグの役割は小さい**：YouTube 自身が「タグは動画の発見にはあまり役立たず、つづりを間違えやすい言葉のときに役立つ」と説明しています。そのため、タグ欄には表記ゆれ（量子コンピュータ／量子コンピューター、ベーブ・ルース／ベーブルース／Babe Ruth）と言い換えだけを入れ、合計500文字以内にしています。（[YouTube ヘルプ：タグを追加する](https://support.google.com/youtube/answer/146402?hl=ja)）
- **ハッシュタグは3〜5個**：説明欄のハッシュタグは、最初の3つがタイトルの上に表示されます。60個を超えると全部無視され、関係のないタグはポリシー違反になるので、内容に合うものだけにしています。（[YouTube ヘルプ：ハッシュタグを使う](https://support.google.com/youtube/answer/6390658?hl=ja)）
- **ショートは本編へつなぐ**：ショートの編集画面で「関連動画」に本編を設定すると、ショートの画面に本編へのリンクが出ます。（[YouTube ヘルプ：ショートに関連動画を追加する](https://support.google.com/youtube/answer/14075157?hl=ja)）
- **チャプター**：説明欄に 0:00 から始まる時刻を3つ以上（各10秒以上）書くと、自動でチャプターになります。本編の説明欄にはすでに入っています。（[YouTube ヘルプ：動画のチャプター](https://support.google.com/youtube/answer/9884579?hl=ja)）
- 説明欄の「（URLを貼る）」は、公開後の動画・再生リストのURLに置きかえてください。

## 目次
1. シリーズ本編（第1回〜第10回）
2. シリーズのショート（10本）
3. 総集編
4. 以前作ったショート（雑学・量子・MLB 8本）

---

# 1. シリーズ本編「ずんだもんの量子技術解説」

## 第1回 量子コンピュータは、いつ役に立つのか？（6分04秒・`longform_quantum/`）
**タイトル（おすすめ）**
```
量子コンピュータはいつ使える？最大の壁「エラー」突破の最前線【ずんだもん解説】
```
<details><summary>ほかの候補（A/Bテスト用）</summary>

```
Google Willow・ノーベル賞・日本の256量子ビット 量子コンピュータの今が6分でわかる【ずんだもん】
```
```
量子コンピュータで暗号は破られる？実用化の目安は2030年前後【ずんだもん解説】
```
</details>

**説明欄**
```
「量子コンピュータって、結局いつ役に立つの？」
その答えに、ここ1〜2年の研究で大きく近づきました。実用化を阻む最大の壁「エラー」を、どうやって乗り越え始めたのかを、ずんだもんと四国めたんが約6分で解説します。

・量子ビットの「重ね合わせ」と「もつれ」とは？（何でも一気に試せるわけではない）
・エラーを減らす「量子誤り訂正」を多数決のたとえで解説
・Google Willow：量子ビットを増やすほどエラーが約半分に（2024年）
・2025年ノーベル物理学賞と、日本の256量子ビット機（理研×富士通）
・本格的な機械は2030年前後が目標？ 今の暗号は大丈夫？

▼チャプター
0:00 予告
0:12 オープニング
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
**タグ**（タグ欄に貼る）
```
量子誤り訂正, Willow, Google, ウィロー, エラー訂正, 論理量子ビット, ノーベル物理学賞 2025, 量子ビット, 実用化, 量子コンピュータ, 量子コンピューター, 量子力学, ずんだもん, 四国めたん, ずんだもん解説, VOICEVOX, 科学解説, わかりやすい, 量子技術解説 第1回
```
**固定コメント**
```
量子コンピュータで一番楽しみな使い道は？ 次に解説してほしいテーマもコメントで！
```
**設定**：再生リスト「ずんだもんの量子技術解説」に追加 / 終了画面に第2回を表示 / カテゴリ「教育」または「科学と技術」/ 言語「日本語」/ 字幕は自動生成でOK

## 第2回 量子コンピュータが得意な計算（6分05秒・`longform_quantum2/`）
**タイトル（おすすめ）**
```
量子コンピュータは「何でも速い」は誤解！本当に得意な3つの計算【ずんだもん解説】
```
<details><summary>ほかの候補（A/Bテスト用）</summary>

```
スパコンの1万3000倍は本当？量子コンピュータが速い計算・速くない計算【ずんだもん解説】
```
```
量子コンピュータは何が得意？暗号・探索・分子シミュレーションを6分で解説【ずんだもん】
```
</details>

**説明欄**
```
量子コンピュータは「何でも爆速になる夢の機械」…ではありません。
本当に得意なのは、干渉をうまく使える一部の計算だけ。暗号を破る素因数分解、探し物を速くする探索、新薬や新素材につながる分子シミュレーションの3つを、ずんだもんと四国めたんが約6分で解説します。

・なぜ量子コンピュータは速くなるの？（原理は「干渉」）
・15＝3×5 を「余りの周期」から見つけるショアのアルゴリズム
・100万回 → 約800回に減らすグローバーのアルゴリズム
・「スパコンの1万3000倍」など、量子の優位性のニュースの読み方
・実は苦手なこと（普通の計算・大量のデータ・AI）

▼チャプター
0:00 予告
0:10 オープニング
0:35 基本の原理：干渉
1:11 得意技① 素因数分解（ショア 1994）
2:23 得意技② 探索（グローバー 1996）
3:06 得意技③ 分子・物質のシミュレーション
3:53 実際に示された「量子の優位性」
4:58 実は苦手なこと
5:34 まとめ
5:49 次回予告

▼この動画で紹介した研究
・ショアのアルゴリズム（1994年）：素因数分解を「周期を見つける問題」に変えて効率よく解く
・グローバーのアルゴリズム（1996年）：N個から1つを約√N回（π/4×√N回）で探す。この種の探索では最適
・ファインマン「Simulating Physics with Computers」（1981年講演、1982年論文）
・窒素固定酵素（FeMoco）の量子計算の見積もり（Reiher ほか, PNAS 2017）
・Google Sycamore（2019年, Nature）：200秒 vs スパコン1万年（IBMは約2.5日と反論）
・Google Willow（2024年）：5分 vs スパコン10^25年（ランダム回路サンプリング）
・Google Quantum Echoes（2025年10月, Nature）：OTOCの計算でスパコンの約1万3000倍

💬 量子コンピュータに一番解いてほしい問題は？ コメントで教えてください！
▶ 第1回「量子コンピュータは、いつ役に立つのか？」も公開中（URLを貼る）

出典:
Shor (1994/1995) arXiv:quant-ph/9508027 https://arxiv.org/abs/quant-ph/9508027
Grover (1996) arXiv:quant-ph/9605043 https://arxiv.org/abs/quant-ph/9605043
IBM Quantum Learning（グローバーのアルゴリズム）https://quantum.cloud.ibm.com/learning/en/modules/computer-science/grovers
Feynman (1982) Int. J. Theor. Phys. 21, 467 https://doi.org/10.1007/BF02650179
Reiher et al. (2017) PNAS 114, 7555 https://doi.org/10.1073/pnas.1619152114
Arute et al. (2019) Nature 574, 505 https://doi.org/10.1038/s41586-019-1666-5
Google（Willow, 2024）https://blog.google/technology/research/google-willow-quantum-chip/
Google Quantum AI (2025) Nature 646, 825 https://doi.org/10.1038/s41586-025-09526-6
Google（Quantum Echoes, 2025）https://blog.google/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/
The Quantum Insider（13,000倍・Frontier 3.2年 vs 約2時間）https://thequantuminsider.com/?p=2381758
Aaronson (2015) "Read the fine print" Nature Physics 11, 291 https://doi.org/10.1038/nphys3272

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子コンピュータ #ずんだもん #科学解説
```
**タグ**（タグ欄に貼る）
```
ショアのアルゴリズム, グローバーのアルゴリズム, 素因数分解, 干渉, 量子優位性, 量子超越性, 分子シミュレーション, RSA暗号, 量子コンピュータ, 量子コンピューター, 量子力学, ずんだもん, 四国めたん, ずんだもん解説, VOICEVOX, 科学解説, わかりやすい, 量子技術解説 第2回
```
**固定コメント**
```
量子コンピュータで一番解いてほしい問題は？ 次に解説してほしいテーマもコメントで！
```
**設定**：再生リスト「ずんだもんの量子技術解説」に追加 / 終了画面に第3回を表示 / カテゴリ「教育」または「科学と技術」/ 言語「日本語」/ 字幕は自動生成でOK

## 第3回 量子コンピュータの作り方（6分07秒・`longform_quantum3/`）
**タイトル（おすすめ）**
```
量子コンピュータはどう作る？超伝導・イオン・原子・光の4方式を比較【ずんだもん解説】
```
<details><summary>ほかの候補（A/Bテスト用）</summary>

```
宇宙より寒い？光で原子をつかむ？量子コンピュータの作り方がすごすぎる【ずんだもん解説】
```
```
量子コンピュータの「主役」はまだ決まっていない 方式ごとの強みと課題【ずんだもん】
```
</details>

**説明欄**
```
量子コンピュータは、実は作り方が1つに決まっていません。
電気回路、宙に浮かせた原子、光でつかんだ原子、光そのもの…。それぞれの方式のしくみと、得意なこと・苦手なことを、ずんだもんと四国めたんが約6分で比べます。

・量子ビットに必要な条件は？（「守る」と「操作する」のバランス）
・超伝導：絶対零度近くまで冷やして、数十ナノ秒で操作
・イオントラップ：98量子ビット、操作の精度99.92%（Quantinuum Helios）
・中性原子：光のピンセットで6100個の原子を並べる（Caltech）
・光：ほぼ室温で動く、日本が強い分野（理研・NTTほか）
・シリコンとトポロジカル（Microsoft Majorana 1 は議論が続く）

▼チャプター
0:00 予告・オープニング
0:33 量子ビットに必要な条件
1:21 方式① 超伝導回路
2:09 方式② イオントラップ
2:54 方式③ 中性原子
3:41 方式④ 光（フォトン）
4:19 ほかの方式：シリコン・トポロジカル
5:04 比べてみよう
5:37 まとめ
5:51 次回予告

💬 どの方式が勝つと思う？ コメントで予想を教えてください！
▶ 第1回「量子コンピュータは、いつ役に立つのか？」（URLを貼る）
▶ 第2回「量子コンピュータが得意な計算」（URLを貼る）

出典:
DiVincenzo (2000)「The Physical Implementation of Quantum Computation」https://arxiv.org/abs/quant-ph/0002077
NobelPrize.org（2025年物理学賞・超伝導回路）https://www.nobelprize.org/prizes/physics/2025/summary/
IBM（冷却システム 15ミリケルビン未満）https://www.ibm.com/think/podcasts/the-coherence-times/ibm-quantum-computers-superconducting-quantum-computing
超伝導とイオンの操作時間・コヒーレンス時間の比較 https://arxiv.org/abs/1904.04178
Quantinuum（Helios, 2025年11月）https://quantinuum.com/blog/introducing-helios-the-most-accurate-quantum-computer-in-the-world
The Quantum Insider（Caltech 6100量子ビット, 2025）https://thequantuminsider.com/2025/09/24/caltech-team-sets-record-with-6100-qubit-array/
The Quantum Insider（Harvard・QuEra 48論理量子ビット, 2023）https://thequantuminsider.com/2023/12/06/harvard-quera-mit-and-the-nist-university-of-maryland-usher-in-new-era-of-quantum-computing-by-performing-complex-error-corrected-quantum-algorithms-on-48-logical-qubits/
NTT（汎用型光量子計算プラットフォーム, 2024年11月）https://group.ntt/jp/newsrelease/2024/11/08/241108a.html
JST（同上）https://www.jst.go.jp/pr/announce/20241108-3/index.html
Intel（Tunnel Falls, 2023）https://newsroom.intel.com/new-technologies/quantum-computing-chip-to-advance-research
Science News（Majorana 1 への専門家の見方）https://www.sciencenews.org/article/microsoft-topological-quantum-majorana

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子コンピュータ #ずんだもん #科学解説
```
**タグ**（タグ欄に貼る）
```
超伝導量子ビット, イオントラップ, 中性原子, 光量子コンピュータ, 光ピンセット, シリコン量子ビット, トポロジカル量子ビット, Majorana 1, 量子コンピュータ, 量子コンピューター, 量子力学, ずんだもん, 四国めたん, ずんだもん解説, VOICEVOX, 科学解説, わかりやすい, 量子技術解説 第3回
```
**固定コメント**
```
どの方式が勝つと思う？ 超伝導・イオン・中性原子・光から予想してコメントしてください！
```
**設定**：再生リスト「ずんだもんの量子技術解説」に追加 / 終了画面に第4回を表示 / カテゴリ「教育」または「科学と技術」/ 言語「日本語」/ 字幕は自動生成でOK

## 第4回 量子通信と量子暗号（6分21秒・`longform_quantum4/`）
**タイトル（おすすめ）**
```
盗み見すると誤りが増える？量子暗号のしくみと「意外な弱点」【ずんだもん解説】
```
<details><summary>ほかの候補（A/Bテスト用）</summary>

```
量子暗号は最強の暗号？光子1個で鍵を送るしくみと限界を解説【ずんだもん解説】
```
```
「今盗んで、あとで解読」量子コンピュータ時代の暗号の守り方【ずんだもん】
```
</details>

**説明欄**
```
「盗み見するとバレる通信」――量子暗号は本当に最強なのでしょうか？
光子1個ずつの向きで暗号の鍵を送る量子鍵配送（BB84）のしくみから、宇宙からの量子通信、そしてあまり知られていない弱点まで、ずんだもんと四国めたんが約6分で解説します。

・暗号の弱点は「鍵をどう届けるか」
・「今盗んで、あとで解読」という量子コンピュータ時代の脅威
・BB84：測り方が一致した光子だけで鍵を作るしくみ
・盗み見すると誤り率が約25%に上がる理由（測ると変わる・コピーできない）
・衛星「墨子」による約1200kmの量子鍵配送
・量子暗号の弱点と、耐量子暗号との使い分け

▼チャプター
0:00 予告
0:11 オープニング
0:28 暗号の基本は「鍵」
1:14 「今盗んで、あとで解読」の脅威
1:46 量子鍵配送のしくみ（BB84）
2:37 なぜ盗み見がバレるのか
3:34 距離の壁と、宇宙からの量子通信
4:26 量子暗号の弱点
5:04 2つの守り方を比べよう
5:42 まとめ
6:05 次回予告

💬 あなたなら耐量子暗号と量子暗号、どちらを使う？ コメントで教えてください！
▶ 第1回〜第3回も公開中（再生リストのURLを貼る）

出典:
Bennett & Brassard（BB84）の解説 arXiv:quant-ph/0601207 https://arxiv.org/abs/quant-ph/0601207
BB84の安全性と誤り率25%の導出 arXiv:1409.1452 https://arxiv.org/abs/1409.1452
Wootters & Zurek (1982)「A single quantum cannot be cloned」Nature 299, 802 https://doi.org/10.1038/299802a0
The Quantum Insider（Harvest now, decrypt later）https://thequantuminsider.com/2026/05/01/harvest-now-decrypt-later-why-should-you-care/
NICT（Tokyo QKD Network, 2010）https://www1.nict.go.jp/en/press/2010/10/14-1.html
中国科学院（墨子 衛星‐地上 約1200km, Nature 2017）https://english.cas.cn/head/201801/t20180119_189420.shtml
APS Physics（衛星中継の大陸間量子通信, 2018）https://physics.aps.org/articles/v11/7
Optica（光ファイバー1002kmの量子鍵配送, 2023）https://www.optica-opn.org/home/newsroom/2023/june/qkd_experiment_breaks_distance_record
NSA（量子鍵配送についての見解）https://www.nsa.gov/Cybersecurity/Post-Quantum-Cybersecurity-Resources/
NSAの見解への反論 arXiv:2307.15116 https://arxiv.org/abs/2307.15116
Cloud Security Alliance（NIST FIPS 203/204/205）https://cloudsecurityalliance.org/articles/nist-fips-203-204-and-205-finalized-an-important-step-towards-a-quantum-safe-future

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子暗号 #ずんだもん #科学解説
```
**タグ**（タグ欄に貼る）
```
量子暗号, 量子鍵配送, QKD, BB84, 耐量子暗号, PQC, Harvest now decrypt later, 墨子, 量子通信, 暗号, 量子コンピュータ, 量子コンピューター, 量子力学, ずんだもん, 四国めたん, ずんだもん解説, VOICEVOX, 科学解説, わかりやすい, 量子技術解説 第4回
```
**固定コメント**
```
あなたなら耐量子暗号と量子暗号、どちらを使う？ 次に解説してほしいテーマもコメントで！
```
**設定**：再生リスト「ずんだもんの量子技術解説」に追加 / 終了画面に第5回を表示 / カテゴリ「教育」または「科学と技術」/ 言語「日本語」/ 字幕は自動生成でOK

## 第5回 量子センサ（5分48秒・`longform_quantum5/`）
**タイトル（おすすめ）**
```
スカイツリーの上は時間が速い？300億年に1秒もずれない時計と量子センサ【ずんだもん解説】
```
<details><summary>ほかの候補（A/Bテスト用）</summary>

```
量子コンピュータより先に役立つ？「量子センサ」のしくみをやさしく解説【ずんだもん解説】
```
```
1cmの高さが時計でわかる？日本発の光格子時計と量子センサ【ずんだもん】
```
</details>

**説明欄**
```
スカイツリーの展望台では、地上より時間が1日に約4ナノ秒速く進む――それを実際に測ったのが、日本発の「光格子時計」です。
量子の状態の「壊れやすさ」を「敏感さ」に変えて、時間・磁場・重力を超精密に測る量子センサを、ずんだもんと四国めたんが約6分で解説します。

・量子センサの原理：壊れやすさを逆に使う
・測り方の3ステップ（重ね合わせ → 待つ → 干渉させて測る）
・光格子時計：18桁の精度、300億年で1秒もずれない
・スカイツリーで一般相対性理論を確かめた実験（2020年）
・ダイヤモンドの量子センサ：室温で心臓の磁場を測る
・原子の干渉で、GPSなしでも位置が分かる？

▼チャプター
0:00 予告・オープニング
0:32 基本の原理：壊れやすさを逆に使う
1:04 量子センサの測り方（3ステップ）
1:52 世界最高レベルの時計「光格子時計」
2:38 スカイツリーで相対性理論を確かめた
3:20 1cmの高さのちがいが分かる時計
3:55 ダイヤモンドの量子センサ
4:39 GPSがなくても位置が分かる？
5:17 まとめ
5:31 次回予告

※「300億年」「3億年」は、精度の桁数から計算した目安です（18桁 → 10^18秒 ≒ 約300億年）。
※1cmの高さの差による時間の進み方の差（約10^-18）は、一般相対性理論の式 Δf/f ≈ gh/c² から計算できます。

💬 量子センサで測ってみたいものは？ コメントで教えてください！
▶ 量子技術解説シリーズ 第1回〜第4回も公開中（再生リストのURLを貼る）

出典:
香取量子計測プロジェクト（光格子時計の提案と実証）https://www.katori-project.t.u-tokyo.ac.jp
JST（スカイツリーでの相対論検証, 2020年4月）https://www.jst.go.jp/pr/announce/20200407/index.html
理化学研究所（同上）https://www.riken.jp/press/2020/20200407_2/index.html
NIST（1秒の定義の見直し）https://www.nist.gov/si-redefinition/second-future
nippon.com（光格子時計と秒の再定義、商用化）https://www.nippon.com/en/in-depth/d01235/
Physics World（ダイヤモンドセンサによる心臓の磁場計測）https://physicsworld.com/a/high-resolution-diamond-sensor-maps-electrical-currents-in-the-heart/
東京工業大学（ダイヤモンド量子センサ）https://www.titech.ac.jp/english/news/2024/069398
Boeing・AOSense の量子航法の飛行試験（2024年）https://gbp.com.sg/stories/boeing-conducts-quantum-navigation-flight-test

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子センサ #ずんだもん #科学解説
```
**タグ**（タグ欄に貼る）
```
量子センサ, 量子センサー, 光格子時計, 原子時計, 一般相対性理論, 東京スカイツリー, NVセンター, ダイヤモンドNVセンタ, 香取秀俊, 量子コンピュータ, 量子コンピューター, 量子力学, ずんだもん, 四国めたん, ずんだもん解説, VOICEVOX, 科学解説, わかりやすい, 量子技術解説 第5回
```
**固定コメント**
```
量子センサで測ってみたいものは？ 次に解説してほしいテーマもコメントで！
```
**設定**：再生リスト「ずんだもんの量子技術解説」に追加 / 終了画面に第6回を表示 / カテゴリ「教育」または「科学と技術」/ 言語「日本語」/ 字幕は自動生成でOK

## 第6回 量子もつれとテレポーテーション（5分40秒・`longform_quantum6/`）
**タイトル（おすすめ）**
```
量子テレポーテーションは瞬間移動？アインシュタインが「不気味」と呼んだ量子もつれ【ずんだもん解説】
```
<details><summary>ほかの候補（A/Bテスト用）</summary>

```
光より速く通信できる？量子もつれの本当のしくみと2022年ノーベル賞【ずんだもん解説】
```
```
手袋のたとえでは説明できない「量子もつれ」をやさしく解説【ずんだもん】
```
</details>

**説明欄**
```
量子テレポーテーションは、人や物の瞬間移動ではありません。では、何が送れるのでしょうか？
アインシュタインが「不気味な遠隔作用」と呼んだ量子もつれ、それを実験で確かめた2022年ノーベル物理学賞、そして量子テレポーテーションのしくみを、ずんだもんと四国めたんが約6分で解説します。

・量子もつれ：測るまで結果が決まっていない「セット」
・手袋のたとえ（最初から決まっている）とのちがい
・ベルの不等式：前もって決まっていれば上限は2、実験では2を超えた
・もつれを使っても、光より速く情報は送れない理由
・量子テレポーテーションの4つの手順と、実験の歩み

▼チャプター
0:00 予告
0:11 オープニング
0:35 量子もつれとは
1:10 手袋のたとえとのちがい
1:51 ベルの不等式：実験で決着をつける
2:40 2022年ノーベル物理学賞
3:07 光より速く情報は送れない
3:39 量子テレポーテーションのしくみ
4:21 テレポーテーションの実験の歩み
5:02 まとめ
5:24 次回予告

※「約2.83」は量子力学で取りうる最大値（2√2）。2015年の実験値 2.42 はデルフト工科大学の論文より。

💬 量子もつれ、直感的に納得できた？ コメントで教えてください！
▶ 量子技術解説シリーズ 第1回〜第5回も公開中（再生リストのURLを貼る）

出典:
Einstein, Podolsky, Rosen (1935) Phys. Rev. 47, 777 https://doi.org/10.1103/PhysRev.47.777
NobelPrize.org（2022年物理学賞）https://www.nobelprize.org/prizes/physics/2022/summary/
QuTech（デルフト工科大学 抜け穴のないベルテスト, 2015）https://qutech.nl/lab/hanson-lab/research-highlights/hanson-lab-loophole-free-bell-test
Hensen et al. (2015) arXiv:1508.05949 https://arxiv.org/abs/1508.05949
Furusawa et al. (1998)「Unconditional quantum teleportation」Science 282, 706 https://doi.org/10.1126/science.282.5389.706
Ren et al. (2017)「Ground-to-satellite quantum teleportation」arXiv:1707.00934 https://arxiv.org/abs/1707.00934
MIT Technology Review（地上から衛星へのテレポーテーション）https://www.technologyreview.com/2017/07/10/150547/first-object-teleported-from-earth-to-orbit/

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子もつれ #ずんだもん #科学解説
```
**タグ**（タグ欄に貼る）
```
量子もつれ, 量子エンタングルメント, 量子テレポーテーション, ベルの不等式, EPRパラドックス, アインシュタイン, ノーベル物理学賞 2022, 量子コンピュータ, 量子コンピューター, 量子力学, ずんだもん, 四国めたん, ずんだもん解説, VOICEVOX, 科学解説, わかりやすい, 量子技術解説 第6回
```
**固定コメント**
```
量子もつれ、直感的に納得できた？ 次に解説してほしいテーマもコメントで！
```
**設定**：再生リスト「ずんだもんの量子技術解説」に追加 / 終了画面に第7回を表示 / カテゴリ「教育」または「科学と技術」/ 言語「日本語」/ 字幕は自動生成でOK

## 第7回 量子アニーリング（6分12秒・`longform_quantum7/`）
**タイトル（おすすめ）**
```
日本で定式化された量子計算「量子アニーリング」とは？しくみと本当の実力【ずんだもん解説】
```
<details><summary>ほかの候補（A/Bテスト用）</summary>

```
30都市の道順で1400億年？量子アニーリングが挑む「組合せ最適化」【ずんだもん解説】
```
```
D-Waveは本当に速い？量子アニーリングとゲート型のちがい【ずんだもん】
```
</details>

**説明欄**
```
量子アニーリングは、1998年に東京工業大学の門脇正史さんと西森秀稔さんが今の基本の形に定式化した、日本ゆかりの量子計算の方法です。
たくさんの選び方から一番よい答えを探す「組合せ最適化」を、量子のゆらぎで解こうとするしくみと、D-Waveの装置、そして「本当に速いのか？」という議論まで、ずんだもんと四国めたんが約6分で解説します。

・組合せ最適化：30都市の道順は約4.4×10^30通り（1秒に1兆通り調べても約1400億年）
・答えを地形に置きかえ、一番低い谷を探す
・焼きなまし（アニーリング）から量子アニーリングへ
・D-Waveの装置（2011年発表、2025年 Advantage2 は4400量子ビット超）
・ゲート型とのちがいと、速さをめぐる議論
・量子に着想を得た、ふつうの計算機（富士通 デジタルアニーラ）

▼チャプター
0:00 予告
0:10 オープニング
0:38 組合せ最適化：選び方が爆発する
1:38 答えを「エネルギーの谷」で考える
2:17 焼きなましから量子アニーリングへ
3:02 D-Waveが実際に作った
3:39 ゲート型とのちがい
4:19 本当に速いの？
5:06 量子に着想を得た、ふつうの計算機
5:38 まとめ
5:55 次回予告

※道順の数は (n−1)!/2 で計算（向きが逆の道順は同じとみなす）。20都市で約6.1×10^16通り、30都市で約4.4×10^30通り。

💬 量子アニーリングで解いてほしい「最適化」の問題は？ コメントで教えてください！
▶ 量子技術解説シリーズ 第1回〜第6回も公開中（再生リストのURLを貼る）

出典:
Kadowaki & Nishimori (1998)「Quantum annealing in the transverse Ising model」Phys. Rev. E 58, 5355 https://doi.org/10.1103/PhysRevE.58.5355
東京工業大学（量子アニーリングの提案と D-Wave）https://www.titech.ac.jp/news/2015/031986
東京工業大学（西森秀稔さんインタビュー）https://www.titech.ac.jp/public-relations/research/stories/faces13-nishimori
D-Wave（Advantage2 の一般提供, 2025年5月）https://www.businesswire.com/news/home/20250520948155/en/D-Wave-Announces-General-Availability-of-Advantage2-Quantum-Computer-Its-Most-Advanced-and-Performant-System
HPCwire（D-Wave の Science 論文と反論, 2025年3月）https://www.hpcwire.com/2025/03/13/d-wave-reports-quantum-supremacy-stirs-immediate-challenge-and-rebuttal/
富士通（デジタルアニーラ クラウドサービス開始, 2018年）https://www.fujitsu.com/global/about/resources/news/press-releases/2018/0515-01.html

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子アニーリング #ずんだもん #科学解説
```
**タグ**（タグ欄に貼る）
```
量子アニーリング, D-Wave, ディーウェーブ, 組合せ最適化, 巡回セールスマン問題, 西森秀稔, 門脇正史, イジングマシン, 量子コンピュータ, 量子コンピューター, 量子力学, ずんだもん, 四国めたん, ずんだもん解説, VOICEVOX, 科学解説, わかりやすい, 量子技術解説 第7回
```
**固定コメント**
```
量子アニーリングで解いてほしい「最適化」の問題は？ 次に解説してほしいテーマもコメントで！
```
**設定**：再生リスト「ずんだもんの量子技術解説」に追加 / 終了画面に第8回を表示 / カテゴリ「教育」または「科学と技術」/ 言語「日本語」/ 字幕は自動生成でOK

## 第8回 量子インターネット（5分40秒・`longform_quantum8/`）
**タイトル（おすすめ）**
```
量子インターネットで何ができる？コピーできない情報を遠くへ届けるしくみ【ずんだもん解説】
```
<details><summary>ほかの候補（A/Bテスト用）</summary>

```
1000kmで300年に1個？光が届かない問題を「量子中継」で解決【ずんだもん解説】
```
```
会ったことのない2つがもつれる？「もつれ交換」と量子インターネット【ずんだもん】
```
</details>

**説明欄**
```
量子インターネットは、今のインターネットを速くするものではありません。量子の状態や「もつれ」を、遠くの相手に届けるためのネットワークです。
コピーできない量子の情報を、どうやって遠くまで届けるのか。量子中継・もつれ交換・量子メモリのしくみと、最新の実験、そしてできるようになることを、ずんだもんと四国めたんが約6分で解説します。

・なぜふつうの通信のように増幅できないのか（量子はコピーできない）
・光ファイバーでは50kmごとに光が1/10に（1000kmなら300年に1個）
・量子中継：短い区間のもつれを「もつれ交換」でつなぐ
・量子メモリ：成功するまで、もつれを保存しておく
・2022年 3ノードの量子ネットワーク、2024年 ボストンの光ファイバー35km
・量子インターネットでできること、6段階のロードマップ

▼チャプター
0:00 予告・オープニング
0:35 なぜふつうに送れないのか
1:10 光ファイバーで光はどれだけ減る？
1:52 量子中継のアイデア：もつれ交換
2:45 量子メモリ：成功するまで待つ
3:26 実験の進歩
4:00 量子インターネットで何ができる？
4:34 6段階のロードマップ
5:09 まとめ
5:25 次回予告

※光ファイバーの損失は 0.2dB/km（よく使われる波長での代表値）として計算。50kmで10dB＝1/10、1000kmで200dB＝10^-20。

💬 量子インターネットで一番やってみたいことは？ コメントで教えてください！
▶ 量子技術解説シリーズ 第1回〜第7回も公開中（再生リストのURLを貼る）

出典:
Briegel, Dür, Cirac, Zoller (1998)「Quantum repeaters for communication」arXiv:quant-ph/9803056 https://arxiv.org/abs/quant-ph/9803056
Dür et al. (1999)「Quantum repeaters based on entanglement purification」arXiv:quant-ph/9808065 https://arxiv.org/abs/quant-ph/9808065
QuTech（3ノード網で隣でないノードへのテレポーテーション, 2022）https://qutech.nl/2022/05/25/teleport-quantum-information-across-network/
AWS Quantum Technologies Blog（ボストン35kmの量子ネットワーク, 2024）https://aws.amazon.com/blogs/quantum-computing/delivering-quantum-information-a-field-deployed-quantum-network/
Knaut et al.「Entanglement of Nanophotonic Quantum Memory Nodes in a Telecommunication Network」arXiv:2310.01316 https://arxiv.org/abs/2310.01316
Wehner, Elkouss, Hanson (2018)「Quantum internet: A vision for the road ahead」Science 362, eaam9288 https://doi.org/10.1126/science.aam9288
Broadbent, Fitzsimons, Kashefi（中身を見せずに計算を頼む方法）arXiv:0807.4154 https://arxiv.org/abs/0807.4154

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子インターネット #ずんだもん #科学解説
```
**タグ**（タグ欄に貼る）
```
量子インターネット, 量子中継, もつれ交換, エンタングルメントスワッピング, 量子メモリ, 量子ネットワーク, QuTech, 量子コンピュータ, 量子コンピューター, 量子力学, ずんだもん, 四国めたん, ずんだもん解説, VOICEVOX, 科学解説, わかりやすい, 量子技術解説 第8回
```
**固定コメント**
```
量子インターネットで一番やってみたいことは？ 次に解説してほしいテーマもコメントで！
```
**設定**：再生リスト「ずんだもんの量子技術解説」に追加 / 終了画面に第9回を表示 / カテゴリ「教育」または「科学と技術」/ 言語「日本語」/ 字幕は自動生成でOK

## 第9回 量子×AIの本当のところ（5分45秒・`longform_quantum9/`）
**タイトル（おすすめ）**
```
量子でAIは爆速になる？期待と現実をやさしく整理【ずんだもん解説】
```
<details><summary>ほかの候補（A/Bテスト用）</summary>

```
18歳が量子に追いついた？「量子AI」の期待と「脱量子化」の話【ずんだもん解説】
```
```
「量子AI」のニュースを見分ける5つのチェックポイント【ずんだもん】
```
</details>

**説明欄**
```
「量子コンピュータとAIが合体すれば最強のAIができる」――本当でしょうか？
データの入り口と出口の壁、18歳の学生が量子の高速化に追いついた「脱量子化」、量子のデータを扱う場面での強み、そしてAIが量子コンピュータを助ける研究まで、ずんだもんと四国めたんが約6分で整理します。

・今のAIは何をしている？（行列の計算を大量に、GPUが得意）
・データの入り口と出口：量子の大きな壁
・期待された高速化と「脱量子化」（2018年 ユーイン・タン）
・量子ニューラルネットの壁「不毛な台地」
・量子が強そうな場面：量子のデータ（2022年 Science）
・AIが量子を助ける：AlphaQubit（2024年 Nature）
・量子AIのニュースを見分ける5つのポイント

▼チャプター
0:00 予告
0:10 オープニング
0:33 今のAIは何をしている？
1:06 データの入り口と出口の問題
1:50 期待された高速化と「脱量子化」
2:41 量子ニューラルネットの壁
3:17 量子が強そうな場面：量子のデータ
3:56 逆向き：AIが量子を助ける
4:38 ニュースの見分け方
5:10 まとめ
5:28 次回予告

💬 あなたが見た「量子AI」のニュース、5つのポイントで見るとどうだった？ コメントで教えてください！
▶ 量子技術解説シリーズ 第1回〜第8回も公開中（再生リストのURLを貼る）

出典:
Harrow, Hassidim, Lloyd (2009)「Quantum algorithm for linear systems of equations」arXiv:0811.3171 https://arxiv.org/abs/0811.3171
Aaronson (2015)「Read the fine print」Nature Physics 11, 291 https://doi.org/10.1038/nphys3272
Scott Aaronson のブログ（ユーイン・タンの脱量子化, 2018）https://scottaaronson.blog/?p=3880
Tang (2018)「A quantum-inspired classical algorithm for recommendation systems」arXiv:1807.04271 https://arxiv.org/abs/1807.04271
McClean et al. (2018)「Barren plateaus in quantum neural network training landscapes」arXiv:1803.11173 https://arxiv.org/abs/1803.11173
Huang et al. (2022)「Quantum advantage in learning from experiments」Science 376, 1182 / arXiv:2112.00778 https://arxiv.org/abs/2112.00778
Google（AlphaQubit, 2024）https://blog.google/technology/google-deepmind/alphaqubit-quantum-error-correction/
Bausch et al. (2024)「Learning high-accuracy error decoding for quantum processors」Nature https://doi.org/10.1038/s41586-024-08148-8

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子コンピュータ #AI #ずんだもん
```
**タグ**（タグ欄に貼る）
```
量子機械学習, 量子AI, AI, 人工知能, 脱量子化, HHLアルゴリズム, ユーイン・タン, データ読み込み, 量子コンピュータ, 量子コンピューター, 量子力学, ずんだもん, 四国めたん, ずんだもん解説, VOICEVOX, 科学解説, わかりやすい, 量子技術解説 第9回
```
**固定コメント**
```
あなたが見た「量子AI」のニュース、5つのポイントで見るとどうだった？ 次に解説してほしいテーマもコメントで！
```
**設定**：再生リスト「ずんだもんの量子技術解説」に追加 / 終了画面に第10回を表示 / カテゴリ「教育」または「科学と技術」/ 言語「日本語」/ 字幕は自動生成でOK

## 第10回 総まとめ：2030年に何が起きる？（5分49秒・`longform_quantum10/`）
**タイトル（おすすめ）**
```
2030年、量子技術はどうなる？計算・通信・センサの未来をまとめて解説【ずんだもん解説・最終回】
```
<details><summary>ほかの候補（A/Bテスト用）</summary>

```
量子技術の全体像が6分でわかる！3つの原理と2030年の予定表【ずんだもん解説】
```
```
量子コンピュータだけじゃない 量子技術の3本柱と、暮らしの変化【ずんだもん】
```
</details>

**説明欄**
```
量子技術解説シリーズ、最終回です。
これまでの9回（量子コンピュータ・量子暗号・量子センサ・量子もつれ・量子アニーリング・量子インターネット・量子×AI）をふりかえり、全部をつなぐ3つの基本原理と、2030年ごろまでの予定表、わたしたちの暮らしの変化を、ずんだもんと四国めたんが約6分でまとめます。

・量子技術は「計算・通信・センサ」の3本柱
・全部をつなぐ3つの基本原理（重ね合わせと干渉／もつれ／測ると変わる・コピーできない）
・2030年ごろまでの予定表（理研×富士通、IBM Starling・Blue Jay、NISTの暗号移行）
・分野ごとの見通しと、日本の強み
・暮らしはどう変わる？ これからのニュースの読み方

▼チャプター
0:00 予告
0:10 オープニング
0:28 9回のふりかえり
1:04 全部をつなぐ3つの基本原理
1:37 2030年ごろまでの予定表
2:39 分野ごとの見通し
3:14 日本の強み
3:50 わたしたちの暮らしはどう変わる？
4:36 これからのニュースの読み方
5:07 まとめ：シリーズを終えて

※予定表の多くは企業・国の計画や目標、または案の段階のものです（2026年11月時点の情報）。

💬 シリーズで一番おもしろかった回は？ 次に解説してほしいテーマもコメントで教えてください！
▶ 量子技術解説シリーズ 第1回〜第9回（再生リストのURLを貼る）

出典:
理研・富士通（256量子ビット、1000量子ビット級の目標）https://monoist.itmedia.co.jp/mn/articles/2504/28/news064.html
HPCwire（IBM Starling 2029・Blue Jay 2033 のロードマップ）https://www.hpcwire.com/2025/06/10/ibm-sets-2029-target-for-fault-tolerant-quantum-computing/
ABI Research（NIST IR 8547 草案：RSA・ECC を2030年以降非推奨、2035年以降使用終了）https://www.abiresearch.com/market-research/insight/7785443-nists-intention-to-deprecate-rsa-and-ecc-w
NIST（1秒の定義の見直し）https://www.nist.gov/si-redefinition/second-future
内閣府（量子未来社会ビジョン：2030年に利用者1000万人）https://www.cao.go.jp/minister/2111_t_kobayashi/kaiken/20220415kaiken.html
香取量子計測プロジェクト（光格子時計）https://www.katori-project.t.u-tokyo.ac.jp
Kadowaki & Nishimori (1998) Phys. Rev. E 58, 5355 https://doi.org/10.1103/PhysRevE.58.5355
NTT（汎用型光量子計算プラットフォーム）https://group.ntt/jp/newsrelease/2024/11/08/241108a.html
（各回の詳しい出典は、それぞれの動画の説明欄に記載）

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子技術 #量子コンピュータ #ずんだもん
```
**タグ**（タグ欄に貼る）
```
量子技術, 2030年, ロードマップ, 誤り耐性量子コンピュータ, 耐量子暗号, NIST, 量子技術の未来, まとめ, 量子コンピュータ, 量子コンピューター, 量子力学, ずんだもん, 四国めたん, ずんだもん解説, VOICEVOX, 科学解説, わかりやすい, 量子技術解説 第10回
```
**固定コメント**
```
シリーズで一番おもしろかった回は？ 次に解説してほしいテーマもコメントで！
```
**設定**：再生リスト「ずんだもんの量子技術解説」に追加 / 終了画面に総集編または第1回を表示 / カテゴリ「教育」または「科学と技術」/ 言語「日本語」/ 字幕は自動生成でOK

---

# 2. シリーズのショート（`longform_quantum*/short.mp4`）
共通の設定：**関連動画**に同じ回の本編を設定 / 再生リスト「ずんだもんの量子技術解説」にも入れる

## ショート1（第1回から・0分22秒）
**タイトル**
```
量子ビットを増やすとエラーが減った！？ #shorts #量子コンピュータ
```
**説明欄**
```
量子ビットを増やすほどエラーが増える――それが量子コンピュータの長年の悩みでした。
2024年、グーグルの「Willow」は符号距離を3→5→7と大きくするたびに、論理エラー率がおよそ半分になることを示しました。
【原理】1個の情報を多数の量子ビットに分けて持たせ、どこが壊れたかだけを測って直す「量子誤り訂正」。
物理エラーが一定の値（しきい値）より小さいと、量子ビットを増やすほど全体のエラーが減ります。

▶ 本編：第1回「量子コンピュータは、いつ役に立つのか？」（URLを貼る）
▶ 再生リスト：ずんだもんの量子技術解説（URLを貼る）

出典:
Google Quantum AI「Quantum error correction below the surface code threshold」(Nature, 2024) 解説: APS Physics https://physics.aps.org/articles/v17/176
Scimex（Willow）https://www.scimex.org/newsfeed/googles-new-quantum-chip-hits-error-correction-target
NobelPrize.org（2025年物理学賞）https://www.nobelprize.org/prizes/physics/2025/summary/

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル

#量子コンピュータ #ずんだもん #shorts
```
**タグ**
```
量子誤り訂正, Willow, 量子コンピュータ, 量子力学, ずんだもん, 四国めたん, VOICEVOX, 科学, 雑学, shorts
```

## ショート2（第2回から・0分25秒）
**タイトル**
```
15＝3×5を量子コンピュータはどう解く？ #shorts #量子コンピュータ
```
**説明欄**
```
7を何回もかけて15で割った余りは 1, 7, 4, 13, 1…と4つごとにくり返します。
この「周期」がわかると、15を3と5に分けられます。
【原理】ショアのアルゴリズムは、素因数分解を「周期を見つける問題」に置きかえ、
量子の干渉（正しい周期の答えが強め合い、ほかが打ち消し合う）で周期を効率よく見つけます。

▶ 本編：第2回「量子コンピュータが得意な計算」（URLを貼る）
▶ 再生リスト：ずんだもんの量子技術解説（URLを貼る）

出典:
Shor (1994/1995) arXiv:quant-ph/9508027 https://arxiv.org/abs/quant-ph/9508027
Grover (1996) arXiv:quant-ph/9605043 https://arxiv.org/abs/quant-ph/9605043
IBM Quantum Learning（グローバーのアルゴリズム）https://quantum.cloud.ibm.com/learning/en/modules/computer-science/grovers

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル

#量子コンピュータ #ずんだもん #shorts
```
**タグ**
```
ショアのアルゴリズム, 素因数分解, 量子コンピュータ, 量子力学, ずんだもん, 四国めたん, VOICEVOX, 科学, 雑学, shorts
```

## ショート3（第3回から・0分22秒）
**タイトル**
```
光のピンセットで原子を6100個並べる！？ #shorts #量子コンピュータ
```
**説明欄**
```
レーザー光を細く絞ると、焦点に原子が引き寄せられます（光ピンセット）。
2025年、カルテックのチームは6100個の原子を並べ、重ね合わせを約13秒保ったと発表しました。
【原理】光の強い場所ほど原子のエネルギーが下がるため、原子は焦点に集まります。
1個1個の原子が量子ビットになり、並べ方も光で自由に変えられます。

▶ 本編：第3回「量子コンピュータの作り方」（URLを貼る）
▶ 再生リスト：ずんだもんの量子技術解説（URLを貼る）

出典:
DiVincenzo (2000)「The Physical Implementation of Quantum Computation」https://arxiv.org/abs/quant-ph/0002077
NobelPrize.org（2025年物理学賞・超伝導回路）https://www.nobelprize.org/prizes/physics/2025/summary/
IBM（冷却システム 15ミリケルビン未満）https://www.ibm.com/think/podcasts/the-coherence-times/ibm-quantum-computers-superconducting-quantum-computing

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル

#量子コンピュータ #ずんだもん #shorts
```
**タグ**
```
中性原子, 光ピンセット, 量子コンピュータ, 量子力学, ずんだもん, 四国めたん, VOICEVOX, 科学, 雑学, shorts
```

## ショート4（第4回から・0分24秒）
**タイトル**
```
盗み見すると誤りが増える「量子暗号」通信 #shorts #量子
```
**説明欄**
```
光の粒（光子）を1個ずつ、向きを変えて送る量子暗号（量子鍵配送, BB84）。
盗聴者は測り方を当てずっぽうで選ぶので、半分は間違えて光子の状態を変えてしまいます。
【原理】量子の状態は「測ると変わる」「完全にはコピーできない（量子複製不可能定理）」。
すべてを盗み見すると受け手の誤り率は約25%になり、誤りの割合を調べれば盗聴に気づけます。

▶ 本編：第4回「量子通信と量子暗号」（URLを貼る）
▶ 再生リスト：ずんだもんの量子技術解説（URLを貼る）

出典:
Bennett & Brassard（BB84）の解説 arXiv:quant-ph/0601207 https://arxiv.org/abs/quant-ph/0601207
BB84の安全性と誤り率25%の導出 arXiv:1409.1452 https://arxiv.org/abs/1409.1452
Wootters & Zurek (1982)「A single quantum cannot be cloned」Nature 299, 802 https://doi.org/10.1038/299802a0

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル

#量子暗号 #ずんだもん #shorts
```
**タグ**
```
量子暗号, 量子鍵配送, BB84, 量子コンピュータ, 量子力学, ずんだもん, 四国めたん, VOICEVOX, 科学, 雑学, shorts
```

## ショート5（第5回から・0分23秒）
**タイトル**
```
スカイツリーの上は時間が速い？ #shorts #量子センサ
```
**説明欄**
```
重力が弱い高い場所ほど、時間は速く進みます（アインシュタインの一般相対性理論）。
2020年、地上と高さ約450mの展望台で光格子時計を比べると、展望台の時計は1日に約4ナノ秒速く進んでいました。
【原理】原子が吸収する光の振動数は自然が決めた「目盛り」。光の格子に閉じ込めた多数の原子で
それを数えると、300億年に1秒もずれないほど正確な時計になり、高さのちがいまで測れます。

▶ 本編：第5回「量子センサ」（URLを貼る）
▶ 再生リスト：ずんだもんの量子技術解説（URLを貼る）

出典:
香取量子計測プロジェクト（光格子時計の提案と実証）https://www.katori-project.t.u-tokyo.ac.jp
JST（スカイツリーでの相対論検証, 2020年4月）https://www.jst.go.jp/pr/announce/20200407/index.html
理化学研究所（同上）https://www.riken.jp/press/2020/20200407_2/index.html

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル

#量子センサ #相対性理論 #ずんだもん #shorts
```
**タグ**
```
光格子時計, 東京スカイツリー, 相対性理論, 量子コンピュータ, 量子力学, ずんだもん, 四国めたん, VOICEVOX, 科学, 雑学, shorts
```

## ショート6（第6回から・0分22秒）
**タイトル**
```
離れていても結果がそろう「量子もつれ」 #shorts #量子
```
**説明欄**
```
もつれた2つの量子ビットは、片方を測って0が出ると、もう片方も必ず0になります。
でも、これを使っても光より速く情報は送れません。
【原理】片方だけを見ると結果は毎回ランダム。そろっていることは、
ふつうの通信で結果を見せ合って初めてわかるため、情報は光の速さを超えません。

▶ 本編：第6回「量子もつれとテレポーテーション」（URLを貼る）
▶ 再生リスト：ずんだもんの量子技術解説（URLを貼る）

出典:
Einstein, Podolsky, Rosen (1935) Phys. Rev. 47, 777 https://doi.org/10.1103/PhysRev.47.777
NobelPrize.org（2022年物理学賞）https://www.nobelprize.org/prizes/physics/2022/summary/
QuTech（デルフト工科大学 抜け穴のないベルテスト, 2015）https://qutech.nl/lab/hanson-lab/research-highlights/hanson-lab-loophole-free-bell-test

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル

#量子もつれ #ずんだもん #shorts
```
**タグ**
```
量子もつれ, 量子テレポーテーション, 量子コンピュータ, 量子力学, ずんだもん, 四国めたん, VOICEVOX, 科学, 雑学, shorts
```

## ショート7（第7回から・0分20秒）
**タイトル**
```
小さな谷をすり抜ける？「量子アニーリング」 #shorts #量子
```
**説明欄**
```
答えのよさを「高さ」に置きかえると、一番低い谷が一番よい答えになります。
ふつうのボールは途中の小さな谷にはまってしまいますが……
【原理】量子のゆらぎ（トンネル効果）を使うと、山を越えずにすり抜けられることがあります。
1998年に門脇正史さん・西森秀稔さんが定式化したアイデアで、本当に速いかは問題によります。

▶ 本編：第7回「量子アニーリング」（URLを貼る）
▶ 再生リスト：ずんだもんの量子技術解説（URLを貼る）

出典:
Kadowaki & Nishimori (1998)「Quantum annealing in the transverse Ising model」Phys. Rev. E 58, 5355 https://doi.org/10.1103/PhysRevE.58.5355
東京工業大学（量子アニーリングの提案と D-Wave）https://www.titech.ac.jp/news/2015/031986
東京工業大学（西森秀稔さんインタビュー）https://www.titech.ac.jp/public-relations/research/stories/faces13-nishimori

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル

#量子アニーリング #ずんだもん #shorts
```
**タグ**
```
量子アニーリング, D-Wave, 量子コンピュータ, 量子力学, ずんだもん, 四国めたん, VOICEVOX, 科学, 雑学, shorts
```

## ショート8（第8回から・0分19秒）
**タイトル**
```
会ったことのない2つがつながる「もつれ交換」 #shorts #量子
```
**説明欄**
```
長い道を短い区間に分け、区間ごとにもつれたペアを作ります。
真ん中の中継点が2つの粒をまとめて測ると、一度も出会っていない両端が直接もつれます。
【原理】光ファイバーでは光子が距離とともに失われ、量子の情報はコピーして増幅できません。
そこで「もつれ交換」で区間をつなぐのが量子中継、量子インターネットの土台です。

▶ 本編：第8回「量子インターネット」（URLを貼る）
▶ 再生リスト：ずんだもんの量子技術解説（URLを貼る）

出典:
Briegel, Dür, Cirac, Zoller (1998)「Quantum repeaters for communication」arXiv:quant-ph/9803056 https://arxiv.org/abs/quant-ph/9803056
Dür et al. (1999)「Quantum repeaters based on entanglement purification」arXiv:quant-ph/9808065 https://arxiv.org/abs/quant-ph/9808065
QuTech（3ノード網で隣でないノードへのテレポーテーション, 2022）https://qutech.nl/2022/05/25/teleport-quantum-information-across-network/

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル

#量子インターネット #ずんだもん #shorts
```
**タグ**
```
量子インターネット, もつれ交換, 量子コンピュータ, 量子力学, ずんだもん, 四国めたん, VOICEVOX, 科学, 雑学, shorts
```

## ショート9（第9回から・0分23秒）
**タイトル**
```
量子でAIは爆速になる？ #shorts #量子コンピュータ #AI
```
**説明欄**
```
「量子×AIで最強」と思いきや……
100万個の数字を量子の状態に入れるだけで、100万回分くらいの手間がかかることがあります。
【原理】計算の真ん中が速くても、データの「入力」と、答えを何度も測って取り出す「出力」が遅いと、
全体は速くなりません。量子AIのニュースは、入口と出口まで見るのがポイントです。

▶ 本編：第9回「量子×AIの本当のところ」（URLを貼る）
▶ 再生リスト：ずんだもんの量子技術解説（URLを貼る）

出典:
Harrow, Hassidim, Lloyd (2009)「Quantum algorithm for linear systems of equations」arXiv:0811.3171 https://arxiv.org/abs/0811.3171
Aaronson (2015)「Read the fine print」Nature Physics 11, 291 https://doi.org/10.1038/nphys3272
Scott Aaronson のブログ（ユーイン・タンの脱量子化, 2018）https://scottaaronson.blog/?p=3880

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル

#量子コンピュータ #AI #ずんだもん #shorts
```
**タグ**
```
量子AI, 量子機械学習, 量子コンピュータ, 量子力学, ずんだもん, 四国めたん, VOICEVOX, 科学, 雑学, shorts
```

## ショート10（第10回から・0分24秒）
**タイトル**
```
量子技術は2030年どうなる？ #shorts #量子コンピュータ
```
**説明欄**
```
量子技術は「計算・通信・センサ」の3本柱。
どれも「重ね合わせと干渉」「もつれ」「測ると変わる」の3つの原理でできています。
2030年前後は、古い暗号（RSA・楕円曲線暗号）の入れかえと、
エラーに強い量子コンピュータが大きな節目になりそうです。

▶ 本編：第10回「総まとめ：2030年に何が起きる？」（URLを貼る）
▶ 再生リスト：ずんだもんの量子技術解説（URLを貼る）

出典:
理研・富士通（256量子ビット、1000量子ビット級の目標）https://monoist.itmedia.co.jp/mn/articles/2504/28/news064.html
HPCwire（IBM Starling 2029・Blue Jay 2033 のロードマップ）https://www.hpcwire.com/2025/06/10/ibm-sets-2029-target-for-fault-tolerant-quantum-computing/
ABI Research（NIST IR 8547 草案：RSA・ECC を2030年以降非推奨、2035年以降使用終了）https://www.abiresearch.com/market-research/insight/7785443-nists-intention-to-deprecate-rsa-and-ecc-w

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル

#量子技術 #ずんだもん #shorts
```
**タグ**
```
量子技術, 2030年, 量子コンピュータ, 量子力学, ずんだもん, 四国めたん, VOICEVOX, 科学, 雑学, shorts
```

---

# 3. 総集編（`longform_quantum_all/`・約59分）
**タイトル（おすすめ）**
```
【総集編】量子技術がまるごとわかる1時間 量子コンピュータ・暗号・センサ・もつれ【ずんだもん解説】
```
**ほかの候補**
```
【作業用・総集編】ずんだもんと学ぶ量子技術 全10回まとめ
```
**説明欄**
```
量子技術解説シリーズ全10回を、1本にまとめた総集編です（約1時間）。
量子コンピュータの「いつ役に立つ？」から、得意な計算、作り方、量子暗号、量子センサ、量子もつれ、量子アニーリング、量子インターネット、量子×AI、そして2030年の見通しまで、ずんだもんと四国めたんが順番に解説します。
気になる回は、下のチャプターから飛べます。

▼チャプター
0:00 第1回 量子コンピュータは、いつ役に立つのか？
6:03 第2回 量子コンピュータが得意な計算
12:09 第3回 量子コンピュータの作り方
18:15 第4回 量子通信と量子暗号
24:37 第5回 量子センサ
30:25 第6回 量子もつれとテレポーテーション
36:05 第7回 量子アニーリング
42:17 第8回 量子インターネット
47:57 第9回 量子×AIの本当のところ
53:42 第10回 総まとめ：2030年に何が起きる？

※各回の詳しい出典は、それぞれの回の説明欄に記載しています（再生リストのURLを貼る）。
※数値や見通しは2026年11月時点の情報です。

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子コンピュータ #ずんだもん #総集編
```
**タグ**
```
総集編, 作業用, 一気見, 量子技術, 量子暗号, 量子センサ, 量子もつれ, 量子アニーリング, 量子インターネット, 量子AI, 勉強, 聞き流し, 量子コンピュータ, 量子コンピューター, 量子力学, ずんだもん, 四国めたん, ずんだもん解説, VOICEVOX, 科学解説, わかりやすい
```
**設定**：第10回の公開後に出す / 各回の説明欄からも総集編へリンク

---

# 4. 以前作ったショート

## はちみつはなぜ腐らない？（`shorts_honey/`）
**タイトル**
```
3000年前のはちみつが食べられる理由 #shorts #雑学
```
**説明欄**
```
はちみつが腐らない理由は3つ！
① 水分が少なく糖が濃い → 浸透圧で菌の水分を奪う
② pH約3〜4.5の酸性
③ ミツバチの酵素（グルコースオキシダーゼ）が過酸化水素を生成
※1歳未満の乳児にははちみつを与えないでください（乳児ボツリヌス症）
※保存はフタをしっかり閉めて。湿気を吸うと発酵することがあります

出典:
Smithsonian Magazine「The Science Behind Honey's Eternal Shelf Life」
https://www.smithsonianmag.com/science-nature/the-science-behind-honeys-eternal-shelf-life-1218690/
Codex Standard for Honey (CXS 12-1981, Rev. 2001)
https://www.ihc-platform.net/codex2001.pdf
厚生労働省「ハチミツによる乳児のボツリヌス症について」(あさコラム)
https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000168157.html
消費者庁 食品安全ポータル（ボツリヌス菌）
https://www.caa.go.jp/policies/policy/consumer_safety/food_safety/food_safety_portal/microorganism_virus/contents_001

VOICEVOX:ずんだもん

#雑学 #豆知識 #はちみつ #科学 #shorts
```
**タグ**
```
はちみつ, 蜂蜜, 腐らない, 雑学, 豆知識, 科学, 食べ物の雑学, 乳児ボツリヌス症, ずんだもん, VOICEVOX
```

## 四角いうんちのウォンバット（`shorts_wombat/`）
**タイトル**
```
うんちが四角い動物がいる！？ #shorts #雑学
```
**説明欄**
```
ウォンバットのうんちはサイコロみたいな四角形！
お尻の穴が四角いわけではなく、腸の壁に「硬い所」と「柔らかい所」があり、
腸の終わりのほうで水分が抜けて固まるときに角ができると考えられています。
この研究は2019年のイグノーベル賞（物理学賞）を受賞しました。

出典:
Yang et al. (2021) "Intestines of non-uniform stiffness mold the corners of wombat feces", Soft Matter 17, 475-488
https://doi.org/10.1039/D0SM01230K
タスマニア大学「Scientists get to the bottom of wombat cubed poo mystery」
https://www.utas.edu.au/news/2021/1/28/1109-scientists-get-to-the-bottom-of-wombat-cubed-poo-mystery/
英国王立化学会（RSC）ニュース
https://www.rsc.org/news-events/articles/2021/jan/wombat-poo/
Georgia Tech「IgNobel for Cubed Poops」
https://www.hu.gatech.edu/Lee/?p=130

VOICEVOX:ずんだもん

#雑学 #豆知識 #ウォンバット #動物 #イグノーベル賞 #shorts
```
**タグ**
```
ウォンバット, 四角いうんち, 動物, 動物の雑学, イグノーベル賞, 雑学, 豆知識, オーストラリア, ずんだもん, VOICEVOX
```
**固定コメント**
```
ほかに「えっ」となる動物の体の秘密、知ってたらコメントで教えてください！
```

## 壁をすり抜ける電子（トンネル効果）（`shorts_quantum/`）
**タイトル**
```
スマホの写真は「壁をすり抜ける電子」が守ってる #shorts #雑学 #量子
```
**説明欄**
```
スマホの写真を保存しているフラッシュメモリは「量子トンネル効果」を使っています。
電子は波の性質をもつので、とても薄い壁（約10nmの絶縁膜）なら確率的にすり抜けられます。
すり抜けた電子を「浮遊ゲート」に閉じ込めることでデータを記録し、電源を切っても消えません。
2025年のノーベル物理学賞は、電気回路での巨視的な量子トンネル効果とエネルギー量子化の発見に贈られました。

出典:
NobelPrize.org「The Nobel Prize in Physics 2025」
https://www.nobelprize.org/prizes/physics/2025/summary/
The Quantum Insider（2025年ノーベル物理学賞の解説）
https://thequantuminsider.com/2025/10/07/clarke-devoret-and-martinis-win-2025-nobel-prize-in-physics-for-revealing-quantum-effects-in-macroscopic-circuits/
Halbleiter.org「Flash cell」（フラッシュメモリセルの構造）
https://www.halbleiter.org/en/digital-technology/flash-cell/
米国特許 US6933554（NANDのトンネル酸化膜 約100Å＝約10nm）
https://patents.google.com/patent/US6933554

VOICEVOX:ずんだもん

#雑学 #豆知識 #量子力学 #量子トンネル効果 #ノーベル賞 #スマホ #shorts
```
**タグ**
```
量子トンネル効果, トンネル効果, フラッシュメモリ, スマホ, 量子力学, ノーベル物理学賞 2025, 雑学, 豆知識, ずんだもん, VOICEVOX
```
**固定コメント**
```
量子力学で他に知りたいテーマ（量子コンピュータ・量子暗号など）があればコメントで！
```

## 盗み見で誤りが増える通信（量子暗号）（`shorts_qkd/`）
**タイトル**
```
盗み見すると誤りが増える「量子暗号」通信 #shorts #雑学 #量子
```
**説明欄**
```
量子暗号通信（量子鍵配送, QKD）は、光子1個ずつの偏光の向きで暗号の鍵を送ります。
量子の状態は「測ると変わる」「完全にはコピーできない（量子複製不可能定理）」ため、
途中で盗み見すると受信側の誤りが増えます。代表的なBB84方式では、
すべての光子を盗み見して送り直す攻撃をすると、誤り率が約25%になります。
送受信者が誤り率を確かめれば、盗聴に気づけるのです。
日本では2010年にNICTなどが東京で量子鍵配送ネットワーク（Tokyo QKD Network）の実証を行いました。

出典:
NICT プレスリリース（2010年10月14日, Tokyo QKD Network）
https://www1.nict.go.jp/en/press/2010/10/14-1.html
NICT Tokyo QKD Network 概要
https://www.nict.go.jp/en/quantum/topics/20101014-1.html
arXiv:1409.1452（BB84の安全性と誤り率25%の導出）
https://arxiv.org/abs/1409.1452
arXiv:quant-ph/0601207（量子暗号の解説）
https://arxiv.org/abs/quant-ph/0601207

VOICEVOX:ずんだもん

#雑学 #豆知識 #量子力学 #量子暗号 #セキュリティ #shorts
```
**タグ**
```
量子暗号, 量子鍵配送, QKD, BB84, 量子力学, セキュリティ, 暗号, 雑学, ずんだもん, VOICEVOX
```
**固定コメント**
```
「量子コンピュータで今の暗号は破られる？」も気になる人はコメントで！
```

## ベーブ・ルース（`shorts_ruth/`）
**タイトル**（候補。1つ選ぶ）
```
大谷翔平より100年前の「二刀流」ベーブ・ルースがエグすぎた #shorts
```
```
【MLB伝説】100年前の二刀流 ベーブ・ルースの成績 #shorts #大谷翔平
```
**説明欄**
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
**タグ**
```
ベーブ・ルース, ベーブルース, Babe Ruth, 大谷翔平, 二刀流, メジャーリーグ, MLB, 野球, ヤンキース, MLBレジェンド, ずんだもん
```
**固定コメント**
```
大谷とルース、二刀流としてすごいのはどっち？ コメントで教えてください！
次に紹介してほしい昔のMLB選手も募集中！
```

## ルー・ゲーリッグ（`shorts_gehrig/`）
**タイトル**（候補。1つ選ぶ）
```
衣笠祥雄が抜いた「鉄の馬」の記録、元の持ち主を知ってる？ #shorts
```
```
【MLB伝説】2130試合連続出場 ルー・ゲーリッグの成績 #shorts #衣笠祥雄
```
**説明欄**
```
【衣笠祥雄が抜いた記録】2130試合連続出場「鉄の馬」ルー・ゲーリッグの成績
約14年間1試合も休まず、通算2,721安打・1,995打点。衣笠が追いかけたメジャーリーグの鉄人を40秒でまとめました。

▼ルー・ゲーリッグ（ゲーリック）成績まとめ
・連続試合出場：2,130試合（1925〜1939年）→ 1987年 衣笠祥雄が2,131試合目で更新（最終2,215試合）
・通算打撃：打率.340 / 2,721安打 / 493本塁打 / 1,995打点 / OPS 1.080
・特徴的な記録：13年連続100打点（1926〜1938）/ 満塁本塁打23本（2013年まで最多）
・タイトル：MVP2回（1927, 1936）/ 三冠王（1934）/ ワールドシリーズ制覇6回
・最も輝いた年（1927年）：打率.373 / 47本塁打 / 175打点（当時の新記録）/ OPS 1.240 / MVP

💬 衣笠とゲーリッグ、連続出場の記録がすごいのはどっち？ コメントで教えてください！
▶ MLBレジェンド図鑑：ベーブ・ルース / ジョージ・シスラー / サイ・ヤング も公開中

※1927年の打点は資料により173〜175
出典：アメリカ野球殿堂 https://baseballhall.org/hall-of-famers/gehrig-lou
MLB.com https://www.mlb.com/player/114680
Baseball-Reference https://www.baseball-reference.com/players/g/gehrilo01.shtml
Britannica https://www.britannica.com/biography/Lou-Gehrig
nippon.com（衣笠祥雄の記録更新）https://www.nippon.com/ja/japan-topics/today0613/
写真：Wikimedia Commons（Public domain）Library of Congress, New York Daily News, El Gráfico ほか
音声：VOICEVOX:ずんだもん

#衣笠祥雄 #ルーゲーリッグ #メジャーリーグ #MLB #鉄人
```
**タグ**
```
ルー・ゲーリッグ, ルーゲーリッグ, Lou Gehrig, 衣笠祥雄, 連続試合出場, 鉄の馬, 鉄人, メジャーリーグ, MLB, 野球, ヤンキース, ずんだもん
```
**固定コメント**
```
衣笠とゲーリッグ、連続出場の記録がすごいのはどっち？ コメントで教えてください！
次に紹介してほしい昔のMLB選手も募集中！
```

## ジョージ・シスラー（`shorts_sisler/`）
**タイトル**（候補。1つ選ぶ）
```
イチローが抜いた「84年前の安打記録」元の持ち主を知ってる？ #shorts
```
```
【MLB伝説】257安打の男 ジョージ・シスラーの成績 #shorts #イチロー
```
**説明欄**
```
【イチローが抜いた84年前の記録】シーズン257安打 ジョージ・シスラーの成績
1920年に257安打、1922年には打率.420。イチローが2004年に262安打で超えるまで84年間残った記録の持ち主を40秒でまとめました。

▼ジョージ・シスラー 成績まとめ
・シーズン安打：257本（1920年）→ 2004年 イチローが262安打で更新
・通算打撃：打率.340 / 2,812安打 / 102本塁打 / 1,178打点 / 375盗塁
・タイトル：首位打者2回（1920, 1922）/ 盗塁王4回 / MVP（1922）
・最も輝いた年（1922年）：打率.420 / 51盗塁 / 41試合連続安打（1941年までア・リーグ記録）/ MVP

💬 イチローの262安打とシスラーの257安打、すごいのはどっち？ コメントで教えてください！
▶ MLBレジェンド図鑑：ベーブ・ルース / ルー・ゲーリッグ / サイ・ヤング も公開中

※通算打点は資料により1,175〜1,178、連続試合安打は41（42とする資料もあり）
出典：アメリカ野球殿堂 https://baseballhall.org/hall-of-famers/sisler-george
Baseball-Reference https://www.baseball-reference.com/players/s/sislege01.shtml
Britannica https://www.britannica.com/biography/George-Sisler
SABR https://sabr.org/journal/article/the-three-or-was-it-two-400-hitters-of-1922/
写真：Wikimedia Commons（Public domain / CC0）Library of Congress, Metropolitan Museum of Art ほか
音声：VOICEVOX:ずんだもん

#イチロー #ジョージシスラー #メジャーリーグ #MLB #安打記録
```
**タグ**
```
ジョージ・シスラー, ジョージシスラー, George Sisler, イチロー, シーズン最多安打, 257安打, メジャーリーグ, MLB, 野球, MLBレジェンド, ずんだもん
```
**固定コメント**
```
イチローの262安打とシスラーの257安打、すごいのはどっち？ コメントで教えてください！
次に紹介してほしい昔のMLB選手も募集中！
```

## サイ・ヤング（`shorts_young/`）
**タイトル**（候補。1つ選ぶ）
```
「サイ・ヤング賞」のサイ・ヤングって誰？ 通算511勝の怪物 #shorts
```
```
【MLB伝説】通算511勝 サイ・ヤングの成績 #shorts #サイヤング賞
```
**説明欄**
```
【サイ・ヤング賞の由来】通算511勝 サイ・ヤングの成績がすごすぎる
毎年発表される「サイ・ヤング賞」。その名前の由来は、メジャーリーグ歴代最多511勝の投手でした。40秒でまとめました。

▼サイ・ヤング 成績まとめ
・通算投手：511勝（MLB歴代最多）/ 防御率2.63 / 749完投 / 7,356投球回 / 2,803奪三振
・記録：投手三冠（1901）/ 完全試合（1904年、20世紀初）
・最も輝いた年（1901年）：33勝10敗 / 防御率1.62 / 158奪三振（すべてリーグ1位）
・サイ・ヤング賞：亡くなった翌年の1956年に創設

💬 511勝、今の投手でも破れると思う？ コメントで教えてください！
▶ MLBレジェンド図鑑：ベーブ・ルース / ルー・ゲーリッグ / ジョージ・シスラー も公開中

※敗戦数は資料により315〜316、投球回は7,354⅔〜7,356
出典：アメリカ野球殿堂 https://baseballhall.org/hall-of-famers/young-cy
Britannica https://www.britannica.com/biography/Cy-Young
StatMuse https://www.statmuse.com/mlb/player/cy-young-66196/career-stats
写真：Wikimedia Commons（Public domain）Bain News Service, Charles M. Conlon, Paul Thompson ほか
音声：VOICEVOX:ずんだもん

#サイヤング賞 #サイヤング #メジャーリーグ #MLB #野球
```
**タグ**
```
サイ・ヤング, サイヤング, Cy Young, サイ・ヤング賞, サイヤング賞, 511勝, メジャーリーグ, MLB, 野球, MLBレジェンド, ずんだもん
```
**固定コメント**
```
511勝、今の投手でも破れると思う？ コメントで教えてください！
次に紹介してほしい昔のMLB選手も募集中！
```

※ MLB のショートは、記録の数字を資料ごとの差の注記つきで載せています（ベーブ・ルースの OPS・長打率を「歴代1位」とは書いていません）。写真はパブリックドメインのものだけです。
