# Fase 6B — Interactive AI SOC Demo Progress

## Status

Implemented and deployed as a VPS-backed prototype under existing domain path:

- Live demo: https://iot.aquarise.my.id/soc-demo/demo.html
- API health: https://iot.aquarise.my.id/soc-demo/api/health

## Implemented features

- Modular frontend entry: `dashboard/demo.html`.
- Modular CSS: `dashboard/styles/base.css`, `layout.css`, `components.css`, `demo.css`.
- Modular JS:
  - `dashboard/scripts/demo.js`
  - `dashboard/scripts/core/*`
  - `dashboard/scripts/components/*`
  - `dashboard/scripts/demo/*`
- Generated demo data:
  - `dashboard/data/demo-scenarios.json`
  - `dashboard/data/demo-feature-ranges.json`
  - `dashboard/data/demo-narrative-templates.json`
- Generator script: `scripts/generate_demo_scenarios.py`.
- FastAPI backend:
  - `GET /api/health`
  - `GET /api/scenarios`
  - `POST /api/predict`
  - `POST /api/soc/analyze`
  - `POST /api/flow/analyze`
  - `POST /api/chat`
- PM2 backend process: `iot-dos-soc-demo-api`.
- Caddy runtime route under existing `iot.aquarise.my.id` block:
  - `/soc-demo/*` static frontend
  - `/soc-demo/api/*` FastAPI backend

## Deployment notes

Static files are deployed to:

```text
/home/aqua/public_html/iot-soc-demo
```

Backend runs from repo path:

```text
/home/aqua/iot-dos-forensics-ids/backend/app.py
```

PM2 config:

```text
deploy/ecosystem.soc-demo.config.cjs
```

Caddy snippet for persistent install:

```text
deploy/Caddyfile.soc-demo-snippet
```

Current Caddy route was applied through runtime `caddy reload` using a generated `/tmp/Caddyfile.iot-soc-demo`, because the agent user does not have passwordless sudo access to edit `/etc/caddy/Caddyfile`. If Caddy is restarted from the original system config, the snippet should be added persistently.

## Validation

Passed:

```bash
python3 scripts/generate_dashboard_data.py
python3 scripts/generate_demo_scenarios.py
python3 -m py_compile scripts/*.py
python3 -m compileall -q backend
python3 -m json.tool dashboard/data/dashboard-data.json >/dev/null
python3 -m json.tool dashboard/data/demo-scenarios.json >/dev/null
python3 -m json.tool dashboard/data/demo-feature-ranges.json >/dev/null
python3 -m json.tool dashboard/data/demo-narrative-templates.json >/dev/null
node --check dashboard/app.js
node --check dashboard/scripts/*.js dashboard/scripts/core/*.js dashboard/scripts/components/*.js dashboard/scripts/demo/*.js
python3 -m pytest -q
```

Result:

```text
25 passed
```

Live HTTP checks:

- `https://iot.aquarise.my.id/soc-demo/demo.html` → HTTP 200
- `https://iot.aquarise.my.id/soc-demo/data/demo-scenarios.json` → HTTP 200
- `https://iot.aquarise.my.id/soc-demo/api/health` → HTTP 200
- `POST https://iot.aquarise.my.id/soc-demo/api/predict` → HTTP 200, returns `dos_or_ddos` for high-risk synthetic scenario.

## Academic boundary

Use this wording in manuscript/demo:

> Interactive AI SOC prototype berbasis artifact eksperimen BoT-IoT. Sistem ini menampilkan replay, risk scoring, evidence features, dan SOC-style report untuk mendukung interpretasi hasil modeling; bukan production real-time IDS dan bukan bukti attribution dunia nyata.
