#!/usr/bin/env node
// Screenshot a time-seekable web prototype at given timestamps.
// Requires Playwright in the working folder: npm i -D playwright && npx playwright install chromium
import { mkdir } from 'node:fs/promises'
import { createRequire } from 'node:module'
import path from 'node:path'
import { pathToFileURL } from 'node:url'
import { parseArgs } from 'node:util'

const { values: a } = parseArgs({
  options: {
    url: { type: 'string' },
    times: { type: 'string' },
    out: { type: 'string', default: 'parity/web' },
    param: { type: 'string', default: 't' },
    size: { type: 'string', default: '360x800' },
    scale: { type: 'string', default: '3' },
    selector: { type: 'string' }, // capture one element (e.g. the phone frame) instead of the viewport
    settle: { type: 'string', default: '600' },
  },
})
if (!a.url || !a.times) {
  console.error('Usage: capture_web.mjs --url URL --times 0.5,4.8 [--out DIR] [--param t] [--size 360x800] [--scale 3] [--selector CSS] [--settle ms]')
  process.exit(2)
}

// Resolve Playwright from the working folder (and its parents), not from this script's
// folder: in the plugin, this script lives in Claude Code's plugin cache, outside the project.
let pw
search: for (const from of [path.join(process.cwd(), 'noop.js'), import.meta.url]) {
  for (const name of ['playwright', 'playwright-core']) {
    try { pw = await import(pathToFileURL(createRequire(from).resolve(name)).href); break search } catch {}
  }
}
if (!pw) {
  console.error('Playwright is missing. In the project folder, run: npm i -D playwright && npx playwright install chromium')
  process.exit(2)
}
const { chromium } = pw.chromium ? pw : pw.default

const [width, height] = a.size.split('x').map(Number)
const browser = await chromium.launch()
const page = await browser.newPage({
  viewport: { width, height },
  deviceScaleFactor: Number(a.scale),
  reducedMotion: 'no-preference',
})
const errors = []
page.on('pageerror', (e) => errors.push(e.message))
await mkdir(a.out, { recursive: true })

for (const t of a.times.split(',').map((s) => s.trim()).filter(Boolean)) {
  const u = new URL(a.url)
  u.searchParams.set(a.param, t)
  await page.goto(u.toString(), { waitUntil: 'networkidle' })
  await page.evaluate(() => document.fonts.ready)
  await page.waitForTimeout(Number(a.settle))
  const target = a.selector ? page.locator(a.selector) : page
  await target.screenshot({ path: `${a.out}/${t}.png` })
  console.log(`✓ ${t}s → ${a.out}/${t}.png`)
}

await browser.close()
if (errors.length) {
  console.error(`✗ ${errors.length} page error(s):\n${errors.join('\n')}`)
  process.exit(1)
}
