# my-web-world · 小崔Studio 个人主页

一个纯静态个人作品站（音乐 / 视频 / 图库），外加一个**本地专用**的卡片管理台用于维护内容。

> 维护约定：**任何项目结构、模块约定、部署流程的改动，都要同步更新本 README。**

---

## 技术栈

- 纯静态站点：HTML + 原生 CSS/JS，无构建步骤
- 样式：[Tailwind CSS CDN](https://cdn.tailwindcss.com)（`tailwind-config.js` 自定义主题）
- 图标：[lucide UMD 构建](https://cdn.jsdelivr.net/npm/lucide@latest/dist/umd/lucide.min.js)（务必用 UMD 版，`window.lucide` 才存在）
- 音乐播放：原生 `<audio>` + `script.js` 里的 `setupMusicCards()` 控制（单曲互斥、播放/加载/错误三态、进度条可点跳）
- 本地管理台：零依赖 Node.js（`http` + `fs`），不引入任何 npm 包

---

## 目录结构

```
my-web-world/
├── index.html              # 首页：三个模块各取前 8 张卡片聚合展示
├── style.css               # 站点主样式（含 .video-grid 横屏媒体查询）
├── script.js               # 首页模块注入、音乐播放器、交互
├── tailwind-config.js      # Tailwind 自定义配置
├── gallery-detail.html     # 图库详情页（1~3）
├── gallery-detail2.html
├── gallery-detail3.html
├── gallery_generator.py    # 图库相关生成脚本
├── pages/                  # 二级模块页（被首页 fetch 注入）
│   ├── music.html          # 音乐作品（方形卡片）
│   ├── video.html          # 视频作品（竖屏 3:4）
│   └── gallery.html        # 图库
└── admin/                  # 本地卡片管理台（不上线）
    ├── server.js           # Node 零依赖后端，端口 8787
    └── index.html          # 前端管理台（增删改 / 排序 / 批量输入）
```

---

## 本地预览

本站**必须用本地 HTTP 服务器访问**，不能直接双击 `file://` 打开。

```bash
cd my-web-world
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

原因：`index.html` 用 `fetch('pages/...')` 拉取二级页内容再注入，而 `file://` 协议下浏览器会因 CORS 拦截 fetch，导致模块加载不出来（`script.js` 已对 `file:` 协议做友好提示）。

---

## 站点约定（重要）

1. **根相对路径**：`pages/` 内所有引用必须用站点根相对路径（`/style.css`、`/script.js`、`/pages/...`、`/gallery-detail.html` 等），否则独立打开或注入后路径会解析错。
2. **lucide 必须引 UMD 构建**：见上「技术栈」。直接引 `lucide@latest` 会拿到 CJS 版，浏览器里 `window.lucide` 为 undefined，图标不渲染。
3. **`script.js` 第一行禁止裸调用第三方全局**：必须先判空 + try/catch，否则 CDN 一挂整站交互（含音乐播放）全部失效。
4. **自定义样式优先用原生 `<link rel="stylesheet">`**，本地 `file://` 打开常失效的 Tailwind `@import` 写法尽量避免。

---

## 模块说明

### 首页聚合
`index.html` 的三个模块区是空容器 `.module-mount[data-module="video|music|gallery"]`，由 `script.js` 的 `loadHomeModules()` 用 `fetch('pages/<module>.html')` 抽取其中的 `#moduleGrid` 注入，**只取每个模块的前 8 张卡片**（`slice(0,8)`）。注入后重跑 `lucide.createIcons()` 与 `setupMusicCards()`。

新增二级模块页：在 `pages/` 建文件 → 网格容器加 `id="moduleGrid"` → 引用用根相对路径 → 首页会自动拉取。

### 音乐模块（方形卡片）
- 结构：`.music-grid > .music-card`（`aspect-ratio:1/1` 真方形）> `.music-cover` + `.music-info`
- 有源卡片含 `<audio preload="metadata" src="...">`；无音频源的按钮保持 `disabled`
- 音频托管在 file.garden（`https://file.garden/aiKTxQW0TE9uaxk7/music/xxx.mp3`，已开通 CORS）

### 视频模块（竖屏 3:4）
- 作品均为竖屏素材；`.video-frame`（3:4 黑底容器）包 B站 iframe，播放器自适应铺满无黑边
- 网格密度：`grid-cols-2 sm:3 md:4 lg:5 xl:6`，容器 `max-w-[1440px]`
- **横屏**（`@media (orientation: landscape)`）下强制一行 4 个、限宽 1080px 并居中（给网格加 `.video-grid` 类）
- 卡片只保留单行标题（`p-3` + `text-sm truncate`）
- 嵌入格式：`https://player.bilibili.com/player.html?isOutside=true&bvid=xxx&cid=xxx&p=1`（cid 从 `api.bilibili.com/x/web-interface/view?bvid=xxx` 的 `pages[0].cid` 取）
- 横屏素材兜底：给卡片容器加 `.video-frame--wide`（16:9）；无源占位用 `.video-placeholder`

### 图库模块
`pages/gallery.html` + 根目录 `gallery-detail*.html` 详情页，`gallery_generator.py` 辅助生成。

---

## 本地卡片管理台（`admin/`，仅本地使用）

用途：本地维护 `pages/*.html` 的卡片（增删改、排序、批量输入），改完再同步 GitHub / 更新 CloudBase。**这个后台不上线。**

### 启动
```bash
cd my-web-world
node admin/server.js          # 默认端口 8787
# 或指定端口： PORT=9000 node admin/server.js
```
浏览器打开 **http://localhost:8787**。

### 用法
- 顶部标签切换 **音乐 music** / **视频 video**，自动加载对应 `pages/*.html` 当前卡片
- **批量添加**：每行一个，追加到列表末尾
  - music：每行一个 `file.garden` 链接，如 `https://file.garden/aiKTxQW0TE9uaxk7/music/210.mp3`（默认以文件名作标题，可改）
  - video：每行一个 `<iframe src="//player.bilibili.com/player.html?..."></iframe>` 片段，或直接贴 `https://player.bilibili.com/player.html?...`（自动提取 src 并补齐 `https:`）
- **卡片列表**：可改标题 / 链接 / 描述，用 `↑ 上移` `↓ 下移` 排序、`删除` 移除
- **保存写回 pages/**：点「保存写回 pages/」，先自动备份 `.bak` 再写入

### 安全机制
- 保存前自动把旧文件备份为 `pages/<module>.html.bak`
- 写回用 `replaceModuleGrid` 配对替换 `#moduleGrid` 内部内容（保留外层 `<div id="moduleGrid">`），round-trip 无损，不会破坏页面其它结构
- **CloudBase 上线时只传 `pages/` 等正式文件，不要把 `admin/` 目录传上去**——它含本地写盘逻辑，属内部工具，不应暴露到线上

---

## 部署

1. 本地用 `admin/` 管理台改好卡片 → 保存写回 `pages/`
2. 同步 GitHub（仓库 `Quiwizen/ai-space`，本机用 `gsync` alias：pull → add → commit → push）
3. 更新 CloudBase（HTTP 托管，**排除 `admin/` 目录**）

CloudBase 的 HTTP 托管与本地 `python3 -m http.server` 同理，线上不需要本地服务器。

---

## 调试手法

本机没有 Chrome，用 Edge 跑无头验证渲染：

```bash
"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
  --headless=new --disable-gpu --no-sandbox --mute-audio \
  --autoplay-policy=no-user-gesture-required \
  --virtual-time-budget=25000 --dump-dom <url>
```

可用 `--dump-dom` 输出渲染后的 HTML，再用 `grep` 数卡片数量 / 检查关键 class 是否生成。后台服务要用后台方式启动，否则命令结束即被杀。
