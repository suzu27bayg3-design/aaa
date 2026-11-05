# 毎日の雑学ショート

1日1本、`YYYY-MM-DD_テーマ/topic.py` に台本・図・投稿用メタデータを書き、次のコマンドで作ります。

```
bash tools/voicevox_engine.sh
python3 tools/trivia_short.py trivia_daily/2026-11-05_octopus/topic.py
```

できるもの（同じフォルダ）: `short.mp4`（1080×1920）/ `cover.png` / `metadata.md`（タイトル・説明欄・タグ・ハッシュタグ・固定コメント）

| 日付 | テーマ | フォルダ |
|---|---|---|
| 2026-11-05 | タコの心臓は3つ・血は青い | `2026-11-05_octopus/` |
