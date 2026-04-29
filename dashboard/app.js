const chartState = {
  classDistribution: null,
  modelComparison: null,
  featureEvidence: null,
};

const appState = {
  data: null,
  modelFilter: 'combined',
  confusionRows: [],
};

const TRACK_LABELS = {
  A_realistic_imbalanced: 'Track A realistis',
  B_balanced_controlled_1_to_1: 'Track B 1:1',
  C_balanced_controlled_1_to_2: 'Track C 1:2',
};

const PALETTE = ['#35f4bd', '#5bb8ff', '#ffd166', '#ff6b7a', '#b7ff6a', '#c09bff', '#ff9f6e'];

function qs(selector) {
  return document.querySelector(selector);
}

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function formatNumber(value) {
  const number = Number(value || 0);
  return number.toLocaleString('id-ID');
}

function formatMetric(value, digits = 4) {
  const number = Number(value);
  if (!Number.isFinite(number)) return '-';
  return number.toFixed(digits);
}

function formatDelta(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return '-';
  return `${number >= 0 ? '+' : ''}${number.toFixed(4)}`;
}

function formatPercent(value, digits = 2) {
  const number = Number(value);
  if (!Number.isFinite(number)) return '-';
  return `${(number * 100).toFixed(digits)}%`;
}

function compactTrack(track) {
  return TRACK_LABELS[track] || track || '-';
}

function modelDisplayName(row) {
  return row.model_display_name || String(row.model || '-').replaceAll('_', ' ');
}

function isMobileLayout() {
  return Boolean(window.matchMedia?.('(max-width: 760px)').matches);
}

function getScopeCount(data, split, label) {
  return Number(data.eda_summary?.scope_counts?.[split]?.[label] || 0);
}

function renderLucideIcons() {
  if (window.lucide?.createIcons) {
    window.lucide.createIcons();
  }
}

function setChartFallback(container, rows, valueKey, labelKey, options = {}) {
  if (!container) return;
  const max = Math.max(...rows.map((row) => Number(row[valueKey] || 0)), 1);
  container.hidden = false;
  container.innerHTML = rows.map((row) => {
    const rawValue = Number(row[valueKey] || 0);
    const width = Math.max((rawValue / max) * 100, rawValue > 0 ? 2 : 0);
    const value = options.metric ? formatMetric(rawValue) : formatNumber(rawValue);
    const subLabel = options.subLabel ? `<small>${escapeHtml(options.subLabel(row))}</small>` : '';
    return `
      <div class="fallback-bar">
        <span class="track">${escapeHtml(row[labelKey])}${subLabel}</span>
        <span class="bar" aria-hidden="true"><span style="--value: ${width}%"></span></span>
        <strong>${value}</strong>
      </div>
    `;
  }).join('');
}

function makeChart(canvas, fallback, config, fallbackRows, valueKey, labelKey, options = {}) {
  const useMobileFallback = isMobileLayout() && options.mobileFallback !== false;
  if (!canvas || !window.Chart || useMobileFallback) {
    if (canvas) canvas.hidden = true;
    canvas?.closest('.chart-wrap')?.classList.add('is-fallback');
    setChartFallback(fallback, fallbackRows, valueKey, labelKey, options);
    return null;
  }

  try {
    canvas.hidden = false;
    canvas.closest('.chart-wrap')?.classList.remove('is-fallback');
    if (fallback) fallback.hidden = true;
    return new window.Chart(canvas, config);
  } catch (error) {
    console.error(error);
    canvas.hidden = true;
    canvas.closest('.chart-wrap')?.classList.add('is-fallback');
    setChartFallback(fallback, fallbackRows, valueKey, labelKey, options);
    return null;
  }
}

function baseChartOptions(extra = {}) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    color: '#effffc',
    plugins: {
      legend: {
        labels: {
          color: '#bdd5d2',
          boxWidth: 12,
          font: { family: 'Fira Sans' },
        },
      },
      tooltip: {
        backgroundColor: 'rgba(2, 5, 6, 0.94)',
        borderColor: 'rgba(151, 255, 229, 0.34)',
        borderWidth: 1,
        titleColor: '#effffc',
        bodyColor: '#bdd5d2',
      },
    },
    ...extra,
  };
}

