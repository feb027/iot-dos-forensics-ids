async function main() {
  const statusEl = document.querySelector('#status');
  const summaryEl = document.querySelector('#summary');
  const datasetSummaryEl = document.querySelector('#dataset-summary');
  const edaSummaryEl = document.querySelector('#eda-summary');
  try {
    const res = await fetch('data/dashboard-data.json');
    const data = await res.json();
    const project = data.project || {};
    const dataset = data.dataset_summary || {};
    const eda = data.eda_summary || {};
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
  } catch (error) {
    statusEl.textContent = 'Gagal memuat dashboard-data.json. Jalankan scripts/generate_dashboard_data.py terlebih dahulu.';
    if (datasetSummaryEl) datasetSummaryEl.textContent = 'Gagal memuat ringkasan dataset.';
    if (edaSummaryEl) edaSummaryEl.textContent = 'Gagal memuat ringkasan EDA.';
    console.error(error);
  }
}

main();
