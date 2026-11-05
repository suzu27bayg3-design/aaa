"""Create '全体系統図（改善反映）' page: copy of 全体系統図 with review items applied.

Added / changed items are drawn in ORANGE. Symbols are cloned from the symbol-list page.
Coordinates in this script are in mm (page is 1:1 A3).
"""
import sys, os, re, copy, math, json, zipfile, shutil
from lxml import etree

SRC, OUT = sys.argv[1], sys.argv[2]
NS = 'http://schemas.microsoft.com/office/visio/2012/main'
RNS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
V = '{%s}' % NS
IN = 1 / 25.4
ORANGE = '#FF8C00'
work = OUT + '.d'
if os.path.exists(work): shutil.rmtree(work)
zipfile.ZipFile(SRC).extractall(work)
P = lambda *a: os.path.join(work, *a)
parser = etree.XMLParser(remove_blank_text=False)
def load(p): return etree.parse(p, parser).getroot()
def save(root, p): etree.ElementTree(root).write(p, xml_declaration=True, encoding='utf-8')

# ---------- locate pages ----------
pages = load(P('visio/pages/pages.xml'))
prels = open(P('visio/pages/_rels/pages.xml.rels'), encoding='utf8').read()
rel_target = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', prels))
def page_file(name):
    for pg in pages.findall(V + 'Page'):
        if pg.get('NameU') == name: return pg, rel_target[pg.find(V + 'Rel').get('{%s}id' % RNS)]
    raise SystemExit('page not found ' + name)
src_pg, src_file = page_file('全体系統図')
sym_pg, sym_file = page_file('ページ - 4')  # ｼﾝﾎﾞﾙ
root = load(P('visio/pages', src_file))
sym = load(P('visio/pages', sym_file))
shapes = root.find(V + 'Shapes')
sym_top = {s.get('ID'): s for s in sym.find(V + 'Shapes').findall(V + 'Shape')}
top = {s.get('ID'): s for s in shapes.findall(V + 'Shape')}
next_id = [max(int(e.get('ID')) for e in root.iter(V + 'Shape')) + 1]

def cell(s, n):
    for c in s.findall(V + 'Cell'):
        if c.get('N') == n: return c
def setc(s, n, v, f=None):
    c = cell(s, n)
    if c is None:
        c = etree.Element(V + 'Cell'); c.set('N', n)
        # cells must precede sections
        first_sec = s.find(V + 'Section')
        if first_sec is not None: first_sec.addprevious(c)
        else:
            t = s.find(V + 'Text'); sh = s.find(V + 'Shapes')
            anchor = t if t is not None else sh
            if anchor is not None: anchor.addprevious(c)
            else: s.append(c)
    c.set('V', str(v))
    if f is None and 'F' in c.attrib: del c.attrib['F']
    if f is not None: c.set('F', f)
def cv(s, n, d=0.0):
    c = cell(s, n)
    try: return float(c.get('V'))
    except Exception: return d
def pos(i):
    s = top[i]; return cv(s, 'PinX') / IN, cv(s, 'PinY') / IN

def renumber(s):
    for e in s.iter(V + 'Shape'):
        e.set('ID', str(next_id[0])); next_id[0] += 1
        for a in ('UniqueID',):
            if a in e.attrib: del e.attrib[a]
    return s

def color(s, col=ORANGE):
    for e in s.iter(V + 'Shape'):
        setc(e, 'LineColor', col)
        for sec in e.findall(V + 'Section'):
            if sec.get('N') == 'Character':
                for c in sec.iter(V + 'Cell'):
                    if c.get('N') == 'Color': c.set('V', col); c.attrib.pop('F', None)

added = []
def place_symbol(sym_id, x, y, angle=0.0, flipx=0, flipy=0, size=3.31, note=''):
    src = TEMPLATES.get(sym_id, sym_top.get(sym_id))
    s = renumber(copy.deepcopy(src))
    if size is not None:
        w = cv(s, 'Width')
        k = size * IN / w
        if abs(k - 1) > 1e-6: scale_shape(s, k)
    setc(s, 'PinX', x * IN); setc(s, 'PinY', y * IN)
    setc(s, 'Angle', angle); setc(s, 'FlipX', flipx); setc(s, 'FlipY', flipy)
    color(s)
    shapes.append(s); added.append((note, s.get('ID')))
    return s

