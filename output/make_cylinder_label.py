"""Add a cylinder spec table (ガス種/容器サイズ/口金サイズ/系列 + number balloon) as one group shape.

Values live in the group's Shape Data (Prop.*); each value cell shows them through a text field,
so editing Shape Data updates the table.
usage: make_cyl_label.py IN.vsdx OUT.vsdx PAGE_FILE X_mm Y_mm(center)
"""
import sys, os, re, zipfile, shutil
from lxml import etree

SRC, OUT, PAGE, CX, CY = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
V = '{http://schemas.microsoft.com/office/visio/2012/main}'
IN = 1 / 25.4
work = OUT + '.d'
if os.path.exists(work): shutil.rmtree(work)
zipfile.ZipFile(SRC).extractall(work)
pp = os.path.join(work, 'visio/pages', PAGE)
root = etree.parse(pp).getroot()
shapes = root.find(V + 'Shapes')
nid = [max(int(e.get('ID')) for e in root.iter(V + 'Shape')) + 1]

ROWS = [('GasType', 'ガス種', 'H2'), ('CylSize', '容器サイズ', '47L'),
        ('Outlet', '口金サイズ', 'W22/14左'), ('Series', '系列', 'B系列')]
C1, C2, RH = 11.0, 15.0, 3.6          # column widths / row height (mm)
W, H = C1 + C2, RH * len(ROWS)
BAL = 4.4                              # balloon diameter
FONT = 1.7                             # mm

def cells(el, items):
    for n, v, *rest in items:
        c = etree.SubElement(el, V + 'Cell'); c.set('N', n); c.set('V', str(v))
        if rest and rest[0]: c.set('F', rest[0])
        if len(rest) > 1 and rest[1]: c.set('U', rest[1])

def geom_rect(el, w, h, nofill=True, noline=False):
    g = etree.SubElement(el, V + 'Section'); g.set('N', 'Geometry'); g.set('IX', '0')
    cells(g, [('NoFill', 1 if nofill else 0), ('NoLine', 1 if noline else 0)])
    for ix, (t, x, y) in enumerate((('MoveTo', 0, 0), ('LineTo', w, 0), ('LineTo', w, h), ('LineTo', 0, h), ('LineTo', 0, 0)), 1):
        r = etree.SubElement(g, V + 'Row'); r.set('T', t); r.set('IX', str(ix)); cells(r, [('X', x), ('Y', y)])

def char(el, size=FONT):
    ch = etree.SubElement(el, V + 'Section'); ch.set('N', 'Character')
    r = etree.SubElement(ch, V + 'Row'); r.set('IX', '0')
    cells(r, [('Font', 'MS Gothic'), ('Color', '#000000'), ('Size', size * IN, None, 'PT'), ('AsianFont', 'MS Gothic')])

def child(parent_shapes, x, y, w, h, name):
    s = etree.SubElement(parent_shapes, V + 'Shape')
    s.set('ID', str(nid[0])); nid[0] += 1; s.set('Type', 'Shape'); s.set('NameU', name); s.set('Name', name)
    s.set('LineStyle', '3'); s.set('FillStyle', '3'); s.set('TextStyle', '3')
    cells(s, [('PinX', x * IN), ('PinY', y * IN), ('Width', w * IN), ('Height', h * IN),
              ('LocPinX', w * IN / 2, 'Width*0.5'), ('LocPinY', h * IN / 2, 'Height*0.5'),
              ('LeftMargin', 0.6 * IN), ('RightMargin', 0.3 * IN), ('TopMargin', 0), ('BottomMargin', 0),
              ('LineWeight', 0.5 / 72), ('LineColor', '#000000')])
    return s

# ---- group ----
g = etree.SubElement(shapes, V + 'Shape')
gid = nid[0]; nid[0] += 1
g.set('ID', str(gid)); g.set('Type', 'Group'); g.set('NameU', '容器仕様表'); g.set('Name', '容器仕様表')
g.set('LineStyle', '3'); g.set('FillStyle', '3'); g.set('TextStyle', '3')
cells(g, [('PinX', CX * IN), ('PinY', CY * IN), ('Width', W * IN), ('Height', H * IN),
          ('LocPinX', W * IN / 2, 'Width*0.5'), ('LocPinY', H * IN / 2, 'Height*0.5'), ('Angle', 0)])
