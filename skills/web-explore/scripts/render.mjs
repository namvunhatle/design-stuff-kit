#!/usr/bin/env node
// Render every <section class="screen"> in an HTML file to PNG, tile a contact
// sheet, and check the rendered DOM for defects nobody should have to find by eye:
// clipped, colliding or off-screen text, contrast, small text, small touch targets,
// screens that render the same (one of them is broken or never drew), and
// (in design-system mode) colours that are not tokens.
//
// Needs Playwright in the working folder: npm i -D playwright
// Uses installed Google Chrome when present; otherwise run: npx playwright install chromium
//
// Usage: node render.mjs explore.html [--out shots/r1] [--scale 3] [--device ios|android]
//        [--small] [--only home,detail] [--measure] [--compare shots/r1]
// --compare lists which screens look the same as in the previous round, so a
// change that did not land is caught, and only changed screens go to the critic.
// Exit code 1 when any check FAILs.
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { createRequire } from 'node:module'
import path from 'node:path'
import { pathToFileURL } from 'node:url'
import { parseArgs } from 'node:util'

const { values: a, positionals } = parseArgs({
  allowPositionals: true,
  options: {
    out: { type: 'string', default: 'shots/r1' },
    scale: { type: 'string', default: '3' },
    device: { type: 'string' },
    small: { type: 'boolean', default: false },
    only: { type: 'string' },
    measure: { type: 'boolean', default: false },
    compare: { type: 'string' },
  },
})
if (!positionals[0]) {
  console.error('Usage: node render.mjs explore.html [--out DIR] [--scale 3] [--device ios|android] [--small] [--only a,b] [--measure] [--compare DIR]')
  process.exit(2)
}
const file = path.resolve(positionals[0])
const out = path.resolve(a.out)

// Resolve Playwright from the working folder, not from this script's folder.
const requireHere = createRequire(path.join(process.cwd(), 'noop.js'))
let pw
for (const name of ['playwright', 'playwright-core']) {
  try { pw = await import(pathToFileURL(requireHere.resolve(name)).href); break } catch {}
}
if (!pw) {
  console.error('Playwright is missing. In this folder run: npm i -D playwright')
  process.exit(2)
}
pw = pw.chromium ? pw : pw.default
let browser
try { browser = await pw.chromium.launch({ channel: 'chrome' }) } catch {
  try { browser = await pw.chromium.launch() } catch {
    console.error('No browser found. Install Google Chrome, or run: npx playwright install chromium')
    process.exit(2)
  }
}

const page = await browser.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: Number(a.scale) })
const pageErrors = []
page.on('pageerror', (e) => pageErrors.push(e.message))
if (a.device) await page.addInitScript((d) => { window.__wxDevice = d }, a.device)
await page.goto(pathToFileURL(file).href, { waitUntil: 'networkidle' })
await page.evaluate(async (small) => {
  if (small) {
    document.documentElement.dataset.size = 'small'
    for (const s of document.querySelectorAll('section.screen')) {
      const android = s.dataset.device === 'android'
      s.style.setProperty('--screen-w', android ? '360px' : '375px')
      s.style.setProperty('--screen-h', android ? '640px' : '667px')
    }
  }
  await document.fonts.ready
  window.__wxFreeze?.()
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))
}, a.small)
await page.waitForTimeout(300)

await mkdir(out, { recursive: true })
const only = a.only ? new Set(a.only.split(',').map((s) => s.trim())) : null
const screens = []
const handles = await page.$$('section.screen')
for (const [i, handle] of handles.entries()) {
  const name = (await handle.getAttribute('data-name')) || `screen-${i + 1}`
  if (only && !only.has(name)) continue
  const png = path.join(out, `${name}.png`)
  await handle.screenshot({ path: png })
  const identicalOk = (await handle.getAttribute('data-identical-ok')) !== null
  screens.push({ name, png, identicalOk })
  console.log(`✓ ${name}`)
}
if (!screens.length) {
  console.error('No <section class="screen"> matched. Check the file and --only.')
  await browser.close()
  process.exit(2)
}

