'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PAGES_DIR = path.join(ROOT, 'pages');
const PORT = process.env.PORT || 8787;
const FILES = { music: 'music.html', video: 'video.html' };

function sendJson(res, code, obj) {
  res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(obj));
}

function readPage(module) {
  const f = FILES[module];
  if (!f) return null;
  const p = path.join(PAGES_DIR, f);
  if (!fs.existsSync(p)) return null;
  return fs.readFileSync(p, 'utf-8');
}

// 配对替换 #moduleGrid 容器内部内容，保留外层 <div id="moduleGrid"> 与结尾 </div>
function replaceModuleGrid(html, inner) {
  const re = /<div[^>]*\bid="moduleGrid"[^>]*>/;
  const m = html.match(re);
  if (!m) throw new Error('未找到 #moduleGrid');
  const afterStart = m.index + m[0].length;
  let depth = 1;
  const tagRe = /<div\b|<\/div>/gi;
  tagRe.lastIndex = afterStart;
  let mm;
  while ((mm = tagRe.exec(html))) {
    if (mm[0] === '<div') depth++;
    else {
      depth--;
      if (depth === 0) {
        const endIdx = mm.index;
        const trimmed = inner.trim();
        return html.slice(0, afterStart) + '\n' + trimmed + '\n' + html.slice(endIdx);
      }
    }
  }
  throw new Error('#moduleGrid 标签未闭合');
}

const server = http.createServer((req, res) => {
  const url = req.url.split('?')[0];

  // 托管前端管理台
  if (req.method === 'GET' && (url === '/' || url === '/index.html')) {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(fs.readFileSync(path.join(__dirname, 'index.html'), 'utf-8'));
    return;
  }

  // 读取页面原文（用于前端解析）
  if (req.method === 'GET' && url === '/api/raw') {
    const u = new URL(req.url, 'http://localhost');
    const mod = u.searchParams.get('m');
    const html = readPage(mod);
    if (html == null) return sendJson(res, 400, { error: '未知模块或文件不存在' });
    return sendJson(res, 200, { module: mod, html });
  }

  // 保存：接收 gridHtml，替换写回 pages/<module>.html（先备份 .bak）
  if (req.method === 'POST' && url === '/api/save') {
    let body = '';
    req.on('data', c => (body += c));
    req.on('end', () => {
      try {
        const { module, gridHtml } = JSON.parse(body);
        const file = FILES[module];
        if (!file) return sendJson(res, 400, { error: '未知模块' });
        const full = path.join(PAGES_DIR, file);
        const original = fs.readFileSync(full, 'utf-8');
        fs.writeFileSync(full + '.bak', original, 'utf-8'); // 自动备份
        const updated = replaceModuleGrid(original, gridHtml);
        fs.writeFileSync(full, updated, 'utf-8');
        return sendJson(res, 200, { ok: true, module, bak: file + '.bak' });
      } catch (e) {
        return sendJson(res, 500, { error: e.message });
      }
    });
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('Not Found');
});

server.listen(PORT, () => {
  console.log('卡片管理台已启动：http://localhost:' + PORT);
  console.log('管理目录：' + PAGES_DIR);
});
