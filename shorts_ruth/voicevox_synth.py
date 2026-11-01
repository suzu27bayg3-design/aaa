#!/usr/bin/env python3
"""VOICEVOXエンジン(HTTP API)でずんだもんのナレーションを作り、voicevox/ に 001_〜.wav として保存する。

前提: VOICEVOXエンジンが http://127.0.0.1:50021 で起動していること
  (VOICEVOXアプリを起動しているだけでもOK。アプリ内でエンジンが動いている)
仕組み: /audio_query でテキスト→読み・アクセント・抑揚の情報(JSON)を作り、
        話速などを調整してから /synthesis に渡すと WAV が返ってくる。
"""
import json
import os
import urllib.parse
import urllib.request

HOST = os.environ.get("VOICEVOX_HOST", "http://127.0.0.1:50021")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "voicevox")
SPEAKER = 3  # ずんだもん(ノーマル)

# (読み上げ文, 種類) hook=冒頭・驚き・オチ(抑揚強め・少し高め), talk=説明
LINES = [
    ("大谷翔平より100年以上前に、二刀流をやった男がいるのだ！", "hook"),
    ("その名は、ベーブ・ルース。最初は、レッドソックスのエース投手だったのだ。", "talk"),
    ("1918年には、投げて13勝、打って11本塁打なのだ。", "talk"),
    ("ヤンキースに移ると打者に専念して、1927年には、シーズン60本塁打！", "hook"),
    ("通算714本塁打。この記録は、39年間も破られなかったのだ。", "talk"),
    ("1934年には日本にも来て、全米チームの主砲として、大歓迎されたのだ。", "talk"),
    ("2022年、大谷が10勝10本を達成して、ルース以来104年ぶりと話題になったのだ。", "talk"),
    ("100年以上前の二刀流、それがベーブ・ルースなのだ！", "hook"),
]
PARAMS = {
    "hook": dict(speedScale=1.15, pitchScale=0.03, intonationScale=1.35),
    "talk": dict(speedScale=1.2, pitchScale=0.0, intonationScale=1.15),
}


def post(path, params, body=None):
    url = f"{HOST}{path}?{urllib.parse.urlencode(params)}"
    data = json.dumps(body).encode() if body is not None else b""
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return r.read()


def main():
    os.makedirs(OUT, exist_ok=True)
    for i, (text, kind) in enumerate(LINES, 1):
        q = json.loads(post("/audio_query", {"text": text, "speaker": SPEAKER}))
        q.update(PARAMS[kind], prePhonemeLength=0.05, postPhonemeLength=0.1,
                 outputSamplingRate=48000)
        wav = post("/synthesis", {"speaker": SPEAKER}, q)
        path = os.path.join(OUT, f"{i:03d}_ずんだもん.wav")
        open(path, "wb").write(wav)
        kana = "".join(p["moras"][0]["text"] and "".join(m["text"] for m in p["moras"]) + "/"
                       for p in q["accent_phrases"])
        print(f"{path}  {kana}")


if __name__ == "__main__":
    main()
