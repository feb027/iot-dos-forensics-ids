export function formatNumber(value, digits = 0) {
  const number = Number(value);
  if (!Number.isFinite(number)) return '-';
  return number.toLocaleString('id-ID', { maximumFractionDigits: digits });
}

export function formatMetric(value, digits = 4) {
  const number = Number(value);
  if (!Number.isFinite(number)) return '-';
  return number.toFixed(digits);
}

export function formatPercent(value, digits = 1) {
  const number = Number(value);
  if (!Number.isFinite(number)) return '-';
  return `${(number * 100).toFixed(digits)}%`;
}

export function riskLabel(score) {
  if (score >= 0.72) return 'high';
  if (score >= 0.45) return 'medium';
  return 'low';
}

export function riskText(score) {
  const label = riskLabel(score);
  return label === 'high' ? 'HIGH RISK' : label === 'medium' ? 'MEDIUM RISK' : 'LOW RISK';
}
