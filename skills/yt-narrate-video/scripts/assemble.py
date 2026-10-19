#!/usr/bin/env python3
"""Check a finished narrated page. Standard library only.

Usage: python3 assemble.py page.html
Fails (exit 1) on a leftover {{token}}, a bad <img> src or SVG <image> href (empty, remote, or a missing local file),
a remote srcset URL on <img> or <source>, a leftover data-sample attribute (sample art),
a duplicate id, or an em-dash in visible text. Otherwise prints '<path>: ok, <size> MB' and exits 0.
"""
import argparse, os, re, sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

DASH = chr(0x2014)
HIDDEN = {'script', 'style', 'noscript', 'template'}
REMOTE = ('http:', 'https:', '//')

class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden, self.srcs, self.dashes = 0, [], []
        self.samples, self.ids, self.srcsets = [], {}, []

    def handle_starttag(self, tag, attrs):
        if tag in HIDDEN: self.hidden += 1
        at, line = dict(attrs), self.getpos()[0]
        if tag == 'img': self.srcs.append(at.get('src'))
        if tag == 'image': self.srcs.append(at.get('href') or at.get('xlink:href'))
        if tag in ('img', 'source') and at.get('srcset'): self.srcsets.append(at['srcset'])
        if 'data-sample' in at: self.samples.append(f'line {line}: <{tag}> has data-sample')
        if at.get('id'): self.ids.setdefault(at['id'], []).append(line)

    def handle_endtag(self, tag):
        if tag in HIDDEN and self.hidden: self.hidden -= 1

    def handle_data(self, data):
        i = data.find(DASH)
        if self.hidden or i < 0: return
        line = self.getpos()[0] + data[:i].count('\n')
        self.dashes.append(f'line {line}: ...{data[max(0, i - 20):i + 20].strip()}...'.replace('\n', ' '))

def img_problem(src, base):
    if src is None or not src.strip(): return 'img with no src'
    src = src.strip()
    if src.lower().startswith(REMOTE): return f'remote img src: {src[:60]}'
    if src.lower().startswith('data:') or src.startswith('#'): return None
    rel = unquote(urlsplit(src).path)
    if os.path.isabs(rel): return f'absolute img path: {src[:60]}'
    if not rel or not os.path.isfile(os.path.join(base, rel)): return f'missing img file: {src[:60]}'
    return None

def srcset_problems(value):
    urls = [c.split()[0] for c in value.split(',') if c.strip()]
    return [f'remote srcset URL: {u[:60]}' for u in urls if u.lower().startswith(REMOTE)]

ap = argparse.ArgumentParser()
ap.add_argument('page')
a = ap.parse_args()

html = open(a.page, encoding='utf-8').read()
scan = Scan()
scan.feed(html); scan.close()
base = os.path.dirname(os.path.abspath(a.page))
found = {
    'UNFILLED tokens': sorted(set(re.findall(r'\{\{[^{}]*\}\}', html))),
    'BAD images': [p for p in (img_problem(s, base) for s in scan.srcs) if p],
    'BAD srcset': [p for v in scan.srcsets for p in srcset_problems(v)],
    'SAMPLE art left': scan.samples,
    'DUPLICATE ids': [f'{k}: lines {", ".join(map(str, v))}' for k, v in scan.ids.items() if len(v) > 1],
    'EM-DASH in visible text': scan.dashes,
}
bad = False
for kind, items in found.items():
    if items:
        bad = True
        print(f'{kind} ({len(items)}):')
        for item in items: print('  ' + item)
if bad: sys.exit(1)
print(f'{a.page}: ok, {os.path.getsize(a.page) / 1e6:.2f} MB')
