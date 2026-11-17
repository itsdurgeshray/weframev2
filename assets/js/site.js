/* Weframe Tech v2 · shared behaviour */
(() => {
  const d = document, root = d.documentElement;
  const FIGMA = new URLSearchParams(location.search).has('figma');
  if (FIGMA) { root.classList.add('figma'); d.addEventListener('DOMContentLoaded', () => d.querySelectorAll('img[loading]').forEach(i => i.loading = 'eager')); }
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = d) => c.querySelector(s), $$ = (s, c = d) => [...c.querySelectorAll(s)];

  /* nav: scrolled state + mobile sheet */
  const nav = $('.nav');
  const onScroll = () => nav && nav.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const menuBtn = $('.menu-btn');
  const setMenu = open => {
    d.body.classList.toggle('menu-open', open);
    menuBtn && menuBtn.setAttribute('aria-expanded', open);
    d.body.style.overflow = open ? 'hidden' : '';
  };
  menuBtn && menuBtn.addEventListener('click', () => setMenu(!d.body.classList.contains('menu-open')));
  $$('.sheet a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
  addEventListener('resize', () => { if (innerWidth >= 1024) setMenu(false); });

  /* reveal */
  if (!FIGMA && !reduce && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
    $$('.rv').forEach(el => io.observe(el));
  } else $$('.rv').forEach(el => el.classList.add('in'));

  /* rails: arrows + dots */
  $$('[data-rail]').forEach(rail => {
    const group = rail.closest('[data-rail-group]') || rail.parentElement;
    const prev = $('[data-prev]', group), next = $('[data-next]', group), dots = $('[data-dots]', group);
    const items = [...rail.children];
    const step = () => (items[1] ? items[1].offsetLeft - items[0].offsetLeft : rail.clientWidth);
    prev && prev.addEventListener('click', () => rail.scrollBy({ left: -step(), behavior: 'smooth' }));
    next && next.addEventListener('click', () => rail.scrollBy({ left: step(), behavior: 'smooth' }));
    if (dots) dots.innerHTML = items.map(() => '<i></i>').join('');
    const upd = () => {
      const max = rail.scrollWidth - rail.clientWidth - 2;
      prev && (prev.disabled = rail.scrollLeft <= 2);
      next && (next.disabled = rail.scrollLeft >= max);
      if (dots) {
        const c = rail.scrollLeft + 1;
        let idx = items.findIndex(it => it.offsetLeft - items[0].offsetLeft + it.offsetWidth / 2 > c);
        if (rail.scrollLeft >= max) idx = items.length - 1;
        [...dots.children].forEach((dt, i) => dt.classList.toggle('on', i === Math.max(0, idx)));
      }
      rail.dispatchEvent(new CustomEvent('railchange'));
    };
    rail.addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true });
    addEventListener('resize', upd); upd();
    rail._go = i => rail.scrollTo({ left: items[i].offsetLeft - items[0].offsetLeft, behavior: 'smooth' });
    if (dots) [...dots.children].forEach((dt, i) => dt.addEventListener('click', () => rail._go(i)));
  });

  /* center-start rails (hero): scroll so the item marked data-start is centred */
  $$('[data-rail][data-center]').forEach(rail => {
    const it = rail.querySelector('[data-start]'); if (!it) return;
    const go = () => { rail.scrollLeft = it.offsetLeft - (rail.clientWidth - it.offsetWidth) / 2; };
    go(); addEventListener('load', go);
  });

  /* tabs */
  $$('[data-tabs]').forEach(tl => {
    const tabs = $$('[role="tab"]', tl);
    const sel = t => {
      tabs.forEach(x => {
        const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
        const p = d.getElementById(x.getAttribute('aria-controls')); if (p) p.hidden = !on;
      });
      tl.dispatchEvent(new CustomEvent('tabchange', { detail: tabs.indexOf(t) }));
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => { sel(t); const sc = t.parentElement; if (sc.scrollWidth > sc.clientWidth) sc.scrollTo({ left: t.offsetLeft - (sc.clientWidth - t.offsetWidth) / 2, behavior: 'smooth' }); });
      t.addEventListener('keydown', e => {
        const k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (k) { const n = tabs[(i + k + tabs.length) % tabs.length]; n.focus(); sel(n); }
      });
    });
    tl._select = i => sel(tabs[i]);
  });

  /* comparison switch (mobile) */
  $$('[data-cmp]').forEach(box => {
    const btns = $$('.cmp-switch button', box);
    btns.forEach(b => b.addEventListener('click', () => {
      btns.forEach(x => x.setAttribute('aria-pressed', x === b));
      $$('[data-them]', box).forEach(el => { el.textContent = el.dataset[b.dataset.k]; });
      $$('[data-them-label]', box).forEach(el => { el.textContent = b.textContent; });
    }));
  });

  /* lite youtube */
  $$('.yt[data-yt]').forEach(a => a.addEventListener('click', e => {
    if (FIGMA) return; e.preventDefault();
    const f = d.createElement('iframe');
    f.src = `https://www.youtube-nocookie.com/embed/${a.dataset.yt}?autoplay=1&rel=0`;
    f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen = true; f.title = a.getAttribute('aria-label') || 'Video';
    a.appendChild(f);
  }));

  /* read more */
  $$('[data-more]').forEach(b => b.addEventListener('click', () => {
    const t = d.getElementById(b.dataset.more); const open = t.classList.toggle('open');
    t.style.webkitLineClamp = open ? 'unset' : ''; b.textContent = open ? 'Show less' : 'Read more';
  }));

  /* ask chips fill input */
  $$('[data-ask]').forEach(form => {
    const inp = $('input', form);
    $$('[data-q]', form.closest('[data-ask-scope]') || form.parentElement).forEach(c => c.addEventListener('click', () => { inp.value = c.dataset.q || c.textContent.trim(); inp.focus(); }));
    form.addEventListener('submit', e => e.preventDefault());
  });

  /* mobile dock */
  const dock = $('.dock');
  if (dock && !FIGMA) {
    const after = $(dock.dataset.after || '.hero'), foot = $('.footer');
    const upd = () => {
      const past = after ? after.getBoundingClientRect().bottom < 40 : scrollY > 400;
      const nearFoot = foot ? foot.getBoundingClientRect().top < innerHeight - 40 : false;
      dock.classList.toggle('show', past && !nearFoot);
    };
    addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true }); upd();
  }
})();
