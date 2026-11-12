const grid = document.getElementById('project-grid');
const filters = document.querySelectorAll('.filter');
const recordLabels = {
  manual: {label: 'MANUAL TESTING', code: '01', glyph: 'M', ornament: '43'},
  automation: {label: 'TEST AUTOMATION', code: '02', glyph: 'A', ornament: '34'},
  defect: {label: 'DEFECT SIMULATION', code: '03', glyph: 'D', ornament: '02'},
  learning: {label: 'LEARNING JOURNAL', code: '04', glyph: 'S', ornament: '↗'}
};

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]);
}

function renderProjects(category = 'all') {
  const projects = window.PORTFOLIO_PROJECTS.filter(item => category === 'all' || item.category === category);
  grid.innerHTML = projects.length ? projects.map(project => {
    const type = recordLabels[project.category] || recordLabels.learning;
    const name = escapeHTML(project.title);
    const status = escapeHTML(project.status);
    const link = project.link ? escapeHTML(project.link) : '';
    const isReady = Boolean(link);
    const title = isReady ? `<a class="record-title-link" href="${link}">${name}<span aria-hidden="true">↗</span></a>` : name;
    const action = isReady ? `<a class="record-open" href="${link}" aria-label="${name} 상세 기록 보기">기록 열람 <span aria-hidden="true">↗</span></a>` : '<span class="record-open record-open-disabled">기록 준비 중 <span aria-hidden="true">·</span></span>';
    return `<article class="record-row record-${escapeHTML(project.category)}">
      <div class="record-index"><span class="record-sequence">${escapeHTML(project.number)}<small> / 04</small></span><span class="record-rail" aria-hidden="true"></span></div>
      <div class="record-main">
        <div class="record-type"><span class="record-type-dot"></span>${escapeHTML(type.label)}<span class="record-status">${status}</span></div>
        <h3>${title}</h3>
        <p class="record-desc">${escapeHTML(project.description)}</p>
        <div class="record-tags">${project.tags.map(tag => `<span>${escapeHTML(tag)}</span>`).join('')}</div>
      </div>
      <div class="record-aside" aria-hidden="true"><div class="record-symbol"><span>${escapeHTML(type.ornament)}</span><i>${escapeHTML(type.glyph)}</i></div></div>
      <div class="record-tail">${action}</div>
    </article>`;
  }).join('') : '<p class="empty">이 분류의 기록은 아직 없습니다.</p>';
}

filters.forEach(button => button.addEventListener('click', () => {
  filters.forEach(item => { item.classList.remove('active'); item.setAttribute('aria-pressed', 'false'); });
  button.classList.add('active');
  button.setAttribute('aria-pressed', 'true');
  renderProjects(button.dataset.filter);
}));

const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
menuButton.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
});
nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  nav.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
}));

if (window.GITHUB_USERNAME) {
  const link = document.getElementById('github-link');
  link.href = `https://github.com/${encodeURIComponent(window.GITHUB_USERNAME)}`;
  link.textContent = 'GitHub 프로필 보기 ↗';
  link.removeAttribute('aria-disabled');
}
document.getElementById('year').textContent = new Date().getFullYear();
renderProjects();
