# 第5回の見本画像: 冒頭の予告 / 縦長ショート / サムネイル別案 / 次回予告
import importlib.util, sys, math
sys.path.insert(0, "/home/user/aaa/tools")
import longform as L
from PIL import Image, ImageDraw
OUT = sys.argv[1]
spec = importlib.util.spec_from_file_location("cfg", "/home/user/aaa/longform_quantum5/script.py")
cfg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cfg)
W, H, GOLD, WHITE, NAVY = L.W, L.H, L.GOLD, L.WHITE, L.NAVY
bg = L.background()

def fig(kind_fig, box, t, size=(W, H)):
    lay = Image.new("RGBA", size)
    L.ANIM_T = t
    L.fig_area(lay, box, kind_fig, cfg)
    L.ANIM_T = None
    return lay

def outlined(d, xy, text, font, fill, anchor="mm", sw=8):
    d.text(xy, text, font=font, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=NAVY)

def portrait(spk, ex, size, mouth=0):
    im = L.face(spk, ex, False, mouth)
    sc = size / im.width
    return im.resize((size, int(im.height * sc)), Image.LANCZOS)

# ---------- ① 冒頭の予告（16:9）----------
def cold(t, hook, sub, step):
    img = bg.copy()
    img = Image.alpha_composite(img, fig({"kind": "tower"}, (380, 300, 1540, 900), t))
    d = ImageDraw.Draw(img)
    a = min(1, t / 0.8)
    outlined(d, (W / 2, 120), hook[0], L.jp(92), WHITE)
    outlined(d, (W / 2, 235), hook[1], L.jp(110), GOLD)
    z = portrait("Z", "panic", 330, 2)
    img.alpha_composite(z, (30, H - z.height + 40))
    d.rounded_rectangle((380, 930, 1540, 1040), 28, fill=(255, 255, 255, 235), outline=(110, 200, 90), width=8)
    d.text((W / 2, 985), sub, font=L.jp(50, True), fill=NAVY, anchor="mm")
    d.rounded_rectangle((W - 330, 30, W - 30, 90), 30, fill=(230, 60, 80))
    d.text((W - 180, 60), step, font=L.jp(30, True), fill=WHITE, anchor="mm")
    return img.convert("RGB")

c1 = cold(0.6, ("スカイツリーの上は", "1日4ナノ秒 未来にいる？"), "えっ、どういうことなのだ！？", "このあと本編")
c2 = cold(4.0, ("重力が弱いほど", "時間は速く進む"), "それを測れる時計があるのだ！？", "このあと本編")
# 予告のあとのタイトル
c3 = L.slide(bg, cfg, 0, cfg.CHAPTERS[0])
c3 = L.with_line(c3, "M", "今日は、スカイツリーで時間の進み方のちがいを測った時計や、ダイヤモンドを使ったセンサを紹介するわ。",
                 "explain", 1, 0, ()).convert("RGB")

# ---------- ② 縦長ショート（1080x1920）----------
SW, SH = 1080, 1920
def vbg():
    im = Image.new("RGBA", (SW, SH))
    d = ImageDraw.Draw(im)
    for y in range(SH):
        k = y / SH
        d.line((0, y, SW, y), fill=(int(20 * (1 - k) + 6 * k), int(30 * (1 - k) + 10 * k), int(72 * (1 - k) + 28 * k), 255))
    return im

