async function main() {
  const statusEl = document.querySelector('#status');
  const summaryEl = document.querySelector('#summary');
  const datasetSummaryEl = document.querySelector('#dataset-summary');
  const edaSummaryEl = document.querySelector('#eda-summary');
  const baselineSummaryEl = document.querySelector('#baseline-summary');
  try {
    const res = await fetch('data/dashboard-data.json');
    const data = await res.json();
    const project = data.project || {};
    const dataset = data.dataset_summary || {};
    const eda = data.eda_summary || {};
    const baseline = data.model_comparison || [];
    statusEl.textContent = project.status || 'Experiment results pending.';
    const items = [
      ['Dataset utama', project.primary_dataset || '-'],
      ['Dataset alternatif', project.alternative_dataset || '-'],
      ['Tema', project.theme || '-'],
      ['Tahap', project.status || '-']
    ];
    summaryEl.innerHTML = items.map(([label, value]) => `
      <article class="metric"><span>${label}</span><strong>${value}</strong></article>
    `).join('');

    if (dataset.rows) {
      const datasetItems = [
        ['Source', dataset.source || '-'],
        ['Rows audited', Number(dataset.rows).toLocaleString('id-ID')],
        ['CSV files', dataset.files || '-'],
        ['Columns', dataset.columns || '-'],
        ['Candidate features', dataset.candidate_features || '-'],
        ['Excluded/leakage columns', (dataset.excluded_columns || []).join(', ')]
      ];
      datasetSummaryEl.innerHTML = `
        <div class="grid compact">
          ${datasetItems.map(([label, value]) => `
            <article class="metric"><span>${label}</span><strong>${value}</strong></article>
          `).join('')}
        </div>
      `;
    } else {
      datasetSummaryEl.textContent = 'Audit dataset belum tersedia.';
    }

    if (eda.total_rows) {
      const train = eda.scope_counts?.train || {};
      const test = eda.scope_counts?.test || {};
      const edaItems = [
        ['EDA rows', Number(eda.total_rows).toLocaleString('id-ID')],
        ['Train normal', Number(train.normal || 0).toLocaleString('id-ID')],
        ['Test normal', Number(test.normal || 0).toLocaleString('id-ID')],
        ['Candidate features', (eda.candidate_features || []).length],
        ['Phase 4 tracks', (eda.recommended_phase4_tracks || []).length],
        ['Figures', (eda.figures || []).length]
      ];
      edaSummaryEl.innerHTML = `
        <div class="grid compact">
          ${edaItems.map(([label, value]) => `
            <article class="metric"><span>${label}</span><strong>${value}</strong></article>
          `).join('')}
        </div>
      `;
    } else {
      edaSummaryEl.textContent = 'EDA/preprocessing belum tersedia.';
    }

    if (baseline.length) {
      const best = baseline[0];
      const baselineItems = [
        ['Completed runs', baseline.length],
        ['Best model', best.model_display_name || best.model],
        ['Best track', best.track],
        ['Macro F1', Number(best.macro_f1).toFixed(4)],
        ['MCC', Number(best.mcc).toFixed(4)],
        ['Recall normal', Number(best.recall_normal).toFixed(4)]
      ];
      baselineSummaryEl.innerHTML = `
        <div class="grid compact">
          ${baselineItems.map(([label, value]) => `
            <article class="metric"><span>${label}</span><strong>${value}</strong></article>
          `).join('')}
        </div>
        <p class="note">Accuracy tidak dipakai sebagai klaim utama karena normal class sangat kecil. Ringkasan ini memakai Macro F1, MCC, balanced accuracy, dan confusion matrix.</p>
      `;
    } else {
      baselineSummaryEl.textContent = 'Baseline model belum dijalankan. Metrik akan muncul setelah Fase 4 selesai.';
    }
  } catch (error) {
    statusEl.textContent = 'Gagal memuat dashboard-data.json. Jalankan scripts/generate_dashboard_data.py terlebih dahulu.';
    if (datasetSummaryEl) datasetSummaryEl.textContent = 'Gagal memuat ringkasan dataset.';
    if (edaSummaryEl) edaSummaryEl.textContent = 'Gagal memuat ringkasan EDA.';
    if (baselineSummaryEl) baselineSummaryEl.textContent = 'Gagal memuat ringkasan baseline.';
    console.error(error);
  }
}

main();
