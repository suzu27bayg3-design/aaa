#!/usr/bin/env python3
"""全動画の投稿用メタデータ（タイトル・説明欄・タグ・ハッシュタグ・固定コメント）を1つの Markdown にまとめる。

使い方: python3 tools/build_upload_metadata.py   # → docs/upload_metadata.md

説明欄とタイトル候補は各フォルダの README.md から取り出す（README を直せば、ここも直る）。
シリーズのショートの説明欄と、YouTube の「タグ」欄の中身は、このファイルに書く。
"""
import importlib.util
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP_DIRS = ["longform_quantum"] + [f"longform_quantum{i}" for i in range(2, 11)]

COMMON_Q = ["量子コンピュータ", "量子コンピューター", "量子力学", "ずんだもん", "四国めたん", "ずんだもん解説",
            "VOICEVOX", "科学解説", "わかりやすい"]

# 本編ごとのタグ（タグ欄は表記ゆれ・言い換えの補助。先頭ほど重要）
EP_TAGS = {
    1: ["量子誤り訂正", "Willow", "Google", "ウィロー", "エラー訂正", "論理量子ビット", "ノーベル物理学賞 2025", "量子ビット", "実用化"],
    2: ["ショアのアルゴリズム", "グローバーのアルゴリズム", "素因数分解", "干渉", "量子優位性", "量子超越性", "分子シミュレーション", "RSA暗号"],
    3: ["超伝導量子ビット", "イオントラップ", "中性原子", "光量子コンピュータ", "光ピンセット", "シリコン量子ビット", "トポロジカル量子ビット", "Majorana 1"],
    4: ["量子暗号", "量子鍵配送", "QKD", "BB84", "耐量子暗号", "PQC", "Harvest now decrypt later", "墨子", "量子通信", "暗号"],
    5: ["量子センサ", "量子センサー", "光格子時計", "原子時計", "一般相対性理論", "東京スカイツリー", "NVセンター", "ダイヤモンドNVセンタ", "香取秀俊"],
    6: ["量子もつれ", "量子エンタングルメント", "量子テレポーテーション", "ベルの不等式", "EPRパラドックス", "アインシュタイン", "ノーベル物理学賞 2022"],
    7: ["量子アニーリング", "D-Wave", "ディーウェーブ", "組合せ最適化", "巡回セールスマン問題", "西森秀稔", "門脇正史", "イジングマシン"],
    8: ["量子インターネット", "量子中継", "もつれ交換", "エンタングルメントスワッピング", "量子メモリ", "量子ネットワーク", "QuTech"],
    9: ["量子機械学習", "量子AI", "AI", "人工知能", "脱量子化", "HHLアルゴリズム", "ユーイン・タン", "データ読み込み"],
    10: ["量子技術", "2030年", "ロードマップ", "誤り耐性量子コンピュータ", "耐量子暗号", "NIST", "量子技術の未来", "まとめ"],
}

