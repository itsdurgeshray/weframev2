/* PDP Blog · special-section indicator, case expand, narration, reading toolbar */
(() => {
  const d = document, $ = (s, c = d) => c.querySelector(s), $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const FIGMA = d.documentElement.classList.contains('figma');

  /* special section: sliding indicator + swipe between tabs on the stage */
  const tl = $('.sp-tabs');
  if (tl) {
    const ind = $('.sp-ind', tl);
    tl.addEventListener('tabchange', e => ind && ind.style.setProperty('--i', e.detail));
    const stage = $('.sp-stage'); let x0 = null, y0 = null;
    stage.addEventListener('touchstart', e => { if (e.target.closest('.rail')) return; x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
    stage.addEventListener('touchend', e => {
      if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0; x0 = null;
      if (Math.abs(dx) < 50 || Math.abs(dy) > Math.abs(dx)) return;
      const tabs = $$('[role="tab"]', tl), cur = tabs.findIndex(t => t.getAttribute('aria-selected') === 'true');
      const n = Math.max(0, Math.min(tabs.length - 1, cur + (dx < 0 ? 1 : -1))); if (n !== cur) tabs[n].click();
    }, { passive: true });
  }

  /* case study expand */
  $$('[data-expand]').forEach(b => b.addEventListener('click', () => {
    const t = d.getElementById(b.dataset.expand), open = t.classList.toggle('open');
    b.setAttribute('aria-expanded', open); b.firstChild.textContent = open ? 'Show Less ' : 'Read Full Now ';
  }));

  /* narration (Web Speech API when available) */
  const nar = $('[data-narrate]'), art = $('[data-article]');
  if (nar && art) {
    const bars = $$('.wave i', nar), speeds = [1, 1.25, 1.5, 2]; let si = 1, utt = null;
    const sp = $('[data-n-speed]', nar);
    sp.addEventListener('click', () => { si = (si + 1) % speeds.length; $('b', sp).textContent = speeds[si] + 'x'; if (utt) { stop(); play(); } });
    const text = () => art.innerText.replace(/\s+/g, ' ');
    const stop = () => { speechSynthesis.cancel(); nar.classList.remove('playing'); utt = null; };
    const play = () => {
      if (!('speechSynthesis' in window)) { nar.classList.toggle('playing'); return; }
      const t = text(); utt = new SpeechSynthesisUtterance(t); utt.rate = speeds[si]; utt.lang = 'en-GB';
      const v = speechSynthesis.getVoices().find(v => /female|samantha|serena|kate|libby|sonia/i.test(v.name) && /^en/.test(v.lang)); if (v) utt.voice = v;
      utt.onboundary = e => { const p = e.charIndex / t.length; bars.forEach((b, i) => b.classList.toggle('done', i / bars.length < p)); };
      utt.onend = () => { nar.classList.remove('playing'); utt = null; };
      speechSynthesis.cancel(); speechSynthesis.speak(utt); nar.classList.add('playing');
    };
    $('[data-n-play]', nar).addEventListener('click', () => (nar.classList.contains('playing') ? stop() : play()));
  }

  /* reading toolbar */
  const tb = $('[data-toolbar]');
  if (tb && !FIGMA) {
    const ring = $('[data-ring]', tb), pct = $('[data-pct]', tb), left = $('[data-left]', tb);
    const main = $('#article'), hero = $('.pdp-hero'), foot = $('.footer');
    const words = (d.querySelector('main').innerText.match(/\S+/g) || []).length;
    const total = 9; void words;
    const C = 2 * Math.PI * 16;
    const upd = () => {
      const top = Math.max(0, main.offsetTop - innerHeight * .6), end = main.offsetTop + main.offsetHeight - innerHeight * .6;
      const p = Math.min(1, Math.max(0, (scrollY - top) / Math.max(1, end - top)));
      ring.style.strokeDashoffset = C * (1 - p);
      pct.textContent = Math.round(p * 100) + '%';
      const m = Math.max(0, Math.ceil(total * (1 - p))); left.textContent = m ? `${m} min left` : 'Finished';
      tb.classList.toggle('show', scrollY > Math.min(hero.offsetHeight * .35, 360));
    };
    addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true }); addEventListener('resize', upd); upd();

    const btn = $('[data-tools]', tb), menu = $('.tb-menu', tb);
    const close = () => { menu.hidden = true; btn.setAttribute('aria-expanded', false); };
    btn.addEventListener('click', e => { e.stopPropagation(); menu.hidden = !menu.hidden; btn.setAttribute('aria-expanded', !menu.hidden); });
    d.addEventListener('click', e => { if (!tb.contains(e.target)) close(); });
    const toast = m => { const t = d.createElement('div'); t.className = 'toast'; t.textContent = m; d.body.appendChild(t); setTimeout(() => t.remove(), 1800); };
    menu.addEventListener('click', async e => {
      const a = e.target.closest('[data-act]'); if (!a) return; close();
      if (a.dataset.act === 'listen') { nar.scrollIntoView({ behavior: 'smooth', block: 'center' }); $('[data-n-play]', nar).focus(); }
      if (a.dataset.act === 'copy') { try { await navigator.clipboard.writeText(location.href); toast('Link copied'); } catch { toast(location.href); } }
      if (a.dataset.act === 'share') { if (navigator.share) navigator.share({ title: d.title, url: location.href }).catch(() => {}); else { try { await navigator.clipboard.writeText(location.href); toast('Link copied'); } catch {} } }
      if (a.dataset.act === 'top') scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
})();
