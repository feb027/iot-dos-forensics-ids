async function main() {
  const statusEl = document.querySelector('#status');
  const summaryEl = document.querySelector('#summary');
  try {
    const res = await fetch('data/dashboard-data.json');
    const data = await res.json();
    const project = data.project || {};
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
  } catch (error) {
    statusEl.textContent = 'Gagal memuat dashboard-data.json. Jalankan scripts/generate_dashboard_data.py terlebih dahulu.';
    console.error(error);
  }
}

main();
