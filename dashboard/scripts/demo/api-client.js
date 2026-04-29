function apiBase() {
  if (window.location.pathname.startsWith('/soc-demo/')) return '/soc-demo/api';
  return '/api';
}

export async function apiGet(path) {
  const response = await fetch(`${apiBase()}${path}`, { cache: 'no-store' });
  if (!response.ok) throw new Error(`API GET ${path} failed: ${response.status}`);
  return response.json();
}

export async function apiPost(path, body) {
  const response = await fetch(`${apiBase()}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error(`API POST ${path} failed: ${response.status}`);
  return response.json();
}
