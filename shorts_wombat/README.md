# YouTube Shorts：うんちが四角い動物！？（ウォンバット）

- 動画: `wombat_short.mp4`（1080×1920 縦型 / 30fps / 約31秒 / H.264 + AAC）
- 生成スクリプト: `make_short.py`（音声モデルは `../shorts_honey/` の `mei_normal.htsvoice` と `mei_happy.htsvoice` を使用。どちらも MMDAgent_Example の Voice/mei/ に入っています）
- 声: 冒頭・驚き・オチは明るい声（Mei happy）、説明は通常の声（Mei normal）に切り替え。話速1.2倍、抑揚強め、明瞭度EQ＋コンプ、BGMダッキング、-14 LUFSに正規化
- 構成: 冒頭1秒で「四角いうんち！？」→ 理由を段階的に明かす → 最後の「だから、うんちは四角いんです」が冒頭につながるループ構成

## 投稿用メタデータ

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

音声: Open JTalk / HTS voice "Mei" (MMDAgent, © Nagoya Institute of Technology, CC BY 3.0)

#雑学 #豆知識 #ウォンバット #動物 #イグノーベル賞 #shorts
```

**タグ**: 雑学, 豆知識, ウォンバット, 動物, うんち, イグノーベル賞, 科学, shorts

**固定コメント案**（コメントが増えるように）
```
ほかに「えっ」となる動物の体の秘密、知ってたらコメントで教えてください！
```

## VOICEVOXの声で作り直す手順
1. VOICEVOXを起動し、メニュー「ファイル → テキスト読み込み」で `voicevox_script.txt` を開く（1行＝1シーンで7行入ります）
2. キャラクターを選び、右側のパラメータを調整（目安: 話速 1.15〜1.25 / 抑揚 1.2〜1.4 / 間の長さ 0.8）
   - 1・3・6・7行目（冒頭・驚き・受賞・オチ）は明るめのスタイル、2・4・5行目（説明）は通常スタイルにするとメリハリが出ます
   - 読み間違いがあれば、アクセント・読みを各行で修正
3. 「ファイル → 音声書き出し → 全部書き出し」で `001_…wav`〜`007_…wav` を書き出す
4. 7ファイルを `shorts_wombat/voicevox/` に入れて push（GitHubのWeb画面の「Add file → Upload files」でも可）
5. `python3 make_short.py --credit "VOICEVOX:キャラ名"` で再生成（画面下にクレジットが入ります）

VOICEVOXは各キャラクターの利用規約に従い、説明欄にも「VOICEVOX:キャラ名」を必ず記載してください。