function renderHero(data) {
  const project = data.project || {};
  qs('#project-status').textContent = project.status || 'Experiment results pending.';
  qs('#telemetry-source').textContent = project.primary_dataset || 'BoT-IoT';

  const trainDos = getScopeCount(data, 'train', 'dos_or_ddos');
  const testDos = getScopeCount(data, 'test', 'dos_or_ddos');
  const trainNormal = getScopeCount(data, 'train', 'normal');
  const testNormal = getScopeCount(data, 'test', 'normal');
  const otherAttack = getScopeCount(data, 'train', 'other_attack') + getScopeCount(data, 'test', 'other_attack');
  const totalScope = trainDos + testDos + trainNormal + testNormal + otherAttack;
  const trackA = (data.advanced_models || []).find((row) => row.track === 'A_realistic_imbalanced');

  const telemetryRows = [
    {
      label: 'DoS/DDoS scope',
      value: trainDos + testDos,
      ratio: totalScope ? (trainDos + testDos) / totalScope : 0,
      hint: 'train + test',
    },
    {
      label: 'Normal audit rows',
      value: trainNormal + testNormal,
      ratio: totalScope ? (trainNormal + testNormal) / totalScope : 0,
      hint: 'minority class',
    },
    {
      label: 'Other attacks excluded',
      value: otherAttack,
      ratio: totalScope ? otherAttack / totalScope : 0,
      hint: 'primary binary task',
    },
    {
      label: 'Track A Delta Macro F1',
      value: trackA ? formatDelta(trackA.delta_macro_f1_vs_baseline) : '-',
      ratio: Math.min(Math.abs(Number(trackA?.delta_macro_f1_vs_baseline || 0)) / 0.05, 1),
      hint: trackA ? modelDisplayName(trackA) : 'not available',
      raw: true,
    },
  ];

  qs('#telemetry-stack').innerHTML = telemetryRows.map((row) => `
    <div class="telemetry-row">
      <header>
        <span>${escapeHtml(row.label)} <small>(${escapeHtml(row.hint)})</small></span>
        <strong>${row.raw ? escapeHtml(row.value) : formatNumber(row.value)}</strong>
      </header>
      <div class="meter" aria-hidden="true"><span style="--value: ${Math.max(row.ratio * 100, row.ratio > 0 ? 2 : 0)}%"></span></div>
    </div>
  `).join('');
}

function renderKpis(data) {
  const dataset = data.dataset_summary || {};
  const trainNormal = getScopeCount(data, 'train', 'normal');
  const testNormal = getScopeCount(data, 'test', 'normal');
  const baselineRuns = data.baseline_summary?.total_completed_runs || (data.model_comparison || []).length;
  const advancedRuns = data.advanced_summary?.total_completed_runs || (data.advanced_models || []).length;
  const trackA = (data.advanced_models || []).find((row) => row.track === 'A_realistic_imbalanced');
  const topShap = data.advanced_summary?.top_shap_feature_groups?.[0] || data.forensic_summary?.top_feature_groups?.[0];

  const cards = [
    {
      icon: 'database',
      label: 'Rows audited',
      value: formatNumber(dataset.rows),
      hint: dataset.source || 'Dataset source unavailable',
    },
    {
      icon: 'activity',
      label: 'Normal rows train/test',
      value: `${formatNumber(trainNormal)} / ${formatNumber(testNormal)}`,
      hint: 'Minority class untuk evaluasi DoS/DDoS',
    },
    {
      icon: 'git-branch',
      label: 'Baseline runs',
      value: formatNumber(baselineRuns),
      hint: 'Fase 4 model comparison',
    },
    {
      icon: 'cpu',
      label: 'Advanced runs',
      value: formatNumber(advancedRuns),
      hint: 'Fase 6A SOTA tabular',
    },
    {
      icon: 'trending-up',
      label: 'Track A Delta Macro F1',
      value: trackA ? formatDelta(trackA.delta_macro_f1_vs_baseline) : '-',
      hint: trackA ? `${modelDisplayName(trackA)} vs ${trackA.baseline_best_model_for_track}` : 'Track A advanced belum tersedia',
    },
    {
      icon: 'fingerprint',
      label: 'Top SHAP/forensic feature group',
      value: topShap?.feature_group || '-',
      hint: topShap?.interpretation_hint || 'Interpretasi fitur belum tersedia',
    },
  ];

  qs('#kpi-grid').innerHTML = cards.map((card) => `
    <article class="kpi-card">
      <div class="label">
        <span>${escapeHtml(card.label)}</span>
        <i data-lucide="${escapeHtml(card.icon)}" aria-hidden="true"></i>
      </div>
      <strong class="value">${escapeHtml(card.value)}</strong>
      <p class="hint">${escapeHtml(card.hint)}</p>
    </article>
  `).join('');
}

