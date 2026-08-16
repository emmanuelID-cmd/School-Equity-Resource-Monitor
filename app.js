import './shared-header.js';

const initialCursor = new URLSearchParams(window.location.search).get('cursor');
const state = { schools: [], total: 0, selected: null, selectedSchool: null, cursor: initialCursor, hasMore: true, loading: false, gapThreshold: 'all' };
const $ = (id) => document.getElementById(id);

function queryParams() {
  const params = new URLSearchParams({ limit: '100', signal: $('signal').value });
  if (state.gapThreshold !== 'all') params.set('gap', state.gapThreshold);
  if ($('year').value) params.set('year', $('year').value);
  else params.set('directory', 'latest');
  if ($('borough').value) params.set('borough', $('borough').value);
  if (state.cursor) params.set('cursor', state.cursor);
  return params;
}

async function loadPage(reset = false, preserveSelection = false) {
  if (state.loading || (!state.hasMore && !reset)) return;
  if (reset) { state.schools = []; state.total = 0; state.cursor = null; state.hasMore = true; if (!preserveSelection) { state.selected = null; state.selectedSchool = null; } history.replaceState({}, '', window.location.pathname); }
  state.loading = true;
  $('status').textContent = `Loading schools… ${state.schools.length.toLocaleString()} loaded`;
  try {
    const pageCursor = state.cursor;
    const response = await fetch(`/api/portfolio?${queryParams()}`);
    if (!response.ok) throw Error(`API ${response.status}`);
    const page = await response.json();
    state.schools.push(...(page.schools || []));
    state.total = Number(page.total || 0);
    state.cursor = page.nextCursor;
    state.hasMore = Boolean(page.hasMore);
    const url = new URL(window.location.href);
    if (pageCursor) url.searchParams.set('cursor', pageCursor); else url.searchParams.delete('cursor');
    history.replaceState({}, '', url);
    render();
    $('status').textContent = `${state.schools.length.toLocaleString()} of ${state.total.toLocaleString()} schools; review signals are observational.`;
  } catch (error) {
    $('status').textContent = `Unable to load portfolio data: ${error.message}`;
    if (reset) $('queue').innerHTML = '<p class="empty">Try again when the portfolio API is available.</p>';
  } finally { state.loading = false; }
}

async function loadMetadata() {
  const response = await fetch('/api/portfolio_meta');
  if (!response.ok) throw Error(`Metadata API ${response.status}`);
  const metadata = await response.json();
  metadata.years.forEach((year) => $('year').insertAdjacentHTML('beforeend', `<option>${year}</option>`));
  metadata.boroughs.forEach((borough) => $('borough').insertAdjacentHTML('beforeend', `<option>${borough}</option>`));
}

function ensureGapControls() {
  if (document.getElementById('gap-controls')) return;
  const controls = document.createElement('fieldset');
  controls.id = 'gap-controls';
  controls.style.cssText = 'display:flex;gap:12px;flex-wrap:wrap;margin:0 0 14px;padding:10px 12px;border:1px solid #dbe3ee;border-radius:6px;background:#f8fafc';
  controls.innerHTML = '<legend style="padding:0 5px;color:#64748b;font-size:11px;font-weight:700">Attendance ↔ graduation gap</legend>' + [['all','All'],['.05','5%'],['.10','10%'],['.15','15%']].map(([value,label]) => `<label style="display:flex;gap:5px;align-items:center;color:#334155;font-size:12px"><input type="checkbox" data-gap="${value}" ${value === 'all' ? 'checked' : ''}>${label}</label>`).join('');
  $('profile').parentElement.insertBefore(controls, $('profile'));
  controls.querySelectorAll('input').forEach((input) => input.onchange = () => { controls.querySelectorAll('input').forEach((other) => { if (other !== input) other.checked = false; }); state.gapThreshold = input.checked ? input.dataset.gap : 'all'; loadPage(true, true); });
}

function ensureTabletLayout() {
  if (document.getElementById('tablet-layout')) return;
  const style = document.createElement('style');
  style.id = 'tablet-layout';
  style.textContent = '@media (min-width:768px) and (max-width:1024px){.grid{grid-template-columns:minmax(250px,38%) minmax(0,1fr);gap:12px}.panel{padding:13px}.queue-item{padding:9px 0;font-size:12px}.profile .metric{grid-template-columns:1fr 68px 68px;font-size:11px}.toolbar select{min-width:145px}}';
  document.head.appendChild(style);
}

function resetGapControls() {
  state.gapThreshold = 'all';
  document.querySelectorAll('#gap-controls input').forEach((input) => { input.checked = input.dataset.gap === 'all'; });
}

