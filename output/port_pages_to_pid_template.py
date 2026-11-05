"""Port pages from an old .vsdx into the P&ID template .vsdx.

- Old pages are drawn at 1:20 (mm). Template pages are 1:1 A3 with a background
  page (frame + title block). Every length cell is rescaled into page inches and
  the drawing is placed inside the free area above the title block.
- Masters are remapped to the template's identical masters (same UniqueID);
  masters missing from the template are imported.
"""
import sys, re, copy, math, zipfile, shutil, os, json
from lxml import etree

NS = 'http://schemas.microsoft.com/office/visio/2012/main'
RNS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
V = '{%s}' % NS
MM = 1 / 25.4

OLD, TPL, OUT, CFG = sys.argv[1:5]
cfg = json.load(open(CFG, encoding='utf8'))
work = OUT + '.d'
if os.path.exists(work): shutil.rmtree(work)
zipfile.ZipFile(TPL).extractall(work)
oldz = zipfile.ZipFile(OLD)
def oread(p): return oldz.read(p)

parser = etree.XMLParser(remove_blank_text=False)
def parse_bytes(b): return etree.fromstring(b, parser)
def parse_file(p): return etree.parse(p, parser).getroot()
def write(root, p):
    etree.ElementTree(root).write(p, xml_declaration=True, encoding='utf-8', standalone=None)

# ---------------- masters ----------------
def master_index(root, rels):
    out = {}
    for m in root.findall(V + 'Master'):
        rid = m.find(V + 'Rel').get('{%s}id' % RNS)
        out[m.get('ID')] = dict(el=m, uid=m.get('UniqueID'), name=m.get('NameU'), file=rels[rid], rid=rid)
    return out
def rels_of(xml):
    return dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', xml))

old_mroot = parse_bytes(oread('visio/masters/masters.xml'))
old_mrels = rels_of(oread('visio/masters/_rels/masters.xml.rels').decode())
old_m = master_index(old_mroot, old_mrels)
new_mpath = f'{work}/visio/masters/masters.xml'
new_mroot = parse_file(new_mpath)
new_mrels_path = f'{work}/visio/masters/_rels/masters.xml.rels'
new_mrels_xml = open(new_mrels_path, encoding='utf8').read()
new_m = master_index(new_mroot, rels_of(new_mrels_xml))
ct_path = f'{work}/[Content_Types].xml'
ct_xml = open(ct_path, encoding='utf8').read()

# style map by name
def styles(xml):
    return {m.group(1): re.search(r"NameU='([^']*)'", m.group(2)).group(1)
            for m in re.finditer(r"<StyleSheet ID='(\d+)'([^>]*)>", xml)}
old_st = styles(oread('visio/document.xml').decode('utf8'))
new_st = styles(open(f'{work}/visio/document.xml', encoding='utf8').read())
new_st_by_name = {v: k for k, v in new_st.items()}
style_map = {}
for k, n in old_st.items():
    if n in new_st_by_name: style_map[k] = new_st_by_name[n]
def map_styles(el):
    for e in el.iter():
        for a in ('LineStyle', 'FillStyle', 'TextStyle'):
            v = e.get(a)
            if v is not None:
                if v not in style_map: raise SystemExit(f'style {v} ({old_st.get(v)}) not in template')
                e.set(a, style_map[v])

master_map = {}
next_mid = max(int(k) for k in new_m) + 1
next_mfile = max(int(re.search(r'(\d+)', v['file']).group(1)) for v in new_m.values()) + 1
next_rid = max(int(x) for x in re.findall(r'Id="rId(\d+)"', new_mrels_xml)) + 1
imported = []
def map_master(old_id):
    global next_mid, next_mfile, next_rid, new_mrels_xml, ct_xml
    if old_id in master_map: return master_map[old_id]
    o = old_m[old_id]
    hit = [k for k, v in new_m.items() if v['uid'] == o['uid']]
    if hit:
        master_map[old_id] = hit[0]; return hit[0]
    # import
    nid, fname, rid = str(next_mid), f'master{next_mfile}.xml', f'rId{next_rid}'
    next_mid += 1; next_mfile += 1; next_rid += 1
    body = parse_bytes(oread('visio/masters/' + o['file']))
    map_styles(body)
    write(body, f'{work}/visio/masters/{fname}')
    el = copy.deepcopy(o['el']); el.set('ID', nid)
    el.find(V + 'Rel').set('{%s}id' % RNS, rid)
    map_styles(el)
    new_mroot.append(el)
    new_mrels_xml = new_mrels_xml.replace('</Relationships>',
        f'<Relationship Id="{rid}" Type="http://schemas.microsoft.com/visio/2010/relationships/master" Target="{fname}"/></Relationships>')
    ct_xml = ct_xml.replace('</Types>', f'<Override PartName="/visio/masters/{fname}" ContentType="application/vnd.ms-visio.master+xml"/></Types>')
    new_m[nid] = dict(el=el, uid=o['uid'], name=o['name'], file=fname, rid=rid)
    master_map[old_id] = nid; imported.append((o['name'], nid))
    return nid

