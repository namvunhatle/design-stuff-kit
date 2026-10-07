#!/usr/bin/env node
// Live preview for web-explore. Serves the folder that holds the HTML file and
// reloads every open page when a file in that folder changes. No dependencies.
// Usage: node serve.mjs explore.html [--port 5173]
// Open the printed LAN address on a phone on the same Wi-Fi to try it in hand.
import http from 'node:http'
import os from 'node:os'
import path from 'node:path'
import { watch } from 'node:fs'
import { readFile, stat } from 'node:fs/promises'
import { parseArgs } from 'node:util'

const { values: a, positionals } = parseArgs({
  allowPositionals: true,
  options: { port: { type: 'string', default: '5173' } },
})
const entry = path.resolve(positionals[0] || 'index.html')
const root = path.dirname(entry)
const start = '/' + path.basename(entry)
const types = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.woff2': 'font/woff2',
  '.woff': 'font/woff', '.ttf': 'font/ttf', '.mp3': 'audio/mpeg', '.mp4': 'video/mp4',
}
const reload = '<script>new EventSource("/__reload").onmessage=()=>location.reload()</script>'
const clients = new Set()

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost')
  if (url.pathname === '/__reload') {
    res.writeHead(200, { 'content-type': 'text/event-stream', 'cache-control': 'no-cache', connection: 'keep-alive' })
    res.write('retry: 500\n\n')
    clients.add(res)
    req.on('close', () => clients.delete(res))
    return
  }
  let file = path.join(root, decodeURIComponent(url.pathname === '/' ? start : url.pathname))
  if (file !== root && !file.startsWith(root + path.sep)) return res.writeHead(403).end()
  try {
    if ((await stat(file)).isDirectory()) file = path.join(file, 'index.html')
    let body = await readFile(file)
    const ext = path.extname(file).toLowerCase()
    if (ext === '.html') {
      const html = body.toString('utf8')
      body = html.includes('</body>') ? html.replace('</body>', reload + '</body>') : html + reload
    }
    res.writeHead(200, { 'content-type': types[ext] || 'application/octet-stream', 'cache-control': 'no-store' })
    res.end(body)
  } catch {
    res.writeHead(404).end('Not found')
  }
})

let timer
watch(root, { recursive: true }, (_, name) => {
  // Renders and installed packages change often and never affect the page.
  if (!name || /^(shots|reference|figma|parity|node_modules)(\/|\\|$)|(^|[\/\\])\./.test(name)) return
  clearTimeout(timer)
  timer = setTimeout(() => clients.forEach((c) => c.write('data: reload\n\n')), 80)
})

server.listen(Number(a.port), '0.0.0.0', () => {
  console.log(`Live preview of ${path.basename(entry)} (reloads on save)`)
  console.log(`  This computer: http://localhost:${a.port}${start}`)
  for (const list of Object.values(os.networkInterfaces()))
    for (const i of list || []) if (i.family === 'IPv4' && !i.internal) console.log(`  Phone, same Wi-Fi: http://${i.address}:${a.port}${start}`)
  console.log('Stop with Ctrl+C.')
})