// Design-system tokens: Chrome blocks cssRules on file:// sheets, so read tokens.css from disk.
const tokenHrefs = await page.$$eval('link[rel="stylesheet"]', (links) => links.map((l) => l.href).filter((h) => /tokens\.css(\?|$)/.test(h)))
const tokenValues = []
for (const href of tokenHrefs) {
  try {
    const css = await readFile(new URL(href.split('?')[0]), 'utf8')
    for (const m of css.matchAll(/--[\w-]+\s*:\s*([^;}]+)/g)) tokenValues.push(m[1].trim())
  } catch {}
}

// ---------- checks, run inside the page ----------
const issues = await page.evaluate(([onlyNames, tokenValues]) => {
  const found = []
  const add = (level, screen, rule, detail) => found.push({ level, screen, rule, detail })
  const rgba = (c) => {
    const m = /^rgba?\(([^)]+)\)$/.exec(c || '')
    if (!m) return null
    const p = m[1].split(/[\s,/]+/).filter(Boolean).map(Number)
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }
  }
  const hex = (c) => '#' + [c.r, c.g, c.b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase()
  const over = (fg, bg) => ({
    r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1,
  })
  const lin = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4 }
  const lum = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b)
  const ratio = (x, y) => { const [h, l] = [lum(x), lum(y)].sort((p, q) => q - p); return (h + 0.05) / (l + 0.05) }
  const label = (el) => {
    const t = (el.textContent || '').trim().replace(/\s+/g, ' ')
    return `"${t.length > 28 ? t.slice(0, 27) + '…' : t}"`
  }
  const chrome = (el) => el.closest('.wx-status, .wx-home')
  const visible = (el) => !el.checkVisibility || el.checkVisibility({ opacityProperty: true, visibilityProperty: true })

  // Background under an element: composite translucent layers up the tree.
  // Returns null when an image or gradient sits underneath (not measurable from the DOM).
  const backdrop = (el, screen) => {
    const layers = []
    for (let n = el; n; n = n.parentElement) {
      const cs = getComputedStyle(n)
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null
      const bg = rgba(cs.backgroundColor)
      if (bg && bg.a > 0) { layers.push(bg); if (bg.a >= 1) break }
      if (n === screen) { layers.push({ r: 255, g: 255, b: 255, a: 1 }); break }
    }
    return layers.reduceRight((acc, layer) => over(layer, acc), { r: 255, g: 255, b: 255, a: 1 })
  }

  // Design-system mode: colours declared in a stylesheet named tokens.css.
  const dsMode = document.documentElement.dataset.mode === 'ds'
  const tokens = new Set()
  if (dsMode) {
    const probe = document.createElement('i')
    document.body.append(probe)
    for (const value of tokenValues) {
      probe.style.color = ''
      probe.style.color = value
      const c = probe.style.color && rgba(getComputedStyle(probe).color)
      if (c) tokens.add(hex(c))
    }
    probe.remove()
    if (!tokens.size) add('FAIL', '(page)', 'ds-tokens', 'data-mode="ds" is set but no colour tokens were found in a stylesheet named tokens.css')
  }

  for (const screen of document.querySelectorAll('section.screen')) {
    const name = screen.dataset.name || '(unnamed)'
    if (onlyNames && !onlyNames.includes(name)) continue
    const sr = screen.getBoundingClientRect()
    const android = screen.dataset.device === 'android'
    const boxes = []
    const unmeasured = []
    const seen = new Set()

    const walker = document.createTreeWalker(screen, NodeFilter.SHOW_TEXT, {
      acceptNode: (t) => (t.data.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT),
    })
    for (let t = walker.nextNode(); t; t = walker.nextNode()) {
      const el = t.parentElement
      if (!el || seen.has(el) || chrome(el) || !visible(el)) continue
      seen.add(el)
      const range = document.createRange()
      range.selectNodeContents(t)
      const r = range.getBoundingClientRect()
      if (!r.width || !r.height) continue
      const cs = getComputedStyle(el)
      const size = parseFloat(cs.fontSize)

      if (!el.closest('[data-bleed]') && (r.left < sr.left - 1 || r.right > sr.right + 1 || r.top < sr.top - 1 || r.bottom > sr.bottom + 1))
        add('FAIL', name, 'off-screen text', `${label(el)} runs past the screen edge`)

      for (let p = el; p && p !== screen; p = p.parentElement) {
        const ps = getComputedStyle(p)
        if (ps.overflowX === 'visible' && ps.overflowY === 'visible') continue
        const pr = p.getBoundingClientRect()
        if (r.right > pr.right + 1 || r.left < pr.left - 1 || r.bottom > pr.bottom + 1 || r.top < pr.top - 1) {
          add(ps.textOverflow === 'ellipsis' ? 'warn' : 'FAIL', name, 'clipped text', `${label(el)} is cut by <${p.tagName.toLowerCase()}${p.className ? '.' + String(p.className).split(' ')[0] : ''}>`)
          break
        }
      }

      if (size < 11) add('warn', name, 'small text', `${label(el)} is ${size}px (11 px minimum for body copy)`)

      if (!el.closest('[data-decorative]')) {
        let fg = rgba(el instanceof SVGElement ? cs.fill : cs.color)
        // SVG text usually sits on sibling shapes the DOM tree does not reveal.
        const bg = el instanceof SVGElement ? null : backdrop(el, screen)
        if (!fg || !bg) unmeasured.push(label(el))
        else {
          fg = { ...fg, a: fg.a * Number(cs.opacity) }
          const value = ratio(over(fg, bg), bg)
          const large = size >= 24 || (size >= 18.66 && Number(cs.fontWeight) >= 700)
          const need = large ? 3 : 4.5
          if (value < need) add('FAIL', name, 'contrast', `${label(el)} ${value.toFixed(2)}:1 on ${hex(bg)}, needs ${need}:1`)
        }
      }
      boxes.push({ el, r })
    }

    for (let i = 0; i < boxes.length; i++)
      for (let j = i + 1; j < boxes.length; j++) {
        const A = boxes[i], B = boxes[j]
        if (A.el.contains(B.el) || B.el.contains(A.el)) continue
        if (A.el.closest('[data-overlap-ok]') || B.el.closest('[data-overlap-ok]')) continue
        const w = Math.min(A.r.right, B.r.right) - Math.max(A.r.left, B.r.left)
        const h = Math.min(A.r.bottom, B.r.bottom) - Math.max(A.r.top, B.r.top)
        if (w > 2 && h > 2) add('FAIL', name, 'text collision', `${label(A.el)} overlaps ${label(B.el)}`)
      }

    if (unmeasured.length)
      add('warn', name, 'contrast not measured', `${unmeasured.length} text element(s) sit on an image, gradient, or SVG shape: ${unmeasured.slice(0, 3).join(', ')}${unmeasured.length > 3 ? '…' : ''}. Check by eye or in the PNG`)

    const min = android ? 48 : 44
    for (const t of screen.querySelectorAll('button, a[href], [role="button"], input, select, textarea, [data-tap]')) {
      if (chrome(t) || !visible(t) || t.closest('[data-storyboard]')) continue
      const r = t.getBoundingClientRect()
      if (r.width && (r.width < min || r.height < min))
        add('FAIL', name, 'touch target', `${label(t) === '""' ? '<' + t.tagName.toLowerCase() + '>' : label(t)} is ${Math.round(r.width)}×${Math.round(r.height)}, needs ${min}×${min}`)
    }

    if (dsMode && tokens.size) {
      const off = new Map()
      for (const el of screen.querySelectorAll('*')) {
        if (chrome(el) || !visible(el)) continue
        const cs = getComputedStyle(el)
        const props = ['color', 'backgroundColor']
        if (parseFloat(cs.borderTopWidth) > 0) props.push('borderTopColor')
        if (el instanceof SVGElement) props.push('fill', 'stroke')
        for (const p of props) {
          if (p === 'color' && ![...el.childNodes].some((n) => n.nodeType === 3 && n.data.trim())) continue
          const c = rgba(cs[p])
          if (!c || c.a === 0) continue
          const h = hex(c)
          if (!tokens.has(h)) off.set(h, (off.get(h) || 0) + 1)
        }
      }
      for (const [h, n] of off) add('warn', name, 'off-token colour', `${h} used ${n}× and is not in tokens.css. Bind it, or label it a deliberate local value`)
    }
  }
  return found
}, [only ? [...only] : null, tokenValues])

