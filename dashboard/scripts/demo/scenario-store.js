import { loadJson } from '../core/data-loader.js';

export async function loadScenarioBundle() {
  const [scenarios, ranges, templates] = await Promise.all([
    loadJson('data/demo-scenarios.json'),
    loadJson('data/demo-feature-ranges.json'),
    loadJson('data/demo-narrative-templates.json'),
  ]);
  return { scenarios, ranges, templates };
}

export function scenarioById(bundle, id) {
  return (bundle.scenarios.scenarios || []).find((scenario) => scenario.id === id) || bundle.scenarios.scenarios?.[0];
}
