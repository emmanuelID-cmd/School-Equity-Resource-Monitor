import './shared-header.js';

const $ = (id) => document.getElementById(id);
const form = $('budget-form');
const school = $('budget-school');
const year = $('budget-year');
const submit = form.querySelector('button[type="submit"]');
const status = $('budget-status');
const result = $('budget-result');
const searchResults = $('budget-search-results');
let selectedSchoolCode = '';
let searchTimer;

for (let value = 2026; value >= 2006; value -= 1) year.append(new Option(value, value));
submit.disabled = true;

const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const validCode = (value) => /^[MXKQR]\d{3}$/.test(value);
const updateSubmitState = () => { submit.disabled = !(selectedSchoolCode && year.value); };

async function searchSchools() {
  const query = school.value.trim();
  selectedSchoolCode = '';
  updateSubmitState();
  if (!query) { searchResults.hidden = true; return; }
  searchResults.innerHTML = '<p class="budget-search-message">Searching schools…</p>';
  searchResults.hidden = false;
  try {
    const response = await fetch(`/api/budget/search?query=${encodeURIComponent(query)}`, { cache: 'no-store' });
    const data = await response.json();
    if (!data.schools.length) { searchResults.innerHTML = '<p class="budget-search-message">No schools found. Refine your search.</p>'; return; }
    searchResults.innerHTML = data.schools.map((item) => `<button type="button" class="budget-search-option" data-code="${esc(item.schoolCode)}"><strong>${esc(item.dbn)}</strong><span>${esc(item.schoolName)} · ${esc(item.borough)}</span></button>`).join('');
    searchResults.querySelectorAll('button').forEach((button) => button.addEventListener('click', () => {
      selectedSchoolCode = button.dataset.code;
      school.value = selectedSchoolCode;
      searchResults.hidden = true;
      updateSubmitState();
      school.focus();
    }));
  } catch {
    searchResults.innerHTML = '<p class="budget-search-message">School search is unavailable. Try again.</p>';
  }
}

async function loadBudget(event) {
  event?.preventDefault();
  const code = selectedSchoolCode;
  if (!validCode(code) || !year.value) return;
  status.textContent = 'Loading budget context…';
  result.innerHTML = '<p class="empty">Loading available fields and source metadata…</p>';
  try {
    const response = await fetch(`/api/budget?school_code=${encodeURIComponent(code)}&fiscal_year=${year.value}`, { cache: 'no-store' });
    const data = await response.json();
    if (!response.ok) throw Error(data.message || 'Budget context is unavailable.');
    result.innerHTML = `<div class="budget-warning" role="note"><strong>Partial budget context.</strong> Galaxy budgeted inputs are not definitive actual spending. Missing fields are not substituted.</div><header class="panel-header"><div><h3>${esc(data.schoolName)} · ${esc(data.dbn)}</h3><p class="muted">Fiscal year ${esc(data.fiscalYear)} · Source date ${esc(data.sourceDate || 'not provided')}</p></div><span class="profile-status">${esc(data.status)}</span></header><p class="budget-meta">Source: <a href="${esc(data.sourceUrl)}" target="_blank" rel="noreferrer">NYCPS Galaxy Budget Summary</a><br>Retrieved: ${esc(data.retrievedAt)}</p><div class="budget-table"><div class="budget-row budget-head"><b>Category / position</b><b>Positions</b><b>Budget</b></div>${(data.records || []).map((item) => `<div class="budget-row"><span>${esc(item.label)}</span><span>${esc(item.positions)}</span><span>$${Number(item.budget).toLocaleString()}</span></div>`).join('') || '<p class="empty">No displayable budget fields were returned.</p>'}</div>`;
    status.textContent = 'Budget context loaded with source limitations shown.';
  } catch (error) {
    status.textContent = error.message;
    result.innerHTML = `<p class="warn" role="alert">${esc(error.message)} No values were substituted.</p>`;
  }
}

school.addEventListener('input', () => { selectedSchoolCode = ''; updateSubmitState(); clearTimeout(searchTimer); searchTimer = setTimeout(searchSchools, 250); });
school.addEventListener('blur', () => setTimeout(() => { searchResults.hidden = true; }, 150));
year.addEventListener('change', () => { updateSubmitState(); if (selectedSchoolCode && school.value === selectedSchoolCode) loadBudget(); });
form.addEventListener('submit', loadBudget);
updateSubmitState();