for (const e of pageErrors) issues.unshift({ level: 'FAIL', screen: '(page)', rule: 'script error', detail: e })

// ---------- identical renders ----------
// Two screens that should differ but render the same: one is broken or never drew.
// Compared as pixels with a small tolerance (anti-aliasing shifts with position).
const diffPage = await browser.newPage()
const share = async (x, y) => diffPage.evaluate(async ([x, y]) => {
  const load = (src) => new Promise((ok, no) => { const i = new Image(); i.onload = () => ok(i); i.onerror = no; i.src = src })
  const [A, B] = await Promise.all([load(x), load(y)])
  if (A.width !== B.width || A.height !== B.height) return 1
  const w = Math.max(1, Math.round(A.width / 3)), h = Math.max(1, Math.round(A.height / 3))
  const px = (img) => { const c = new OffscreenCanvas(w, h); const g = c.getContext('2d'); g.drawImage(img, 0, 0, w, h); return g.getImageData(0, 0, w, h).data }
  const a = px(A), b = px(B)
  let changed = 0
  for (let i = 0; i < a.length; i += 4)
    if (Math.abs(a[i] - b[i]) + Math.abs(a[i + 1] - b[i + 1]) + Math.abs(a[i + 2] - b[i + 2]) > 24) changed++
  return changed / (w * h)
}, [x, y])
const uri = (bytes) => `data:image/png;base64,${bytes.toString('base64')}`
const SAME = 0.001 // under 0.1% of pixels changed counts as the same image
for (const s of screens) s.bytes = await readFile(s.png)
const reported = new Set()
for (let i = 0; i < screens.length; i++) {
  if (reported.has(i)) continue
  const group = [screens[i]]
  for (let j = i + 1; j < screens.length; j++)
    if (!reported.has(j) && (await share(uri(screens[i].bytes), uri(screens[j].bytes))) < SAME) { group.push(screens[j]); reported.add(j) }
  if (group.length > 1 && !group.every((s) => s.identicalOk))
    issues.push({ level: 'FAIL', screen: group.map((s) => s.name).join(', '), rule: 'identical renders',
      detail: 'these screens render the same; one is broken or never drew. Mark data-identical-ok on each if that is intended' })
}