function renderDataset(data) {
  const dataset = data.dataset_summary || {};
  const trainRows = (data.class_distribution || [])
    .filter((row) => row.split === 'train' && row.group === 'category_counts')
    .sort((a, b) => Number(b.count) - Number(a.count));
  const fallback = qs('#class-distribution-fallback');

  chartState.classDistribution?.destroy();
  chartState.classDistribution = makeChart(
    qs('#class-distribution-chart'),
    fallback,
    {
      type: 'doughnut',
      data: {
        labels: trainRows.map((row) => row.label),
        datasets: [{
          data: trainRows.map((row) => row.count),
          backgroundColor: PALETTE,
          borderColor: '#071011',
          borderWidth: 2,
        }],
      },
      options: baseChartOptions({
        cutout: '62%',
        plugins: {
          ...baseChartOptions().plugins,
          tooltip: {
            ...baseChartOptions().plugins.tooltip,
            callbacks: {
              label: (item) => `${item.label}: ${formatNumber(item.raw)} (${formatPercent(trainRows[item.dataIndex]?.rate || 0)})`,
            },
          },
        },
      }),
    },
    trainRows,
    'count',
    'label',
  );

  setChartFallback(fallback, trainRows, 'count', 'label', {
    subLabel: (row) => formatPercent(row.rate || 0),
  });

  const snapshot = [
    ['Source', dataset.source || '-'],
    ['Rows audited', formatNumber(dataset.rows)],
    ['CSV files', formatNumber(dataset.files)],
    ['Columns', formatNumber(dataset.columns)],
    ['Candidate features', formatNumber(dataset.candidate_features)],
    ['Excluded/leakage columns', (dataset.excluded_columns || []).join(', ') || '-'],
  ];

  qs('#dataset-snapshot').innerHTML = snapshot.map(([label, value]) => `
    <div class="metric-row">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
    </div>
  `).join('');
}

function modelRowsForFilter(data) {
  const baseline = (data.model_comparison || []).map((row) => ({ ...row, kind: 'baseline' }));
  const advanced = (data.advanced_models || []).map((row) => ({ ...row, kind: 'advanced' }));
  if (appState.modelFilter === 'baseline') return baseline;
  if (appState.modelFilter === 'advanced') return advanced;
  return [...advanced, ...baseline];
}

function renderModeling(data) {
  const rows = modelRowsForFilter(data)
    .sort((a, b) => Number(b.macro_f1) - Number(a.macro_f1))
    .slice(0, isMobileLayout() && appState.modelFilter === 'combined' ? 8 : 14);
  const labels = rows.map((row) => `${row.kind === 'advanced' ? 'ADV' : 'BASE'} - ${modelDisplayName(row)} - ${compactTrack(row.track)}`);
  const fallbackRows = rows.map((row, index) => ({ ...row, chartLabel: labels[index] }));
  const fallback = qs('#model-comparison-fallback');

  qs('#model-chart-title').textContent = appState.modelFilter === 'combined'
    ? 'Perbandingan Model'
    : appState.modelFilter === 'baseline'
      ? 'Baseline Runs'
      : 'Advanced Runs';

  chartState.modelComparison?.destroy();
  chartState.modelComparison = makeChart(
    qs('#model-comparison-chart'),
    fallback,
    {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Macro F1',
          data: rows.map((row) => row.macro_f1),
          backgroundColor: rows.map((row) => row.kind === 'advanced' ? 'rgba(53, 244, 189, 0.78)' : 'rgba(91, 184, 255, 0.72)'),
          borderColor: rows.map((row) => row.kind === 'advanced' ? '#35f4bd' : '#5bb8ff'),
          borderWidth: 1,
        }],
      },
      options: baseChartOptions({
        indexAxis: 'y',
        scales: {
          x: {
            min: 0,
            max: 1,
            grid: { color: 'rgba(151, 255, 229, 0.12)' },
            ticks: { color: '#9bb6b4' },
          },
          y: {
            grid: { display: false },
            ticks: { color: '#bdd5d2', autoSkip: false },
          },
        },
        plugins: {
          ...baseChartOptions().plugins,
          legend: { display: false },
        },
      }),
    },
    fallbackRows,
    'macro_f1',
    'chartLabel',
    { metric: true },
  );

  setChartFallback(fallback, fallbackRows, 'macro_f1', 'chartLabel', { metric: true });
  if (chartState.modelComparison) fallback.hidden = true;

  qs('#model-table').innerHTML = rows.map((row) => `
    <div class="model-row">
      <span>
        ${escapeHtml(modelDisplayName(row))}
        <small>${escapeHtml(row.kind)} - ${escapeHtml(compactTrack(row.track))}</small>
      </span>
      <strong>${formatMetric(row.macro_f1)}</strong>
    </div>
  `).join('');
}

