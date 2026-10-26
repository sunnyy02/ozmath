/* Headless browser smoke test and screenshots.
 *   python3 -m http.server 8765 &   (from the repo root)
 *   node tests/smoke.js [http://localhost:8765] [screenshots-dir]
 * Needs Playwright (npm i -D playwright, then npx playwright install chromium).
 */
'use strict';
const { chromium } = require('playwright');
const BASE = process.argv[2] || 'http://localhost:8765';
const OUT = process.argv[3] || 'screenshots';
const fs = require('fs');

(async function () {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const errors = [];
  let failed = 0;
  const check = function (ok, msg) { console.log((ok ? 'ok   ' : 'FAIL ') + msg); if (!ok) failed++; };

  async function page(w, theme) {
    const ctx = await browser.newContext({ viewport: { width: w || 1200, height: 900 }, colorScheme: theme || 'light' });
    const p = await ctx.newPage();
    p.on('pageerror', function (e) { errors.push(e.message); });
    p.on('console', function (m) { if (m.type() === 'error') errors.push(m.text()); });
    return p;
  }

  let p = await page();
  await p.goto(BASE + '/');
  await p.waitForSelector('.band-card');
  check((await p.locator('#stats .stat').count()) === 4, 'home shows 4 stats');
  await p.screenshot({ path: OUT + '/01-home.png', fullPage: true });

  await p.goto(BASE + '/explore/#qm_m1_002');
  await p.waitForSelector('#cy canvas');
  check((await p.locator('h1').textContent()).includes('choosing a method'), 'explore opens topic from hash');
  await p.waitForTimeout(400);
  await p.screenshot({ path: OUT + '/02-explore.png', fullPage: true });
  await p.fill('#q', 'discriminant');
  check((await p.locator('.topic-list li').count()) >= 2, 'explore search filters');

  await p.goto(BASE + '/diagnose/?target=qm_m1_007&demo=1');
  await p.waitForSelector('text=Where the gap starts');
  const rootsText = await p.locator('.card').nth(1).textContent();
  check(/Root cause/.test(rootsText), 'demo diagnosis shows a root cause');
  await p.waitForTimeout(400);
  await p.screenshot({ path: OUT + '/03-demo-result.png', fullPage: true });

  // a real session: answer the first question wrong twice
  await p.goto(BASE + '/diagnose/?target=qm_m1_003&seed=s1');
  await p.waitForSelector('.question');
  await p.screenshot({ path: OUT + '/04-question.png', fullPage: true });
  for (let i = 0; i < 2; i++) {
    await p.click("text=I don't know");
    await p.click('.feedback .btn.primary');
    await p.waitForSelector('.question');
  }
  check((await p.locator('.why').textContent()).includes('prerequisite'), 'after two misses the tool checks a prerequisite');
  // type a correct numeric answer if it is numeric, else pick the right choice
  const before = await p.locator('.muted.small').first().textContent();
  check(/Question 3/.test(before), 'question counter advanced to 3');

  // reload restores the session
  await p.reload();
  await p.waitForSelector('.question');
  check(/Question 3/.test(await p.locator('.muted.small').first().textContent()), 'reload resumes the session');

  // screening
  await p.goto(BASE + '/diagnose/?scope=Year%2010&demo=1');
  await p.waitForSelector('text=By topic group');
  check(true, 'screening demo renders group summary');
  await p.screenshot({ path: OUT + '/05-screening.png', fullPage: true });

  // Year 12: a Methods Unit 4 target backtracks across units, and a unit screen works
  await p.goto(BASE + '/diagnose/?target=qm_m4_018&demo=1');
  await p.waitForSelector('text=Where the gap starts');
  const path = await p.locator('.path-list').textContent();
  check(/Year 12/.test(path), 'Unit 4 demo learning path shows Year 12 labels');
  await p.waitForTimeout(400);
  await p.screenshot({ path: OUT + '/08-methods-u4-demo.png', fullPage: true });
  await p.goto(BASE + '/diagnose/?scope=Methods%20U3&demo=1');
  await p.waitForSelector('text=By topic group');
  check((await p.locator('text=Checked: Methods U3 (Year 12)').count()) === 1, 'unit screen is labelled Year 12');
  await p.goto(BASE + '/explore/?band=methods#qm_m4_014');
  await p.waitForSelector('#cy canvas');
  check((await p.locator('.topic-list li').count()) === 93, 'explore lists all 93 Methods topics');
  await p.waitForTimeout(400);
  await p.screenshot({ path: OUT + '/09-explore-methods-u4.png', fullPage: true });

  // full map
  await p.goto(BASE + '/map/?levels=Methods%20U1,Methods%20U2,Methods%20U3,Methods%20U4,Year%209,Year%2010,Year%2010%20Optional');
  await p.waitForSelector('#cy canvas');
  check(/133 of 133 topics/.test(await p.locator('#summary').textContent()), 'full map shows all 133 topics');
  await p.goto(BASE + '/map/?focus=qm_m2_014');
  await p.waitForSelector('text=Builds towards');
  check(/topics before it/.test(await p.locator('#sel').textContent()), 'full map focuses a topic and lists its prerequisites');
  await p.waitForTimeout(600);
  await p.screenshot({ path: OUT + '/10-full-map-focus.png' });
  await p.uncheck('#soft');
  check(/\(\d+ hard, 0 soft\)/.test(await p.locator('#summary').textContent()), 'soft links can be hidden');

  // start page, phone width, dark theme
  const m = await page(390, 'dark');
  await m.goto(BASE + '/diagnose/');
  await m.waitForSelector('text=Diagnose one topic');
  const sw = await m.evaluate(function () { return document.documentElement.scrollWidth; });
  check(sw <= 390, 'no horizontal scroll at 390px (scrollWidth ' + sw + ')');
  await m.screenshot({ path: OUT + '/06-start-phone-dark.png', fullPage: true });
  await m.goto(BASE + '/explore/#qm_10o_005');
  await m.waitForSelector('#cy canvas');
  const sw2 = await m.evaluate(function () { return document.documentElement.scrollWidth; });
  check(sw2 <= 390, 'explore has no horizontal scroll at 390px (scrollWidth ' + sw2 + ')');
  await m.screenshot({ path: OUT + '/07-explore-phone-dark.png', fullPage: true });

  check(errors.length === 0, 'no console errors' + (errors.length ? ': ' + errors.join(' | ') : ''));
  await browser.close();
  console.log(failed ? failed + ' checks failed' : 'smoke: all checks passed');
  process.exit(failed ? 1 : 0);
})();
