const grid = document.getElementById('project-grid');
const filters = document.querySelectorAll('.filter');
const visualClasses = { manual: '', automation: 'art-automation', learning: 'art-learning' };

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]);
}

function renderProjects(category = 'all') {
  const projects = window.PORTFOLIO_PROJECTS.filter(item => category === 'all' || item.category === category);
  grid.innerHTML = projects.length ? projects.map(project => {
    const name = escapeHTML(project.title);
    const status = escapeHTML(project.status);
    const link = project.link ? `<a class="card-link" href="${escapeHTML(project.link)}" target="_blank" rel="noopener noreferrer">자세히 보기 ↗</a>` : '<span class="card-link" style="color:#929a9e;border-color:#ccd0d1">기록 준비 중 ↗</span>';
    return `<article class="project-card">
      <div class="project-art ${visualClasses[project.category] || ''}"><span class="art-code">TH QA LAB / ${escapeHTML(project.english)}</span><div class="art-label">${project.artwork}</div><span class="art-index">${escapeHTML(project.number)} / 03</span></div>
      <div class="card-body"><div class="card-meta"><span>${escapeHTML(project.english)}</span><span class="badge ${project.status === '예정' ? 'planned' : ''}">${status}</span></div>
      <h3>${name}</h3><p>${escapeHTML(project.description)}</p><div class="card-bottom"><div class="tags">${project.tags.map(tag => `<span>${escapeHTML(tag)}</span>`).join('')}</div>${link}</div></div>
    </article>`;
  }).join('') : '<p class="empty">이 분류의 프로젝트는 아직 없습니다.</p>';
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
