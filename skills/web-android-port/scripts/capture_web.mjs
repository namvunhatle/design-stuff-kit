#!/usr/bin/env node
// Screenshot a time-seekable web prototype at given timestamps.
// Requires Playwright: npm i -D playwright && npx playwright install chromium
import { mkdir } from 'node:fs/promises'
import { parseArgs } from 'node:util'
import { chromium } from 'playwright'

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