# --- length scaling for cloned symbols (same rules as the page port) ---
XFORM = {'PinX', 'PinY', 'Width', 'Height', 'LocPinX', 'LocPinY', 'TxtPinX', 'TxtPinY', 'TxtWidth', 'TxtHeight', 'TxtLocPinX', 'TxtLocPinY'}
GEOM = {'MoveTo': 'XY', 'LineTo': 'XY', 'ArcTo': 'XYA', 'EllipticalArcTo': 'XYAB', 'Ellipse': 'XYABCD', 'NURBSTo': 'XY', 'PolylineTo': 'XY'}
def sc(c, k):
    try: c.set('V', repr(float(c.get('V')) * k))
    except (TypeError, ValueError): pass
def scale_shape(s, k):
    for c in s.findall(V + 'Cell'):
        if c.get('N') in XFORM: sc(c, k)
    for sec in s.findall(V + 'Section'):
        for row in sec.findall(V + 'Row'):
            if sec.get('N') == 'Geometry':
                for c in row.findall(V + 'Cell'):
                    if c.get('N') in GEOM.get(row.get('T'), ''): sc(c, k)
            elif sec.get('N') in ('Connection', 'Control'):
                for c in row.findall(V + 'Cell'):
                    if c.get('N') in ('X', 'Y', 'XDyn', 'YDyn'): sc(c, k)
    sh = s.find(V + 'Shapes')
    if sh is not None:
        for ch in sh.findall(V + 'Shape'): scale_shape(ch, k)

def line(x1, y1, x2, y2, col=ORANGE, pattern=1, weight_pt=0.72, note=''):
    L = math.hypot(x2 - x1, y2 - y1) * IN; a = math.atan2(y2 - y1, x2 - x1)
    s = etree.SubElement(shapes, V + 'Shape'); s.set('ID', str(next_id[0])); next_id[0] += 1
    s.set('Type', 'Shape'); s.set('LineStyle', '3'); s.set('FillStyle', '3'); s.set('TextStyle', '3')
    for n, v in (('PinX', (x1 + x2) / 2 * IN), ('PinY', (y1 + y2) / 2 * IN), ('Width', L), ('Height', 0),
                 ('LocPinX', L / 2), ('LocPinY', 0), ('Angle', a), ('BeginX', x1 * IN), ('BeginY', y1 * IN),
                 ('EndX', x2 * IN), ('EndY', y2 * IN), ('LineWeight', weight_pt / 72), ('LineColor', col),
                 ('LinePattern', pattern), ('ObjType', 2)):
        c = etree.SubElement(s, V + 'Cell'); c.set('N', n); c.set('V', str(v))
    g = etree.SubElement(s, V + 'Section'); g.set('N', 'Geometry'); g.set('IX', '0')
    nf = etree.SubElement(g, V + 'Cell'); nf.set('N', 'NoFill'); nf.set('V', '1')
    for ix, (t, x) in enumerate((('MoveTo', 0), ('LineTo', L)), 1):
        r = etree.SubElement(g, V + 'Row'); r.set('T', t); r.set('IX', str(ix))
        for n, v in (('X', x), ('Y', 0)):
            c = etree.SubElement(r, V + 'Cell'); c.set('N', n); c.set('V', str(v))
    added.append((note, s.get('ID')))
    return s

