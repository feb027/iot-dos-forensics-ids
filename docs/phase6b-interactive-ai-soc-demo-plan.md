# Fase 6B — Interactive AI SOC Demo Plan

## Keputusan awal

Demo interaktif **bisa berjalan di GitHub Pages** jika dibuat sebagai static-first dashboard:

- data scenario disiapkan sebagai JSON,
- interaksi dijalankan di browser dengan JavaScript modules,
- narasi AI SOC dibuat deterministik dari artifact/model evidence,
- tidak ada API key atau backend live.

VPS diperlukan hanya jika ingin fitur dinamis seperti:

- LLM live chat/enrichment,
- model inference real-time via backend Python/Node,
- upload CSV/flow pengguna,
- database session/history,
- auth/private demo.

Rekomendasi untuk UAS: **static-first GitHub Pages + optional VPS backend later**. Ini paling aman, reproducible, ringan, dan tetap terlihat modern.

## Nama fitur

**Interactive AI SOC Demo**

Tagline:

> Replay trafik IoT, lihat prediksi DoS/DDoS, baca bukti fitur, dan dapatkan ringkasan investigasi ala AI SOC analyst.

## Konsep demo

### 1. Incident Replay

User memilih skenario:

- Normal traffic
- DoS/DDoS true positive
- False positive normal-as-attack
- False negative attack-as-normal
- Borderline high-risk traffic

Dashboard menampilkan:

- timeline replay,
- prediction card,
- confidence/risk score,
- top evidence features,
- SHAP/importance bars,
- outcome: TP/TN/FP/FN jika known sample,
- recommended analyst action.

### 2. What-if Attack Simulator

User mengubah fitur utama:

- `N_IN_Conn_P_DstIP`
- `N_IN_Conn_P_SrcIP`
- `srate`
- `stddev`
- `state_number`
- `mean`
- `max`
- `min`
- `proto`

Output berubah secara interaktif:

- predicted label,
- risk level,
- feature evidence,
- explanation narrative,
- mitigation suggestion.

Catatan: jika tidak menjalankan model asli di browser, beri label:

> Educational simulator based on model artifacts and forensic feature patterns, not production live inference.

### 3. AI SOC Analyst Panel

Panel ringkasan otomatis:

- Incident summary
- Evidence chain
- Why model flags/does not flag the traffic
- FP/FN risk note
- Analyst recommendation
- Academic limitation note

Implementasi awal: template generator deterministic dari JSON evidence.

Implementasi opsional VPS: LLM enrichment via backend OpenAI-compatible/local Ollama, tetap grounded ke JSON evidence.

## GitHub Pages vs VPS

| Fitur | GitHub Pages | VPS |
|---|---:|---:|
| Static dashboard | Ya | Ya |
| ES module JS modular | Ya | Ya |
| Fetch JSON artifact | Ya | Ya |
| Incident replay | Ya | Ya |
| What-if simulator deterministic | Ya | Ya |
| SHAP/evidence visualization | Ya | Ya |
| AI SOC narrative template | Ya | Ya |
| Live LLM chat | Tidak aman/tidak ideal | Ya |
| Backend model inference | Tidak | Ya |
| Upload file user | Terbatas client-side only | Ya |
| API key secret | Tidak bisa aman | Ya |

## Rekomendasi deployment

### Phase 6B-MVP

Deploy di GitHub Pages.

Alasan:

- sudah ada Pages aktif,
- tidak butuh backend,
- bisa dipresentasikan langsung,
- artifact-driven dan reproducible,
- aman dari masalah API key/geolocation/rate limit.

### Phase 6B-Plus optional

Deploy full-stack ke VPS jika MVP sudah stabil.

Subdomain kandidat:

- `iot-dos.aquarise.my.id`
- `soc-iot.aquarise.my.id`
- `demo-iot.aquarise.my.id`

VPS stack:

- static frontend served by Caddy,
- optional FastAPI backend for `/api/explain`, `/api/predict`, `/api/chat`,
- PM2/systemd for backend process,
- Caddy API route before SPA/static catch-all.

## Modular dashboard structure

