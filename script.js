// 图标库加载失败不能影响后续脚本（曾因 CDN 返回 CJS 包导致整个文件中断）
try {
  if (typeof lucide !== 'undefined' && typeof lucide.createIcons === 'function') {
    lucide.createIcons();
  } else {
    console.warn('[icons] lucide 未就绪，跳过图标渲染');
  }
} catch (e) {
  console.warn('[icons] lucide 初始化失败：', e);
}

const nav = document.querySelector('nav');
window.addEventListener('scroll', () => {
  if (window.scrollY > 60) {
    nav.classList.add('shadow-hover');
  } else {
    nav.classList.remove('shadow-hover');
  }
});

function setupToggle(toggleId, hiddenClass) {
  const toggle = document.getElementById(toggleId);
  const hiddenItems = document.querySelectorAll('.' + hiddenClass);
  toggle?.addEventListener('click', () => {
    hiddenItems.forEach(item => {
      item.classList.toggle('show');
    });
    const span = toggle.querySelector('span');
    const icon = toggle.querySelector('i');
    if (span && icon) {
      if (hiddenItems[0]?.classList.contains('show')) {
        span.textContent = '收起';
        icon.classList.add('rotate-180');
      } else {
        span.textContent = '查看更多';
        icon.classList.remove('rotate-180');
      }
    }
  });
}

setupToggle('galleryToggle', 'gallery-hidden');
setupToggle('videoToggle', 'video-hidden');
setupToggle('musicToggle', 'music-hidden');

/* ===== 方形音乐卡片播放控制 ===== */
function formatTime(sec) {
  if (!isFinite(sec)) return '00:00';
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
}

function setupMusicCards() {
  const cards = document.querySelectorAll('.music-card');
  if (!cards.length) return;

  cards.forEach(card => {
    const audio = card.querySelector('audio');
    const btn = card.querySelector('.music-play-btn');
    const bar = card.querySelector('.music-progress-bar');
    const progress = card.querySelector('.music-progress');
    const timeEl = card.querySelector('.music-time');
    if (!audio || !btn) return;

    const setError = msg => {
      card.classList.remove('is-playing', 'is-loading');
      card.classList.add('is-error');
      if (timeEl) timeEl.textContent = msg;
      console.error('[music] ' + msg + '：' + (audio.currentSrc || audio.src));
    };
    const clearError = () => card.classList.remove('is-error');

    btn.addEventListener('click', () => {
      // 同一时间只播放一首
      cards.forEach(other => {
        if (other === card) return;
        const otherAudio = other.querySelector('audio');
        if (otherAudio && !otherAudio.paused) {
          otherAudio.pause();
        }
        other.classList.remove('is-playing');
      });
      if (audio.paused) {
        clearError();
        card.classList.add('is-loading');
        const p = audio.play();
        if (p && typeof p.catch === 'function') {
          p.catch(err => {
            console.error('[music] 播放失败：', err);
            setError('播放失败');
          });
        }
      } else {
        audio.pause();
      }
    });

    audio.addEventListener('loadedmetadata', () => {
      if (timeEl && audio.paused) timeEl.textContent = formatTime(audio.duration);
    });
    audio.addEventListener('error', () => setError('加载失败'));
    audio.addEventListener('play', () => card.classList.add('is-playing'));
    audio.addEventListener('playing', () => {
      card.classList.remove('is-loading');
      card.classList.add('is-playing');
    });
    audio.addEventListener('waiting', () => card.classList.add('is-loading'));
    audio.addEventListener('pause', () => card.classList.remove('is-playing'));
    audio.addEventListener('ended', () => {
      card.classList.remove('is-playing', 'is-loading');
      if (bar) bar.style.width = '0%';
      if (timeEl) timeEl.textContent = '00:00';
    });
    audio.addEventListener('timeupdate', () => {
      if (!audio.duration) return;
      if (bar) bar.style.width = (audio.currentTime / audio.duration * 100) + '%';
      if (timeEl) timeEl.textContent = formatTime(audio.currentTime);
    });

    progress?.addEventListener('click', e => {
      if (!audio.duration) return;
      const rect = progress.getBoundingClientRect();
      audio.currentTime = ((e.clientX - rect.left) / rect.width) * audio.duration;
    });
  });
}

setupMusicCards();

/* ===== 首页模块：从 pages/ 拉取二级页面内容并注入对应区块 ===== */
function injectModule(mount) {
  const name = mount.getAttribute('data-module');
  const url = 'pages/' + name + '.html';
  return fetch(url)
    .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
    .then(html => {
      const doc = new DOMParser().parseFromString(html, 'text/html');
      const grid = doc.getElementById('moduleGrid');
      if (!grid) throw new Error('未找到 #moduleGrid');
      // 首页只展示每个模块的前 8 个卡片
      const items = Array.from(grid.children).slice(0, 8);
      grid.innerHTML = '';
      items.forEach(it => grid.appendChild(it));
      grid.removeAttribute('id');
      mount.innerHTML = '';
      mount.appendChild(document.importNode(grid, true));
    });
}

function loadHomeModules() {
  const mounts = Array.from(document.querySelectorAll('.module-mount'));
  if (!mounts.length) return;

  if (location.protocol === 'file:') {
    mounts.forEach(m => {
      m.innerHTML = '<p class="col-span-full text-center text-neutral-500 text-sm py-10">请通过本地服务器打开本页（终端运行 ' +
        '<code>python3 -m http.server</code> 后访问 http://localhost:8000），直接双击文件无法加载模块内容。</p>';
    });
    return;
  }

  Promise.all(mounts.map(injectModule))
    .then(() => {
      try { if (typeof lucide !== 'undefined' && typeof lucide.createIcons === 'function') lucide.createIcons(); } catch (e) {}
      setupMusicCards();
    })
    .catch(err => {
      console.error('[home] 模块加载失败：', err);
      mounts.forEach(m => {
        if (!m.children.length) {
          m.innerHTML = '<p class="col-span-full text-center text-neutral-500 text-sm py-10">模块加载失败，请确认 pages/ 目录存在并通过本地服务器访问。</p>';
        }
      });
    });
}

loadHomeModules();