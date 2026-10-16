'use strict';
const descriptions = {
  before: 'Before: the small table font remains active in the body.',
  after: 'After: the table stays compact and the body returns to its normal font.'
};
for (const button of document.querySelectorAll('[data-state]')) {
  button.addEventListener('click', () => {
    const state = button.dataset.state;
    for (const other of document.querySelectorAll('[data-state]')) other.setAttribute('aria-pressed', String(other === button));
    const image = document.querySelector('#demo-image');
    image.src = `assets/demo-${state}.webp`;
    image.alt = descriptions[state];
    document.querySelector('#demo-filename').textContent = `${state}.pdf`;
    document.querySelector('#demo-description').textContent = descriptions[state];
  });
}
const prefix = 'git clone https://github.com/Yunbo-max/Resubmit.git\ncd Resubmit\n';
for (const button of document.querySelectorAll('[data-agent]')) {
  button.addEventListener('click', () => {
    const agent = button.dataset.agent;
    for (const other of document.querySelectorAll('[data-agent]')) other.setAttribute('aria-pressed', String(other === button));
    document.querySelector('#install-command').textContent = `${prefix}python scripts/install_skill.py --agent ${agent} --skill selecting-conference-venues\npython scripts/install_skill.py --agent ${agent} --skill resubmitting-papers`;
    document.querySelector('#install-note').textContent = `Installs both skill folders under ~/.${agent === 'codex' ? 'agents' : 'claude'}/skills/. Remove either command to install just one. Existing installations are never overwritten.`;
    document.querySelector('#copy-status').textContent = '';
  });
}
document.querySelector('#copy-install').addEventListener('click', async () => {
  const text = document.querySelector('#install-command').textContent;
  try {
    if (!navigator.clipboard) throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText(text);
    document.querySelector('#copy-status').textContent = 'Copied. Review the commands before running them.';
  } catch (_) {
    document.querySelector('#copy-status').textContent = 'Clipboard unavailable here. Select and copy the commands above.';
  }
});
