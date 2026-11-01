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
    ("2130試合連続出場。鉄の馬と呼ばれた男、ルー・ゲーリッグの成績を見ていくのだ！", "hook"),
    ("通算打撃成績は、打率、さんわりよんぶ、493本塁打、1995打点。オーピーエスは、いってんぜろはちぜろ、なのだ！", "talk"),
    ("約14年間、1試合も休まず、2130試合連続出場。満塁ホームランは23本なのだ。", "talk"),
    ("タイトルは、MVP2回。1934年には三冠王。ワールドシリーズも6回制覇したのだ。", "talk"),
    ("最も輝いたのは1927年。打率、さんわりななぶさんりん、47本塁打、175打点で、MVPなのだ！", "hook"),
    ("引退のとき、自分は地球上で最も幸運な男だと語った、それがルー・ゲーリッグなのだ。", "hook"),
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