# ---------------- geometry scaling ----------------
XFORM = {'PinX', 'PinY', 'Width', 'Height', 'LocPinX', 'LocPinY', 'BeginX', 'BeginY', 'EndX', 'EndY',
         'TxtPinX', 'TxtPinY', 'TxtWidth', 'TxtHeight', 'TxtLocPinX', 'TxtLocPinY'}
GEOM = {  # row type -> cells that are lengths
    'MoveTo': 'XY', 'LineTo': 'XY', 'ArcTo': 'XYA', 'EllipticalArcTo': 'XYAB', 'Ellipse': 'XYABCD',
    'NURBSTo': 'XY', 'PolylineTo': 'XY', 'SplineStart': 'XY', 'SplineKnot': 'XY', 'InfiniteLine': 'XYAB',
}
CONST_F = re.compile(r'^\s*-?[\d.]+(\s*(mm|cm|m|in|pt|ft|"|\'))?\s*$', re.I)

def fmt(x): return repr(float(x))

def scale_cell(c, k):
    v = c.get('V')
    if v in (None, '', 'Themed'): return
    try: c.set('V', fmt(float(v) * k))
    except ValueError: return
    f = c.get('F')
    if f is not None and CONST_F.match(f): del c.attrib['F']

def scale_fn_string(c, k, kind):
    # NURBS(knotLast, degree, xType, yType, x1,y1,k1,w1, ...) / POLYLINE(xType, yType, x1,y1, ...)
    v = c.get('V')
    m = re.match(r'(\w+)\((.*)\)$', v or '')
    if not m: return
    a = [x.strip() for x in m.group(2).split(',')]
    if kind == 'NURBS':
        xt, yt = a[2], a[3]; i0, step = 4, 4
    else:
        xt, yt = a[0], a[1]; i0, step = 2, 2
    for i in range(i0, len(a), step):
        # type 0 = fraction of Width/Height (leave), type 1 = local coordinates (scale)
        if xt == '1': a[i] = fmt(float(a[i]) * k)
        if yt == '1': a[i + 1] = fmt(float(a[i + 1]) * k)
    c.set('V', f'{m.group(1)}({",".join(a)})')
    if c.get('F') and c.get('F') != 'Inh': del c.attrib['F']

FONT_K = 1.0
def scale_shape(s, k, dx=0.0, dy=0.0):
    if FONT_K != 1.0:
        for sec in s.findall(V + 'Section'):
            if sec.get('N') == 'Character':
                for c in sec.iter(V + 'Cell'):
                    if c.get('N') == 'Size':
                        scale_cell(c, FONT_K)
                        if c.get('F') == 'Inh': del c.attrib['F']
    for c in s.findall(V + 'Cell'):
        n = c.get('N')
        if n in XFORM:
            scale_cell(c, k)
            if n in ('PinX', 'BeginX', 'EndX') and dx: c.set('V', fmt(float(c.get('V')) + dx))
            if n in ('PinY', 'BeginY', 'EndY') and dy: c.set('V', fmt(float(c.get('V')) + dy))
    for sec in s.findall(V + 'Section'):
        sn = sec.get('N')
        for row in sec.findall(V + 'Row'):
            if sn == 'Geometry':
                t = row.get('T'); cells = GEOM.get(t, '')
                for c in row.findall(V + 'Cell'):
                    n = c.get('N')
                    if n in cells: scale_cell(c, k)
                    elif n == 'E' and t == 'NURBSTo': scale_fn_string(c, k, 'NURBS')
                    elif n == 'A' and t == 'PolylineTo': scale_fn_string(c, k, 'POLYLINE')
            elif sn in ('Connection', 'Control'):
                for c in row.findall(V + 'Cell'):
                    if c.get('N') in ('X', 'Y', 'XDyn', 'YDyn'): scale_cell(c, k)
            elif sn in ('User', 'Property'):
                for c in row.findall(V + 'Cell'):
                    if c.get('N') == 'Value' and c.get('U') == 'DL': scale_cell(c, k)
    sh = s.find(V + 'Shapes')
    if sh is not None:
        for ch in sh.findall(V + 'Shape'): scale_shape(ch, k)