# シリーズのショート（タイトル・説明欄の本文）。数字は本編と同じ出典に基づく
SERIES_SHORTS = {
    1: ("量子ビットを増やすとエラーが減った！？ #shorts #量子コンピュータ",
        "量子ビットを増やすほどエラーが増える――それが量子コンピュータの長年の悩みでした。\n"
        "2024年、グーグルの「Willow」は符号距離を3→5→7と大きくするたびに、論理エラー率がおよそ半分になることを示しました。\n"
        "【原理】1個の情報を多数の量子ビットに分けて持たせ、どこが壊れたかだけを測って直す「量子誤り訂正」。\n"
        "物理エラーが一定の値（しきい値）より小さいと、量子ビットを増やすほど全体のエラーが減ります。"),
    2: ("15＝3×5を量子コンピュータはどう解く？ #shorts #量子コンピュータ",
        "7を何回もかけて15で割った余りは 1, 7, 4, 13, 1…と4つごとにくり返します。\n"
        "この「周期」がわかると、15を3と5に分けられます。\n"
        "【原理】ショアのアルゴリズムは、素因数分解を「周期を見つける問題」に置きかえ、\n"
        "量子の干渉（正しい周期の答えが強め合い、ほかが打ち消し合う）で周期を効率よく見つけます。"),
    3: ("光のピンセットで原子を6100個並べる！？ #shorts #量子コンピュータ",
        "レーザー光を細く絞ると、焦点に原子が引き寄せられます（光ピンセット）。\n"
        "2025年、カルテックのチームは6100個の原子を並べ、重ね合わせを約13秒保ったと発表しました。\n"
        "【原理】光の強い場所ほど原子のエネルギーが下がるため、原子は焦点に集まります。\n"
        "1個1個の原子が量子ビットになり、並べ方も光で自由に変えられます。"),
    4: ("盗み見すると誤りが増える「量子暗号」通信 #shorts #量子",
        "光の粒（光子）を1個ずつ、向きを変えて送る量子暗号（量子鍵配送, BB84）。\n"
        "盗聴者は測り方を当てずっぽうで選ぶので、半分は間違えて光子の状態を変えてしまいます。\n"
        "【原理】量子の状態は「測ると変わる」「完全にはコピーできない（量子複製不可能定理）」。\n"
        "すべてを盗み見すると受け手の誤り率は約25%になり、誤りの割合を調べれば盗聴に気づけます。"),
    5: ("スカイツリーの上は時間が速い？ #shorts #量子センサ",
        "重力が弱い高い場所ほど、時間は速く進みます（アインシュタインの一般相対性理論）。\n"
        "2020年、地上と高さ約450mの展望台で光格子時計を比べると、展望台の時計は1日に約4ナノ秒速く進んでいました。\n"
        "【原理】原子が吸収する光の振動数は自然が決めた「目盛り」。光の格子に閉じ込めた多数の原子で\n"
        "それを数えると、300億年に1秒もずれないほど正確な時計になり、高さのちがいまで測れます。"),
    6: ("離れていても結果がそろう「量子もつれ」 #shorts #量子",
        "もつれた2つの量子ビットは、片方を測って0が出ると、もう片方も必ず0になります。\n"
        "でも、これを使っても光より速く情報は送れません。\n"
        "【原理】片方だけを見ると結果は毎回ランダム。そろっていることは、\n"
        "ふつうの通信で結果を見せ合って初めてわかるため、情報は光の速さを超えません。"),
    7: ("小さな谷をすり抜ける？「量子アニーリング」 #shorts #量子",
        "答えのよさを「高さ」に置きかえると、一番低い谷が一番よい答えになります。\n"
        "ふつうのボールは途中の小さな谷にはまってしまいますが……\n"
        "【原理】量子のゆらぎ（トンネル効果）を使うと、山を越えずにすり抜けられることがあります。\n"
        "1998年に門脇正史さん・西森秀稔さんが定式化したアイデアで、本当に速いかは問題によります。"),
    8: ("会ったことのない2つがつながる「もつれ交換」 #shorts #量子",
        "長い道を短い区間に分け、区間ごとにもつれたペアを作ります。\n"
        "真ん中の中継点が2つの粒をまとめて測ると、一度も出会っていない両端が直接もつれます。\n"
        "【原理】光ファイバーでは光子が距離とともに失われ、量子の情報はコピーして増幅できません。\n"
        "そこで「もつれ交換」で区間をつなぐのが量子中継、量子インターネットの土台です。"),
    9: ("量子でAIは爆速になる？ #shorts #量子コンピュータ #AI",
        "「量子×AIで最強」と思いきや……\n"
        "100万個の数字を量子の状態に入れるだけで、100万回分くらいの手間がかかることがあります。\n"
        "【原理】計算の真ん中が速くても、データの「入力」と、答えを何度も測って取り出す「出力」が遅いと、\n"
        "全体は速くなりません。量子AIのニュースは、入口と出口まで見るのがポイントです。"),
    10: ("量子技術は2030年どうなる？ #shorts #量子コンピュータ",
         "量子技術は「計算・通信・センサ」の3本柱。\n"
         "どれも「重ね合わせと干渉」「もつれ」「測ると変わる」の3つの原理でできています。\n"
         "2030年前後は、古い暗号（RSA・楕円曲線暗号）の入れかえと、\n"
         "エラーに強い量子コンピュータが大きな節目になりそうです。"),
}
SHORT_EXTRA_TAGS = {1: ["量子誤り訂正", "Willow"], 2: ["ショアのアルゴリズム", "素因数分解"], 3: ["中性原子", "光ピンセット"],
                    4: ["量子暗号", "量子鍵配送", "BB84"], 5: ["光格子時計", "東京スカイツリー", "相対性理論"],
                    6: ["量子もつれ", "量子テレポーテーション"], 7: ["量子アニーリング", "D-Wave"],
                    8: ["量子インターネット", "もつれ交換"], 9: ["量子AI", "量子機械学習"], 10: ["量子技術", "2030年"]}