function filteredSchools() {
  if (state.gapThreshold === 'all') return state.schools;
  const threshold = Number(state.gapThreshold);
  return state.schools.filter((school) => (school.evidence || []).some((evidence) => evidence.gap >= threshold && evidence.denominator >= 10 && evidence.graduation?.denominator >= 10));
}

function render() {
  const schools = filteredSchools();
  $('count').textContent = `${schools.length.toLocaleString()} of ${state.total.toLocaleString()} schools`;
  $('queue').style.maxHeight = '620px';
  $('queue').style.overflowY = 'auto';
  if (schools.length && !state.selected) {
    state.selected = `${schools[0].dbn}|${schools[0].schoolYear}`;
    state.selectedSchool = schools[0];
  }
  const queueSchools = state.selectedSchool && !schools.some((school) => `${school.dbn}|${school.schoolYear}` === state.selected) ? [{ ...state.selectedSchool, noThresholdMatch: true }, ...schools] : schools;
  $('queue').innerHTML = queueSchools.map((school) => `<button class="queue-item ${state.selected === `${school.dbn}|${school.schoolYear}` ? 'selected' : ''}" data-key="${school.dbn}|${school.schoolYear}"><strong>${school.dbn}</strong><span>${school.borough} · ${school.schoolName || 'School name unavailable'}</span><em>${school.noThresholdMatch ? 'No match for selected threshold' : (school.signals?.length ? 'Attendance + graduation gap' : 'Insufficient data')}</em></button>`).join('') || '<p class="empty">No schools meet this disparity threshold.</p>';
  document.querySelectorAll('.queue-item').forEach((button) => button.onclick = () => { state.selected = button.dataset.key; state.selectedSchool = queueSchools.find((school) => `${school.dbn}|${school.schoolYear}` === state.selected); render(); showProfile(state.selectedSchool); });
  if (!schools.length) { $('profile').innerHTML = '<p class="empty">No schools meet this disparity threshold.</p>'; return; }
  if (state.selected && !schools.some((school) => `${school.dbn}|${school.schoolYear}` === state.selected)) { $('profile').innerHTML = '<p class="empty">The selected school has no match for this disparity threshold.</p>'; return; }
  if (state.selected) showProfile(schools.find((school) => `${school.dbn}|${school.schoolYear}` === state.selected));
}

function showProfile(school) {
  if (!school) { $('profile').innerHTML = '<p class="empty">Select a school to inspect its evidence.</p>'; return; }
  const signals = school.signals || [];
  const warnings = [...new Set(school.warnings || [])];
  const warningHtml = warnings.length ? `<div class="warn"><strong>Data quality notes</strong><ul>${warnings.map((warning) => `<li>${warning}</li>`).join('')}</ul></div>` : '';
  $('profile').innerHTML = `<div class="profile-head"><div><h3><a href="schools.html?dbn=${encodeURIComponent(school.dbn)}&school_year=${encodeURIComponent(school.schoolYear)}">${school.dbn}</a></h3><p>${school.schoolName || 'School name unavailable'} · ${school.borough} · ${school.schoolYear}</p></div><span class="profile-status">${signals.length ? 'Needs review' : 'Insufficient data'}</span></div>${signals.length ? signals.map((signal) => `<div class="metric"><span>${signal.demographic} · 90%+ attendance</span><b>${(signal.value * 100).toFixed(1)}%</b><small>grad ${((signal.graduation?.value || 0) * 100).toFixed(1)}%</small></div>`).join('') : '<p class="warn">No matched demographic pair meets the review threshold with adequate denominators.</p>'}${warningHtml}<p class="note">Observed pattern only. This screen does not claim that attendance causes graduation outcomes.</p><a class="profile-link" href="schools.html?dbn=${encodeURIComponent(school.dbn)}&school_year=${encodeURIComponent(school.schoolYear)}">Open full School Equity Profile</a>`;
}

['year', 'borough'].forEach((id) => $(id).onchange = () => loadPage(true));
$('signal').onchange = () => { resetGapControls(); loadPage(true); };
$('queue').addEventListener('scroll', (event) => { const element = event.currentTarget; if (element.scrollTop + element.clientHeight >= element.scrollHeight - 80) loadPage(); });
ensureGapControls();
ensureTabletLayout();
loadMetadata().then(() => loadPage(!initialCursor)).catch((error) => {
  $('status').textContent = `Unable to load school-year options: ${error.message}`;
  $('queue').innerHTML = '<p class="empty">School-year options are unavailable.</p>';
});