def text(x, y, txt, size_mm=1.6, w=None, h=None, col=ORANGE, align=1, bold=False, angle=0.0, note='', bg=False):
    n_lines = txt.count('\n') + 1
    w = w if w else max(len(l) for l in txt.split('\n')) * size_mm * 0.95 + 1
    h = h if h else n_lines * size_mm * 1.35 + 0.6
    s = etree.SubElement(shapes, V + 'Shape'); s.set('ID', str(next_id[0])); next_id[0] += 1
    s.set('Type', 'Shape'); s.set('LineStyle', '3'); s.set('FillStyle', '3'); s.set('TextStyle', '3')
    for n, v in (('PinX', x * IN), ('PinY', y * IN), ('Width', w * IN), ('Height', h * IN), ('LocPinX', w * IN / 2),
                 ('LocPinY', h * IN / 2), ('Angle', angle), ('LeftMargin', 0), ('RightMargin', 0), ('TopMargin', 0),
                 ('BottomMargin', 0), ('VerticalAlign', 1)):
        c = etree.SubElement(s, V + 'Cell'); c.set('N', n); c.set('V', str(v))
    ch = etree.SubElement(s, V + 'Section'); ch.set('N', 'Character')
    r = etree.SubElement(ch, V + 'Row'); r.set('IX', '0')
    for n, v in (('Font', 'MS Gothic'), ('Color', col), ('Style', '1' if bold else '0'), ('Size', size_mm * IN), ('AsianFont', 'MS Gothic')):
        c = etree.SubElement(r, V + 'Cell'); c.set('N', n); c.set('V', str(v))
    pa = etree.SubElement(s, V + 'Section'); pa.set('N', 'Paragraph')
    r = etree.SubElement(pa, V + 'Row'); r.set('IX', '0')
    c = etree.SubElement(r, V + 'Cell'); c.set('N', 'HorzAlign'); c.set('V', str(align))
    if bg:
        for n, v in (('FillForegnd', '#FFFFFF'), ('FillPattern', 1)):
            c = etree.Element(V + 'Cell'); c.set('N', n); c.set('V', str(v)); ch.addprevious(c)
        g = etree.Element(V + 'Section'); g.set('N', 'Geometry'); g.set('IX', '0')
        c = etree.SubElement(g, V + 'Cell'); c.set('N', 'NoLine'); c.set('V', '1')
        for ix, (t_, X, Y) in enumerate((('MoveTo', 0, 0), ('LineTo', w * IN, 0), ('LineTo', w * IN, h * IN), ('LineTo', 0, h * IN), ('LineTo', 0, 0)), 1):
            r_ = etree.SubElement(g, V + 'Row'); r_.set('T', t_); r_.set('IX', str(ix))
            for n, v in (('X', X), ('Y', Y)):
                c = etree.SubElement(r_, V + 'Cell'); c.set('N', n); c.set('V', str(v))
        pa.addnext(g)
    t = etree.SubElement(s, V + 'Text'); cp = etree.SubElement(t, V + 'cp'); cp.set('IX', '0'); cp.tail = txt
    added.append((note, s.get('ID')))
    return s

def bubble(x, y, label, d=5.0, note=''):
    s = etree.SubElement(shapes, V + 'Shape'); s.set('ID', str(next_id[0])); next_id[0] += 1
    s.set('Type', 'Shape'); s.set('LineStyle', '3'); s.set('FillStyle', '3'); s.set('TextStyle', '3')
    W = d * IN
    for n, v in (('PinX', x * IN), ('PinY', y * IN), ('Width', W), ('Height', W), ('LocPinX', W / 2), ('LocPinY', W / 2),
                 ('LineColor', ORANGE), ('LineWeight', 0.72 / 72), ('FillForegnd', '#FFFFFF'), ('FillPattern', 1),
                 ('LeftMargin', 0), ('RightMargin', 0), ('TopMargin', 0), ('BottomMargin', 0)):
        c = etree.SubElement(s, V + 'Cell'); c.set('N', n); c.set('V', str(v))
    ch = etree.SubElement(s, V + 'Section'); ch.set('N', 'Character')
    r = etree.SubElement(ch, V + 'Row'); r.set('IX', '0')
    for n, v in (('Font', 'MS Gothic'), ('Color', ORANGE), ('Size', 1.3 * IN), ('AsianFont', 'MS Gothic')):
        c = etree.SubElement(r, V + 'Cell'); c.set('N', n); c.set('V', str(v))
    g = etree.SubElement(s, V + 'Section'); g.set('N', 'Geometry'); g.set('IX', '0')
    r = etree.SubElement(g, V + 'Row'); r.set('T', 'Ellipse'); r.set('IX', '1')
    for n, v in (('X', W / 2), ('Y', W / 2), ('A', W), ('B', W / 2), ('C', W / 2), ('D', W)):
        c = etree.SubElement(r, V + 'Cell'); c.set('N', n); c.set('V', str(v))
    t = etree.SubElement(s, V + 'Text'); cp = etree.SubElement(t, V + 'cp'); cp.set('IX', '0'); cp.tail = label
    added.append((note, s.get('ID')))

# 逆止弁: シンボルリストと同じマスター(Check valve)の、この図面上の既存インスタンス(3.31mm)を複製
# 安全弁: シンボルリストの図形(Relief (angle))をそのままの大きさ(4mm)で複製
CHECK, RELIEF, PLUG = 'CHECK', '387', '480'
TEMPLATES = {'CHECK': copy.deepcopy(top['415'])}
UP = dict(angle=math.pi / 2, flipx=1)      # flow upward
DOWN = dict(angle=-math.pi / 2, flipx=1)   # flow downward

