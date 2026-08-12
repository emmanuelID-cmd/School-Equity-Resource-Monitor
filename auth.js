const sessionKey = 'serm-auth-session';

export async function loadSupabaseConfig() {
  const response = await fetch('/api/config', { cache: 'no-store' });
  if (!response.ok) throw Error('Unable to load authentication configuration.');
  const config = await response.json();
  if (!config.supabaseUrl || !config.publishableKey) throw Error('Supabase configuration is missing.');
  return config;
}

export async function signIn(email, password) {
  const config = await loadSupabaseConfig();
  const response = await fetch(`${config.supabaseUrl}/auth/v1/token?grant_type=password`, {
    method: 'POST',
    headers: { apikey: config.publishableKey, 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw Error(payload.error_description || payload.msg || 'Unable to sign in.');
  localStorage.setItem(sessionKey, JSON.stringify(payload));
  return payload;
}

export function currentSession() {
  try { return JSON.parse(localStorage.getItem(sessionKey) || 'null'); } catch { return null; }
}

export function signOut() { localStorage.removeItem(sessionKey); }

export async function authenticatedRequest(path, options = {}) {
  const session = currentSession();
  if (!session?.access_token) throw Error('Please sign in to continue.');
  const config = await loadSupabaseConfig();
  const headers = { apikey: config.publishableKey, Authorization: `Bearer ${session.access_token}`, 'Content-Type': 'application/json', ...(options.headers || {}) };
  const response = await fetch(`${config.supabaseUrl}/rest/v1/${path}`, { ...options, headers });
  const payload = await response.json().catch(() => null);
  if (response.status === 401) { signOut(); window.location.replace('login.html?expired=1'); throw Error('Your session expired. Please sign in again.'); }
  if (!response.ok) throw Error(payload?.message || payload?.hint || 'Action Plans request failed.');
  return payload;
}
