#!/usr/bin/env python3
"""Normalize any YouTube link and parse creator chapters from a description.

Usage:
  python3 yt_url.py URL                      -> JSON: id, kind, start, canonical, deep_link template
  python3 yt_url.py URL --chapters desc.txt  -> adds "chapters" parsed from a description file

Handles youtu.be, watch?v=, shorts/, live/, embed/, v/, m. and music. hosts,
youtube-nocookie.com, t= / start= in seconds or 1h2m3s form, and playlist links.
Import as a module to use parse() and deep_link().
"""
import json, re, sys
from urllib.parse import urlparse, parse_qs

ID_RE = re.compile(r'^[A-Za-z0-9_-]{11}$')


def to_seconds(v):
    if not v:
        return 0
    v = str(v).strip().lower()
    if re.fullmatch(r'\d+s?', v):
        v = v.rstrip('s')
    if v.isdigit():
        return int(v)
    m = re.fullmatch(r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s?)?', v)
    if m and any(m.groups()):
        h, mi, s = (int(x or 0) for x in m.groups())
        return h * 3600 + mi * 60 + s
    parts = v.split(':')
    if all(p.isdigit() for p in parts) and 1 < len(parts) <= 3:
        sec = 0
        for p in parts:
            sec = sec * 60 + int(p)
        return sec
    return 0


def parse(url):
    url = url.strip()
    if ID_RE.match(url):
        url = 'https://www.youtube.com/watch?v=' + url
    if not re.match(r'^https?://', url):
        url = 'https://' + url
    u = urlparse(url)
    host = u.netloc.lower().split(':')[0]
    q = parse_qs(u.query)
    parts = [p for p in u.path.split('/') if p]
    vid, kind = None, 'video'
    if host == 'youtu.be' or host.endswith('.youtu.be'):
        vid = parts[0] if parts else None
    elif any(host == d or host.endswith('.' + d) for d in ('youtube.com', 'youtube-nocookie.com')):
        if parts and parts[0] in ('shorts', 'live', 'embed', 'v', 'e'):
            vid = parts[1] if len(parts) > 1 else None
            kind = {'shorts': 'short', 'live': 'live'}.get(parts[0], 'video')
        else:
            vid = (q.get('v') or [None])[0]
    if vid and not ID_RE.match(vid):
        vid = vid[:11] if ID_RE.match(vid[:11]) else None
    playlist = (q.get('list') or [None])[0]
    start = to_seconds((q.get('t') or q.get('start') or [None])[0])
    if not start and u.fragment.startswith('t='):
        start = to_seconds(u.fragment[2:])
    if not vid:
        return {'ok': False, 'error': 'No video id found. Playlist-only and channel links need one specific video.',
                'playlist': playlist, 'input': url}
    return {'ok': True, 'id': vid, 'kind': kind, 'start': start, 'playlist': playlist,
            'canonical': f'https://www.youtube.com/watch?v={vid}',
            'short_link': f'https://youtu.be/{vid}',
            'deep_link': f'https://youtu.be/{vid}?t={{seconds}}'}


def deep_link(vid, seconds):
    return f'https://youtu.be/{vid}?t={int(seconds)}'


CH_RE = re.compile(r'^\s*[\(\[]?((?:\d{1,2}:)?\d{1,2}:\d{2})(?!:?\d)[\)\]]?\s*[-\u2013\u2014:|.]?\s*(.+?)\s*$')


def chapters(description):
    """Creator chapters: lines that start with a timestamp. Valid only if the first is 0:00 and there are 3+."""
    out = []
    for line in description.splitlines():
        m = CH_RE.match(line)
        if m and m.group(2):
            out.append({'start': to_seconds(m.group(1)), 'title': m.group(2)})
    out.sort(key=lambda c: c['start'])
    if len(out) >= 3 and out[0]['start'] == 0:
        return out
    return []


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    r = parse(sys.argv[1])
    if '--chapters' in sys.argv:
        i = sys.argv.index('--chapters') + 1
        if i >= len(sys.argv):
            print('--chapters needs a file path', file=sys.stderr); sys.exit(1)
        r['chapters'] = chapters(open(sys.argv[i], encoding='utf-8').read())
    print(json.dumps(r, indent=2, ensure_ascii=False))
    sys.exit(0 if r.get('ok') else 2)
