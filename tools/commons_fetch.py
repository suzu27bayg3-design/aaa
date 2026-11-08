#!/usr/bin/env python3
"""Wikimedia Commons から、自由なライセンスの写真を探して取り込む（撮影者・ライセンスも一緒に保存）。

使い方:
  python3 tools/commons_fetch.py search "Genbudo"                 # 候補の一覧（大きさ・ライセンス・撮影者）
  python3 tools/commons_fetch.py get travel_shorts/genbudo/photos "File:A.jpg" "File:B.jpg"
      → photos/A.jpg ... と photos/credits.json（画面と説明欄のクレジットに使う）

しくみ:
  Commons の API（action=query, prop=imageinfo）で、ファイルの大きさ・URL・ライセンス名・撮影者を取る。
  幅2400pxの縮小版（thumburl）を取り込む。API は混むと「リクエストが多すぎる」と返すので、間をあけてやり直す。
  使ってよいのは CC0 / パブリックドメイン / CC BY / CC BY-SA だけ（NC=非営利限定、ND=改変禁止は使わない）。
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "ScienceShortsBot/1.0 (https://github.com/suzu27bayg3-design/aaa; educational shorts with credits)"
OK = re.compile(r"^(CC0|Public domain|PD.*|CC BY(-SA)? [0-9.]+.*)$", re.I)


def call(params, tries=6):
    url = API + "?" + urllib.parse.urlencode(dict(params, format="json", maxlag=5))
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40) as r:
                return json.loads(r.read())
        except (json.JSONDecodeError, urllib.error.HTTPError, urllib.error.URLError):
            time.sleep(10 * 2 ** k)  # 10, 20, 40 ... 秒あけてやり直す
    raise SystemExit("Commons API did not answer")


def meta(p):
    ii = p["imageinfo"][0]
    m = ii.get("extmetadata", {})
    clean = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()  # noqa: E731
    return dict(title=p["title"], width=ii["width"], height=ii["height"],
                license=clean(m.get("LicenseShortName", {}).get("value")),
                artist=clean(m.get("Artist", {}).get("value")),
                page=ii.get("descriptionurl"), thumb=ii.get("thumburl") or ii["url"])


def search(q):
    d = call(dict(action="query", generator="search", gsrsearch=f"{q} filetype:bitmap", gsrnamespace=6,
                  gsrlimit=50, prop="imageinfo", iiprop="size|extmetadata|url", iiurlwidth=2400,
                  iiextmetadatafilter="LicenseShortName|Artist"))
    rows = [meta(p) for p in d.get("query", {}).get("pages", {}).values()]
    rows.sort(key=lambda r: -r["width"] * r["height"])
    for r in rows:
        flag = "OK " if OK.match(r["license"]) else "NG "
        print(flag, f"{r['width']}x{r['height']}", "|", r["license"], "|", r["artist"][:30], "|", r["title"])


def get(outdir, titles):
    os.makedirs(outdir, exist_ok=True)
    d = call(dict(action="query", titles="|".join(titles), prop="imageinfo", iiprop="size|extmetadata|url",
                  iiurlwidth=2400, iiextmetadatafilter="LicenseShortName|Artist"))
    credits = []
    for p in d["query"]["pages"].values():
        r = meta(p)
        if not OK.match(r["license"]):
            print("skip (license):", r["title"], r["license"])
            continue
        name = re.sub(r"[^\w.-]+", "_", r["title"][5:])
        path = os.path.join(outdir, name)
        req = urllib.request.Request(r["thumb"], headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as resp, open(path, "wb") as f:
            f.write(resp.read())
        r["file"] = name
        credits.append(r)
        print("got", name, r["license"], r["artist"][:40])
        time.sleep(2)
    with open(os.path.join(outdir, "credits.json"), "w", encoding="utf-8") as f:
        json.dump(credits, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    if sys.argv[1] == "search":
        search(sys.argv[2])
    else:
        get(sys.argv[2], sys.argv[3:])
