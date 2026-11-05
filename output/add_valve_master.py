"""Add a valve spec master sheet and model drop-down with lookup formulas."""
import sys, copy, collections
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.comments import Comment

LIST, REF, OUT = sys.argv[1:4]
wb = openpyxl.load_workbook(LIST)
ws = wb['弁・計器リスト']
ref = openpyxl.load_workbook(REF)['弁・計器リスト']

# main-sheet column -> master column header
AUTO = [('J', '品名'), ('K', 'メーカー'), ('M', '口径'), ('N', '接続'), ('O', '主要材質'),
        ('U', '温度（℃）'), ('V', '防爆'), ('W', '防爆等級'), ('X', 'レンジ'), ('Y', '詳細仕様')]
# columns whose value depends on the use, not the model: filled in master only for instruments
PER_USE_X = {'ダイヤフラム弁', '空圧ダイヤフラム弁', '逆止弁'}

def norm(v):
    if v is None: return None
    v = str(v).strip()
    return v.replace('"', '”') if v else None

# ---- collect models from reference + current list ----
obs = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
src = collections.defaultdict(list)
for sheet, tagcol in ((ref, 'E'), (ws, 'E')):
    for r in range(3, sheet.max_row + 1):
        m = norm(sheet[f'L{r}'].value)
        if not m: continue
        src[m].append(str(sheet[f'{tagcol}{r}'].value))
        for c, _ in AUTO:
            obs[m][c][norm(sheet[f'{c}{r}'].value)] += 1

master = []
for m in sorted(obs, key=lambda k: (obs[k]['J'].most_common(1)[0][0] or '', k)):
    row = {}
    notes = []
    for c, h in AUTO:
        cnt = obs[m][c]
        vals = [(v, n) for v, n in cnt.most_common() if v]
        v = vals[0][0] if vals else None
        if c == 'X' and (row.get('J') in PER_USE_X): v = None  # range of a valve depends on the use
        row[c] = v
        if len(vals) > 1 and not (c == 'X' and v is None):
            notes.append(f'{h}: ' + ' / '.join(f'{a}（{n}件）' for a, n in vals))
    row['tags'] = ', '.join(sorted(set(t for t in src[m] if t and t != 'None' and t != '未付番')))
    row['note'] = '参考リスト内で記載が分かれていた → ' + '；'.join(notes) if notes else ''
    master.append((m, row))

# ---- master sheet ----
if '弁仕様マスタ' in wb.sheetnames: del wb['弁仕様マスタ']
ms = wb.create_sheet('弁仕様マスタ', wb.sheetnames.index('弁・計器リスト') + 1)
F = Font(name='ＭＳ Ｐ明朝', size=9); FB = Font(name='ＭＳ Ｐ明朝', size=9, bold=True)
thin = Side(style='thin'); BD = Border(left=thin, right=thin, top=thin, bottom=thin)
ms['A1'] = '弁仕様マスタ（型式ごとの仕様）'; ms['A1'].font = Font(name='ＭＳ Ｐ明朝', size=12, bold=True)
ms['A2'] = ('「弁・計器リスト」のL列（型式）をプルダウンで選ぶと、このシートの値が J・K・M・N・O・U・V・W・X・Y 列に入ります。'
            '新しい型式は表の最終行の下に追記すると、プルダウンにも自動で追加されます。黄色の列が入力欄です。')
ms['A2'].font = F; ms['A2'].alignment = Alignment(wrap_text=True, vertical='top')
ms.merge_cells('A2:M2'); ms.row_dimensions[2].height = 30
HDR = ['型式'] + [h for _, h in AUTO] + ['使用Tag（参考）', '備考']
WID = [26, 16, 10, 10, 8, 10, 10, 6, 12, 14, 44, 30, 40]
fill_in = PatternFill('solid', fgColor='FFF2CC'); fill_h = PatternFill('solid', fgColor='D9D9D9')
for i, (h, w) in enumerate(zip(HDR, WID), 1):
    c = ms.cell(3, i, h); c.font = FB; c.border = BD; c.fill = fill_h
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ms.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
for k, (m, row) in enumerate(master, 4):
    vals = [m] + [row[c] for c, _ in AUTO] + [row['tags'], row['note']]
    for i, v in enumerate(vals, 1):
        c = ms.cell(k, i, v); c.font = F; c.border = BD
        c.alignment = Alignment(vertical='top', wrap_text=True)
        if i <= 1 + len(AUTO): c.fill = fill_in
