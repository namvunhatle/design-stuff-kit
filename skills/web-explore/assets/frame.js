// web-explore device frames: adds the status bar, camera, and home indicator to
// every <section class="screen">, wraps it in a captioned figure, and freezes
// animations for storyboard frames. Load at the end of <body>, after frame.css.
(() => {
  const fallback = window.__wxDevice || document.documentElement.dataset.device || 'ios'
  const icons = {
    ios:
      '<svg width="18" height="12" viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></svg>' +
      '<svg width="16" height="12" viewBox="0 0 16 12"><path d="M8 2.6c2.3 0 4.4.9 6 2.4l1.3-1.4A10.4 10.4 0 0 0 8 .7 10.4 10.4 0 0 0 .7 3.6L2 5c1.6-1.5 3.7-2.4 6-2.4Zm0 3.8c1.3 0 2.5.5 3.4 1.3l1.3-1.4A6.8 6.8 0 0 0 8 4.5a6.8 6.8 0 0 0-4.7 1.8l1.3 1.4C5.5 6.9 6.7 6.4 8 6.4Zm0 3.8 2-2.1a3 3 0 0 0-4 0l2 2.1Z"/></svg>' +
      '<svg width="27" height="13" viewBox="0 0 27 13"><rect x=".5" y=".5" width="23" height="12" rx="3.5" fill="none" stroke="currentColor" opacity=".4"/><rect x="2" y="2" width="20" height="9" rx="2"/><path d="M25 4.5v4c.8-.3 1.3-1.1 1.3-2s-.5-1.7-1.3-2Z" opacity=".4"/></svg>',
    android:
      '<svg width="16" height="16" viewBox="0 0 16 16"><path d="M8 13.5 15.5 4A12 12 0 0 0 .5 4L8 13.5Z"/></svg>' +
      '<svg width="14" height="14" viewBox="0 0 14 14"><path d="M14 0v14H0L14 0Z"/></svg>' +
      '<svg width="9" height="15" viewBox="0 0 9 15"><path d="M3 0h3v1.5h2a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1V2.5a1 1 0 0 1 1-1h2V0Z"/></svg>',
  }

  for (const screen of document.querySelectorAll('section.screen')) {
    if (!screen.dataset.device) screen.dataset.device = fallback
    const device = screen.dataset.device === 'android' ? 'android' : 'ios'

    if (screen.dataset.chrome !== 'none') {
      const status = document.createElement('div')
      status.className = 'wx-status'
      status.setAttribute('aria-hidden', 'true')
      status.innerHTML = `<span>${screen.dataset.time || (device === 'ios' ? '9:41' : '12:30')}</span><span class="wx-island"></span><span class="wx-icons">${icons[device]}</span>`
      const home = document.createElement('div')
      home.className = 'wx-home'
      home.setAttribute('aria-hidden', 'true')
      screen.prepend(status)
      screen.append(home)
    }

    if (!screen.parentElement.classList.contains('wx-fig')) {
      const fig = document.createElement('figure')
      fig.className = 'wx-fig'
      screen.replaceWith(fig)
      const caption = document.createElement('figcaption')
      caption.textContent = screen.dataset.name || ''
      fig.append(screen, caption)
    }
  }

  // Storyboard frames: pause every animation inside the screen at data-freeze ms.
  const freeze = () => {
    for (const screen of document.querySelectorAll('section.screen[data-freeze]')) {
      const at = Number(screen.dataset.freeze)
      for (const anim of document.getAnimations()) {
        const target = anim.effect && anim.effect.target
        if (target && screen.contains(target)) {
          anim.currentTime = at
          anim.pause()
        }
      }
    }
  }
  requestAnimationFrame(freeze)
  window.__wxFreeze = freeze
})()