# ============ No.1  analyzer panels -> sample-gas switching headers ============
panels = {  # panel id: (inlet xs from glued connectors, top y, bottom y, outlet x)
    '118': ('PC', 116.8, 102.4, 74.0),
    '30': ('GC-EPD', 125.0, 113.8, 118.4),
    '67': ('CRDS', 125.0, 113.8, 146.4),
}
conns = root.find(V + 'Connects')
for pid, (nm, yT, yB, ox) in panels.items():
    xs = sorted({cv(top[c.get('FromSheet')], 'EndX') / IN for c in conns if c.get('ToSheet') == pid})
    for c in [c for c in conns if c.get('ToSheet') == pid or c.get('FromSheet') == pid]: conns.remove(c)
    shapes.remove(top[pid])
    yC = yB + 2.0
    ycv = yT - 3.0 if nm != 'PC' else yT - 4.0
    for x in xs:
        line(x, yT, x, yC, note=f'No.1 {nm} 入口配管')
        place_symbol(CHECK, x, ycv, **DOWN, note=f'No.1 {nm} 入口逆止弁')
    line(min(xs), yC, max(xs), yC, note=f'No.1 {nm} 切替ヘッダー')
    line(ox, yC, ox, yB, note=f'No.1 {nm} 出口')
    if nm == 'PC':
        text(min(xs) - 7.5, yC, 'PC用\n切替ヘッダー', size_mm=1.2, note='No.1 PC 表記')
    else:
        text((min(xs) + max(xs)) / 2, yC + 1.3, f'{nm}用 切替ヘッダー', size_mm=1.1, bg=True, note=f'No.1 {nm} 表記')

# ============ No.3  check valves on VENT No.2 connections ============
for vid, y in (('1241', 244.25), ('1239', 244.25), ('1237', 237.75), ('1243', 245.0), ('1245', 245.4)):
    x, _ = pos(vid); place_symbol(CHECK, x, y, **UP, note=f'No.3 VENT接続逆止弁({vid})')

# ============ No.5  GC-EPD carrier gas, No.6 PH2 ============
for vid in ('414', '413'):
    x, _ = pos(vid); place_symbol(CHECK, x, 107.2, **DOWN, note=f'No.5 キャリアガス逆止弁({vid})')
x, _ = pos('640'); place_symbol(CHECK, x, 109.0, **UP, note='No.6 PH2送出逆止弁')

# ============ No.2  relief valves on standard-gas cylinder regulators ============
# 281 (GC-EPD span gas): branch down from the horizontal line at y=97.9
place_symbol(RELIEF, 101.6, 94.4, angle=math.pi, size=None, note='No.2 安全弁(281下流)')
line(101.6, 97.9, 101.6, 96.4, note='No.2 安全弁分岐')
line(103.6, 94.4, 105.4, 94.4, note='No.2 安全弁吹出')
text(106.6, 94.4, 'VENT', size_mm=1.1, note='No.2 吹出先')
# 292 (API-MS span gas): branch up from the horizontal line at y=100.0
place_symbol(RELIEF, 217.2, 103.6, size=None, note='No.2 安全弁(292下流)')
line(217.2, 100.0, 217.2, 101.6, note='No.2 安全弁分岐')
line(215.2, 103.6, 213.6, 103.6, note='No.2 安全弁吹出')
text(211.6, 103.6, 'VENT', size_mm=1.1, note='No.2 吹出先')

# ============ No.4  low-flow switch on dilution N2 ============
for y_line, bx, by, tag in ((280.21, 67.2, 286.0, '261'), (264.39, 66.4, 270.1, '262')):
    line(bx, y_line, bx, by - 2.5, pattern=2, note='No.4 FIS取出し')
    bubble(bx, by, f'FIS\n{tag}', note='No.4 流量スイッチ')
    line(bx + 2.5, by, bx + 6.0, by, pattern=2, note='No.4 信号線')
    text(bx + 6.3 + 13, by, 'L：H2遮断BOXへ（インターロック）', size_mm=1.1, align=0, w=26, note='No.4 信号先')