last_m = 3 + len(master)
ms.freeze_panes = 'B4'
# dynamic named range for the drop-down (grows when rows are appended)
dn = DefinedName('型式リスト', attr_text="OFFSET('弁仕様マスタ'!$A$4,0,0,COUNTA('弁仕様マスタ'!$A$4:$A$500),1)")
wb.defined_names['型式リスト'] = dn

# ---- main sheet formulas ----
MCOL = {c: openpyxl.utils.get_column_letter(i + 2) for i, (c, _) in enumerate(AUTO)}  # J->B, K->C ...
def lit(v):
    if v in (None, ''): return '""'
    if isinstance(v, (int, float)): return repr(v)
    return '"' + str(v).replace('"', '""') + '"'

data_rows = []
for r in range(3, ws.max_row + 1):
    # data rows have a value in J (品名) or H (名称); section rows only have E
    if ws[f'H{r}'].value is None and ws[f'J{r}'].value is None: continue
    data_rows.append(r)
    model = norm(ws[f'L{r}'].value)
    if model: ws[f'L{r}'] = model
    mrow = dict(master).get(model) if model else None
    diffs = []
    for c, h in AUTO:
        orig = ws[f'{c}{r}'].value
        if mrow is not None and norm(orig) and mrow[c] and norm(orig) != mrow[c] and not (c == 'Y' and str(orig).startswith('接続先')):
            diffs.append(f'{h}「{orig}」')
        rng = f"'弁仕様マスタ'!${MCOL[c]}$4:${MCOL[c]}$500"
        key = f"'弁仕様マスタ'!$A$4:$A$500"
        look = f'INDEX({rng},MATCH($L{r},{key},0))'
        fb = lit(orig)
        ws[f'{c}{r}'] = f'=IF($L{r}="",{fb},IFERROR(IF({look}="",{fb},{look}),{fb}))'
    if diffs:
        z = ws[f'Z{r}'].value or ''
        ws[f'Z{r}'] = (z + ' / ' if z else '') + '型式選択前の記載: ' + '、'.join(diffs)

# drop-down on model column
dv = DataValidation(type='list', formula1='=型式リスト', allow_blank=True, showDropDown=False)
dv.errorStyle = 'warning'
dv.errorTitle = 'マスタにない型式'
dv.error = '弁仕様マスタにない型式です。口径などは自動入力されません。先に「弁仕様マスタ」へ追加してください。'
dv.promptTitle = '型式'
dv.prompt = 'プルダウンから選ぶと、口径・接続・材質・温度などが自動で入ります。'
dv.showInputMessage = True; dv.showErrorMessage = True
ws.add_data_validation(dv)
for r in data_rows: dv.add(f'L{r}')

# mark auto columns in header
note_fill = PatternFill('solid', fgColor='E2EFDA')
for c, h in AUTO:
    ws[f'{c}1'].fill = note_fill
    ws[f'{c}1'].comment = Comment('型式（L列）を選ぶと「弁仕様マスタ」から自動入力されます（数式）。', 'list')
ws['L1'].fill = PatternFill('solid', fgColor='FFF2CC')
ws['L1'].comment = Comment('プルダウンで型式を選択してください。', 'list')

wb.save(OUT)
print('models', len(master), 'data rows', len(data_rows), 'master rows end', last_m)
for m, row in master:
    if row['note']: print(' ', m, row['note'][:120])
