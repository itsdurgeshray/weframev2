/* Home · tech stack wheel, matched to the live build:
   the ring rotates so the active slice sits at 12 o'clock (always forward, cumulative),
   the badge stays fixed, autoplay every 3.5s, paused on hover / off-screen, click jumps and autoplay continues. */
(() => {
  const d = document, wrap = d.querySelector('[data-wheel]'), DATA = window.WF_STACK;
  if (!wrap || !DATA) return;
  const FIGMA = d.documentElement.classList.contains('figma');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ring = wrap.querySelector('[data-ring]'), segs = [...wrap.querySelectorAll('.seg-g')];
  const badge = wrap.querySelector('[data-w-badge]'), swap = wrap.querySelector('[data-w-swap]');
  const title = wrap.querySelector('[data-w-title]'), list = wrap.querySelector('[data-w-icons]');
  const n = DATA.cats.length, STEP = 360 / n, DELAY = 3500;
  let cur = 0, angle = 0, timer = null, hover = false, visible = false, swapT = null, badgeT = null;

  const render = i => {
    const c = DATA.cats[i];
    title.textContent = c.n;
    list.setAttribute('aria-label', `${c.n} technologies`);
    list.style.gridTemplateColumns = `repeat(${c.items.length},max-content)`;
    list.innerHTML = c.items.map(t => `<li>${DATA.icons[t]}<span class="sr-only">${t}</span></li>`).join('');
  };

  const go = i => {
    if (i === cur) return;
    angle -= STEP * ((i - cur + n) % n);           // always rotate forward, never unwind
    cur = i;
    ring.style.transform = `rotate(${angle}deg)`;
    segs.forEach((s, k) => s.setAttribute('aria-pressed', k === i));
    if (reduce) { render(i); badge.innerHTML = DATA.cats[i].badge; return; }
    clearTimeout(swapT); clearTimeout(badgeT);
    swap.classList.add('out'); badge.classList.add('out');
    swapT = setTimeout(() => {
      render(i); swap.classList.remove('out'); swap.classList.add('pre');
      void swap.offsetWidth; swap.classList.remove('pre');
    }, 300);
    badgeT = setTimeout(() => { badge.innerHTML = DATA.cats[i].badge; badge.classList.remove('out'); }, 350);
  };

  const stop = () => { clearTimeout(timer); timer = null; };
  const play = () => {
    stop();
    if (FIGMA || reduce || hover || !visible || d.hidden) return;
    timer = setTimeout(() => { go((cur + 1) % n); play(); }, DELAY);
  };

  segs.forEach((s, i) => {
    s.addEventListener('click', () => { go(i); play(); });
    s.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(i); play(); } });
  });
  wrap.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') { hover = true; stop(); } });
  wrap.addEventListener('pointerleave', e => { if (e.pointerType === 'mouse') { hover = false; play(); } });
  d.addEventListener('visibilitychange', play);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(es => { visible = es[0].isIntersecting; play(); }, { threshold: .25 }).observe(wrap);
  } else { visible = true; play(); }
})();
