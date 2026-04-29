# Fase 6C — SOC Replay Visual Overhaul

## Tujuan

Meningkatkan demo Fase 6B yang sebelumnya terasa seperti timeline statis menjadi replay investigasi SOC yang lebih visual dan presentable untuk UAS. Fokusnya bukan menambah klaim eksperimen baru, tetapi membuat interpretasi artifact lebih mudah dipahami.

## UI Skills yang digunakan

- `baseline-ui` dari UI Skills: guardrail aksesibilitas, typography data, fokus, dan anti-slop UI.
- `fixing-motion-performance` dari UI Skills: animasi dibatasi ke `transform`/`opacity`, ada `prefers-reduced-motion`, dan tidak memakai loop layout berat.
- Prinsip `frontend-design`/`interface-design` dari ui-skills.com: demo harus punya signature interaction yang khas domain SOC, bukan dashboard generik.

## Implementasi

Komponen baru:

- `dashboard/scripts/components/network-replay.js`
  - Visual packet replay dari source/bot ke IoT gateway lalu device/service.
  - Mode visual berbeda untuk attack, normal, false positive, dan missed/FN case.
- `dashboard/scripts/components/event-stream.js`
  - Live SOC event stream dengan timestamp.
- `dashboard/scripts/components/threat-meter.js`
  - Threat meter berbasis risk score heuristic.
- `dashboard/scripts/demo/replay-engine.js`
  - Play/scrub engine untuk replay timeline.

Perubahan UI:

- `dashboard/demo.html` sekarang memiliki SOC Replay Console, packet replay canvas, scrubber, speed control, threat meter, compact timeline, dan event stream.
- `dashboard/styles/demo.css` ditambah styling Fase 6C untuk SOC war-room, packet pulses, traffic sparkline, event stream, dan reduced-motion fallback.

## Batas akademik

Visual replay adalah representasi edukatif dari skenario dan fitur artifact. Packet animation bukan capture PCAP asli dan tidak menambah metrik eksperimen baru. Risk score tetap heuristic demo berbasis fitur penting/SHAP, bukan probabilitas model LightGBM/XGBoost.

## Validasi

Validasi wajib:

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

Expected: semua lulus.
