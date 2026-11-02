# 解説動画 第4回：量子通信と量子暗号（ずんだもん×四国めたん）

- 動画: `quantum_longform4.mp4`（1920×1080 横長 / 約5分50秒 / H.264 + AAC）
- サムネイル: `thumbnail.png`（1280×720）
- 生成: `bash ../tools/voicevox_engine.sh` → `python3 ../tools/longform.py script.py`
- チャプター: `chapters.txt`
- 新しい図: `bb84`（送り手のビット・測り方 → 光子の向き → 受け手の測り方・結果 → 鍵に使うか）

---

## 投稿用メタデータ

### タイトル（候補。おすすめ順）
```
盗み見すると必ずバレる？量子暗号のしくみと「意外な弱点」【ずんだもん解説】
```
```
量子暗号は最強の暗号？光子1個で鍵を送るしくみと限界を解説【ずんだもん解説】
```
```
「今盗んで、あとで解読」量子コンピュータ時代の暗号の守り方【ずんだもん】
```

### 説明欄
```
「盗み見すると必ずバレる通信」――量子暗号は本当に最強なのでしょうか？
光子1個ずつの向きで暗号の鍵を送る量子鍵配送（BB84）のしくみから、宇宙からの量子通信、そしてあまり知られていない弱点まで、ずんだもんと四国めたんが約6分で解説します。

・暗号の弱点は「鍵をどう届けるか」
・「今盗んで、あとで解読」という量子コンピュータ時代の脅威
・BB84：測り方が一致した光子だけで鍵を作るしくみ
・盗み見すると誤り率が約25%に上がる理由（測ると変わる・コピーできない）
・衛星「墨子」による約1200kmの量子鍵配送
・量子暗号の弱点と、耐量子暗号との使い分け

▼チャプター
0:00 オープニング
0:17 暗号の基本は「鍵」
1:03 「今盗んで、あとで解読」の脅威
1:34 量子鍵配送のしくみ（BB84）
2:27 なぜ盗み見がバレるのか
3:11 距離の壁と、宇宙からの量子通信
4:02 量子暗号の弱点
4:40 2つの守り方を比べよう
5:18 まとめ

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
NSA（量子鍵配送についての見解）https://www.nsa.gov/Cybersecurity/Quantum-Key-Distribution-QKD-and-Quantum-Cryptography-QC/
NSAの見解への反論 arXiv:2307.15116 https://arxiv.org/abs/2307.15116
Cloud Security Alliance（NIST FIPS 203/204/205）https://cloudsecurityalliance.org/articles/nist-fips-203-204-and-205-finalized-an-important-step-towards-a-quantum-safe-future

音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん
立ち絵: 坂本アヒル（ずんだもん立ち絵素材 / 四国めたん立ち絵素材）

#量子暗号 #ずんだもん #科学解説
```

### 固定コメント
```
あなたなら耐量子暗号と量子暗号、どちらを使う？ 次に解説してほしいテーマもコメントで！
```

### 投稿時の設定
- **終了画面**: 第3回の動画、または再生リスト
- **再生リスト**: 「ずんだもんの量子技術解説」に追加
- 第2回の短編「盗み見がバレる通信！？」（`../shorts_qkd/`）と相互に紹介すると、ショートから長尺へ誘導しやすい