def cv(s, n, d=None):
    for c in s.findall(V + 'Cell'):
        if c.get('N') == n:
            try: return float(c.get('V'))
            except (TypeError, ValueError): return d
    return d

def bbox(shapes):
    xs, ys = [], []
    for s in shapes:
        if cv(s, 'BeginX') is not None and cv(s, 'EndX') is not None:
            xs += [cv(s, 'BeginX'), cv(s, 'EndX')]; ys += [cv(s, 'BeginY'), cv(s, 'EndY')]
            continue
        x, y, w, h = cv(s, 'PinX'), cv(s, 'PinY'), cv(s, 'Width', 0), cv(s, 'Height', 0)
        if x is None or y is None: continue
        a = cv(s, 'Angle', 0) or 0
        lx, ly = cv(s, 'LocPinX', w / 2), cv(s, 'LocPinY', h / 2)
        for px, py in ((0, 0), (w, 0), (0, h), (w, h)):
            ux, uy = px - lx, py - ly
            xs.append(x + ux * math.cos(a) - uy * math.sin(a)); ys.append(y + ux * math.sin(a) + uy * math.cos(a))
    return min(xs), min(ys), max(xs), max(ys)

# ---------------- pages ----------------
pages_path = f'{work}/visio/pages/pages.xml'
pages_root = parse_file(pages_path)
prels_path = f'{work}/visio/pages/_rels/pages.xml.rels'
prels_xml = open(prels_path, encoding='utf8').read()
old_pages = parse_bytes(oread('visio/pages/pages.xml'))
old_prels = rels_of(oread('visio/pages/_rels/pages.xml.rels').decode())
template_page = [p for p in pages_root.findall(V + 'Page') if p.get('ID') == cfg['template_page_id']][0]
tpl_title_page = cfg['title_from_page']  # page file with title texts to clone

next_pid = max(int(p.get('ID')) for p in pages_root.findall(V + 'Page')) + 1
next_pfile = max(int(x) for x in re.findall(r'page(\d+)\.xml', prels_xml)) + 1
next_prid = max(int(x) for x in re.findall(r'Id="rId(\d+)"', prels_xml)) + 1
area = cfg['area_mm']  # [x0,y0,x1,y1]
ax0, ay0, ax1, ay1 = [v * MM for v in area]
report = []

title_src = parse_file(f'{work}/visio/pages/{tpl_title_page}')
def title_shape(sid, text):
    for s in title_src.find(V + 'Shapes').findall(V + 'Shape'):
        if s.get('ID') == sid:
            n = copy.deepcopy(s); t = n.find(V + 'Text')
            for ch in list(t): t.remove(ch)
            cp = etree.SubElement(t, V + 'cp'); cp.set('IX', '0')
            t.text = None; cp.tail = text + '\n'
            return n
    raise SystemExit('title shape not found')

