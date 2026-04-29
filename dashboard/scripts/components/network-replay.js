import { escapeHtml } from '../core/dom.js';
import { formatMetric } from '../core/format.js';

function replayMode(scenario = {}) {
  const outcome = `${scenario.expected_outcome || ''} ${scenario.scenario_type || ''}`.toLowerCase();
  if (outcome.includes('fn_')) return 'missed';
  if (outcome.includes('fp_')) return 'false-positive';
  if (outcome.includes('normal')) return 'normal';
  if (outcome.includes('attack') || outcome.includes('dos')) return 'attack';
  return 'investigate';
}

function packetCount(risk, mode) {
  if (mode === 'missed') return 7;
  if (mode === 'false-positive') return 3;
  if (mode === 'normal') return 2;
  return Math.max(4, Math.min(10, Math.round(3 + risk * 8)));
}

export function renderNetworkReplay(container, scenario = {}, prediction = {}, activeIndex = -1) {
  const features = scenario.features || {};
  const risk = Number(prediction.risk_score ?? 0);
  const mode = replayMode(scenario);
  const active = Math.max(0, activeIndex + 1);
  const packets = Array.from({ length: packetCount(risk, mode) }, (_, index) => index);
  const stepLabel = activeIndex < 0 ? 'Ready' : `T+0${activeIndex * 2}s`;
  const status = mode === 'missed' ? 'Silent miss risk' : mode === 'false-positive' ? 'Analyst fatigue risk' : risk >= 0.7 ? 'Flood pattern detected' : risk >= 0.45 ? 'Suspicious flow' : 'Normal drift';

  container.className = `network-replay mode-${mode}`;
  container.style.setProperty('--risk', `${Math.max(6, Math.round(risk * 100))}%`);
  container.innerHTML = `
    <div class="replay-hud" aria-label="Ringkasan replay jaringan">
      <span class="mono-pill">${escapeHtml(stepLabel)}</span>
      <strong>${escapeHtml(status)}</strong>
      <span class="mono-pill">risk ${formatMetric(risk, 3)}</span>
    </div>
    <div class="network-canvas" role="img" aria-label="Visual replay paket dari attacker ke IoT gateway dan target">
      <div class="grid-plane" aria-hidden="true"></div>
      <div class="node node-attacker">
        <span class="node-ring"></span>
        <strong>${mode === 'normal' ? 'Client' : 'Bot/Source'}</strong>
        <small>src conn ${formatMetric(features.N_IN_Conn_P_SrcIP || 0, 1)}</small>
      </div>
      <div class="node node-gateway">
        <span class="node-ring"></span>
        <strong>IoT Gateway</strong>
        <small>dst conn ${formatMetric(features.N_IN_Conn_P_DstIP || 0, 1)}</small>
      </div>
      <div class="node node-target">
        <span class="node-ring"></span>
        <strong>Device/Service</strong>
        <small>${escapeHtml(features.proto || 'tcp').toUpperCase()} flow</small>
      </div>
      <svg class="attack-paths" viewBox="0 0 1000 360" preserveAspectRatio="none" aria-hidden="true">
        <path class="path-base" d="M115 180 C290 60, 440 60, 510 180 S725 300, 885 180" />
        <path class="path-hot" d="M115 180 C290 60, 440 60, 510 180 S725 300, 885 180" />
      </svg>
      <div class="packet-layer" aria-hidden="true">
        ${packets.map((_, index) => `<span class="packet packet-${index % 5}" style="--delay:${index * 110}ms; --size:${8 + (index % 4) * 2}px"></span>`).join('')}
      </div>
      <div class="alert-beacon ${activeIndex >= 2 ? 'is-hot' : ''}" aria-hidden="true">ALERT</div>
      <div class="traffic-spark" aria-hidden="true">
        ${Array.from({ length: 20 }, (_, i) => `<span style="--h:${18 + ((i * 17) % 80)}%; --d:${i * 35}ms"></span>`).join('')}
      </div>
    </div>
  `;
}
