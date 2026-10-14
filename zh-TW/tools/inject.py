#!/usr/bin/env python3
"""Rebuild notebooks with translated markdown cells.

Usage:
    python3 inject.py <repo_root> <zh_dir> <translated_json_dir> [notebook_relpath ...]

Reads every <translated_json_dir>/<key>.partN.json (same schema as extract.py output),
replaces the markdown `source` of the listed cell indices in the original notebook
and writes the result to <zh_dir>/<relpath>.  Code cells, outputs and metadata are
left byte-for-byte unchanged.  A notebook is only written when ALL its parts exist.
"""
import json, os, sys, glob, collections
import nbformat

def main():
    root, zh, tdir = sys.argv[1:4]
    only = set(sys.argv[4:])
    parts = collections.defaultdict(dict)
    for fn in sorted(glob.glob(os.path.join(tdir, '*.part*.json'))):
        d = json.load(open(fn, encoding='utf-8'))
        parts[d['notebook']][d['part']] = d
    for rel, ps in sorted(parts.items()):
        if only and rel not in only:
            continue
        nparts = next(iter(ps.values()))['nparts']
        missing = [n for n in range(1, nparts + 1) if n not in ps]
        if missing:
            print(f'SKIP {rel}: missing parts {missing}')
            continue
        nb = nbformat.read(os.path.join(root, rel), as_version=4)
        n = 0
        for p in ps.values():
            for c in p['cells']:
                cell = nb.cells[c['i']]
                assert cell.cell_type == 'markdown', (rel, c['i'])
                cell.source = c['src']
                n += 1
        out = os.path.join(zh, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        nbformat.write(nb, out)
        print(f'WROTE {out} ({n} markdown cells)')

if __name__ == '__main__':
    main()
