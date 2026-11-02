"""坂本アヒル氏のPSD立ち絵から、表情×目×口の組み合わせPNGを書き出す。

PSDToolの約束事: 名前が「*」で始まる層は同じグループ内で1つだけ表示（ラジオボタン）、
「!」で始まるグループは常に表示。ここでは「グループのパス/層名」を指定して表示を切り替える。

使い方: python3 tools/psd_parts.py <ずんだもん.psd> <四国めたん.psd>
出力: assets/characters/<名前>/<表情>__<目o|c><口0|1|2>.png
"""
import os, sys
from psd_tools import PSDImage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find(psd, path):
    node = psd
    for name in path.split("/"):
        node = next(x for x in node if x.name.lstrip("*!") == name)
    return node


def pick(psd, path):
    """path の層を表示し、同じグループの「*」層を非表示にする（親も表示）"""
    parts = path.split("/")
    parent = psd if len(parts) == 1 else find(psd, "/".join(parts[:-1]))
    target = find(psd, path)
    for x in parent:
        if x.name.startswith("*") and x is not target:
            x.visible = False
    target.visible = True
    for i in range(1, len(parts)):
        find(psd, "/".join(parts[:i])).visible = True


def show(psd, path, on=True):
    find(psd, path).visible = on


CHARS = {
    "zundamon": dict(
        crop=(196, 80, 866, 866),
        base=["服装1", "服装1/いつもの服", "服装1/左腕/基本", "服装1/右腕/基本", "枝豆/枝豆通常",
              "顔色/ほっぺ", "眉/普通眉", "目/目セット", "目/目セット/普通白目", "目/目セット/黒目/カメラ目線"],
        hide=["服装2", "パーカー裏地", "記号など/汗3", "記号など/汗2", "記号など/汗1", "記号など/涙"],
        mouth=["口/むふ", "口/ほあ", "口/ほあー"],
        closed="目/なごみ目",
        expr={
            "happy": ["眉/上がり眉"],
            "smug": ["眉/上がり眉", "服装1/右腕/腰", "服装1/左腕/腰"],
            "shy": ["眉/困り眉1", "顔色/ほっぺ赤め", "目/目セット/黒目/目逸らし", "服装1/左腕/口元"],
            "panic": ["眉/困り眉2", "顔色/青ざめ", "目/目セット/見開き白目", "服装1/右腕/苦しむ",
                      "服装1/左腕/苦しむ", "+記号など/汗1", "+記号など/汗2"],
            "think": ["眉/困り眉1", "目/目セット/黒目/目逸らし", "服装1/左腕/考える"],
        }),
    "metan": dict(
        crop=(180, 0, 900, 846),
        base=["白ロリ服", "白ロリ服/右腕/普通", "白ロリ服/左腕/普通", "顔色/普通2", "眉/ごきげん",
              "目/目セット", "目/目セット/普通白目", "目/目セット/黒目/カメラ目線"],
        hide=["その他の服", "記号など/汗", "記号など/涙", "白ロリ服/右腕/まんじゅう", "白ロリ服/左腕/まんじゅう袋"],
        mouth=["口/ほほえみ", "口/お", "口/わあー"],
        closed="目/目閉じ",
        expr={
            "happy": [],
            "explain": ["白ロリ服/右腕/指差す", "眉/太眉ごきげん"],
            "smug": ["眉/ややおこ", "白ロリ服/左腕/口元に指"],
            "shy": ["眉/こまり", "顔色/赤面", "目/目セット/黒目/目そらし"],
            "panic": ["眉/こまり", "顔色/青ざめ", "目/目セット/見開き白目", "+記号など/汗"],
        }),
}


def build(psd_path, name):
    cfg = CHARS[name]
    out = os.path.join(ROOT, "assets", "characters", name)
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith(".png"):
            os.remove(os.path.join(out, f))
    for ex, ops in cfg["expr"].items():
        for eye in "oc":
            for mi, mouth in enumerate(cfg["mouth"]):
                psd = PSDImage.open(psd_path)
                for h in cfg["hide"]:
                    show(psd, h, False)
                for p in cfg["base"] + ops:
                    show(psd, p[1:]) if p.startswith("+") else pick(psd, p)
                if eye == "c":
                    pick(psd, cfg["closed"])
                pick(psd, mouth)
                img = psd.composite(force=True).crop(cfg["crop"])
                img.save(os.path.join(out, f"{ex}__{eye}{mi}.png"))
        print(name, ex)


if __name__ == "__main__":
    build(sys.argv[1], "zundamon")
    build(sys.argv[2], "metan")