SHORT_HASH = {1: "#量子コンピュータ #ずんだもん #shorts", 2: "#量子コンピュータ #ずんだもん #shorts",
              3: "#量子コンピュータ #ずんだもん #shorts", 4: "#量子暗号 #ずんだもん #shorts",
              5: "#量子センサ #相対性理論 #ずんだもん #shorts", 6: "#量子もつれ #ずんだもん #shorts",
              7: "#量子アニーリング #ずんだもん #shorts", 8: "#量子インターネット #ずんだもん #shorts",
              9: "#量子コンピュータ #AI #ずんだもん #shorts", 10: "#量子技術 #ずんだもん #shorts"}

# 以前作ったショート（説明欄は各 README から取る）
OLD_SHORTS = [
    ("shorts_honey", "はちみつはなぜ腐らない？", ["はちみつ", "蜂蜜", "腐らない", "雑学", "豆知識", "科学", "食べ物の雑学", "乳児ボツリヌス症", "ずんだもん", "VOICEVOX"]),
    ("shorts_wombat", "四角いうんちのウォンバット", ["ウォンバット", "四角いうんち", "動物", "動物の雑学", "イグノーベル賞", "雑学", "豆知識", "オーストラリア", "ずんだもん", "VOICEVOX"]),
    ("shorts_quantum", "壁をすり抜ける電子（トンネル効果）", ["量子トンネル効果", "トンネル効果", "フラッシュメモリ", "スマホ", "量子力学", "ノーベル物理学賞 2025", "雑学", "豆知識", "ずんだもん", "VOICEVOX"]),
    ("shorts_qkd", "盗み見で誤りが増える通信（量子暗号）", ["量子暗号", "量子鍵配送", "QKD", "BB84", "量子力学", "セキュリティ", "暗号", "雑学", "ずんだもん", "VOICEVOX"]),
    ("shorts_ruth", "ベーブ・ルース", ["ベーブ・ルース", "ベーブルース", "Babe Ruth", "大谷翔平", "二刀流", "メジャーリーグ", "MLB", "野球", "ヤンキース", "MLBレジェンド", "ずんだもん"]),
    ("shorts_gehrig", "ルー・ゲーリッグ", ["ルー・ゲーリッグ", "ルーゲーリッグ", "Lou Gehrig", "衣笠祥雄", "連続試合出場", "鉄の馬", "鉄人", "メジャーリーグ", "MLB", "野球", "ヤンキース", "ずんだもん"]),
    ("shorts_sisler", "ジョージ・シスラー", ["ジョージ・シスラー", "ジョージシスラー", "George Sisler", "イチロー", "シーズン最多安打", "257安打", "メジャーリーグ", "MLB", "野球", "MLBレジェンド", "ずんだもん"]),
    ("shorts_young", "サイ・ヤング", ["サイ・ヤング", "サイヤング", "Cy Young", "サイ・ヤング賞", "サイヤング賞", "511勝", "メジャーリーグ", "MLB", "野球", "MLBレジェンド", "ずんだもん"]),
]

COMP_TAGS = ["総集編", "作業用", "一気見", "量子技術", "量子暗号", "量子センサ", "量子もつれ", "量子アニーリング",
             "量子インターネット", "量子AI", "勉強", "聞き流し"]


def load(path):
    spec = importlib.util.spec_from_file_location("cfg", path)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    return cfg


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def blocks_after(md, heading_re):
    """見出し（正規表現）の後ろから、次の ### / ** 見出しまでにある ``` ブロックを全部返す"""
    m = re.search(heading_re, md)
    if not m:
        return []
    rest = md[m.end():]
    stop = re.search(r"\n(###|\*\*)", rest)
    if stop:
        rest = rest[:stop.start()]
    return [b.strip("\n") for b in re.findall(r"```\n(.*?)```", rest, re.S)]


def tag_line(tags):
    seen, out = set(), []
    for t in tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
    s = ", ".join(out)
    assert len(s) <= 500, (len(s), s)
    return s


def code(s):
    return "```\n" + s.rstrip("\n") + "\n```\n"


def sources_of(md, n=3):
    m = re.search(r"出典:?\n(.*?)\n\n", md, re.S)
    return "\n".join(m.group(1).splitlines()[:n]) if m else ""


