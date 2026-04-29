# Review Fase 6 Dashboard Polish

Tanggal review: 2026-04-29

Branch: `phase-6-dashboard-polish`

PR: https://github.com/feb027/iot-dos-forensics-ids/pull/7

## Executive summary

Dashboard sudah kuat dari sisi artifact-driven data, claim safety, dan validasi teknis dasar. `dashboard/data/dashboard-data.json` dapat diregenerasi dari artifact repo tanpa diff, metrik utama cocok dengan `results/tables/` dan `results/metrics/`, serta tidak ditemukan raw dataset besar atau model binary yang ter-track.

Namun, ada satu masalah visual penting pada fallback chart distribusi kelas: saat Chart.js tersedia di desktop, fallback bar tetap dibuat dan tidak disembunyikan setelah chart berhasil dibuat. Ini berisiko membuat chart dan fallback tampil bersamaan pada panel `Class Distribution`. Selain itu, `docs/dashboard-spec.md` masih stale karena menyebut arah desain light/white dan data contract lama, sementara Fase 6 sudah memakai dark SOC dashboard yang disetujui.

## Validation commands and results

| Command | Result |
|---|---|
| `python3 scripts/generate_dashboard_data.py` | PASS. Output: `wrote /home/aqua/iot-dos-forensics-ids/dashboard/data/dashboard-data.json` |
| `python3 -m py_compile scripts/*.py` | PASS. Exit code 0, no output. |
| `python3 -m pytest -q` | PASS. Output: `22 passed in 2.75s` |
| `python3 -m json.tool dashboard/data/dashboard-data.json >/dev/null` | PASS. Exit code 0, no output. |
| `node --check dashboard/app.js` | PASS. Exit code 0, no output. |
| `python3 -m http.server 8000 -d dashboard` + `curl -I http://127.0.0.1:8000/` | PASS. HTTP 200, `Content-type: text/html`, `Content-Length: 10273`. |
| `curl -I http://127.0.0.1:8000/app.js` | PASS. HTTP 200, `Content-type: text/javascript`, `Content-Length: 21918`. |
| `curl -I http://127.0.0.1:8000/styles.css` | PASS. HTTP 200, `Content-type: text/css`, `Content-Length: 16447`. |
| `curl -I http://127.0.0.1:8000/data/dashboard-data.json` | PASS. HTTP 200, `Content-type: application/json`, `Content-Length: 79965`. |
| DOM selector static check | PASS. All `qs('#...')` IDs referenced by `dashboard/app.js` exist in `dashboard/index.html`. |
| Chart.js CDN check | PASS. `https://cdn.jsdelivr.net/npm/chart.js@4.4.9/dist/chart.umd.min.js` returned HTTP 200. |
| Lucide CDN check | PASS. `https://unpkg.com/lucide@latest/dist/umd/lucide.min.js` redirected then returned HTTP 200. |

Playwright/browser runtime check was not available in this environment:

- `command -v playwright`: exit code 1.
- `node -e "require('playwright')"`: `playwright-node unavailable`.
- `python3 -c "import importlib.util; ..."`: `playwright-python unavailable`.
- No local `chromium`, `chromium-browser`, `google-chrome`, or `firefox` binary was found.

Fallback review used static server, HTTP checks, `node --check`, DOM selector checking, and manual static review of HTML/CSS/JS.

## Critical issues

None.

## Important issues

1. `dashboard/app.js:298` recreates and unhides `#class-distribution-fallback` after `makeChart()` has already created a Chart.js doughnut. In `makeChart()`, successful chart rendering hides the fallback, but `renderDataset()` immediately calls `setChartFallback(...)`, and `setChartFallback()` sets `container.hidden = false`. The modeling and forensics charts already handle this correctly with `if (chartState.modelComparison) fallback.hidden = true;` and `if (chartState.featureEvidence) fallback.hidden = true;`. Required fix: apply the same pattern for `chartState.classDistribution` or only call `setChartFallback()` when the chart was not created.

2. `docs/dashboard-spec.md:25-31` is stale relative to the approved Fase 6 direction. It still states `Light/white academic style` and `No unnecessary dark theme`, while `docs/phase6-dashboard-design-brief.md` explicitly approves OLED dark/SOC cybersecurity styling and documents the implemented dark dashboard. This is not a penalty against the dark theme; the issue is documentation inconsistency.

## Minor issues

1. Full browser-level JS/runtime verification could not be completed because Playwright and browser binaries are unavailable in the local environment. Static checks did not reveal missing DOM IDs or syntax errors, and local HTTP serving works.

2. `docs/phase-gates.md` still has Fase 6 checklist items unchecked for GitHub Pages and dashboard claims review. That may be expected before this review lands, but it should be synchronized after the required fixes are applied.

## Artifact/data consistency check

PASS.

`scripts/generate_dashboard_data.py` reads from committed artifact sources, including:

- `results/metrics/dataset_audit.json`
- `results/metrics/preprocessing_summary.json`
- `results/metrics/baseline_summary.json`
- `results/metrics/forensic_summary.json`
- `results/metrics/advanced_summary.json`
- `results/tables/class_distribution.csv`
- `results/tables/baseline_model_metrics.csv`
- `results/tables/baseline_confusion_matrices.csv`
- `results/tables/forensic_feature_importance.csv`
- `results/tables/forensic_error_analysis.csv`
- `results/tables/advanced_model_metrics.csv`
- `results/tables/advanced_confusion_matrices.csv`
- `results/tables/advanced_shap_summary.csv`

