import { escapeHtml } from '../core/dom.js';
import { formatMetric, riskText } from '../core/format.js';

export function renderThreatMeter(container, prediction = {}, scenario = {}) {
  const risk = Number(prediction.risk_score ?? 0);
  const level = riskText(risk);
  const label = prediction.label === 'dos_or_ddos' ? 'DoS/DDoS' : 'Normal';
  container.innerHTML = `
    <div class="threat-orb" style="--risk:${Math.round(risk * 100)}%" aria-label="Threat meter ${escapeHtml(level)}">
      <span>${Math.round(risk * 100)}</span>
      <small>risk</small>
    </div>
    <div class="threat-copy">
      <p class="section-kicker">Threat Meter</p>
      <h4>${escapeHtml(level)} · ${escapeHtml(label)}</h4>
      <p>Replay memakai fitur scenario aktif dan heuristic evidence untuk memvisualkan intensitas trafik. Score: ${formatMetric(risk, 3)}.</p>
      <small>${escapeHtml(scenario.scenario_type || 'artifact-grounded demo')}</small>
    </div>
  `;
}
