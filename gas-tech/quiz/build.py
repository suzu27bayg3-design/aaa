"""Build quiz.html from koatsu-koukikai/law-set-*.md.

Usage: python3 gas-tech/quiz/build.py
"""
import glob
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SETS_DIR = os.path.join(HERE, '..', 'koatsu-koukikai')
REPO_URL = 'https://github.com/suzu27bayg3-design/aaa/blob/ccr-f6cae4a9-q43ilw/gas-tech/koatsu-koukikai/'


def inline_md(text):
    """Escape text and convert the inline markdown used in the notes (links, bold)."""
    out = html.escape(text, quote=False)
    out = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)',
                 lambda m: '<a href="%s" target="_blank" rel="noopener">%s</a>' % (html.escape(m.group(2)), m.group(1)),
                 out)
    out = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', out)
    return out


def block_md(text):
    """Convert an explanation body: '- ' lines become a list, other lines paragraphs."""
    parts, items = [], []
    for line in text.strip().splitlines():
        line = line.strip()
        if line.startswith('- '):
            items.append('<li>%s</li>' % inline_md(line[2:]))
            continue
        if items:
            parts.append('<ul>%s</ul>' % ''.join(items))
            items = []
        if line:
            parts.append('<p>%s</p>' % inline_md(line))
    if items:
        parts.append('<ul>%s</ul>' % ''.join(items))
    return ''.join(parts)


def parse_set(path):
    src = open(path, encoding='utf-8').read()
    num = re.search(r'law-set-(\d+)\.md$', path).group(1)
    title = src.splitlines()[0].lstrip('# ').strip()
    m = re.search(r'第 \d+ 回\s*(.*)$', title)
    topic = m.group(1).strip() if m and m.group(1).strip() else '総論'

    questions = {}
    for qm in re.finditer(r'^### 問 (\d+)（(.+?)）\n(.*?)(?=^### |^---)', src, re.S | re.M):
        qn, qtopic, body = int(qm.group(1)), qm.group(2), qm.group(3)
        stmts = re.findall(r'^([イロハ])．(.+)$', body, re.M)
        choice_line = re.search(r'^\(1\).*$', body, re.M).group(0)
        choices = [c.strip() for c in re.split(r'\(\d\)', choice_line) if c.strip()]
        questions[qn] = {'n': qn, 'topic': qtopic,
                         'stmts': [[k, inline_md(v)] for k, v in stmts],
                         'choices': choices}

    for am in re.finditer(r'<details><summary>問 (\d+) → \((\d)\)[^<]*</summary>(.*?)</details>', src, re.S):
        qn = int(am.group(1))
        questions[qn]['answer'] = int(am.group(2))
        questions[qn]['explain'] = block_md(am.group(3))

    qs = [questions[k] for k in sorted(questions)]
    for q in qs:
        assert len(q['stmts']) == 3 and len(q['choices']) == 5 and 'answer' in q, (path, q['n'])
    return {'id': num, 'topic': topic, 'url': REPO_URL + os.path.basename(path), 'questions': qs}


def main():
    sets = [parse_set(p) for p in sorted(glob.glob(os.path.join(SETS_DIR, 'law-set-*.md')))]
    template = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    data = json.dumps(sets, ensure_ascii=False).replace('</', '<\\/')
    out = template.replace('/*QUIZ_DATA*/[]', data)
    with open(os.path.join(HERE, 'quiz.html'), 'w', encoding='utf-8') as f:
        f.write(out)
    print('sets:', len(sets), 'questions:', sum(len(s['questions']) for s in sets))


if __name__ == '__main__':
    main()