Spot checks against source artifacts:

| Check | Dashboard value | Source value | Match |
|---|---:|---:|---|
| Dataset rows | 3,668,522 | 3,668,522 from `results/metrics/dataset_audit.json` | Yes |
| Advanced Track A LightGBM macro F1 | 0.98847752 | 0.98847752 from `results/tables/advanced_model_metrics.csv` | Yes |
| Advanced Track A LightGBM MCC | 0.97704843 | 0.97704843 from `results/tables/advanced_model_metrics.csv` | Yes |
| Advanced Track A LightGBM delta macro F1 | 0.0218161 | 0.0218161 from `results/tables/advanced_model_metrics.csv` | Yes |
| Advanced Track A LightGBM confusion matrix | TN=106, FP=1, FN=4, TP=715417 | Same values from `results/tables/advanced_model_metrics.csv` and generated confusion JSON | Yes |
| Baseline Track A Decision Tree macro F1 | 0.96666142 | 0.96666142 from `results/tables/baseline_model_metrics.csv` | Yes |
| Baseline Track A Decision Tree MCC | 0.93444061 | 0.93444061 from `results/tables/baseline_model_metrics.csv` | Yes |
| Top SHAP feature group | `N_IN_Conn_P_DstIP` | `N_IN_Conn_P_DstIP` from `results/metrics/advanced_summary.json` | Yes |
| Top SHAP normalized value | 0.4761954813 | 0.4761954813 from `results/metrics/advanced_summary.json` | Yes |

`git diff -- dashboard/data/dashboard-data.json` was empty after regeneration, so the committed JSON is in sync with the generator output.

## Visual/readability check

Mostly PASS with one required fix.

Strengths:

- Dark SOC/cybersecurity direction is acceptable for this project and matches the user-approved visual direction.
- Typography, section hierarchy, sticky navigation, KPI cards, confusion matrix panel, and evidence accordion are appropriate for an academic dashboard aimed at a lecturer.
- Mobile CSS includes one-column layout, chart fallback bars, reduced chart heights, wrapped nav links, and single-column confusion matrix under narrow screens.
- Accessibility basics are present: skip link, visible focus states, semantic sections/headings, canvas `aria-label`, non-color text values, and `prefers-reduced-motion`.
- Chart fallback strategy is good in principle and protects readability if Chart.js fails.

Required visual fix:

- The `Class Distribution` panel fallback visibility bug must be fixed before merge because it can create duplicated chart/fallback content on desktop when Chart.js loads successfully.

## Claim safety check

PASS.

No unsupported performance overclaim was found in the dashboard copy. The dashboard explicitly states that accuracy is not the main claim, keeps normal-class imbalance visible, and includes limitation text for controlled subsets, sampled SHAP, split-similarity risk, and the difference between global SHAP aggregation and Track A-specific interpretation.

Track A is highlighted as the realistic/audit-distribution result, while best overall Track C is framed as a same-track comparison rather than proof of real-world generalization. SHAP/global feature importance is described as dataset-backed supporting evidence, not causal or perfect real-world detection proof.

## Raw/large artifact tracking check

PASS.

Tracked files under restricted data/model paths:

- `data/raw/.gitkeep`
- `data/processed/.gitkeep`
- `results/models/.gitkeep`

Local raw files exist under `data/raw/bot-iot-hf/`, but they are ignored and not tracked:

- `data/raw/bot-iot-hf/train.csv` size 369,103,929 bytes.
- `data/raw/bot-iot-hf/test.csv` size 92,281,052 bytes.

Ignore checks confirm raw/processed/model binary patterns are covered:

- `.gitignore:16:data/raw/*`
- `.gitignore:17:data/processed/*`
- `.gitignore:21:*.pkl`

## Docs/status check

Mostly PASS, with one required stale-doc update.

Current Fase 6-specific documents are aligned:

- `docs/phase6-dashboard-polish-plan.md` lists the validation commands, claim rules, and Track A/controlled-subset caution.
- `docs/phase6-dashboard-design-brief.md` documents the approved dark SOC direction and implemented notes.
- `README.md` status is current for Fase 6 dashboard polish and Fase 6A artifacts.

Stale doc:

- `docs/dashboard-spec.md` still reflects an older light-theme/data-contract draft. Update it so it does not contradict the approved Fase 6 dashboard direction.

## Score

86/100

## Verdict

NEEDS REVISION

## Required fixes before merge

1. Fix the `Class Distribution` fallback visibility bug in `dashboard/app.js` so fallback bars are hidden when the Chart.js doughnut renders successfully.

2. Update `docs/dashboard-spec.md` to reflect the current artifact-driven dark SOC dashboard direction and current data contract, or clearly mark it as superseded by `docs/phase6-dashboard-design-brief.md`.

3. Re-run and keep passing:
   - `python3 scripts/generate_dashboard_data.py`
   - `python3 -m py_compile scripts/*.py`
   - `python3 -m pytest -q`
   - `python3 -m json.tool dashboard/data/dashboard-data.json >/dev/null`
   - `node --check dashboard/app.js`
