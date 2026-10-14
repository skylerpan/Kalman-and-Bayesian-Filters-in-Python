#!/usr/bin/env python3
"""Extract markdown cells from the original notebooks into JSON chunks for translation.

Usage:
    python3 extract.py <repo_root> <out_dir> [--max-cells 40] [--max-words 5000]

For each notebook under <repo_root> (top-level, Supporting_Notebooks/, animations/)
writes one or more files  <out_dir>/<relpath with / -> __>.partN.json  containing
    {"notebook": "<relpath>", "part": N, "nparts": M,
     "cells": [{"i": <cell index>, "src": "<markdown source>"}, ...]}
"""
import json, os, sys, glob, argparse

def notebooks(root):
    pats = ['*.ipynb', 'Supporting_Notebooks/*.ipynb', 'animations/*.ipynb']
    out = []
    for p in pats:
        out += sorted(glob.glob(os.path.join(root, p)))
    return [os.path.relpath(f, root) for f in out]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root'); ap.add_argument('out')
    ap.add_argument('--max-cells', type=int, default=40)
    ap.add_argument('--max-words', type=int, default=5000)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    total = 0
    for rel in notebooks(a.root):
        nb = json.load(open(os.path.join(a.root, rel), encoding='utf-8'))
        cells = [{'i': i, 'src': ''.join(c['source'])}
                 for i, c in enumerate(nb['cells']) if c['cell_type'] == 'markdown']
        # chunk
        parts, cur, words = [], [], 0
        for c in cells:
            w = len(c['src'].split())
            if cur and (len(cur) >= a.max_cells or words + w > a.max_words):
                parts.append(cur); cur, words = [], 0
            cur.append(c); words += w
        if cur: parts.append(cur)
        key = rel.replace('/', '__').replace('.ipynb', '')
        for n, p in enumerate(parts, 1):
            fn = os.path.join(a.out, f'{key}.part{n}.json')
            json.dump({'notebook': rel, 'part': n, 'nparts': len(parts), 'cells': p},
                      open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            total += 1
            print(f'{fn}: {len(p)} cells, {sum(len(c["src"].split()) for c in p)} words')
    print('chunks:', total)

if __name__ == '__main__':
    main()
