# 项目长期约定（my-web-world 个人主页）

## 前端资源引用

- **lucide 图标必须引 UMD 构建**：`https://cdn.jsdelivr.net/npm/lucide@latest/dist/umd/lucide.min.js`。
  直接引 `lucide@latest` 会拿到 CJS 版（`dist/cjs/lucide.js`），浏览器里 `window.lucide` 为 undefined。
- **`script.js` 第一行禁止裸调用第三方全局**。必须先判空 + try/catch，否则 CDN 一挂，整站交互（含音乐播放）全部失效。
- 自定义样式优先用原生 `<link rel="stylesheet">`，不要用 `<style type="text/tailwindcss">@import "style.css";</style>`（本地 file:// 打开时常失效）。

## 音乐模块（方形卡片）

- 结构：`.music-grid` > `.music-card`（`aspect-ratio:1/1` 真方形）> `.music-cover` + `.music-info`。
- 播放逻辑集中在 `script.js` 的 `setupMusicCards()`：单曲互斥、`is-playing`/`is-loading`/`is-error` 三态、进度条可点跳。
- **新增曲目**：复制一个 `.music-card` 块并填 `<audio src>` 即可，JS 自动接管；无音频源的按钮保持 `disabled`。
- 音频托管在 file.garden（`https://file.garden/aiKTxQW0TE9uaxk7/music/xxx.mp3`），已开通 CORS。

## 视频模块（竖屏 3:4）

- 作品均为竖屏素材；`.video-frame`（3:4 黑底容器）包 B站 iframe，播放器自适应铺满无黑边。
- 网格密度：`grid-cols-2 sm:3 md:4 lg:5 xl:6 gap-4`，容器 `max-w-[1440px]`；1440 视口下单卡约 215×330、一屏约 2.4 行。
- 卡片只保留单行标题（`p-3` + `text-sm truncate`），不再放「作品简介 · 创作主题」。
- **B站外链播放器自适应容器比例**，横竖由页面容器决定；查素材原始比例用 `api.bilibili.com/x/web-interface/view?bvid=xxx` 的 `dimension`。
- 将来若有横屏素材，给该卡片容器加 `.video-frame--wide`（16:9）兜底；无源占位用 `.video-placeholder`。
- 嵌入格式：`https://player.bilibili.com/player.html?isOutside=true&bvid=xxx&cid=xxx&p=1`，cid 可从 view 接口 `pages[0].cid` 取。

## 调试手法

- 本机没有 Chrome，用 Edge 跑无头：`"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" --headless=new --disable-gpu --no-sandbox --mute-audio --autoplay-policy=no-user-gesture-required --virtual-time-budget=25000 --dump-dom <url>`。
- 页面内用 `fetch('/__result?d='+JSON.stringify(state))` 把调试状态写进 `python3 -m http.server` 的日志再读取；后台服务要用 run_in_background 启动，否则命令结束即被杀。
