lucide.createIcons();

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