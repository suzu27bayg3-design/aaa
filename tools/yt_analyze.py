"""YouTube Studio の書き出しデータ（CSV）を読み込み、動画ごとの成績を分析してレポートを作る。

使い方:
  python3 tools/yt_analyze.py <書き出したZIP または CSV または フォルダ> [-o analysis/report]

入力: YouTube Studio → アナリティクス → 詳細モード → 右上の「エクスポート」→「カンマ区切り値 (.csv)」
      で保存されるZIP（中に「表データ.csv / Table data.csv」などが入っている）。
      日本語・英語どちらの画面で書き出した列名にも対応する。

出力: <出力先>.html（表とグラフ）と <出力先>.md（要点）

考え方（基本の原理）:
  動画が見られる流れは「漏斗（ろうと）」になっている。
    インプレッション（サムネイルが表示された回数）
      × クリック率（表示されたうち、クリックされた割合）
      = インプレッションからの視聴回数
      → どれだけ見続けたか（平均再生率）→ 登録・高評価
  どの段階で落ちているかを見れば、直すべき場所（サムネイル・タイトルか、冒頭か、中身か）が分かる。
  また、クリック率などの「割合」は、母数（インプレッション数）が少ないと偶然で大きくぶれる。
  そこで 95% 信頼区間（Wilson の方法）を付け、ぶれの範囲を超えた差だけを「差がある」と判断する。
"""
import argparse
import csv
import html
import io
import math
import os
import re
import statistics
import sys
import zipfile

# ---- 列名の対応表（日本語・英語の画面のどちらで書き出しても読めるように） -----------------
COLS = {
    "id": ["コンテンツ", "Content", "動画", "Video"],
    "title": ["動画のタイトル", "Video title"],
    "published": ["動画公開時刻", "Video publish time", "公開日時"],
    "duration": ["長さ", "Duration"],
    "views": ["視聴回数", "Views"],
    "watch_hours": ["総再生時間（単位: 時間）", "総再生時間 (単位: 時間)", "Watch time (hours)", "総再生時間"],
    "avd": ["平均視聴時間", "Average view duration"],
    "avp": ["平均再生率 (%)", "平均再生率（%）", "Average percentage viewed (%)", "平均再生率"],
    "impressions": ["インプレッション数", "Impressions"],
    "ctr": ["インプレッションのクリック率 (%)", "インプレッションのクリック率（%）", "Impressions click-through rate (%)",
            "インプレッションのクリック率"],
    "subs": ["チャンネル登録者", "Subscribers", "登録者の増加数", "Subscribers gained"],
    "likes": ["高評価", "Likes"],
    "comments": ["コメントの追加回数", "Comments added", "コメント"],
    "shares": ["共有", "Shares"],
}


def norm(s):
    return re.sub(r"[\s　（）()]", "", s or "").lower()


def find_col(header, key):
    cands = [norm(c) for c in COLS[key]]
    for i, h in enumerate(header):
        if norm(h) in cands:
            return i
    for i, h in enumerate(header):  # 部分一致（例: 「平均再生率」）
        if any(c and c in norm(h) for c in cands):
            return i
    return None


def num(s):
    s = (s or "").strip().replace(",", "").replace("%", "")
    if not s or s in ("-", "—"):
        return None
    if ":" in s:  # 0:01:23 / 1:23 のような時間表記 → 秒
        sec = 0
        for p in s.split(":"):
            sec = sec * 60 + float(p)
        return sec
    try:
        return float(s)
    except ValueError:
        return None


