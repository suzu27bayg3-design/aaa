# YouTube Shorts：はちみつはなぜ腐らない？

- 動画: `honey_short.mp4`（1080×1920 縦型 / 30fps / 約36秒 / H.264 + AAC）
- 声: VOICEVOX:ずんだもん（〜のだ口調）。`bash ../tools/voicevox_engine.sh` → `python3 voicevox_synth.py && python3 make_short.py`
- 構成: 7シーン。浸透圧は図で説明し、最後の「数千年前のはちみつでも腐っていない」が冒頭につながるループ
- 生成スクリプト: `make_short.py`

## 投稿用メタデータ

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

**タグ**: 雑学, 豆知識, はちみつ, 蜂蜜, 腐らない, 浸透圧, 科学, shorts

## 再生成する方法

```bash
sudo apt-get install -y open-jtalk open-jtalk-mecab-naist-jdic ffmpeg fonts-ipafont-gothic fonts-noto-color-emoji
pip install pillow numpy
# Mei音声（CC BY 3.0）を MMDAgent_Example から取得し、mei_normal.htsvoice をこのフォルダへ
#   https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/
python3 make_short.py
```

台本は `make_short.py` の `SCENES` を書き換えれば別の雑学動画にも流用できます。

## サムネイル
動画の**最後の0.4秒**にサムネイル専用のコマ（`thumb.png` と同じ画像）が入っています。
YouTubeアプリで投稿するとき（または投稿後の「編集」で）サムネイルの鉛筆アイコンをタップし、
コマ選択バーを**右端まで**動かすとこのコマを選べます。
動画を作り直した場合は `python3 ../tools/add_thumb_frame.py <動画> --text ... --emoji ...` で再度追加してください（2回実行すると2回分足されます）。
