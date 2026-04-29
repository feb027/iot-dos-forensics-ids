import { escapeHtml } from '../core/dom.js';

function list(items = []) {
  return `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`;
}

export function renderAnalystReport(container, report) {
  if (!report) {
    container.innerHTML = '<p class="muted">Belum ada report. Pilih skenario lalu jalankan analisis.</p>';
    return;
  }
  container.innerHTML = `
    <div class="report-grid">
      <section class="report-block">
        <h3>Incident Summary</h3>
        <p>${escapeHtml(report.summary)}</p>
      </section>
      <section class="report-block">
        <h3>Evidence Chain</h3>
        ${list(report.evidence_chain)}
      </section>
      <section class="report-block">
        <h3>FP/FN Risk Note</h3>
        <p>${escapeHtml(report.risk_note)}</p>
      </section>
      <section class="report-block">
        <h3>Recommended Actions</h3>
        ${list(report.recommendations)}
      </section>
      <section class="report-block">
        <h3>Academic Boundary</h3>
        <p>${escapeHtml(report.limitation)}</p>
      </section>
      <section class="report-block">
        <h3>Grounding</h3>
        ${list(report.grounding || [])}
      </section>
    </div>
  `;
}

export function reportToText(report) {
  if (!report) return '';
  return [
    `Incident Summary: ${report.summary}`,
    `Evidence Chain:\n- ${(report.evidence_chain || []).join('\n- ')}`,
    `FP/FN Risk Note: ${report.risk_note}`,
    `Recommended Actions:\n- ${(report.recommendations || []).join('\n- ')}`,
    `Academic Boundary: ${report.limitation}`,
  ].join('\n\n');
}
