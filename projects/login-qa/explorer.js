(() => {
  'use strict';
  const data = window.LOGIN_QA_DATA;
  if (!data) return;
  const $ = id => document.getElementById(id);
  const esc = v => String(v ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const field = (label, value) => `<div class="qa-field"><span class="qa-field-label">${esc(label)}</span><p class="qa-field-text">${esc(value || '—')}</p></div>`;
  const reqName = id => data.traces.find(r => r.id === id)?.name || '';
  const reqOptions = data.traces.map(r => `<option value="${esc(r.id)}">${esc(r.id)} · ${esc(r.name)}</option>`).join('');
  $('analysis-req').insertAdjacentHTML('beforeend', reqOptions);
  $('tc-req').insertAdjacentHTML('beforeend', reqOptions);
  const outcomes = [...new Set(data.testCases.map(t => t.result).filter(Boolean))];
  $('tc-result').insertAdjacentHTML('beforeend', outcomes.map(o => `<option value="${esc(o)}">${esc(o)}</option>`).join(''));
  const inText = (query, ...values) => values.join(' ').toLocaleLowerCase().includes(query);

  function renderAnalysis() {
    const q = $('analysis-search').value.trim().toLocaleLowerCase();
    const r = $('analysis-req').value;
    const rows = data.analysis.filter(a => (!r || a.req === r) && inText(q, a.req, reqName(a.req), a.question, a.reason, a.answer, a.status));
    $('analysis-count').textContent = `총 ${data.analysis.length}건 중 ${rows.length}건 표시 · 항목을 눌러 상세 확인`;
    $('analysis-results').innerHTML = rows.map(a => `<details class="qa-details"><summary><span><span class="qa-item-kicker">${esc(a.req)} · 추가 확인 ${esc(a.number)} · ${esc(reqName(a.req))}</span><span class="qa-item-title">${esc(a.question)}</span><span class="qa-item-sub">${esc(a.status)}</span></span></summary><div class="qa-detail-body">${field('확인이 필요한 이유',a.reason)}${field('가상 기획자 답변 · 분석서 원문',a.answer)}</div></details>`).join('') || '<p class="qa-none">검색 조건과 일치하는 분석 항목이 없습니다.</p>';
  }
  function renderTests() {
    const q=$('tc-search').value.trim().toLocaleLowerCase(), req=$('tc-req').value, status=$('tc-result').value;
    const rows=data.testCases.filter(t => (!req || t.req.includes(req)) && (!status || t.result === status) && inText(q,t.id,...t.req,t.major,t.middle,t.minor,t.purpose,t.prereq,t.data,t.steps,t.expected,t.actual,t.result,t.notes));
    $('tc-count').textContent=`총 ${data.testCases.length}건 중 ${rows.length}건 표시 · 항목을 눌러 실행 기록 확인`;
    $('tc-results').innerHTML=rows.map(t=>`<details class="qa-details" id="${esc(t.id)}"><summary><span><span class="qa-item-kicker">${esc(t.id)} · ${esc(t.req.join(', '))}<span class="qa-badge">${esc(t.result || '미기록')}</span></span><span class="qa-item-title">${esc(t.purpose)}</span><span class="qa-item-sub">${esc([t.middle,t.minor].filter(Boolean).join(' / '))}</span></span></summary><div class="qa-detail-body">${field('사전 조건',t.prereq)}${field('테스트 데이터 · 실습용',t.data)}${field('테스트 절차',t.steps)}${field('기대 결과',t.expected)}${field('실제 결과 · 원본 기록',t.actual)}${field('테스트 결과',t.result)}${t.notes ? field('비고',t.notes) : ''}</div></details>`).join('') || '<p class="qa-none">검색 조건과 일치하는 테스트 케이스가 없습니다.</p>';
  }
  function renderTrace() {
    $('trace-rows').innerHTML=data.traces.map(t=>`<tr><td><button type="button" class="trace-pick" data-req="${esc(t.id)}">${esc(t.id)} ↗</button></td><td>${esc(t.name)}</td><td>${esc(t.questions)}건</td><td class="trace-ids">${esc(t.testIds.join(' · ') || '—')}</td><td>${esc(t.testIds.length)}건</td></tr>`).join('');
    $('trace-rows').addEventListener('click',e=>{
      const b=e.target.closest('button[data-req]'); if(!b)return;
      $('tc-req').value=b.dataset.req; $('tc-search').value=''; $('tc-result').value=''; renderTests();
      $('test-cases').scrollIntoView({behavior:'smooth',block:'start'});
    });
  }
  ['analysis-search','analysis-req'].forEach(id=>$(id).addEventListener('input',renderAnalysis));
  ['tc-search','tc-req','tc-result'].forEach(id=>$(id).addEventListener('input',renderTests));
  renderAnalysis(); renderTests(); renderTrace();
})();
