import { escapeHtml } from '../core/dom.js';
import { formatPercent } from '../core/format.js';

export function renderEvidenceBars(container, evidence = []) {
  const rows = evidence.slice(0, 7);
  const max = Math.max(...rows.map((row) => Number(row.weight || row.value || row.score || 0)), 0.001);
  container.innerHTML = rows.map((row) => {
    const raw = Number(row.weight || row.value || row.score || 0);
    const width = Math.max((raw / max) * 100, raw > 0 ? 3 : 0);
    const detail = row.hint || row.reason || row.interpretation_hint || '';
    return `
      <div class="evidence-bar">
        <header>
          <span>${escapeHtml(row.feature || row.feature_group || row.name)}</span>
          <strong>${formatPercent(raw, 1)}</strong>
        </header>
        <div class="track" aria-hidden="true"><span style="--value:${width}%"></span></div>
        ${detail ? `<small class="muted">${escapeHtml(detail)}</small>` : ''}
      </div>
    `;
  }).join('');
}