const unchanged = []
if (a.compare) {
  for (const s of screens) {
    try {
      const before = await readFile(path.join(path.resolve(a.compare), `${s.name}.png`))
      if (before.equals(s.bytes) || (await share(uri(before), uri(s.bytes))) < SAME) unchanged.push(s.name)
    } catch {}
  }
}
await diffPage.close()

// ---------- optional measurements for the Figma rebuild ----------
if (a.measure) {
  const dir = path.join(out, 'measure')
  await mkdir(dir, { recursive: true })
  const data = await page.evaluate((onlyNames) => {
    const result = {}
    for (const screen of document.querySelectorAll('section.screen')) {
      const name = screen.dataset.name || '(unnamed)'
      if (onlyNames && !onlyNames.includes(name)) continue
      const sr = screen.getBoundingClientRect()
      result[name] = [...screen.querySelectorAll('[data-layer]')].map((el) => {
        const r = el.getBoundingClientRect()
        const cs = getComputedStyle(el)
        return {
          layer: el.dataset.layer,
          x: +(r.left - sr.left).toFixed(1), y: +(r.top - sr.top).toFixed(1), w: +r.width.toFixed(1), h: +r.height.toFixed(1),
          text: el.children.length ? undefined : el.textContent.trim() || undefined,
          font: `${cs.fontWeight} ${cs.fontSize}/${cs.lineHeight} ${cs.fontFamily.split(',')[0]}`,
          letterSpacing: cs.letterSpacing, color: cs.color, background: cs.backgroundColor,
          radius: cs.borderRadius, opacity: cs.opacity, padding: cs.padding, gap: cs.gap,
        }
      })
    }
    return result
  }, only ? [...only] : null)
  for (const [name, layers] of Object.entries(data)) await writeFile(path.join(dir, `${name}.json`), JSON.stringify(layers, null, 2))
  console.log(`✓ measurements for [data-layer] elements → ${path.relative(process.cwd(), dir)}/`)
}

