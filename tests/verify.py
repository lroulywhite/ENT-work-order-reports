#!/usr/bin/env python3
"""Verify the built simulation in headless Chromium.

Checks, at four embed sizes:
  1. Full path works (Back, Restart, wrong-report tips, stray-click nudge).
  2. The checklist bar count matches the current step.
  3. No guide card, and none of its shadow, covers a control the learner must click.

Setup:  pip install -r requirements-dev.txt && playwright install chromium
Run:    python3 tests/verify.py
"""
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
URL = (ROOT / "simulations" / "ENT _ Run a Work Order Report [Simulation].html").as_uri()
SIZES = [(1920, 1006, "full"), (1280, 720, "hd"), (900, 520, "small"), (390, 844, "phone")]

CLEARANCE = """() => {
  const c = document.getElementById('sim-card').getBoundingClientRect();
  const hs = [...document.querySelectorAll('.hs')].map(h => h.getBoundingClientRect());
  const ring = document.getElementById('sim-ring'); const rr = ring.hidden ? null : ring.getBoundingClientRect();
  const s = Math.min(innerWidth/1920, innerHeight/1006), K = Math.min(1.7, Math.max(1, 1/s));
  const z = {l:c.left-80*s*K, r:c.right+80*s*K, t:c.top-70*s*K, b:c.bottom+210*s*K}; // shadow reach + room for a nudge message
  const hit = a => a && a.left < z.r && a.right > z.l && a.top < z.b && a.bottom > z.t;
  return {box: hs.some(a => a.left < c.right && a.right > c.left && a.top < c.bottom && a.bottom > c.top),
          shadow: hs.some(hit) || hit(rr), inside: c.left >= -1 && c.top >= -1 && c.right <= innerWidth + 1};
}"""

async def clearance_path(pg, label, problems):
    await pg.goto(URL); await pg.click('#b-start')
    hs = lambda i: pg.evaluate(f"document.querySelectorAll('.hs')[{i}].click()")
    async def check(name):
        r = await pg.evaluate(CLEARANCE)
        if r['box'] or r['shadow'] or not r['inside']:
            problems.append(f"{label}/{name}: {r}")
    for name, pick in [('actions',0),('reports',0),('choose',4),('select',0),('run',0),('viewer',0)]:
        await check(name); await hs(pick)
    await check('toolsmenu'); await pg.click('#b-next')
    await check('email'); await hs(0)
    await check('emailmenu')

async def functional(pg, problems):
    await pg.goto(URL)
    title = lambda: pg.evaluate("document.querySelector('#sim-card h2').textContent")
    bar = lambda: pg.evaluate("document.getElementById('bcount').textContent")
    hs = lambda i: pg.evaluate(f"document.querySelectorAll('.hs')[{i}].click()")
    def expect(label, got, want):
        if got != want: problems.append(f"{label}: got {got!r}, want {want!r}")
    expect('intro bar', await bar(), '0 of 4 covered')
    await pg.click('#b-start'); expect('step 1', await title(), 'Select Actions')
    await pg.mouse.click(300, 500)
    expect('nudge', (await pg.evaluate("document.querySelector('.sim-msg').hidden")), False)
    await hs(0); await hs(0); expect('choose', await title(), 'Choose the report'); expect('bar after Reports', await bar(), '1 of 4 covered')
    await hs(5); expect('wrong (Open Items) stays', await title(), 'Choose the report')
    await hs(0); expect('wrong (other) stays', await title(), 'Choose the report')
    await hs(4); expect('confirm', await title(), 'Confirm your choice'); expect('bar after choice', await bar(), '2 of 4 covered')
    await hs(0); await hs(0); expect('viewer', await title(), 'Select Tools'); expect('bar after run', await bar(), '3 of 4 covered')
    await hs(0); expect('tools menu', await title(), 'Export formats'); await pg.click('#b-next')
    await hs(0); expect('email menu', await title(), 'Email choices'); expect('bar after email', await bar(), '4 of 4 covered')
    await pg.click('#b-next'); await pg.wait_for_timeout(300)
    expect('final', await title(), 'You can run a work order report'); expect('bar final', await bar(), '4 of 4 covered')
    await pg.click('#b-back'); expect('back from final', await title(), 'Email choices')
    await pg.click('#b-back'); expect('back to email click', await title(), 'Select Email Options'); expect('bar after back', await bar(), '3 of 4 covered')
    await pg.click('#b-restart'); expect('restart', await title(), 'Run a work order report'); expect('bar after restart', await bar(), '0 of 4 covered')

async def main():
    problems, errors = [], []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h, label in SIZES:
            pg = await b.new_page(viewport={'width': w, 'height': h})
            pg.on('pageerror', lambda e: errors.append(str(e)))
            pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            await clearance_path(pg, label, problems)
            if label == 'full': await functional(pg, problems)
            await pg.close()
        await b.close()
    problems += [f"console error: {e}" for e in errors]
    print("PASS" if not problems else "FAIL"); [print(" -", x) for x in problems]
    sys.exit(1 if problems else 0)

asyncio.run(main())