prop = etree.SubElement(g, V + 'Section'); prop.set('N', 'Property')
for key, label, val in [('No', '番号', '')] + ROWS:
    r = etree.SubElement(prop, V + 'Row'); r.set('N', key)
    cells(r, [('Value', val, None, 'STR'), ('Prompt', ''), ('Label', label), ('Format', ''), ('Type', 0)])
gs = etree.SubElement(g, V + 'Shapes')

# value / label cells
for i, (key, label, val) in enumerate(ROWS):
    yc = H - RH * (i + 0.5)
    lab = child(gs, C1 / 2, yc, C1, RH, f'項目_{key}')
    geom_rect(lab, C1 * IN, RH * IN)
    char(lab)
    pa = etree.SubElement(lab, V + 'Section'); pa.set('N', 'Paragraph')
    r = etree.SubElement(pa, V + 'Row'); r.set('IX', '0'); cells(r, [('HorzAlign', 0)])
    t = etree.SubElement(lab, V + 'Text'); cp = etree.SubElement(t, V + 'cp'); cp.set('IX', '0'); cp.tail = label

    v = child(gs, C1 + C2 / 2, yc, C2, RH, f'値_{key}')
    geom_rect(v, C2 * IN, RH * IN)
    char(v)
    pa = etree.SubElement(v, V + 'Section'); pa.set('N', 'Paragraph')
    r = etree.SubElement(pa, V + 'Row'); r.set('IX', '0'); cells(r, [('HorzAlign', 1)])
    fs = etree.SubElement(v, V + 'Section'); fs.set('N', 'Field')
    r = etree.SubElement(fs, V + 'Row'); r.set('IX', '0')
    cells(r, [('Value', val, f'Sheet.{gid}!Prop.{key}', 'STR'), ('Format', '', 'FIELDPICTURE(0)'), ('Type', 0)])
    t = etree.SubElement(v, V + 'Text'); cp = etree.SubElement(t, V + 'cp'); cp.set('IX', '0')
    f = etree.SubElement(t, V + 'fld'); f.set('IX', '0'); f.text = val

# number balloon on the top-left corner (white fill, drawn on top)
b = child(gs, 0.2, H + 1.6, BAL, BAL, '番号')
for c in b.findall(V + 'Cell'):
    if c.get('N') in ('LeftMargin', 'RightMargin'): c.set('V', '0')
cells(b, [('FillForegnd', '#FFFFFF'), ('FillPattern', 1)])
char(b, 1.6)
fs = etree.SubElement(b, V + 'Section'); fs.set('N', 'Field')
r = etree.SubElement(fs, V + 'Row'); r.set('IX', '0')
cells(r, [('Value', '', f'Sheet.{gid}!Prop.No', 'STR'), ('Format', '', 'FIELDPICTURE(0)'), ('Type', 0)])
gg = etree.SubElement(b, V + 'Section'); gg.set('N', 'Geometry'); gg.set('IX', '0')
r = etree.SubElement(gg, V + 'Row'); r.set('T', 'Ellipse'); r.set('IX', '1')
w = BAL * IN
cells(r, [('X', w / 2), ('Y', w / 2), ('A', w), ('B', w / 2), ('C', w / 2), ('D', w)])
t = etree.SubElement(b, V + 'Text'); cp = etree.SubElement(t, V + 'cp'); cp.set('IX', '0')
f = etree.SubElement(t, V + 'fld'); f.set('IX', '0'); f.text = ''

etree.ElementTree(root).write(pp, xml_declaration=True, encoding='utf-8')
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(work, '[Content_Types].xml'), '[Content_Types].xml')
    for dp, dn, fn in os.walk(work):
        for fname in sorted(fn):
            full = os.path.join(dp, fname); arc = os.path.relpath(full, work)
            if arc != '[Content_Types].xml': z.write(full, arc)
print('group id', gid)
