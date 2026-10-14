#!/usr/bin/env python3
"""Structural check: translated notebook (or translated JSON chunk) vs. original.

Usage:
    python3 check.py nb   <repo_root> <zh_dir> [relpath ...]      # compare notebooks
    python3 check.py json <orig_json_dir> <zh_json_dir> [file ...] # compare chunks

Checks per markdown cell:
  * same number of `$$` and `$` delimiters
  * same set of link URLs  ](...)  and image / <img src> paths
  * same heading lines (count + level)
  * same number of ``` fences
  * same HTML tags
  * cell has CJK text when the original has >= 8 latin words (untranslated detector)
Checks per notebook: same cell count/types, code cells identical, nbformat valid.
Exit code 1 if any ERROR. WARNINGs (untranslated) are listed but do not fail.
"""
import json, os, sys, glob, re
import nbformat

RE_URL = re.compile(r'\]\(([^)\s]+)')
RE_IMG = re.compile(r'<img[^>]*src="([^"]+)"')
RE_HTML = re.compile(r'</?([a-zA-Z][a-zA-Z0-9]*)\b')
RE_CJK = re.compile(r'[一-鿿]')
RE_LATIN = re.compile(r'[A-Za-z]{2,}')
RE_HEAD = re.compile(r'^(#+)\s', re.M)

errors, warns = [], []

def strip_math_code(s):
    s = re.sub(r'\$\$.*?\$\$', ' ', s, flags=re.S)
    s = re.sub(r'`[^`]*`', ' ', s)
    s = re.sub(r'\$[^$]*\$', ' ', s)
    s = re.sub(r'\]\([^)]*\)', ']', s)
    return s

def cmp_md(tag, a, b):
    def dd(s): return s.count('$$')
    def sd(s): return s.count('$') - 2 * s.count('$$')
    if dd(a) != dd(b): errors.append(f'{tag}: $$ count {dd(a)} -> {dd(b)}')
    if sd(a) != sd(b): errors.append(f'{tag}: $ count {sd(a)} -> {sd(b)}')
    if a.count('```') != b.count('```'): errors.append(f'{tag}: ``` fence count differs')
    if sorted(RE_URL.findall(a)) != sorted(RE_URL.findall(b)):
        errors.append(f'{tag}: link URLs differ {RE_URL.findall(a)} -> {RE_URL.findall(b)}')
    if sorted(RE_IMG.findall(a)) != sorted(RE_IMG.findall(b)):
        errors.append(f'{tag}: <img src> differ')
    if sorted(RE_HTML.findall(a)) != sorted(RE_HTML.findall(b)):
        errors.append(f'{tag}: html tags differ {sorted(RE_HTML.findall(a))} -> {sorted(RE_HTML.findall(b))}')
    ha, hb = RE_HEAD.findall(a), RE_HEAD.findall(b)
    if ha != hb: errors.append(f'{tag}: headings differ {ha} -> {hb}')
    plain = strip_math_code(a)
    if len(RE_LATIN.findall(plain)) >= 8 and not RE_CJK.search(b):
        warns.append(f'{tag}: looks untranslated')
    if a.strip() and not b.strip():
        errors.append(f'{tag}: translated cell is empty')

def check_nb(root, zh, rel):
    o = nbformat.read(os.path.join(root, rel), as_version=4)
    t_path = os.path.join(zh, rel)
    if not os.path.exists(t_path):
        errors.append(f'{rel}: missing translated notebook'); return
    t = nbformat.read(t_path, as_version=4)
    try:
        nbformat.validate(t)
    except Exception as e:
        errors.append(f'{rel}: nbformat invalid: {e}')
    if len(o.cells) != len(t.cells):
        errors.append(f'{rel}: cell count {len(o.cells)} -> {len(t.cells)}'); return
    for i, (a, b) in enumerate(zip(o.cells, t.cells)):
        tag = f'{rel}[{i}]'
        if a.cell_type != b.cell_type:
            errors.append(f'{tag}: cell type differs'); continue
        if a.cell_type != 'markdown':
            if a != b: errors.append(f'{tag}: non-markdown cell modified')
            continue
        cmp_md(tag, a.source, b.source)
    if o.metadata != t.metadata:
        errors.append(f'{rel}: notebook metadata differs')

def check_json(odir, tdir, names):
    for fn in names:
        o = json.load(open(os.path.join(odir, fn), encoding='utf-8'))
        tp = os.path.join(tdir, fn)
        if not os.path.exists(tp):
            errors.append(f'{fn}: missing'); continue
        try:
            t = json.load(open(tp, encoding='utf-8'))
        except Exception as e:
            errors.append(f'{fn}: bad json: {e}'); continue
        oi = [c['i'] for c in o['cells']]; ti = [c['i'] for c in t.get('cells', [])]
        if oi != ti:
            errors.append(f'{fn}: cell index list differs {oi} -> {ti}'); continue
        for a, b in zip(o['cells'], t['cells']):
            cmp_md(f'{fn}[{a["i"]}]', a['src'], b['src'])

def main():
    mode, x, y = sys.argv[1:4]
    rest = sys.argv[4:]
    if mode == 'nb':
        rels = rest or [os.path.relpath(f, y) for p in ['*.ipynb', 'Supporting_Notebooks/*.ipynb', 'animations/*.ipynb']
                        for f in sorted(glob.glob(os.path.join(y, p)))]
        for rel in rels: check_nb(x, y, rel)
    else:
        names = rest or sorted(os.path.basename(f) for f in glob.glob(os.path.join(y, '*.json')))
        check_json(x, y, names)
    for w in warns: print('WARN ', w)
    for e in errors: print('ERROR', e)
    print(f'{len(errors)} errors, {len(warns)} warnings')
    sys.exit(1 if errors else 0)

if __name__ == '__main__':
    main()
