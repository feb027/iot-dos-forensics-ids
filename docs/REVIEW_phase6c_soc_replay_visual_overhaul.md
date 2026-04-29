# Review Fase 6C - SOC Replay Visual Overhaul

Repo: `/home/aqua/iot-dos-forensics-ids`  
Branch: `phase-6c-soc-replay-visual-overhaul`  
PR: `#9`  
Tanggal review: 2026-04-29

## Verdict

**Score: 90/100**  
**Verdict: APPROVED**

Tidak ada critical issue. Perubahan layak diterima untuk Fase 6C karena replay sekarang jauh lebih presentable dibanding timeline 1-4 statis, tetap menjaga boundary akademik, dan validasi teknis lulus.

## Ringkasan Review

1. **Visual replay lebih menarik:** APPROVED. Halaman `dashboard/demo.html` sekarang menampilkan SOC replay console dengan visual jaringan, packet animation, HUD, threat meter, event stream, scrubber, dan mode visual berbeda untuk attack/normal/FP/FN. Ini jelas lebih kuat untuk demo UAS dibanding timeline angka 1-4 yang statis.
2. **Frontend modular:** APPROVED. Implementasi tidak menjadi monolith baru. Orkestrasi tetap di `dashboard/scripts/demo.js`, sedangkan visual utama dipisah ke `network-replay.js`, `event-stream.js`, `threat-meter.js`, dan `replay-engine.js`. Ukuran modul baru masih kecil dan mudah diaudit.
3. **Animasi dan performa:** APPROVED dengan catatan minor. Animasi utama memakai `transform` dan `opacity`, bukan `top/left/width/height`, dan ada `@media (prefers-reduced-motion: reduce)`. Catatan: `.timeline-step` masih memakai `transition: all .28s ease`, looping animation belum dipause saat off-screen, dan replay frame masih rebuild beberapa container via `innerHTML`. Ini belum blocker karena permukaan DOM kecil, tetapi sebaiknya diperbaiki pada polish berikutnya.
4. **Aksesibilitas minimal:** APPROVED. Kontrol utama memakai elemen native (`button`, `select`, `input type="range"`), ada skip link, `aria-label`, `aria-live`, teks status, dan risk tidak hanya disampaikan lewat warna. Catatan minor: scenario card aktif bisa ditingkatkan dengan `aria-pressed` atau `aria-current`.
5. **Academic boundary:** APPROVED. README dan progress report menyatakan visual replay bukan PCAP aktual, risk score adalah heuristic demo, dan tidak ada klaim metric/model baru. Teks UI juga masih mengarah ke artifact-grounded prototype.
6. **Caddy helper script:** APPROVED dengan catatan minor. `deploy/install_soc_demo_caddy.py` idempotent melalui marker `/soc-demo`, membuat backup sebelum menulis, dan tidak menghapus konfigurasi lama. Risiko tersisa: pencarian site block masih berbasis string hardcoded dan belum memvalidasi Caddyfile setelah write; ini acceptable untuk helper kecil, tetapi dokumentasi sudah benar meminta `caddy validate`.

## Temuan Minor

- `dashboard/styles/demo.css`: `.timeline-step { ... transition: all .28s ease; }` sebaiknya dibatasi menjadi `transition: opacity .18s ease-out, transform .18s ease-out;` agar tidak membuka risiko animasi layout/paint jika properti lain berubah.
- `dashboard/styles/demo.css`: `.packet` dan `.traffic-spark span` melakukan infinite animation. Reduced motion sudah ditangani, tetapi belum ada pause off-screen dengan IntersectionObserver atau mekanisme visibility. Untuk halaman demo pendek ini bukan blocker.
- `dashboard/scripts/demo.js`: `renderReplayFrame()` merender ulang timeline, network replay, event stream, dan threat meter setiap frame. Lebih efisien jika DOM visual dibuat stabil lalu hanya class/state aktif yang diubah, tetapi beban saat ini masih kecil.
- `dashboard/scripts/demo.js`: `renderForm()` menambahkan listener `input` setiap scenario dipilih ulang. Dampaknya kecil, tetapi bisa menumpuk callback jika user sering mengganti skenario.
- `deploy/install_soc_demo_caddy.py`: idempotency sudah ada, tetapi parser konfigurasi belum structural. Jika Caddyfile memiliki lebih dari satu block serupa atau format berbeda, insertion bisa kurang presisi.

## Validasi

Semua validasi yang diminta lulus:

```text
python3 scripts/generate_dashboard_data.py
PASS - wrote dashboard/data/dashboard-data.json

python3 scripts/generate_demo_scenarios.py
PASS - scenarios=4

python3 -m py_compile scripts/*.py deploy/install_soc_demo_caddy.py
PASS

python3 -m compileall -q backend
PASS

python3 -m pytest -q
PASS - 27 passed in 3.56s

node --check dashboard/app.js and all dashboard/scripts modules
PASS
```

Catatan: generator JSON memperbarui timestamp saat validasi; diff sementara dari proses validasi sudah dikembalikan agar review ini hanya menulis file review.

## Keterbatasan Review

Saya tidak menjalankan verifikasi browser visual langsung atau screenshot Playwright. Penilaian visual dilakukan dari source HTML/CSS/JS, struktur komponen, dan validasi sintaks/test. Karena itu, potensi masalah framing responsif kecil atau overlap visual runtime masih perlu dicek manual di browser sebelum presentasi UAS.

## Keputusan Akhir

**APPROVED.** Fase 6C memenuhi tujuan visual overhaul tanpa melewati boundary akademik proyek. Catatan yang tersisa bersifat polish/performance minor, bukan blocker untuk merge.