// ---------- contact sheet ----------
const sheet = await browser.newPage({ viewport: { width: 1400, height: 800 }, deviceScaleFactor: 2 })
// about:blank cannot load file:// images, so embed them.
const cells = (await Promise.all(screens.map(async (s) =>
  `<figure><img src="data:image/png;base64,${(await readFile(s.png)).toString('base64')}"><figcaption>${s.name}</figcaption></figure>`))).join('')
await sheet.setContent(`<style>body{margin:0;padding:32px;background:#e6e6ea;font:500 13px system-ui;color:#55555c;display:flex;flex-wrap:wrap;gap:28px;width:${Math.min(screens.length, 5) * 278}px}figure{margin:0;display:flex;flex-direction:column;gap:8px}img{width:250px;border-radius:14px}</style>${cells}`)
await sheet.waitForLoadState('networkidle')
await sheet.screenshot({ path: path.join(out, 'sheet.png'), fullPage: true })
await browser.close()

// ---------- report ----------
const fails = issues.filter((i) => i.level === 'FAIL')
const warns = issues.filter((i) => i.level !== 'FAIL')
const lines = [
  `# Render report`,
  ``,
  `${path.basename(file)} · ${screens.length} screen(s) · ${a.small ? 'small phone' : 'default size'} · ${new Date().toLocaleString('sv').slice(0, 16)}`,
  ``,
  `**${fails.length} FAIL · ${warns.length} warn**`,
  ``,
]
if (a.compare) lines.push(`Unchanged since \`${a.compare}\` (same pixels): ${unchanged.length ? unchanged.join(', ') : 'none'}. Changed: ${screens.filter((s) => !unchanged.includes(s.name)).map((s) => s.name).join(', ') || 'none'}.`, ``)
if (issues.length) {
  lines.push('| Level | Screen | Check | Detail |', '|---|---|---|---|')
  for (const i of [...fails, ...warns]) lines.push(`| ${i.level} | ${i.screen} | ${i.rule} | ${i.detail.replace(/\|/g, '\\|')} |`)
}
await writeFile(path.join(out, 'report.md'), lines.join('\n') + '\n')

console.log(`\n${fails.length} FAIL · ${warns.length} warn`)
for (const i of [...fails, ...warns].slice(0, 40)) console.log(`  ${i.level.padEnd(4)} ${i.screen} · ${i.rule}: ${i.detail}`)
if (issues.length > 40) console.log(`  … ${issues.length - 40} more in report.md`)
if (a.compare) console.log(`\nUnchanged since ${a.compare}: ${unchanged.join(', ') || 'none'}`)
console.log(`\nPNGs, sheet.png and report.md → ${path.relative(process.cwd(), out) || '.'}/`)
process.exit(fails.length ? 1 : 0)
