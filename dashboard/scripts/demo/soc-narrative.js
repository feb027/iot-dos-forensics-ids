import { riskText } from '../core/format.js';

export function buildLocalReport(scenario, prediction) {
  const label = prediction.label === 'dos_or_ddos' ? 'DoS/DDoS' : 'Normal';
  const top = (prediction.evidence || []).slice(0, 4).map((row) => `${row.feature}: ${row.reason}`);
  return {
    source: 'client-side deterministic fallback',
    summary: `Skenario ${scenario.name} dianalisis sebagai ${label} dengan risk score ${prediction.risk_score.toFixed(3)} (${riskText(prediction.risk_score)}).`,
    evidence_chain: top.length ? top : ['Tidak ada evidence dominan yang tersedia.'],
    risk_note: scenario.expected_outcome?.includes('FN')
      ? 'Kasus FN perlu diperhatikan karena attack dapat lolos sebagai normal.'
      : scenario.expected_outcome?.includes('FP')
        ? 'Kasus FP perlu diperhatikan karena trafik normal bisa membebani analyst sebagai alert.'
        : 'Baca hasil bersama confusion matrix dan batasan normal class kecil.',
    recommendations: [
      'Validasi destination/source concentration pada flow serupa.',
      'Prioritaskan mitigasi rate limiting dan isolasi trafik jika risk high.',
      'Gunakan hasil ini sebagai triage awal, bukan bukti attribution aktor.',
    ],
    limitation: 'Report ini artifact-grounded dari hasil eksperimen BoT-IoT dan simulator edukatif, bukan production real-time IDS.',
    grounding: scenario.grounding || ['dashboard/data/demo-scenarios.json', 'results/tables/advanced_shap_summary.csv'],
  };
}