function setupModelTabs() {
  document.querySelectorAll('.tab-button').forEach((button) => {
    button.addEventListener('click', () => {
      appState.modelFilter = button.dataset.filter || 'combined';
      document.querySelectorAll('.tab-button').forEach((item) => {
        const active = item === button;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      renderModeling(appState.data);
    });
  });
}

function getMetricForConfusion(data, row) {
  const source = row.kind === 'advanced' ? data.advanced_models : data.model_comparison;
  return (source || []).find((metric) => metric.track === row.track && metric.model === row.model) || {};
}

function renderConfusionOptions(data) {
  const baseline = (data.confusion_matrix || []).map((row) => ({ ...row, kind: 'baseline' }));
  const advanced = (data.advanced_confusion || []).map((row) => ({ ...row, kind: 'advanced' }));
  appState.confusionRows = [...advanced, ...baseline];
  const select = qs('#confusion-select');

  select.innerHTML = appState.confusionRows.map((row, index) => `
    <option value="${index}">
      ${escapeHtml(row.kind.toUpperCase())} - ${escapeHtml(row.model.replaceAll('_', ' '))} - ${escapeHtml(compactTrack(row.track))}
    </option>
  `).join('');

  const trackAIndex = appState.confusionRows.findIndex((row) => row.kind === 'advanced' && row.track === 'A_realistic_imbalanced');
  select.value = String(trackAIndex >= 0 ? trackAIndex : 0);
  select.addEventListener('change', () => renderConfusionMatrix(data));
  renderConfusionMatrix(data);
}

function renderConfusionMatrix(data) {
  const selected = appState.confusionRows[Number(qs('#confusion-select').value)] || appState.confusionRows[0];
  if (!selected) {
    qs('#confusion-grid').innerHTML = '<p class="muted">Confusion matrix belum tersedia.</p>';
    return;
  }

  const metric = getMetricForConfusion(data, selected);
  const total = Number(selected.tn_normal_correct || 0)
    + Number(selected.fp_normal_as_attack || 0)
    + Number(selected.fn_attack_as_normal || 0)
    + Number(selected.tp_attack_correct || 0);

  qs('#confusion-meta').innerHTML = [
    `${selected.kind}`,
    modelDisplayName(selected),
    compactTrack(selected.track),
    `Macro F1 ${formatMetric(metric.macro_f1)}`,
    `MCC ${formatMetric(metric.mcc)}`,
  ].map((item) => `<span>${escapeHtml(item)}</span>`).join('');

  const cells = [
    ['TN', 'Normal benar', selected.tn_normal_correct, 'good'],
    ['FP', 'Normal dibaca attack', selected.fp_normal_as_attack, 'risk'],
    ['FN', 'Attack dibaca normal', selected.fn_attack_as_normal, 'risk'],
    ['TP', 'Attack benar', selected.tp_attack_correct, 'good'],
  ];

  qs('#confusion-grid').innerHTML = cells.map(([code, label, value, tone]) => {
    const rate = total ? Number(value || 0) / total : 0;
    return `
      <div class="matrix-cell ${tone}">
        <span>${escapeHtml(code)} - ${escapeHtml(label)}</span>
        <strong>${formatNumber(value)}</strong>
        <small>${formatPercent(rate, 4)} dari selected test rows</small>
      </div>
    `;
  }).join('');
}

function renderForensics(data) {
  const shapRows = data.advanced_summary?.top_shap_feature_groups || [];
  const featureRows = shapRows.length ? shapRows : (data.forensic_summary?.top_feature_groups || []);
  const normalizedKey = shapRows.length ? 'normalized' : 'mean_normalized_importance';
  const labelRows = featureRows.slice(0, 8).map((row) => ({
    ...row,
    chartLabel: row.feature_group,
    chartValue: Number(row[normalizedKey] || 0),
  }));
  const fallback = qs('#feature-fallback');

  chartState.featureEvidence?.destroy();
  chartState.featureEvidence = makeChart(
    qs('#feature-chart'),
    fallback,
    {
      type: 'bar',
      data: {
        labels: labelRows.map((row) => row.chartLabel),
        datasets: [{
          label: shapRows.length ? 'Normalized mean |SHAP|' : 'Mean normalized importance',
          data: labelRows.map((row) => row.chartValue),
          backgroundColor: 'rgba(53, 244, 189, 0.74)',
          borderColor: '#35f4bd',
          borderWidth: 1,
        }],
      },
      options: baseChartOptions({
        indexAxis: 'y',
        scales: {
          x: {
            min: 0,
            grid: { color: 'rgba(151, 255, 229, 0.12)' },
            ticks: { color: '#9bb6b4' },
          },
          y: {
            grid: { display: false },
            ticks: { color: '#bdd5d2' },
          },
        },
        plugins: {
          ...baseChartOptions().plugins,
          legend: { display: false },
        },
      }),
    },
    labelRows,
    'chartValue',
    'chartLabel',
    { metric: true },
  );

  setChartFallback(fallback, labelRows, 'chartValue', 'chartLabel', { metric: true });
  if (chartState.featureEvidence) fallback.hidden = true;

  qs('#feature-list').innerHTML = labelRows.map((row) => `
    <div class="feature-row">
      <span>
        ${escapeHtml(row.feature_group)}
        <small>${escapeHtml(row.interpretation_hint || 'Tidak ada interpretation hint.')}</small>
      </span>
      <strong>${formatMetric(row.chartValue)}</strong>
    </div>
  `).join('');
}

function renderAdvanced(data) {
  const trackA = (data.advanced_models || []).find((row) => row.track === 'A_realistic_imbalanced') || {};
  const best = data.advanced_summary?.best_overall_by_macro_f1_mcc || data.advanced_models?.[0] || {};
  const skipped = data.advanced_summary?.skipped_runs || [];

  qs('#advanced-grid').innerHTML = `
    <article class="advanced-card highlight">
      <p class="section-kicker">Track A realistis</p>
      <h3>${escapeHtml(modelDisplayName(trackA))}</h3>
      <strong class="big-value">${formatDelta(trackA.delta_macro_f1_vs_baseline)}</strong>
      <p>Delta Macro F1 terhadap baseline track yang sama. Macro F1: ${formatMetric(trackA.macro_f1)}; MCC: ${formatMetric(trackA.mcc)}.</p>
    </article>
    <article class="advanced-card">
      <p class="section-kicker">Best overall</p>
      <h3>${escapeHtml(modelDisplayName(best))}</h3>
      <strong class="big-value">${formatMetric(best.macro_f1)}</strong>
      <p>${escapeHtml(compactTrack(best.track))}; dibandingkan dengan ${escapeHtml(best.baseline_best_model_for_track || 'baseline terbaik')} pada track yang sama.</p>
    </article>
    <article class="advanced-card">
      <p class="section-kicker">Runtime control</p>
      <h3>Skipped heavy runs</h3>
      <strong class="big-value">${formatNumber(skipped.length)}</strong>
      <p>XGBoost dan CatBoost Track A dapat dilewati untuk menjaga runtime dan memori lokal.</p>
    </article>
  `;
}

function renderEvidence(data) {
  const edaWarnings = data.eda_summary?.warnings || [];
  const forensicLimitations = data.forensic_summary?.limitations || [];
  const advancedLimitations = data.advanced_summary?.limitations || [];
  const policies = [
    data.baseline_summary?.metric_policy,
    data.advanced_summary?.metric_policy,
    data.forensic_summary?.interpretation_policy,
  ].filter(Boolean);
  const outputPaths = [
    ...(data.forensic_summary?.outputs?.tables || []),
    ...(data.forensic_summary?.outputs?.figures || []),
    ...(data.advanced_summary?.outputs?.tables || []),
    ...(data.advanced_summary?.outputs?.figures || []),
  ];

  const groups = [
    ['Kebijakan metrik', policies],
    ['Batasan dan risiko', [
      ...edaWarnings,
      ...forensicLimitations,
      ...advancedLimitations,
      'Controlled subsets can overstate performance and must not replace Track A interpretation.',
      'Global SHAP aggregation differs from Track A-specific interpretation, so both contexts must remain separate.',
    ]],
    ['Artifact evidence', outputPaths],
  ];

  qs('#evidence-grid').innerHTML = groups.map(([title, items], index) => `
    <details ${index === 0 ? 'open' : ''}>
      <summary>${escapeHtml(title)}</summary>
      <ul>
        ${items.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}
      </ul>
    </details>
  `).join('');
}

function renderError(error) {
  console.error(error);
  qs('#project-status').textContent = 'Gagal memuat dashboard-data.json';
  qs('#telemetry-stack').innerHTML = '<p class="muted">Jalankan scripts/generate_dashboard_data.py lalu buka dashboard melalui static server.</p>';
}

async function main() {
  try {
    setupModelTabs();
    const response = await fetch('data/dashboard-data.json');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    appState.data = data;

    renderHero(data);
    renderKpis(data);
    renderDataset(data);
    renderModeling(data);
    renderConfusionOptions(data);
    renderForensics(data);
    renderAdvanced(data);
    renderEvidence(data);
    renderLucideIcons();
  } catch (error) {
    renderError(error);
  }
}

document.addEventListener('DOMContentLoaded', main);
