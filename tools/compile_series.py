#!/usr/bin/env python3
"""シリーズ全回をつなげた「総集編」を作る。

使い方:
  python3 tools/compile_series.py -o longform_quantum_all/quantum_all.mp4 \
      longform_quantum/script.py longform_quantum2/script.py ... longform_quantum10/script.py

各回の動画（台本の OUT）を順につなげ、各回の始まりの時刻を chapters.txt に書く
（YouTube の説明欄に貼るとチャプターになる）。各回の動画は同じ設定で書き出しているので、
再エンコードせずにつなげる。
"""
import argparse
import importlib.util
import os
import subprocess
import tempfile


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scripts", nargs="+")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    items = []
    for sc in a.scripts:
        spec = importlib.util.spec_from_file_location("cfg", sc)
        cfg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cfg)
        video = os.path.join(os.path.dirname(os.path.abspath(sc)), cfg.OUT)
        items.append((cfg.TITLE, video))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    lst = os.path.join(tempfile.mkdtemp(), "list.txt")
    with open(lst, "w") as f:
        for _, v in items:
            f.write(f"file '{v}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", "-movflags", "+faststart", a.out], check=True)
    t = 0.0
    lines = []
    for i, (title, v) in enumerate(items, 1):
        h, m, s = int(t // 3600), int(t % 3600 // 60), int(t % 60)
        stamp = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
        lines.append(f"{stamp} 第{i}回 {title}")
        t += duration(v)
    with open(os.path.join(os.path.dirname(os.path.abspath(a.out)), "chapters.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", a.out, f"{t / 60:.1f} min")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
