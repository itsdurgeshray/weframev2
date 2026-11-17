/* Expertise page · plan switcher synced with the pricing rail (mobile) */
(() => {
  const d = document, rail = d.querySelector('.pricing'), btns = [...d.querySelectorAll('.price-seg [data-go]')];
  if (!rail || !btns.length) return;
  const items = [...rail.children];
  const go = i => rail.scrollTo({ left: items[i].offsetLeft - (rail.clientWidth - items[i].offsetWidth) / 2, behavior: 'smooth' });
  btns.forEach(b => b.addEventListener('click', () => go(+b.dataset.go)));
  const sync = () => {
    const c = rail.scrollLeft + rail.clientWidth / 2;
    let best = 0, dist = Infinity;
    items.forEach((it, i) => { const m = it.offsetLeft + it.offsetWidth / 2, dd = Math.abs(m - c); if (dd < dist) { dist = dd; best = i; } });
    btns.forEach((b, i) => b.setAttribute('aria-pressed', i === best));
  };
  rail.addEventListener('scroll', () => requestAnimationFrame(sync), { passive: true });
  addEventListener('load', sync); sync();
})();
