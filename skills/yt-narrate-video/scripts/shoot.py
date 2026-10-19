#!/usr/bin/env python3
"""Screenshot sections of the page for self-critique, at desktop, mobile and dark.

Usage: python3 shoot.py page.html out_dir [ID ...]
ID is an element id (with or without #). No ID shoots the top of the page.
Needs a system Chrome or Chromium (set CHROME_BIN to pick one). Standard library only.
Prints JS errors. Font load failures inside a sandbox are expected and harmless.
"""
import glob, json, os, pathlib, shutil, subprocess, sys, tempfile

DESKTOP, MOBILE_WIN, MOBILE_W, MOBILE_H = (1360, 900), (500, 900), 390, 844
BUDGET_MS, TIMEOUT_S = 3000, 60
FILE_ACCESS = ['--allow-file-access-from-files']
NAMES = ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser']
APPS = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/Applications/Chromium.app/Contents/MacOS/Chromium']
CACHE = ['~/.cache/*/chromium-*/chrome-linux*/chrome',
         '~/.cache/*/chromium_headless_shell-*/chrome-linux*/headless_shell']

def find_browser():
    env = os.environ.get('CHROME_BIN')
    if env: return env
    for p in [shutil.which(n) for n in NAMES] + [a for a in APPS if os.path.exists(a)]:
        if p: return p
    for pat in CACHE:
        hits = sorted(glob.glob(os.path.expanduser(pat)), reverse=True)
        if hits: return hits[0]

def shoot(browser, url, png, size, extra=()):
    """Return (uncaught-error console lines, failure reason or None) from one headless run."""
    if os.path.exists(png): os.remove(png)
    with tempfile.TemporaryDirectory() as prof:
        cmd = [browser, '--headless=new', '--disable-gpu', '--hide-scrollbars',
               f'--screenshot={png}', f'--window-size={size[0]},{size[1]}',
               f'--virtual-time-budget={BUDGET_MS}', f'--user-data-dir={prof}',
               '--enable-logging=stderr', '--v=0', *extra, url]
        if hasattr(os, 'geteuid') and os.geteuid() == 0: cmd.insert(1, '--no-sandbox')
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_S)
        except subprocess.TimeoutExpired:
            return [], f'timeout after {TIMEOUT_S}s'
    lines = [l for l in r.stderr.splitlines() if l.strip() and 'CONSOLE' not in l]
    errs = [l.split('"', 1)[-1].split('", source', 1)[0] for l in r.stderr.splitlines()
            if 'CONSOLE' in l and 'Uncaught' in l]
    if r.returncode: return errs, f'chrome exit {r.returncode}: {lines[-1] if lines else "no stderr"}'
    if not os.path.exists(png): return errs, 'no PNG written'
    return errs, None

def framed(browser, url, png, size, frame, target, extra=()):
    """Return shoot()'s result for url inside an iframe of the given size, scrolled to element id target.
    The wrapper scrolls the frame itself: a #id URL is not reliable under smooth scroll."""
    wrap = os.path.join(os.path.dirname(png), '_wrap_' + os.path.basename(png) + '.html')
    with open(wrap, 'w') as f:
        f.write(f'<body style="margin:0"><iframe src="{url}" style="border:0;display:block;'
                f'width:{frame[0]}px;height:min({frame[1]}px,100vh)"></iframe><script>'
                f'const f=document.querySelector("iframe");f.onload=()=>{{const d=f.contentDocument,'
                f'e=d&&d.getElementById({json.dumps(target)});if(e){{d.documentElement.style.scrollBehavior="auto";'
                f'e.scrollIntoView()}}else if({json.dumps(target)}!=="top")'
                f'throw new Error("no element #"+{json.dumps(target)})}}</script>')
    try: errs, why = shoot(browser, pathlib.Path(wrap).resolve().as_uri(), png, size, extra)
    finally: os.remove(wrap)
    print(png if not why else f'FAILED {os.path.basename(png)}: {why}')
    return errs, why

def main(page, out, ids):
    if not os.path.isfile(page): print('page not found:', page); return 1
    browser = find_browser()
    if not browser:
        print('no Chrome or Chromium found: screenshots skipped, the page can still ship'); return 0
    os.makedirs(out, exist_ok=True)
    src = pathlib.Path(page).resolve().as_uri()
    ids = [i.lstrip('#') for i in ids] or ['top']
    errs, failed = {'desktop': [], 'mobile': [], 'dark': []}, 0
    def take(tag, name, *args):
        nonlocal failed
        e, why = framed(browser, src, os.path.join(out, name), *args)
        errs[tag] += e; failed += bool(why)
    for i in ids:
        take('desktop', f'desktop_{i}.png', DESKTOP, DESKTOP, i, FILE_ACCESS)
        take('mobile', f'mobile_{i}.png', MOBILE_WIN, (MOBILE_W, MOBILE_H), i, FILE_ACCESS)
    take('dark', f'dark_{ids[0]}.png', DESKTOP, DESKTOP, ids[0], FILE_ACCESS + ['--force-dark-mode'])
    for tag, e in errs.items(): print(tag, 'js errors:', sorted(set(e)) or 'none')
    return 1 if failed else 0

sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3:]) if len(sys.argv) > 2 else print(__doc__) or 1)