Jangan monolith `app.js` dan `styles.css` besar. Pecah menjadi modules.

Target structure:

```text
dashboard/
├── index.html                    # landing/current dashboard shell
├── demo.html                     # Interactive AI SOC demo entry
├── styles/
│   ├── base.css                  # reset, tokens, typography
│   ├── layout.css                # grid, cards, responsive layout
│   ├── dashboard.css             # existing dashboard sections
│   ├── demo.css                  # incident replay + simulator styles
│   └── components.css            # badges, buttons, panels, bars
├── scripts/
│   ├── app.js                    # current dashboard entry only
│   ├── demo.js                   # demo entry only
│   ├── core/
│   │   ├── data-loader.js        # fetch JSON helpers
│   │   ├── format.js             # metric/number formatting
│   │   ├── state.js              # small state/event helpers
│   │   └── dom.js                # safe DOM utility functions
│   ├── components/
│   │   ├── metric-card.js
│   │   ├── evidence-bar.js
│   │   ├── timeline.js
│   │   ├── scenario-picker.js
│   │   ├── risk-meter.js
│   │   └── analyst-report.js
│   ├── demo/
│   │   ├── scenario-store.js     # loads demo scenarios
│   │   ├── replay-engine.js      # timeline playback
│   │   ├── what-if-engine.js     # deterministic simulator
│   │   ├── soc-narrative.js      # grounded narrative generator
│   │   └── mitigation-rules.js   # action recommendations
│   └── charts/
│       ├── chart-manager.js
│       ├── fallback-bars.js
│       └── shap-bars.js
└── data/
    ├── dashboard-data.json
    ├── demo-scenarios.json
    ├── demo-feature-ranges.json
    └── demo-narrative-templates.json
```

## Data generation scripts

Add scripts:

```text
scripts/generate_demo_scenarios.py
scripts/generate_demo_feature_ranges.py
```

Sources:

- `results/tables/forensic_error_examples.csv`
- `results/tables/forensic_feature_importance.csv`
- `results/tables/advanced_shap_summary.csv`
- `results/tables/advanced_model_metrics.csv`
- `results/metrics/advanced_summary.json`
- `results/metrics/forensic_summary.json`

Generated outputs:

- `dashboard/data/demo-scenarios.json`
- `dashboard/data/demo-feature-ranges.json`
- `dashboard/data/demo-narrative-templates.json`
- optional `results/tables/demo_scenarios.csv`

## MVP implementation steps

1. Refactor dashboard static assets into modular structure without changing visual output.
2. Add `demo.html` as separate page linked from existing dashboard nav.
3. Generate `demo-scenarios.json` from existing error examples and top feature artifacts.
4. Implement incident replay UI.
5. Implement deterministic AI SOC analyst narrative generator.
6. Implement what-if simulator with safe educational label.
7. Add mobile responsive checks and fallback rendering.
8. Run local browser smoke test.
9. Codex dashboard/lecturer review.
10. Commit, PR, merge, verify GitHub Pages.

## Validation commands

```bash
python3 scripts/generate_dashboard_data.py
python3 scripts/generate_demo_scenarios.py
python3 -m py_compile scripts/*.py
python3 -m pytest -q
python3 -m json.tool dashboard/data/dashboard-data.json >/dev/null
python3 -m json.tool dashboard/data/demo-scenarios.json >/dev/null
node --check dashboard/scripts/app.js
node --check dashboard/scripts/demo.js
```

Browser checks:

- dashboard old page still loads,
- demo page loads,
- scenario picker works,
- timeline replay works,
- what-if sliders update prediction/risk/evidence,
- no console errors,
- mobile no horizontal overflow.

## Academic framing

Use wording:

- "interactive prototype"
- "AI SOC-style evidence summarization"
- "artifact-grounded investigation narrative"
- "educational what-if simulator"

Avoid wording:

- "production IDS"
- "real-time detection system" unless backend/live capture exists
- "LLM proves the attack"
- "MITRE attribution" from dataset-only traffic features

## Final recommendation

Build GitHub Pages MVP first. Only move to VPS if the user wants live LLM/backend inference after static demo is approved.
