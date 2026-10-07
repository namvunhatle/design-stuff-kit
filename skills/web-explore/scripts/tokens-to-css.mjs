#!/usr/bin/env node
// Turn design-tokens.json into tokens.css for web-explore's design-system mode.
// Accepts nested groups whose leaves have "value" (or the W3C "$value") and an
// optional "description". References like "{color.text}" become var(--color-text).
// Descriptions are kept as comments: they are how Claude picks the right token.
// Usage: node tokens-to-css.mjs design-tokens.json [--out explore/<feature>/tokens.css]
import { readFile, writeFile } from 'node:fs/promises'
import { parseArgs } from 'node:util'

const { values: a, positionals } = parseArgs({ allowPositionals: true, options: { out: { type: 'string', default: 'tokens.css' } } })
if (!positionals[0]) {
  console.error('Usage: node tokens-to-css.mjs design-tokens.json [--out tokens.css]')
  process.exit(2)
}
const tokens = JSON.parse(await readFile(positionals[0], 'utf8'))
const name = (parts) => '--' + parts.join('-').replace(/[^a-zA-Z0-9-]/g, '-').toLowerCase()
const ref = (v) => String(v).replace(/\{([^}]+)\}/g, (_, p) => `var(${name(p.split('.'))})`)
const lines = []
let undescribed = 0

const walk = (node, parts) => {
  if (node && typeof node === 'object' && ('value' in node || '$value' in node)) {
    const value = node.value ?? node.$value
    const description = node.description ?? node.$description
    if (!description) undescribed++
    lines.push(`  ${name(parts)}: ${ref(value)};${description ? ` /* ${String(description).replace(/\*\//g, '* /')} */` : ''}`)
    return
  }
  if (node && typeof node === 'object')
    for (const [key, child] of Object.entries(node)) if (!key.startsWith('$')) walk(child, [...parts, key])
}
walk(tokens, [])

await writeFile(a.out, `/* Generated from ${positionals[0]} by tokens-to-css.mjs. Edit the JSON, not this file. */\n:root {\n${lines.join('\n')}\n}\n`)
console.log(`✓ ${lines.length} tokens → ${a.out}`)
if (undescribed) console.log(`  ${undescribed} token(s) have no description. Add one: it is how Claude chooses between similar tokens.`)