def read_table(path):
    """ZIP・フォルダ・CSV のどれでも「表データ」を読み込んで行のリストを返す"""
    def pick(names):
        for n in names:
            b = os.path.basename(n)
            if re.search(r"(表データ|Table data)", b, re.I) and b.lower().endswith(".csv"):
                return n
        csvs = [n for n in names if n.lower().endswith(".csv")]
        return csvs[0] if csvs else None
    if zipfile.is_zipfile(path):
        z = zipfile.ZipFile(path)
        name = pick(z.namelist())
        raw = z.read(name)
    elif os.path.isdir(path):
        name = pick([os.path.join(path, f) for f in os.listdir(path)])
        raw = open(name, "rb").read()
    else:
        name, raw = path, open(path, "rb").read()
    if name is None:
        sys.exit("CSV が見つかりませんでした")
    for enc in ("utf-8-sig", "utf-16", "cp932"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    rows = list(csv.reader(io.StringIO(text)))
    return name, rows[0], rows[1:]


def wilson(k, n, z=1.96):
    """割合 k/n の 95% 信頼区間（Wilson の方法）。n が小さいほど区間が広くなる"""
    if not n:
        return None, None
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def load(path):
    name, header, body = read_table(path)
    idx = {k: find_col(header, k) for k in COLS}
    videos, total = [], None
    for r in body:
        if not any(r):
            continue
        g = lambda k: r[idx[k]] if idx[k] is not None and idx[k] < len(r) else ""
        v = {"id": g("id"), "title": g("title") or g("id"), "published": g("published")}
        for k in ("duration", "views", "watch_hours", "avd", "avp", "impressions", "ctr", "subs", "likes",
                  "comments", "shares"):
            v[k] = num(g(k))
        if re.match(r"^(合計|Total)$", (v["id"] or "").strip(), re.I):
            total = v
            continue
        videos.append(v)
    return name, header, idx, videos, total


def kind(v):
    d = v.get("duration")
    if d is None:
        return "不明"
    return "ショート" if d <= 180 else "通常"


def analyze(videos):
    """動画ごとの指標と、気づいたことを返す"""
    for v in videos:
        v["kind"] = kind(v)
        if v["impressions"] and v["ctr"] is not None:
            clicks = v["impressions"] * v["ctr"] / 100
            lo, hi = wilson(clicks, v["impressions"])
            v["ctr_lo"], v["ctr_hi"] = lo * 100, hi * 100
        else:
            v["ctr_lo"] = v["ctr_hi"] = None
        if v["avp"] is None and v["avd"] and v["duration"]:
            v["avp"] = 100 * v["avd"] / v["duration"]
        views = v["views"] or 0
        v["subs_per_1k"] = 1000 * v["subs"] / views if views and v["subs"] is not None else None
        v["likes_per_1k"] = 1000 * v["likes"] / views if views and v["likes"] is not None else None
    notes = []
    for kd in ("ショート", "通常"):
        g = [v for v in videos if v["kind"] == kd]
        if len(g) < 2:
            continue
        ctrs = [v["ctr"] for v in g if v["ctr"] is not None]
        avps = [v["avp"] for v in g if v["avp"] is not None]
        med_ctr = statistics.median(ctrs) if ctrs else None
        med_avp = statistics.median(avps) if avps else None
        for v in g:
            t = v["title"][:40]
            # ショートはフィードで自動再生されることが多く、クリック率はあまり当てにならないので通常動画だけで判断する
            if kd == "通常" and med_ctr is not None and v["ctr_hi"] is not None and v["ctr_hi"] < med_ctr:
                notes.append(("サムネイル・タイトル", t,
                              f"クリック率 {v['ctr']:.1f}%（95%区間 {v['ctr_lo']:.1f}〜{v['ctr_hi']:.1f}%）が、"
                              f"同じ種類の動画の中央値 {med_ctr:.1f}% を偶然では説明できないほど下回っている"))
            if kd == "通常" and med_ctr is not None and v["ctr_lo"] is not None and v["ctr_lo"] > med_ctr:
                notes.append(("うまくいった例", t,
                              f"クリック率 {v['ctr']:.1f}% が中央値 {med_ctr:.1f}% をはっきり上回る。"
                              "サムネイルとタイトルの型をほかの動画にも使う"))
            if med_avp is not None and v["avp"] is not None and v["avp"] < 0.8 * med_avp:
                notes.append(("冒頭・構成", t,
                              f"平均再生率 {v['avp']:.0f}% が中央値 {med_avp:.0f}% の8割未満。"
                              "最初の数秒で離れていないか、視聴者維持率のグラフで確認する"))
            if v["subs_per_1k"] is not None and (v["views"] or 0) >= 300 and v["subs_per_1k"] < 1:
                notes.append(("登録への導線", t,
                              f"1000回再生あたりの登録 {v['subs_per_1k']:.1f}人。終わり方とシリーズへの誘導を見直す"))
            if kd == "通常" and (v["impressions"] or 0) < 1000 and v["impressions"] is not None:
                notes.append(("データ不足", t,
                              f"インプレッション {int(v['impressions'])} 回。まだ数が少なく、割合の比較はぶれが大きい"))
    return notes


# ---- レポート（HTML と Markdown） --------------------------------------------------
def bar_svg(items, unit, width=720, color="#4c7cf0", ci=None):
    """横棒グラフの SVG。ci があれば信頼区間のひげを描く"""
    if not items:
        return "<p>データなし</p>"
    vmax = max(max(v for _, v in items), max((h for _, h in (ci or {}).values() if h is not None), default=0)) or 1
    rowh, lw = 30, 260
    h = rowh * len(items) + 20
    out = [f'<svg viewBox="0 0 {width} {h}" width="100%" role="img">']
    for i, (lab, val) in enumerate(items):
        y = 10 + i * rowh
        w = (width - lw - 90) * val / vmax
        out.append(f'<text x="{lw - 8}" y="{y + 19}" text-anchor="end" class="lab">{html.escape(lab[:22])}</text>')
        out.append(f'<rect x="{lw}" y="{y + 5}" width="{w:.1f}" height="{rowh - 12}" rx="4" fill="{color}"/>')
        if ci and lab in ci and ci[lab][0] is not None:
            lo, hi = ci[lab]
            x1 = lw + (width - lw - 90) * lo / vmax
            x2 = lw + (width - lw - 90) * hi / vmax
            out.append(f'<line x1="{x1:.1f}" x2="{x2:.1f}" y1="{y + 14}" y2="{y + 14}" class="ci"/>')
        nd = 0 if unit == "回" else 1
        out.append(f'<text x="{lw + w + 6:.1f}" y="{y + 19}" class="val">{val:,.{nd}f}{unit}</text>')
    out.append("</svg>")
    return "".join(out)


def fmt(x, nd=1, unit=""):
    return "—" if x is None else f"{x:,.{nd}f}{unit}"


def mmss(s):
    return "—" if s is None else f"{int(s // 60)}:{int(s % 60):02d}"


def report(path, out):
    name, header, idx, videos, total = load(path)
    if not videos:
        sys.exit("動画の行が見つかりませんでした")
    notes = analyze(videos)
    missing = [k for k, i in idx.items() if i is None and k in ("views", "impressions", "ctr", "avp", "avd", "subs")]
    videos.sort(key=lambda v: -(v["views"] or 0))
    groups = {kd: [v for v in videos if v["kind"] == kd] for kd in ("ショート", "通常", "不明")}

    sections = []
    for kd, g in groups.items():
        if not g:
            continue
        ctr_items = [(v["title"], v["ctr"]) for v in g if v["ctr"] is not None]
        ci = {v["title"]: (v["ctr_lo"], v["ctr_hi"]) for v in g}
        sections.append(f"<h2>{kd}動画（{len(g)}本）</h2>")
        sections.append("<h3>視聴回数</h3>" + bar_svg([(v["title"], v["views"] or 0) for v in g], "回"))
        if ctr_items:
            sections.append("<h3>インプレッションのクリック率（線は95%信頼区間）</h3>"
                            + bar_svg(ctr_items, "%", color="#f0a020", ci=ci))
        avp_items = [(v["title"], v["avp"]) for v in g if v["avp"] is not None]
        if avp_items:
            sections.append("<h3>平均再生率</h3>" + bar_svg(avp_items, "%", color="#3fb27f"))
        rows = "".join(
            f"<tr><td>{html.escape(v['title'][:50])}</td><td>{fmt(v['views'], 0)}</td><td>{fmt(v['impressions'], 0)}</td>"
            f"<td>{fmt(v['ctr'], 1, '%')}</td><td>{mmss(v['avd'])}</td><td>{fmt(v['avp'], 0, '%')}</td>"
            f"<td>{fmt(v['subs'], 0)}</td><td>{fmt(v['subs_per_1k'], 1)}</td><td>{fmt(v['likes_per_1k'], 1)}</td></tr>"
            for v in g)
        sections.append(
            "<div class='tw'><table><tr><th>動画</th><th>視聴回数</th><th>インプレッション</th><th>クリック率</th>"
            "<th>平均視聴時間</th><th>平均再生率</th><th>登録者</th><th>登録/1000回</th><th>高評価/1000回</th></tr>"
            f"{rows}</table></div>")
    note_html = "".join(f"<li><b>{html.escape(c)}</b>｜{html.escape(t)}：{html.escape(m)}</li>" for c, t, m in notes) \
        or "<li>はっきりした差は見つかりませんでした（データが少ない場合はしばらく待って再分析）</li>"
    miss_html = f"<p class='warn'>この書き出しに無かった指標: {', '.join(missing)}（詳細モードで列を追加して書き出すと分析できる）</p>" \
        if missing else ""
    page = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>YouTube成績レポート</title>
<style>
:root{{--bg:#fff;--fg:#1d2433;--sub:#5b6478;--line:#e3e6ee;--ci:#c0392b}}
@media (prefers-color-scheme:dark){{:root{{--bg:#12151c;--fg:#e8ebf2;--sub:#a3abbd;--line:#2a2f3b;--ci:#ff8a7a}}}}
body{{background:var(--bg);color:var(--fg);font-family:"Noto Sans JP",sans-serif;max-width:960px;margin:0 auto;padding:16px;line-height:1.7}}
h1{{font-size:1.5rem}} h2{{border-bottom:2px solid var(--line);padding-bottom:4px;margin-top:2rem}}
.lab{{font-size:12px;fill:var(--fg)}} .val{{font-size:12px;fill:var(--sub)}} .ci{{stroke:var(--ci);stroke-width:2}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;font-size:.85rem;min-width:720px}}
td,th{{border-bottom:1px solid var(--line);padding:4px 6px;text-align:right}} td:first-child,th:first-child{{text-align:left}}
.warn{{color:var(--ci)}} .box{{border:1px solid var(--line);border-radius:8px;padding:8px 16px}}
</style></head><body>
<h1>YouTube 成績レポート</h1>
<p>入力: {html.escape(os.path.basename(name))}／動画 {len(videos)} 本</p>
{miss_html}
<div class="box"><h2 style="margin-top:.5rem">気づいたこと（改善の候補）</h2><ul>{note_html}</ul></div>
<div class="box"><h3>読み方（基本の原理）</h3>
<p>動画が見られる流れは「インプレッション × クリック率 → 視聴 → 平均再生率 → 登録」の漏斗。
クリック率が低ければサムネイルとタイトル、平均再生率が低ければ冒頭と構成、登録が少なければ終わり方とシリーズ誘導を直す。</p>
<p>クリック率の線（95%信頼区間）は、偶然によるぶれの範囲。インプレッションが少ないほど線が長くなる。
線どうしが重なっている動画の差は、偶然の範囲かもしれない。</p>
<p>ショート（3分以下）と通常の動画は、見られ方がちがうため別々に比べている。
ショートはフィードで自動的に流れてくることが多く、サムネイルのクリック率はあまり意味を持たない。
ショートでは平均再生率（どれだけ最後まで見られたか）と、登録につながったかを中心に見る。</p></div>
{''.join(sections)}
</body></html>"""
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    open(out + ".html", "w", encoding="utf-8").write(page)
    md = [f"# YouTube 成績レポート\n\n入力: `{os.path.basename(name)}`／動画 {len(videos)} 本\n"]
    if missing:
        md.append(f"\n> この書き出しに無かった指標: {', '.join(missing)}\n")
    md.append("\n## 気づいたこと\n")
    md += [f"- **{c}**｜{t}：{m}\n" for c, t, m in notes] or ["- はっきりした差は見つかりませんでした\n"]
    for kd, g in groups.items():
        if not g:
            continue
        md.append(f"\n## {kd}動画（{len(g)}本）\n\n| 動画 | 視聴回数 | クリック率 | 平均再生率 | 登録/1000回 |\n|---|---:|---:|---:|---:|\n")
        md += [f"| {v['title'][:30]} | {fmt(v['views'], 0)} | {fmt(v['ctr'], 1, '%')} | {fmt(v['avp'], 0, '%')} | "
               f"{fmt(v['subs_per_1k'], 1)} |\n" for v in g]
    open(out + ".md", "w", encoding="utf-8").write("".join(md))
    print("wrote", out + ".html", out + ".md")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--out", default="analysis/report")
    a = ap.parse_args()
    report(a.input, a.out)