for spec in cfg['pages']:
    global_font = None
    op = [p for p in old_pages.findall(V + 'Page') if p.get('ID') == spec['old_page_id']][0]
    orid = op.find(V + 'Rel').get('{%s}id' % RNS)
    ofile = old_prels[orid]
    proot = parse_bytes(oread('visio/pages/' + ofile))
    shapes_el = proot.find(V + 'Shapes')
    tops = shapes_el.findall(V + 'Shape')
    # drop excluded shapes
    drop = set(spec.get('drop_ids', []))
    if spec.get('drop_ids_file'): drop |= set(json.load(open(spec['drop_ids_file'])))
    for s in tops:
        if s.get('ID') in drop: shapes_el.remove(s)
    cs = proot.find(V + 'Connects')
    if cs is not None:
        for c in list(cs):
            if c.get('FromSheet') in drop or c.get('ToSheet') in drop: cs.remove(c)
    tops = shapes_el.findall(V + 'Shape')
    bx0, by0, bx1, by1 = bbox(tops)
    old_scale = cv(op.find(V + 'PageSheet'), 'DrawingScale') / cv(op.find(V + 'PageSheet'), 'PageScale')
    k = min((ax1 - ax0) / (bx1 - bx0), (ay1 - ay0) / (by1 - by0), 1.0 / old_scale * spec.get('max_paper_scale', 1.0))
    # centre in area
    dx = (ax0 + ax1) / 2 - (bx0 + bx1) / 2 * k
    dy = (ay0 + ay1) / 2 - (by0 + by1) / 2 * k
    FONT_K = min(1.0, k * old_scale) if spec.get('scale_font', True) else 1.0
    for s in tops: scale_shape(s, k, dx, dy)
    # masters & styles
    for e in proot.iter(V + 'Shape'):
        if e.get('Master'): e.set('Master', map_master(e.get('Master')))
    map_styles(proot)
    # title texts
    sid_max = max(int(e.get('ID')) for e in proot.iter(V + 'Shape'))
    for i, (src_id, text) in enumerate(spec['titles']):
        t = title_shape(src_id, text); t.set('ID', str(sid_max + 1 + i)); shapes_el.append(t)
    nb = bbox(shapes_el.findall(V + 'Shape')[:len(tops)])
    report.append(dict(page=spec['name'], k_paper=k * old_scale, bbox_mm=[round(v / MM, 1) for v in nb]))
    # write page part
    pfile = f'page{next_pfile}.xml'; next_pfile += 1
    write(proot, f'{work}/visio/pages/{pfile}')
    used = sorted({e.get('Master') for e in proot.iter(V + 'Shape') if e.get('Master')}, key=int)
    rel = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for j, mid in enumerate(used, 1):
        rel.append(f'<Relationship Id="rId{j}" Type="http://schemas.microsoft.com/visio/2010/relationships/master" Target="../masters/{new_m[mid]["file"]}"/>')
    rel.append('</Relationships>')
    open(f'{work}/visio/pages/_rels/{pfile}.rels', 'w', encoding='utf8').write(''.join(rel))
    # pages.xml entry
    np_ = copy.deepcopy(template_page)
    np_.set('ID', str(next_pid)); next_pid += 1
    np_.set('NameU', spec['name']); np_.set('Name', spec['name']); np_.set('IsCustomNameU', '1'); np_.set('IsCustomName', '1')
    np_.set('ViewScale', '-1'); np_.set('ViewCenterX', '8.2677165354331'); np_.set('ViewCenterY', '5.8464566929134')
    for rb in np_.iter(V + 'RefBy'): rb.set('ID', np_.get('ID'))
    ps = np_.find(V + 'PageSheet')
    for sec in ps.findall(V + 'Section'):
        if sec.get('N') == 'Layer': ps.remove(sec)
    olayer = [s for s in op.find(V + 'PageSheet').findall(V + 'Section') if s.get('N') == 'Layer']
    if olayer: ps.append(copy.deepcopy(olayer[0]))
    rid = f'rId{next_prid}'; next_prid += 1
    np_.find(V + 'Rel').set('{%s}id' % RNS, rid)
    pages_root.append(np_)
    prels_xml = prels_xml.replace('</Relationships>',
        f'<Relationship Id="{rid}" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="{pfile}"/></Relationships>')
    ct_xml = ct_xml.replace('</Types>', f'<Override PartName="/visio/pages/{pfile}" ContentType="application/vnd.ms-visio.page+xml"/></Types>')

write(pages_root, pages_path)
write(new_mroot, new_mpath)
open(prels_path, 'w', encoding='utf8').write(prels_xml)
open(new_mrels_path, 'w', encoding='utf8').write(new_mrels_xml)
open(ct_path, 'w', encoding='utf8').write(ct_xml)

# zip ([Content_Types].xml first)
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(ct_path, '[Content_Types].xml')
    for dp, dn, fn in os.walk(work):
        for f in sorted(fn):
            full = os.path.join(dp, f); arc = os.path.relpath(full, work)
            if arc != '[Content_Types].xml': z.write(full, arc)
print(json.dumps(dict(report=report, imported=imported, master_map=master_map), ensure_ascii=False, indent=1))
