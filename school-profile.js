import './shared-header.js';

const params = new URLSearchParams(location.search);
const dbn = params.get('dbn');
const selectedYear = params.get('school_year');
const status = document.getElementById('profile-status');
const target = document.getElementById('school-profile');
const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

function showProfile(profile) {
  status.textContent = 'Profile loaded; findings are observational.';
  const years = ['2015','2016','2017','2018','2019','2020','2021','2022'].map((year) => `<option value="${year}" ${year === profile.schoolYear ? 'selected' : ''}>${year}</option>`).join('');
  const rows = profile.demographics.map((row) => `<tr><th scope="row">${esc(row.demographic)}</th><td>${row.attendance90 == null ? '—' : `${(row.attendance90 * 100).toFixed(1)}%`}</td><td>${row.graduation4 == null ? '—' : `${(row.graduation4 * 100).toFixed(1)}%`}</td><td>${row.gap == null ? '—' : `${(row.gap * 100).toFixed(1)} pp`}</td><td>${row.attendanceDenominator ?? '—'} / ${row.graduationDenominator ?? '—'}</td></tr>`).join('');
  target.innerHTML = `<div class="profile-toolbar"><label for="profile-year">School year</label><select id="profile-year">${years}</select></div><header class="profile-head"><div><h2>${esc(profile.schoolName || profile.dbn)}</h2><p>${esc(profile.dbn)} · ${esc(profile.borough)} · ${esc(profile.schoolYear)}</p></div></header><h3>Demographic comparison</h3><div style="overflow-x:auto"><table><thead><tr><th scope="col" class="group-header">Group</th><th scope="col">90%+<br>attendance</th><th scope="col">4-year<br>graduation</th><th scope="col" class="bottom-header">Gap</th><th scope="col">Attendance denominator /<br>Graduation denominator</th></tr></thead><tbody>${rows}</tbody></table></div><p class="note">Observed association only. This profile does not claim that attendance causes graduation outcomes.</p>${profile.warnings.length ? `<div class="warn"><strong>Data quality notes</strong><ul>${profile.warnings.map((warning) => `<li>${esc(warning)}</li>`).join('')}</ul></div>` : ''}`;
  target.insertAdjacentHTML('afterbegin', '<a class="back-link" href="schools.html">← Back to Schools directory</a>');
  renderComparisonChart(profile);
  document.getElementById('profile-year').addEventListener('change', (event) => { location.href = `schools.html?dbn=${encodeURIComponent(profile.dbn)}&school_year=${encodeURIComponent(event.target.value)}`; });
}

function renderComparisonChart(profile) {
  const points = profile.demographics.filter((row) => row.attendance90 != null && row.graduation4 != null);
  const chart = document.createElement('section');
  chart.className = 'comparison-chart';
  chart.setAttribute('aria-labelledby', 'comparison-chart-title');
  if (points.length < 2) {
    chart.innerHTML = '<h3 id="comparison-chart-title">Attendance and graduation comparison</h3><p class="empty">There is not enough matched demographic data to display a comparison chart for this school year.</p>';
    target.querySelector('.note').before(chart);
    return;
  }
  const width = 960; const height = 500; const pad = { left: 72, right: 36, top: 42, bottom: 88 };
  const x = (index) => pad.left + (index + 0.5) * ((width - pad.left - pad.right) / points.length);
  const y = (value) => height - pad.bottom - value * (height - pad.top - pad.bottom);
  const circles = points.map((point, index) => { const center = x(index); const attendanceY = y(point.attendance90); const graduationY = y(point.graduation4); return `<g class="chart-point-group" data-chart-index="${index}" tabindex="0" role="img" aria-label="${esc(point.demographic)}: ${(point.attendance90 * 100).toFixed(1)} percent attendance, ${(point.graduation4 * 100).toFixed(1)} percent graduation, gap ${(point.gap * 100).toFixed(1)} percentage points"><line class="chart-gap" x1="${center}" y1="${attendanceY}" x2="${center}" y2="${graduationY}"/><circle class="chart-point attendance-point" cx="${center}" cy="${attendanceY}" r="8"/><circle class="chart-point graduation-point" cx="${center}" cy="${graduationY}" r="8"/><text class="chart-point-label" x="${center}" y="${Math.min(attendanceY, graduationY) - 16}">${(point.attendance90 * 100).toFixed(1)}% / ${(point.graduation4 * 100).toFixed(1)}%</text><text class="chart-group-label" x="${center}" y="${height - pad.bottom + 24}">${esc(point.demographic)}</text></g>`; }).join('');
  chart.innerHTML = `<h3 id="comparison-chart-title">Attendance and graduation gap by demographic group</h3><p>Each group compares 90%+ attendance with four-year graduation. The connecting distance represents the observed percentage-point gap; it does not imply causation.</p><div class="chart-frame"><div class="chart-tooltip" role="status" aria-live="polite">Select or hover a demographic group for details.</div><svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="comparison-chart-title comparison-chart-description"><desc id="comparison-chart-description">Dumbbell chart with demographic groups on the horizontal axis and percentage rates from zero to one hundred on the vertical axis. Blue points show attendance, and purple points show graduation.</desc><line class="chart-axis" x1="${pad.left}" y1="${height - pad.bottom}" x2="${width - pad.right}" y2="${height - pad.bottom}"/><line class="chart-axis" x1="${pad.left}" y1="${pad.top}" x2="${pad.left}" y2="${height - pad.bottom}"/><text class="chart-label" x="${width / 2}" y="${height - 18}">Demographic group</text><text class="chart-label" transform="translate(15 ${height / 2}) rotate(-90)">Rate (%)</text>${[0, .25, .5, .75, 1].map((tick) => `<text class="chart-tick" x="${pad.left - 10}" y="${y(tick) + 4}">${tick * 100}%</text>`).join('')}${circles}</svg></div>`;
  target.querySelector('.note').before(chart);
  const tooltip = chart.querySelector('.chart-tooltip');
  const showPoint = (index) => { const point = points[index]; tooltip.textContent = `${point.demographic}: ${(point.attendance90 * 100).toFixed(1)}% attendance · ${(point.graduation4 * 100).toFixed(1)}% graduation · gap ${point.gap == null ? '—' : `${(point.gap * 100).toFixed(1)} pp`} · denominators ${point.attendanceDenominator ?? '—'} / ${point.graduationDenominator ?? '—'}`; chart.querySelectorAll('.chart-point-group').forEach((group) => group.classList.toggle('focused', group.dataset.chartIndex === String(index))); };
  chart.querySelectorAll('.chart-point-group').forEach((control) => { control.addEventListener('mouseenter', () => showPoint(control.dataset.chartIndex)); control.addEventListener('focus', () => showPoint(control.dataset.chartIndex)); control.addEventListener('click', () => showPoint(control.dataset.chartIndex)); });
}

