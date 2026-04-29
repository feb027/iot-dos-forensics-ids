import { qs, setHtml, escapeHtml, renderLucideIcons } from './core/dom.js';
import { formatMetric, formatPercent, riskLabel, riskText } from './core/format.js';
import { loadScenarioBundle, scenarioById } from './demo/scenario-store.js';
import { predictRisk } from './demo/what-if-engine.js';
import { apiGet, apiPost } from './demo/api-client.js';
import { renderEvidenceBars } from './components/evidence-bar.js';
import { renderTimeline } from './components/timeline.js';
import { renderNetworkReplay } from './components/network-replay.js';
import { renderEventStream } from './components/event-stream.js';
import { renderThreatMeter } from './components/threat-meter.js';
import { startReplay, scrubReplay } from './demo/replay-engine.js';
import { renderAnalystReport, reportToText } from './components/analyst-report.js';
import { buildLocalReport } from './demo/soc-narrative.js';

const state = { bundle: null, scenario: null, prediction: null, report: null, apiOnline: false };
const featureOrder = ['proto', 'N_IN_Conn_P_DstIP', 'N_IN_Conn_P_SrcIP', 'srate', 'drate', 'stddev', 'state_number', 'mean', 'max', 'min'];

function renderMetricRows(container, rows) {
  container.innerHTML = rows.map(([label, value]) => `<div class="metric-row"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`).join('');
}

async function checkApi() {
  const status = qs('#api-status');
  try {
    const health = await apiGet('/health');
    state.apiOnline = true;
    status.textContent = 'online';
    status.className = 'status-pill online';
    renderMetricRows(qs('#api-details'), [
      ['Service', health.service],
      ['Mode', health.mode],
      ['Artifacts', `${health.scenarios} scenarios`],
    ]);
  } catch (error) {
    state.apiOnline = false;
    status.textContent = 'offline fallback';
    status.className = 'status-pill offline';
    renderMetricRows(qs('#api-details'), [['Fallback', 'client-side JSON + deterministic report']]);
  }
}

function renderScenarios() {
  const scenarios = state.bundle.scenarios.scenarios || [];
  setHtml('#scenario-list', scenarios.map((scenario) => `
    <button class="scenario-card ${state.scenario?.id === scenario.id ? 'is-active' : ''}" type="button" data-scenario-id="${escapeHtml(scenario.id)}">
      <strong>${escapeHtml(scenario.name)}</strong>
      <small>${escapeHtml(scenario.description)}</small>
    </button>
  `).join(''));
  document.querySelectorAll('[data-scenario-id]').forEach((button) => {
    button.addEventListener('click', () => selectScenario(button.dataset.scenarioId));
  });
}

function renderForm(features) {
  const ranges = state.bundle.ranges.features || {};
  const html = featureOrder.map((feature) => {
    if (feature === 'proto') {
      const value = features.proto || 'tcp';
      return `<label class="field"><header><span>proto</span><strong>${escapeHtml(value)}</strong></header><select name="proto"><option ${value==='tcp'?'selected':''}>tcp</option><option ${value==='udp'?'selected':''}>udp</option><option ${value==='arp'?'selected':''}>arp</option><option ${value==='icmp'?'selected':''}>icmp</option></select></label>`;
    }
    const range = ranges[feature] || { min: 0, max: 10, step: 0.01 };
    const value = Number(features[feature] ?? range.default ?? 0);
    return `<label class="field"><header><span>${escapeHtml(feature)}</span><strong data-value-for="${escapeHtml(feature)}">${formatMetric(value, 3)}</strong></header><input type="range" name="${escapeHtml(feature)}" min="${range.min}" max="${range.max}" step="${range.step || 0.001}" value="${value}"></label>`;
  }).join('');
  qs('#whatif-form').innerHTML = html;
  qs('#whatif-form').addEventListener('input', () => runLocalPrediction());
}

function currentFeatures() {
  const form = qs('#whatif-form');
  const data = new FormData(form);
  const features = {};
  for (const feature of featureOrder) {
    features[feature] = feature === 'proto' ? data.get(feature) : Number(data.get(feature) || 0);
  }
  document.querySelectorAll('[data-value-for]').forEach((el) => {
    const feature = el.dataset.valueFor;
    el.textContent = formatMetric(features[feature], 3);
  });
  return features;
}

