#!/usr/bin/env python3
"""Inline images into the page and downscale them for the web.

Usage: python3 assemble.py page.html images_dir out.html [--width 1100] [--hero-width 1400] [--quality 76]
Every {{IMG:name}} in page.html becomes a base64 data URI of images_dir/name.jpg (or .png).
Fails if an image is missing or a {{PLACEHOLDER}} is left unfilled.
"""
import argparse, base64, os, re, sys
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('page'); ap.add_argument('images'); ap.add_argument('out')
ap.add_argument('--width', type=int, default=1100)
ap.add_argument('--hero-width', type=int, default=1400)
ap.add_argument('--quality', type=int, default=76)
a = ap.parse_args()

html = open(a.page, encoding='utf-8').read()
missing = []

def uri(m):
    name = m.group(1)
    for ext in ('.jpg', '.jpeg', '.png'):
        path = os.path.join(a.images, name + ext)
        if os.path.exists(path):
            break
    else:
        missing.append(name); return m.group(0)
    im = cv2.imread(path)
    w = a.hero_width if name == 'hero' else a.width
    if im.shape[1] > w:
        im = cv2.resize(im, (w, int(im.shape[0] * w / im.shape[1])), interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode('.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, a.quality, cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.tobytes()).decode()

html = re.sub(r'\{\{IMG:([\w-]+)\}\}', uri, html)
left = re.findall(r'\{\{(?:[A-Z0-9_]+|IMG:[^{}]*)\}\}', html)
if missing: print('MISSING images:', ', '.join(missing)); sys.exit(1)
if left: print('UNFILLED placeholders:', ', '.join(sorted(set(left)))); sys.exit(1)
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
open(a.out, 'w', encoding='utf-8').write(html)
print(f'{a.out}: {len(html)/1e6:.2f} MB')