def main():
    out = ["# 投稿用メタデータ一覧（タイトル・説明欄・タグ・ハッシュタグ）\n",
           "`python3 tools/build_upload_metadata.py` で各 README から作り直せます。"
           "「タイトル」「説明欄」「タグ」「固定コメント」はそれぞれコピーしてそのまま貼れます。\n",
           "## 基本の考え方（なぜこう書くか）\n",
           "- **タイトルと説明欄の最初の2〜3行がいちばん大事**：YouTube は、タイトル・サムネイル・説明欄などのメタデータから"
           "動画の内容を判断して検索や関連動画に出します。検索されやすい言葉（量子コンピュータ、大谷翔平 など）を前のほうに置き、"
           "後半で「？」を使って続きが気になる形にしています。"
           "（[YouTube ヘルプ：動画のメタデータに関するポリシー](https://support.google.com/youtube/answer/2801973?hl=ja)、"
           "[YouTube ヘルプ：パフォーマンスに関するよくある質問](https://support.google.com/youtube/answer/141805?hl=ja)）\n",
           "- **タグの役割は小さい**：YouTube 自身が「タグは動画の発見にはあまり役立たず、つづりを間違えやすい言葉のとき"
           "に役立つ」と説明しています。そのため、タグ欄には表記ゆれ（量子コンピュータ／量子コンピューター、ベーブ・ルース／"
           "ベーブルース／Babe Ruth）と言い換えだけを入れ、合計500文字以内にしています。"
           "（[YouTube ヘルプ：タグを追加する](https://support.google.com/youtube/answer/146402?hl=ja)）\n",
           "- **ハッシュタグは3〜5個**：説明欄のハッシュタグは、最初の3つがタイトルの上に表示されます。60個を超えると全部無視され、"
           "関係のないタグはポリシー違反になるので、内容に合うものだけにしています。"
           "（[YouTube ヘルプ：ハッシュタグを使う](https://support.google.com/youtube/answer/6390658?hl=ja)）\n",
           "- **ショートは本編へつなぐ**：ショートの編集画面で「関連動画」に本編を設定すると、ショートの画面に本編へのリンクが出ます。"
           "（[YouTube ヘルプ：ショートに関連動画を追加する](https://support.google.com/youtube/answer/14075157?hl=ja)）\n",
           "- **チャプター**：説明欄に 0:00 から始まる時刻を3つ以上（各10秒以上）書くと、自動でチャプターになります。"
           "本編の説明欄にはすでに入っています。"
           "（[YouTube ヘルプ：動画のチャプター](https://support.google.com/youtube/answer/9884579?hl=ja)）\n",
           "- 説明欄の「（URLを貼る）」は、公開後の動画・再生リストのURLに置きかえてください。\n",
           "\n## 目次\n",
           "1. シリーズ本編（第1回〜第10回）\n2. シリーズのショート（10本）\n3. 総集編\n4. 以前作ったショート（雑学・量子・MLB 8本）\n"]

    # --- 1. 本編 ---
    out.append("\n---\n\n# 1. シリーズ本編「ずんだもんの量子技術解説」\n")
    cfgs = {}
    for i, d in enumerate(EP_DIRS, 1):
        cfg = load(os.path.join(ROOT, d, "script.py"))
        cfgs[i] = cfg
        md = read(f"{d}/README.md")
        titles = blocks_after(md, r"### タイトル[^\n]*\n")
        desc = blocks_after(md, r"### 説明欄[^\n]*\n")
        pin = blocks_after(md, r"### 固定コメント[^\n]*\n")
        dur = re.search(r"約(\d+分\d+秒)", md)
        out.append(f"\n## 第{i}回 {cfg.TITLE}（{dur.group(1) if dur else ''}・`{d}/`）\n")
        out.append("**タイトル（おすすめ）**\n")
        out.append(code(titles[0]))
        if len(titles) > 1:
            out.append("<details><summary>ほかの候補（A/Bテスト用）</summary>\n\n")
            for t in titles[1:]:
                out.append(code(t))
            out.append("</details>\n\n")
        out.append("**説明欄**\n")
        out.append(code(desc[0]))
        out.append("**タグ**（タグ欄に貼る）\n")
        out.append(code(tag_line(EP_TAGS[i] + COMMON_Q + [f"量子技術解説 第{i}回"])))
        if pin:
            out.append("**固定コメント**\n")
            out.append(code(pin[0]))
        nxt = f"第{i + 1}回" if i < 10 else "総集編または第1回"
        out.append(f"**設定**：再生リスト「ずんだもんの量子技術解説」に追加 / 終了画面に{nxt}を表示 / "
                   "カテゴリ「教育」または「科学と技術」/ 言語「日本語」/ 字幕は自動生成でOK\n")

    # --- 2. シリーズのショート ---
    out.append("\n---\n\n# 2. シリーズのショート（`longform_quantum*/short.mp4`）\n")
    out.append("共通の設定：**関連動画**に同じ回の本編を設定 / 再生リスト「ずんだもんの量子技術解説」にも入れる\n")
    for i, d in enumerate(EP_DIRS, 1):
        cfg = cfgs[i]
        md = read(f"{d}/README.md")
        title, body = SERIES_SHORTS[i]
        dur = re.search(r"short\.mp4`（[^）]*約(\d+分\d+秒)", md)
        desc = (body + f"\n\n▶ 本編：第{i}回「{cfg.TITLE}」（URLを貼る）\n"
                "▶ 再生リスト：ずんだもんの量子技術解説（URLを貼る）\n\n"
                "出典:\n" + sources_of(md) + "\n\n"
                "音声: VOICEVOX:ずんだもん / VOICEVOX:四国めたん\n立ち絵: 坂本アヒル\n\n" + SHORT_HASH[i])
        out.append(f"\n## ショート{i}（第{i}回から・{dur.group(1) if dur else ''}）\n")
        out.append("**タイトル**\n")
        out.append(code(title))
        out.append("**説明欄**\n")
        out.append(code(desc))
        out.append("**タグ**\n")
        out.append(code(tag_line(SHORT_EXTRA_TAGS[i] + ["量子コンピュータ", "量子力学", "ずんだもん", "四国めたん",
                                                         "VOICEVOX", "科学", "雑学", "shorts"])))

    # --- 3. 総集編 ---
    md = read("longform_quantum_all/README.md")
    titles = blocks_after(md, r"### タイトル[^\n]*\n")
    desc = blocks_after(md, r"### 説明欄[^\n]*\n")
    out.append("\n---\n\n# 3. 総集編（`longform_quantum_all/`・約59分）\n")
    out.append("**タイトル（おすすめ）**\n")
    out.append(code(titles[0] if titles else ""))
    for t in titles[1:]:
        out.append("**ほかの候補**\n")
        out.append(code(t))
    out.append("**説明欄**\n")
    out.append(code(desc[0] if desc else ""))
    out.append("**タグ**\n")
    out.append(code(tag_line(COMP_TAGS + COMMON_Q)))
    out.append("**設定**：第10回の公開後に出す / 各回の説明欄からも総集編へリンク\n")

    # --- 4. 以前のショート ---
    out.append("\n---\n\n# 4. 以前作ったショート\n")
    for d, name, tags in OLD_SHORTS:
        md = read(f"{d}/README.md")
        titles = blocks_after(md, r"(### タイトル[^\n]*|\*\*タイトル\*\*)\n")
        desc = blocks_after(md, r"(### 説明欄[^\n]*|\*\*説明欄\*\*)\n")
        pin = blocks_after(md, r"(### 固定コメント[^\n]*|\*\*固定コメント[^\n]*)\n")
        out.append(f"\n## {name}（`{d}/`）\n")
        out.append("**タイトル**" + ("（候補。1つ選ぶ）" if len(titles) > 1 else "") + "\n")
        for t in titles:
            out.append(code(t))
        out.append("**説明欄**\n")
        out.append(code(desc[0] if desc else ""))
        out.append("**タグ**\n")
        out.append(code(tag_line(tags)))
        if pin:
            out.append("**固定コメント**\n")
            out.append(code(pin[0]))
    out.append("\n※ MLB のショートは、記録の数字を資料ごとの差の注記つきで載せています（ベーブ・ルースの OPS・長打率を"
               "「歴代1位」とは書いていません）。写真はパブリックドメインのものだけです。\n")

    dst = os.path.join(ROOT, "docs", "upload_metadata.md")
    with open(dst, "w", encoding="utf-8") as f:
        f.write("".join(o if o.endswith("\n") else o + "\n" for o in out))
    print("wrote", dst)


if __name__ == "__main__":
    main()
