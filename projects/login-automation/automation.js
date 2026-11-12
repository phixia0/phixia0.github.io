(() => {
  const search = document.getElementById('auto-search');
  const group = document.getElementById('auto-group');
  const rows = [...document.querySelectorAll('.auto-tc-table tbody tr')];
  const count = document.getElementById('auto-count');
  const render = () => {
    const q = search.value.trim().toLowerCase();
    const g = group.value;
    let visible = 0;
    for (const row of rows) {
      const ok = (!g || row.dataset.group === g) && (!q || row.dataset.q.includes(q));
      row.hidden = !ok;
      if (ok) visible++;
    }
    count.textContent = `${visible}건 표시 / 전체 34건`;
  };
  search.addEventListener('input', render);
  group.addEventListener('change', render);
  render();
  for (const btn of document.querySelectorAll('[data-copy]')) {
    btn.addEventListener('click', async () => {
      const el = document.getElementById(btn.dataset.copy);
      try {
        await navigator.clipboard.writeText(el.textContent);
        btn.textContent = '복사 완료';
        setTimeout(() => btn.textContent = '코드 복사', 1400);
      } catch { btn.textContent = '선택 후 복사'; }
    });
  }
})();