def short(hook, figdef, box, t, spk, ex, line, tag, prog, scale=1.12):
    im = vbg()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 60, 400, 120), 30, fill=(66, 133, 244))
    d.text((220, 90), tag, font=L.jp(34, True), fill=WHITE, anchor="mm")
    outlined(d, (SW / 2, 250), hook[0], L.jp(84), WHITE, sw=7)
    outlined(d, (SW / 2, 370), hook[1], L.jp(96), GOLD, sw=8)
    pan = Image.new("RGBA", (SW, SH))
    ImageDraw.Draw(pan).rounded_rectangle((30, 470, SW - 30, 1250), 36, fill=(255, 255, 255, 18),
                                          outline=(110, 150, 255, 120), width=3)
    im = Image.alpha_composite(im, pan)
    # 図は横長動画と同じ大きさで描いてから、少し拡大して真ん中に置く
    bw, bh = box
    lay = Image.new("RGBA", (bw + 40, bh + 40))
    L.ANIM_T = t
    L.fig_area(lay, (20, 20, bw + 20, bh + 20), figdef, cfg)
    L.ANIM_T = None
    lay = lay.resize((int(lay.width * scale), int(lay.height * scale)), Image.LANCZOS)
    im.alpha_composite(lay, (int((SW - lay.width) / 2), int(860 - lay.height / 2)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((SW / 2 - 300, 1270, SW / 2 + 300, 1340), 35, fill=(230, 60, 80))
    d.text((SW / 2, 1305), "▶ 続きは本編（量子センサ）", font=L.jp(34, True), fill=WHITE, anchor="mm")
    other = "M" if spk == "Z" else "Z"
    p1 = portrait(spk, ex, 360, 2)
    p2 = portrait(other, "happy", 280, 0)
    p2 = Image.alpha_composite(p2, Image.new("RGBA", p2.size, (0, 0, 0, 90)))
    xs = (20, SW - 300) if spk == "Z" else (SW - 380, 20)
    im.alpha_composite(p2.crop((0, 0, p2.width, 300)), (xs[1], 1360))
    im.alpha_composite(p1.crop((0, 0, p1.width, 300)), (xs[0], 1355))
    d.rounded_rectangle((40, 1640, SW - 40, 1860), 30, fill=(255, 255, 255, 240), outline=L.SPK[spk][1], width=8)
    f = L.jp(52, True)
    ls = L.wrap(d, line, f, SW - 140)[:3]
    for i, ln in enumerate(ls):
        d.text((70, 1752 - len(ls) * 33 + i * 66), ln, font=f, fill=NAVY)
    d.rectangle((0, SH - 24, SW * prog, SH), fill=GOLD)
    return im.convert("RGB")

s1 = short(("スカイツリーの上は", "時間が速い？"), {"kind": "tower"}, (900, 620), 3.2, "M", "explain",
           "高さ450メートルの展望台の時計は、地上より1日に約4ナノ秒速く進んでいたの。", "量子解説 #5", 0.55)
s2 = short(("壊れやすさが", "最強のセンサに？"), {"kind": "dial"}, (900, 560), 5.0, "Z", "think",
           "針のずれを測れば、磁場や重力の強さが分かるのだ！", "量子解説 #5", 0.35)
s3 = short(("ダイヤの中の", "小さな磁石"), dict(cfg.CHAPTERS[6]["fig"]), (900, 520), 2.0, "M", "explain",
           "窒素と原子の抜けた穴のペアが、まわりの磁場に敏感に反応するの。室温で動くのが強みよ。", "量子解説 #5", 0.75)

# ---------- ③ サムネイル別案（1280x720）----------
def thumb_fig():
    img = Image.alpha_composite(bg.copy(), fig({"kind": "tower"}, (120, 260, 1200, 1000), 2.0))
    d = ImageDraw.Draw(img)
    outlined(d, (1380, 300), "1日4ナノ秒", L.jp(150), GOLD, sw=12)
    outlined(d, (1380, 470), "未来にいる？", L.jp(130), WHITE, sw=12)
    z = portrait("Z", "panic", 470, 2)
    img.alpha_composite(z, (W - 470, H - z.height + 120))
    d.rounded_rectangle((40, 40, 330, 120), 24, fill=(66, 133, 244), outline=WHITE, width=5)
    d.text((185, 80), "量子解説 #5", font=L.jp(46), fill=WHITE, anchor="mm")
    return img.convert("RGB").resize((1280, 720), Image.LANCZOS)

def thumb_num():
    img = Image.alpha_composite(bg.copy(), Image.new("RGBA", (W, H), (0, 0, 0, 40)))
    d = ImageDraw.Draw(img)
    ic = L.icon_img("⏱️", 300)
    img.alpha_composite(ic, (90, 330))
    outlined(d, (1060, 330), "300億年で", L.jp(170), WHITE, sw=14)
    outlined(d, (1060, 560), "1秒もずれない", L.jp(170), GOLD, sw=14)
    d.rounded_rectangle((W / 2 - 430, 760, W / 2 + 430, 870), 55, fill=(230, 60, 80), outline=WHITE, width=6)
    d.text((W / 2, 815), "日本発の「光格子時計」", font=L.jp(64), fill=WHITE, anchor="mm")
    m = portrait("M", "explain", 430, 0)
    img.alpha_composite(m, (W - 430, H - m.height + 200))
    d.rounded_rectangle((40, 40, 330, 120), 24, fill=(66, 133, 244), outline=WHITE, width=5)
    d.text((185, 80), "量子解説 #5", font=L.jp(46), fill=WHITE, anchor="mm")
    return img.convert("RGB").resize((1280, 720), Image.LANCZOS)

# ---------- ④ 次回予告（最後の約20秒）----------
def teaser():
    pan = Image.new("RGBA", (W, H))
    ImageDraw.Draw(pan).rounded_rectangle((60, 130, W - 60, 800), 30, fill=(0, 0, 0, 90))
    img = Image.alpha_composite(bg.copy(), pan)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((90, 160, 420, 230), 35, fill=(230, 60, 80))
    d.text((255, 195), "次回予告", font=L.jp(44), fill=WHITE, anchor="mm")
    outlined(d, (W / 2 + 160, 195), "第6回 量子もつれとテレポーテーション", L.jp(56), GOLD, sw=6)
    img = Image.alpha_composite(img, fig({"kind": "pair"}, (200, 250, 1720, 640), 1.7))
    img = L.with_line(img, "Z", "離れていても結果がそろう！？ 次回も見てほしいのだ！", "smug", 2, 0, ())
    d = ImageDraw.Draw(img)
    d.text((W - 90, 245), "※最後の約20秒に、終了画面で第6回の動画を表示", font=L.jp(28, True), fill=(200, 210, 240), anchor="rm")
    return img.convert("RGB")

for name, im in (("c1", c1), ("c2", c2), ("c3", c3), ("s1", s1), ("s2", s2), ("s3", s3),
                 ("t_fig", thumb_fig()), ("t_num", thumb_num()), ("next", teaser())):
    im.save(f"{OUT}/{name}.png")
print("ok")