# ============ No.12  plugs on open ends ============
DROPS = ['760', '761', '762', '764', '763', '765', '766', '770', '769', '771', '844', '845', '846', '848', '847', '849',
         '850', '851', '852', '854', '853', '855', '858', '860', '859', '832', '834', '835', '837', '836', '838',
         '786', '788', '787', '802', '803', '804', '806', '805', '807', '820', '821', '822', '824', '823', '825',
         '970', '968', '975', '969', '976', '1229', '1232', '1235']
LEFT_ENDS = ['585', '586', '581', '582', '583', '584', '579', '580', '573', '574', '575', '576']
RIGHT_ENDS = ['703', '704', '699', '700', '701', '702', '691', '692', '687', '688', '689', '690']
for v in DROPS:
    x, y = pos(v); place_symbol(PLUG, x, y - 1.655 - 0.83, angle=math.pi / 2, size=1.65, note=f'No.12 プラグ({v})')
for v in LEFT_ENDS:
    x, y = pos(v); place_symbol(PLUG, x - 1.655 - 0.83, y, angle=0, size=1.65, note=f'No.12 プラグ({v})')
for v in RIGHT_ENDS:
    x, y = pos(v); place_symbol(PLUG, x + 1.655 + 0.83, y, angle=math.pi, size=1.65, note=f'No.12 プラグ({v})')

# ============ No.13  duplicate shape ============
if '1075' in top: shapes.remove(top['1075'])
for c in [c for c in conns if '1075' in (c.get('FromSheet'), c.get('ToSheet'))]: conns.remove(c)

# ============ No.10  reused tags from the earlier valve list ============
REUSE = {1197: 'V112', 1207: 'RV111', 1196: 'V215', 1195: 'V212', 1194: 'V214', 1183: 'RV211', 1192: 'V217',
         1180: 'V122', 1170: 'RV121', 1179: 'V222', 1169: 'V312', 1167: 'V314', 1153: 'RV311', 1162: 'V316', 857: 'V311',
         637: 'V131', 627: 'RV131', 636: 'V132', 638: 'V232', 639: 'V233', 642: 'V133',
         1088: 'V252', 1086: 'V351', 1089: 'V253', 1087: 'V151', 784: 'V251', 1243: 'V503'}
OFFS = {1167: (0, 2.4), 1194: (0, 2.4), 1207: (-7.5, 0), 1170: (-7.5, 0), 1183: (6.5, 2.0), 1153: (6.5, 2.0),
        627: (-6.0, 2.5), 1088: (-4.0, 0), 1089: (-4.0, 0), 1086: (0, -2.4), 1087: (0, -2.4)}
BELOW = {1180, 1179, 1169, 1162, 1197, 1196, 1195, 1192, 642}
OFFS.update({627: (5.0, 3.9), 784: (-3.9, 0)})
for sid, tag in REUSE.items():
    x, y = pos(str(sid))
    if sid in BELOW:
        text(x, y - 2.62, tag, size_mm=1.0, note=f'No.10 Tag({sid})'); continue
    if sid == 857:
        text(x + 1.15, y - 4.8, tag, size_mm=1.0, angle=math.pi / 2, note='No.10 Tag(857)'); continue
    dx, dy = OFFS.get(sid, (3.4, 0))
    text(x + dx, y + dy, tag, size_mm=1.25, align=1, note=f'No.10 Tag({sid})')

# ============ No.15  destination drawing numbers on off-sheet labels ============
for lid, dwg in (('705', 'SIB00106'), ('707', 'SIB00106'), ('709', 'SIB00106'), ('711', 'SIB00106'),
                 ('713', 'SIB00101'), ('715', 'SIB00101')):
    x, y = pos(lid); text(47.2, y, dwg, size_mm=1.2, note=f'No.15 図番({lid})')
x, y = pos('1029'); text(x, y + 3.6, '→SIB00106', size_mm=1.2, note='No.15 図番(1029)')

# ============ title / legend ============
for s in shapes.findall(V + 'Shape'):
    t = s.find(V + 'Text')
    if t is None: continue
    full = ''.join(t.itertext())
    if full.startswith('Flowsheet 全体系統図'):
        for ch in list(t): t.remove(ch)
        cp = etree.SubElement(t, V + 'cp'); cp.set('IX', '0'); cp.tail = 'Flowsheet 全体系統図（改善反映案）\n原料ガス, 精製器, 分析計, VENTライン\n'
    if full.strip() == 'SIB00104':
        for ch in list(t): t.remove(ch)
        cp = etree.SubElement(t, V + 'cp'); cp.set('IX', '0'); cp.tail = 'SIB00107\n'
