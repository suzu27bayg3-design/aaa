# 解説動画 第8回：量子インターネット（ずんだもん×四国めたん）

- 動画: `quantum_longform8.mp4`（1920×1080 横長 / 約5分40秒 / H.264 + AAC）
- ショート: `short.mp4`（1080×1920 縦長 / 約0分19秒）。投稿時に「関連動画」を本編に設定する
- 構成: 冒頭の予告（約10秒）→ 本編 → まとめ → 次回予告（最後の約20秒。終了画面で次回の動画を表示）
- サムネイル: `thumbnail.png`（1280×720）
- 生成: `bash ../tools/voicevox_engine.sh` → `python3 ../tools/longform.py script.py`
- チャプター: `chapters.txt`
- 新しい図: `repeater`（区間ごとのもつれ → 中継点でまとめて測る → 端と端がもつれる）

---

## 投稿用メタデータ

### タイトル（候補。おすすめ順）
```
量子インターネットで何ができる？コピーできない情報を遠くへ届けるしくみ【ずんだもん解説】
```
```
1000kmで300年に1個？光が届かない問題を「量子中継」で解決【ずんだもん解説】
```
```
会ったことのない2つがもつれる？「もつれ交換」と量子インターネット【ずんだもん】
```

### 説明欄
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

### 固定コメント
```
量子インターネットで一番やってみたいことは？ 次に解説してほしいテーマもコメントで！
```
