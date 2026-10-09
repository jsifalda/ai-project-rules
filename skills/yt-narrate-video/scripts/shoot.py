#!/usr/bin/env python3
"""Screenshot sections of the page for self-critique, at desktop and mobile widths.

Usage: python3 shoot.py page.html out_dir SELECTOR [SELECTOR ...]
Prints JS errors. Font 403s inside a sandbox are expected and harmless.
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

async def main(page, out, sels):
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, tag in [(1360, 'desktop'), (390, 'mobile')]:
            pg = await b.new_page(viewport={'width': w, 'height': 900})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('file://' + os.path.abspath(page)); await pg.wait_for_timeout(700)
            for s in sels:
                el = await pg.query_selector(s)
                if not el: print('not found:', s); continue
                await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(250)
                name = s.strip('#.').replace(' ', '_')
                await el.screenshot(path=os.path.join(out, f'{tag}_{name}.png'))
            print(tag, 'js errors:', errs or 'none')
        await b.close()

asyncio.run(main(sys.argv[1], sys.argv[2], sys.argv[3:]))