legend = ('凡例：オレンジ色＝指摘事項による追加・変更（No.は「フロー改善点」シート）\n'
          'No.1  分析計前パネル→切替ヘッダー、各入口に逆止弁（H2・O2同時開放禁止）\n'
          'No.2  標準ガス容器用減圧弁の二次側に安全弁（吹出しはVENTへ）\n'
          'No.3  VENT No.2 の各接続に逆止弁\n'
          'No.4  希釈N2に流量スイッチ FIS261/262（低流量でH2遮断）\n'
          'No.5  GC-EPD キャリアガス（He・Ar）出口に逆止弁\n'
          'No.6  H2精製装置 PH2送出に逆止弁\n'
          'No.10 以前の弁計器リストのTagを記入\n'
          'No.12 予備弁・ヘッダー端末の開放端にプラグ\n'
          'No.13 重複図形（ID1075）を削除\n'
          'No.15 外部シートラベルに接続先図番を記入')
text(12.8 + 34.6, 42.0, legend, size_mm=1.3, w=69, h=24, align=0, note='凡例')
frame = line(12.0, 28.5, 82.5, 28.5, note='凡例枠'); line(82.5, 28.5, 82.5, 55.5, note='凡例枠')
line(82.5, 55.5, 12.0, 55.5, note='凡例枠'); line(12.0, 55.5, 12.0, 28.5, note='凡例枠')

# ---------- write new page part ----------
nums = [int(x) for x in re.findall(r'page(\d+)\.xml', prels)]
new_file = f'page{max(nums) + 1}.xml'
save(root, P('visio/pages', new_file))
rels_src = open(P('visio/pages/_rels', src_file + '.rels'), encoding='utf8').read()
# add relief-valve master (116) relationship if missing
mrels = open(P('visio/masters/_rels/masters.xml.rels'), encoding='utf8').read()
mroot = load(P('visio/masters/masters.xml'))
mfile = {m.get('ID'): dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', mrels))[m.find(V + 'Rel').get('{%s}id' % RNS)]
         for m in mroot.findall(V + 'Master')}
used = sorted({e.get('Master') for e in root.iter(V + 'Shape') if e.get('Master')}, key=int)
rel = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
for j, mid in enumerate(used, 1):
    rel.append(f'<Relationship Id="rId{j}" Type="http://schemas.microsoft.com/visio/2010/relationships/master" Target="../masters/{mfile[mid]}"/>')
rel.append('</Relationships>')
open(P('visio/pages/_rels', new_file + '.rels'), 'w', encoding='utf8').write(''.join(rel))
newp = copy.deepcopy(src_pg)
new_pid = str(max(int(p.get('ID')) for p in pages.findall(V + 'Page')) + 1)
newp.set('ID', new_pid); newp.set('NameU', '全体系統図（改善反映）'); newp.set('Name', '全体系統図（改善反映）')
for rb in newp.iter(V + 'RefBy'): rb.set('ID', new_pid)
rid_num = max(int(x) for x in re.findall(r'Id="rId(\d+)"', prels)) + 1
rid = f'rId{rid_num}'
newp.find(V + 'Rel').set('{%s}id' % RNS, rid)
src_pg.addnext(newp)
save(pages, P('visio/pages/pages.xml'))
prels = prels.replace('</Relationships>', f'<Relationship Id="{rid}" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="{new_file}"/></Relationships>')
open(P('visio/pages/_rels/pages.xml.rels'), 'w', encoding='utf8').write(prels)
ct = open(P('[Content_Types].xml'), encoding='utf8').read()
ct = ct.replace('</Types>', f'<Override PartName="/visio/pages/{new_file}" ContentType="application/vnd.ms-visio.page+xml"/></Types>')
open(P('[Content_Types].xml'), 'w', encoding='utf8').write(ct)

if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(P('[Content_Types].xml'), '[Content_Types].xml')
    for dp, dn, fn in os.walk(work):
        for f in sorted(fn):
            full = os.path.join(dp, f); arc = os.path.relpath(full, work)
            if arc != '[Content_Types].xml': z.write(full, arc)
import collections
cnt = collections.Counter(n.split(' ')[0] + ' ' + re.sub(r'\(.*', '', n.split(' ', 1)[1]) if ' ' in n else n for n, _ in added)
print(new_file, 'page', new_pid, 'added', len(added))
for k, v in sorted(cnt.items()): print(' ', k, v)
