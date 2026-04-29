export function qs(selector, root = document) {
  return root.querySelector(selector);
}

export function qsa(selector, root = document) {
  return Array.from(root.querySelectorAll(selector));
}

export function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

export function setHtml(selector, html) {
  const el = typeof selector === 'string' ? qs(selector) : selector;
  if (el) el.innerHTML = html;
}

export function renderLucideIcons() {
  if (window.lucide?.createIcons) window.lucide.createIcons();
}
