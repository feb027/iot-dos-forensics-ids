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

Rekomendasi terbaru setelah diskusi: **VPS-backed demo as primary target + GitHub Pages static fallback**. MVP tetap harus artifact-grounded, tetapi fitur unggulan memakai backend agar demo terasa lebih modern dan hidup.

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

Deploy **full-stack ke VPS** sebagai target utama, dengan GitHub Pages sebagai static fallback/demo cadangan.

Alasan:

- fitur live LLM/SOC analyst bisa berjalan aman karena API key disimpan di backend,
- model inference atau explain endpoint bisa dijalankan server-side,
- demo terasa lebih modern daripada static-only,
- domain/subdomain VPS memberi kesan produk/prototype nyata,
- GitHub Pages tetap dipakai sebagai bukti static artifact dan fallback kalau backend bermasalah saat presentasi.

### Phase 6B-Plus optional

Tambahkan fitur lanjutan setelah full-stack MVP stabil.

Subdomain kandidat:

- `iot-dos.aquarise.my.id`
- `soc-iot.aquarise.my.id`
- `demo-iot.aquarise.my.id`

VPS stack:

- static frontend served by Caddy,
- optional FastAPI backend for `/api/explain`, `/api/predict`, `/api/chat`,
- PM2/systemd for backend process,
- Caddy API route before SPA/static catch-all.


## VPS-backed feature set

Target fitur yang memang membutuhkan VPS/backend:

1. **Live AI SOC Analyst**
   - Endpoint: `POST /api/soc/analyze`
   - Input: selected scenario + model evidence + SHAP/evidence features.
   - Output: structured incident report: summary, evidence chain, FP/FN risk, recommended action.
   - Guardrail: backend only accepts artifact-grounded JSON, not free-form hallucinated claims.

2. **Server-side prediction/explanation endpoint**
   - Endpoint: `POST /api/predict`
   - Input: what-if feature values.
   - Output: predicted label, risk score, top features, explanation.
   - MVP can use deterministic/surrogate rules; later can load actual exported LightGBM/XGBoost model if model artifact is safe to store on VPS but not committed.

3. **Upload CSV/flow sample for demo**
   - Endpoint: `POST /api/flow/analyze`
   - User uploads or pastes one flow row.
   - Backend validates allowed columns only, rejects label/leakage columns, returns prediction/explanation.

4. **Analyst chat constrained to project evidence**
   - Endpoint: `POST /api/chat`
   - Chatbot answers only from project artifacts: metrics, tables, references, limitations.
   - If answer is not grounded, return "tidak tersedia di artifact".

## Proposed VPS stack

```text
Caddy HTTPS
  ├── /                  -> modular static frontend
  ├── /assets/*          -> static assets
  └── /api/*             -> FastAPI backend on localhost:<port>

FastAPI backend
  ├── loads sanitized dashboard/demo JSON
  ├── optional loads local model artifacts from ignored server path
  ├── calls LLM provider/local Ollama only server-side
  └── returns structured JSON reports
```

Suggested subdomain: `soc-iot.aquarise.my.id` or `iot-dos.aquarise.my.id`.

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

Build VPS-backed MVP first because the user wants features that require backend/live AI. Keep GitHub Pages as static fallback and artifact showcase.
