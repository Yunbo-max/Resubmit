'use strict';
(() => {
  const root = document.getElementById('revision');
  const image = document.getElementById('revision-image');
  const play = document.getElementById('play-demo');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let timer = null;
  function stop() {
    if (timer !== null) window.clearInterval(timer);
    timer = null;
    document.body.classList.remove('playing');
    play.textContent = 'Play comparison';
    play.setAttribute('aria-pressed', 'false');
  }
  function setMode(mode) {
    if (!['before', 'after'].includes(mode)) return;
    root.dataset.mode = mode;
    image.src = image.dataset[`${mode}Src`];
    image.alt = mode === 'before'
      ? 'Before the scoped fix: the table font remains active in the following body paragraphs.'
      : 'After the scoped fix: body text returns to its normal size while the table stays compact.';
    document.getElementById('revision-filename').textContent = `${mode}.pdf`;
    document.getElementById('revision-status').textContent = mode === 'before'
      ? 'Before: the smaller font continues into the body.'
      : 'After: the body returns to its normal font.';
    root.querySelectorAll('button[data-mode]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.mode === mode));
    });
  }
  root.querySelectorAll('button[data-mode]').forEach(button => {
    button.addEventListener('click', () => { stop(); setMode(button.dataset.mode); });
  });
  play.addEventListener('click', () => {
    if (timer !== null) { stop(); return; }
    if (reduced.matches) {
      setMode(root.dataset.mode === 'before' ? 'after' : 'before');
      return;
    }
    document.body.classList.add('playing');
    play.textContent = 'Pause comparison';
    play.setAttribute('aria-pressed', 'true');
    timer = window.setInterval(() => setMode(root.dataset.mode === 'before' ? 'after' : 'before'), 2800);
  });
  reduced.addEventListener('change', stop);
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
})();
