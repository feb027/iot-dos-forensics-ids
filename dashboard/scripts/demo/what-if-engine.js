const WEIGHTS = {
  N_IN_Conn_P_DstIP: 0.30,
  N_IN_Conn_P_SrcIP: 0.16,
  srate: 0.14,
  stddev: 0.12,
  state_number: 0.10,
  mean: 0.08,
  max: 0.06,
  drate: 0.04,
};

function clamp(value, min = 0, max = 1) {
  return Math.max(min, Math.min(max, value));
}

function norm(feature, value) {
  const n = Number(value || 0);
  const denominators = {
    N_IN_Conn_P_DstIP: 25,
    N_IN_Conn_P_SrcIP: 25,
    srate: 1,
    drate: 1,
    stddev: 1.6,
    state_number: 6,
    mean: 5,
    max: 5,
  };
  return clamp(n / (denominators[feature] || 1));
}

export function predictRisk(features) {
  const evidence = Object.entries(WEIGHTS).map(([feature, weight]) => {
    const value = norm(feature, features[feature]);
    return {
      feature,
      value: Number(features[feature] || 0),
      weight: value * weight,
      reason: featureReason(feature),
    };
  });
  const protoBonus = String(features.proto || '').toLowerCase() === 'udp' ? 0.04 : String(features.proto || '').toLowerCase() === 'tcp' ? 0.025 : 0.01;
  const score = clamp(evidence.reduce((sum, row) => sum + row.weight, 0) + protoBonus);
  return {
    label: score >= 0.55 ? 'dos_or_ddos' : 'normal',
    risk_score: score,
    confidence: score >= 0.55 ? score : 1 - score,
    evidence: evidence.sort((a, b) => b.weight - a.weight).slice(0, 6),
    model: 'artifact-grounded surrogate IDS',
    threshold: 0.55,
  };
}

function featureReason(feature) {
  const reasons = {
    N_IN_Conn_P_DstIP: 'konsentrasi koneksi ke destination IP/gateway IoT',
    N_IN_Conn_P_SrcIP: 'indikasi pola flood dari source tertentu',
    srate: 'source packet rate agresif',
    drate: 'ketidakseimbangan request-response',
    stddev: 'variasi flow abnormal',
    state_number: 'status koneksi abnormal/gagal',
    mean: 'intensitas umum trafik',
    max: 'spike maksimum trafik',
  };
  return reasons[feature] || 'fitur pendukung';
}
