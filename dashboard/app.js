async function main() {
  const statusEl = document.querySelector('#status');
  const summaryEl = document.querySelector('#summary');
  const datasetSummaryEl = document.querySelector('#dataset-summary');
  try {
    const res = await fetch('data/dashboard-data.json');
    const data = await res.json();
    const project = data.project || {};
    const dataset = data.dataset_summary || {};
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
  } catch (error) {
    statusEl.textContent = 'Gagal memuat dashboard-data.json. Jalankan scripts/generate_dashboard_data.py terlebih dahulu.';
    if (datasetSummaryEl) datasetSummaryEl.textContent = 'Gagal memuat ringkasan dataset.';
    console.error(error);
  }
}

main();