function renderPrediction(prediction) {
  state.prediction = prediction;
  const label = prediction.label === 'dos_or_ddos' ? 'DoS/DDoS' : 'Normal';
  const badge = qs('#risk-level');
  const level = riskLabel(prediction.risk_score);
  badge.className = `risk-badge ${level}`;
  badge.textContent = riskText(prediction.risk_score);
  qs('#risk-meter-fill').style.setProperty('--value', `${Math.round(prediction.risk_score * 100)}%`);
  renderMetricRows(qs('#prediction-summary'), [
    ['Prediction', label],
    ['Risk score', formatMetric(prediction.risk_score, 3)],
    ['Confidence', formatPercent(prediction.confidence, 1)],
    ['Model', prediction.model || 'surrogate IDS'],
  ]);
  renderEvidenceBars(qs('#evidence-bars'), prediction.evidence || []);
  renderReplayFrame(state.scenario?.timeline?.length ? state.scenario.timeline.length - 1 : -1);
}

function renderReplayFrame(activeIndex = -1) {
  if (!state.scenario) return;
  const steps = state.scenario.timeline || [];
  renderTimeline(qs('#timeline'), steps, activeIndex);
  renderNetworkReplay(qs('#network-replay'), state.scenario, state.prediction || predictRisk(state.scenario.features || {}), activeIndex);
  renderEventStream(qs('#event-stream'), steps, activeIndex, state.scenario);
  renderThreatMeter(qs('#threat-meter'), state.prediction || predictRisk(state.scenario.features || {}), state.scenario);
  const scrub = qs('#replay-scrub');
  scrub.max = String(Math.max(0, steps.length - 1));
  scrub.value = String(activeIndex);
  qs('#replay-clock').textContent = activeIndex < 0 ? 'ready' : `00:${String(activeIndex * 2).padStart(2, '0')}`;
}

function runLocalPrediction() {
  const features = currentFeatures();
  renderPrediction(predictRisk(features));
}

async function analyzeScenarioViaApi() {
  const features = currentFeatures();
  let prediction;
  try {
    prediction = await apiPost('/predict', { features, scenario_id: state.scenario.id });
  } catch (_) {
    prediction = predictRisk(features);
  }
  renderPrediction(prediction);
  try {
    state.report = await apiPost('/soc/analyze', { scenario_id: state.scenario.id, features, prediction });
  } catch (_) {
    state.report = buildLocalReport(state.scenario, prediction);
  }
  renderAnalystReport(qs('#analyst-report'), state.report);
}

function selectScenario(id) {
  state.scenario = scenarioById(state.bundle, id);
  renderScenarios();
  qs('#scenario-title').textContent = state.scenario.name;
  qs('#scenario-outcome').textContent = state.scenario.expected_outcome || 'demo';
  renderForm(state.scenario.features || {});
  runLocalPrediction();
  state.report = buildLocalReport(state.scenario, state.prediction);
  renderAnalystReport(qs('#analyst-report'), state.report);
}

function renderEvidenceBoundary() {
  const sources = state.bundle.scenarios.sources || [];
  const cards = [
    ['Prototype scope', 'VPS-backed interactive prototype. Bukan production real-time IDS.'],
    ['Claim policy', 'Report harus grounded ke artifact model, SHAP, FP/FN, dan batasan dataset.'],
    ['Artifact sources', sources.join(', ') || 'demo-scenarios.json'],
  ];
  setHtml('#demo-evidence-grid', cards.map(([title, body]) => `<article class="panel"><p class="section-kicker">${escapeHtml(title)}</p><p class="note">${escapeHtml(body)}</p></article>`).join(''));
}

async function init() {
  state.bundle = await loadScenarioBundle();
  await checkApi();
  selectScenario(state.bundle.scenarios.scenarios?.[0]?.id);
  renderEvidenceBoundary();
  qs('#replay-button').addEventListener('click', () => startReplay({
    steps: state.scenario.timeline || [],
    speed: Number(qs('#replay-speed').value || 1),
    onFrame: (index) => renderReplayFrame(index),
  }));
  qs('#replay-scrub').addEventListener('input', (event) => scrubReplay({
    steps: state.scenario.timeline || [],
    index: event.target.value,
    onFrame: (index) => renderReplayFrame(index),
  }));
  qs('#analyze-button').addEventListener('click', analyzeScenarioViaApi);
  qs('#copy-report-button').addEventListener('click', async () => navigator.clipboard?.writeText(reportToText(state.report)));
  renderLucideIcons();
}

init().catch((error) => {
  console.error(error);
  document.body.insertAdjacentHTML('afterbegin', `<div class="section"><div class="panel">Demo gagal dimuat: ${escapeHtml(error.message)}</div></div>`);
});