function loadProfile() {
  return fetch(`/api/profile?dbn=${encodeURIComponent(dbn)}&school_year=${encodeURIComponent(selectedYear)}`).then((response) => { if (!response.ok) throw Error(response.status === 404 ? 'School profile not found for this school year.' : `API ${response.status}`); return response.json(); }).then(showProfile);
}

function loadDirectory() {
  let schools = [];
  let cursor = null;
  let hasMore = true;
  let loading = false;
  const yearOptions = ['2015','2016','2017','2018','2019','2020','2021','2022'].map((year) => `<option>${year}</option>`).join('');
  target.innerHTML = '<div class="schools-toolbar"><label for="school-search">Search DBN or School Name</label><input id="school-search" type="search" placeholder="e.g. 01M292 or Orchard"><label for="school-borough">Borough</label><select id="school-borough"><option value="">All boroughs</option><option>Bronx</option><option>Brooklyn</option><option>Manhattan</option><option>Queens</option><option>Staten Island</option></select><label for="school-year">School Year</label><select id="school-year"><option value="">All years</option>' + yearOptions + '</select></div><div id="school-list" class="schools-list"></div>';
  const list = document.getElementById('school-list');
  const render = () => { const term = document.getElementById('school-search').value.toLowerCase(); const boroughControl = document.getElementById('school-borough'); const borough = boroughControl.disabled ? '' : boroughControl.value; const matches = schools.filter((school) => `${school.dbn} ${school.schoolName || ''}`.toLowerCase().includes(term) && (!borough || school.borough === borough)); list.innerHTML = matches.map((school) => `<a class="queue-item" href="schools.html?dbn=${encodeURIComponent(school.dbn)}&school_year=${encodeURIComponent(school.schoolYear)}"><strong>${esc(school.dbn)}</strong><span>${esc(school.schoolName || 'School name unavailable')} · ${esc(school.borough)} · ${esc(school.schoolYear)}</span></a>`).join('') || '<p class="empty">No schools match your filters.</p>'; };
  const loadPage = (reset = false) => { if (loading || (!hasMore && !reset)) return; if (reset) { schools.length = 0; cursor = null; hasMore = true; } loading = true; const query = new URLSearchParams({limit:'100'}); const boroughControl = document.getElementById('school-borough'); const borough = boroughControl.disabled ? '' : boroughControl.value; const year = document.getElementById('school-year').value; const searchValue = document.getElementById('school-search').value.trim(); if (borough) query.set('borough', borough); if (year) query.set('year', year); if (/^\d{2}[A-Za-z]\d{3}$/.test(searchValue)) query.set('dbn', searchValue.toUpperCase()); else if (searchValue) query.set('school_name', searchValue); if (cursor) query.set('cursor', cursor); fetch(`/api/portfolio?${query}`).then((response) => response.json()).then((body) => { schools.push(...(body.schools || [])); cursor = body.nextCursor; hasMore = Boolean(body.hasMore); render(); status.textContent = `${schools.length.toLocaleString()} schools loaded. Search by DBN, School Name, Borough, or School Year.`; }).catch((error) => { status.textContent = `Unable to load schools: ${error.message}`; }).finally(() => { loading = false; }); };
  const search = document.getElementById('school-search');
  const boroughControl = document.getElementById('school-borough');
  const updateSearchMode = () => { const isDbn = /^\d{2}[A-Za-z]\d{3}$/.test(search.value.trim()); boroughControl.disabled = isDbn; boroughControl.setAttribute('aria-describedby', 'school-search-help'); document.getElementById('school-search-help').textContent = isDbn ? 'DBN search active — Borough filter is not applied.' : 'Search by DBN or school name.'; render(); };
  search.insertAdjacentHTML('afterend', '<p id="school-search-help" class="field-help">Search by DBN or school name.</p>');
  search.addEventListener('input', () => { updateSearchMode(); if (search.value.trim()) loadPage(true); });
  document.getElementById('school-borough').addEventListener('change', () => loadPage(true));
  document.getElementById('school-year').addEventListener('change', () => loadPage(true));
  list.addEventListener('scroll', () => { if (list.scrollTop + list.clientHeight >= list.scrollHeight - 80) loadPage(); });
  loadPage();
}

if (dbn && selectedYear) loadProfile().catch((error) => { status.textContent = `Unable to load profile: ${error.message}`; target.innerHTML = '<p class="empty">Check the DBN and school year, then try again.</p>'; });
else loadDirectory();
