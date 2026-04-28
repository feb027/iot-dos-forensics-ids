# Review Fase 0A/0B

## Ringkasan

Fase 0A/0B pada repo ini **cukup kuat sebagai scaffold awal** untuk proyek UAS bertema IoT Security, IDS, dan *digital forensics*. Arah proyek sudah konsisten dengan judul, dataset utama dan alternatif sudah ditetapkan, prinsip *evidence-first* sudah tertulis jelas, struktur folder sudah tersedia, dan dashboard placeholder sudah disiapkan sebagai dasar GitHub Pages.

Namun, fase ini **belum layak dinyatakan selesai penuh** karena masih ada beberapa masalah fondasional yang langsung memengaruhi kesiapan masuk Fase 1, terutama pada konsistensi status fase, reproducibility command, dan kontrol proses repo.

## Temuan Utama

### Kekuatan

1. Scope awal sudah tepat dan realistis untuk UAS.
   - Fokus biner `normal` vs `DoS/DDoS` di [README.md](/home/aqua/iot-dos-forensics-ids/README.md:22) sudah sesuai untuk baseline IDS IoT sebelum berkembang ke multi-kelas.

2. Aturan anti-halusinasi dan *evidence-first* sudah kuat.
   - Prinsip pada [README.md](/home/aqua/iot-dos-forensics-ids/README.md:28), [AGENTS.md](/home/aqua/iot-dos-forensics-ids/AGENTS.md:19), dan [docs/workflow.md](/home/aqua/iot-dos-forensics-ids/docs/workflow.md:37) sudah sangat tepat untuk proyek akademik berbasis eksperimen.

3. Struktur dokumen kontrol proyek sudah cukup lengkap untuk fase scaffold.
   - `project-brief`, `roadmap`, `project-control`, `phase-gates`, `workflow`, `dashboard-spec`, `research-log`, `experiment-log`, dan `report-outline` sudah tersedia dan saling mendukung.

4. Placeholder dashboard sudah mengikuti prinsip aman.
   - Dashboard belum mengarang hasil dan hanya menampilkan status scaffold dari `dashboard/data/dashboard-data.json`, dengan generator sederhana di [scripts/generate_dashboard_data.py](/home/aqua/iot-dos-forensics-ids/scripts/generate_dashboard_data.py:10).

### Revisi Wajib

1. Sinkronkan status fase 0B dengan kondisi repo aktual.
   - Di [docs/project-control.md](/home/aqua/iot-dos-forensics-ids/docs/project-control.md:9) status masih `In progress`.
   - Di [docs/project-control.md](/home/aqua/iot-dos-forensics-ids/docs/project-control.md:49) masih tertulis `Push initial scaffold to GitHub`.
   - Di [docs/phase-gates.md](/home/aqua/iot-dos-forensics-ids/docs/phase-gates.md:29) dan [docs/phase-gates.md](/home/aqua/iot-dos-forensics-ids/docs/phase-gates.md:35) checklist repo dan push masih kosong.
   - Padahal repo Git sudah ada dan `git status -sb` menunjukkan `main...origin/main`, sehingga dokumentasi kontrol belum konsisten dengan keadaan aktual. Ini harus dibereskan sebelum masuk Fase 1 agar phase gate bisa dipercaya.

2. Rapikan instruksi reproducibility karena command yang didokumentasikan belum portable pada environment ini.
   - [AGENTS.md](/home/aqua/iot-dos-forensics-ids/AGENTS.md:89) masih memakai `python ...`.
   - Validasi menunjukkan `python` tidak tersedia di environment ini, sedangkan `python3 -m py_compile scripts/generate_dashboard_data.py` berhasil.
   - Sebelum Fase 1, tentukan satu standar eksekusi yang konsisten, misalnya `python3` atau environment manager tertentu, lalu samakan semua command di README dan AGENTS.

3. Tambahkan baseline test/repo check yang benar-benar bisa dieksekusi.
   - `python3 -m pytest -q` saat direview berhenti dengan `no tests ran` dan exit code 5.
   - Untuk scaffold awal, minimal harus ada satu smoke test sederhana atau instruksi bahwa fase ini memang belum memiliki test dan pengecekan diganti oleh command validasi lain yang eksplisit.
   - Jika tidak, aturan “run existing tests before making changes” sulit dijalankan secara konsisten pada fase berikutnya.

4. Tegaskan kepatuhan workflow Git sebelum Fase 1 dimulai.
   - Instruksi global menyebut pekerjaan harus dilakukan di branch kerja, bukan `main`.
   - Saat review, worktree berada di branch `main`.
   - Untuk proyek yang akan melewati beberapa fase review, kebiasaan kerja di branch perlu ditegakkan sejak awal agar histori per fase rapi dan aman.

5. Lengkapi definisi kualitas sumber untuk Fase 1 literature review.
   - [references/literature-matrix.md](/home/aqua/iot-dos-forensics-ids/references/literature-matrix.md:1) masih template minimal.
   - Sebelum masuk Fase 1, perlu ditegaskan bahwa referensi utama harus mengutamakan paper/jurnal/prosiding yang relevan, bukan sekadar blog atau artikel populer, serta membedakan paper tentang dataset, IDS IoT, DoS/DDoS, dan *network forensics*.

### Risiko Akademik dan Teknis Sebelum Fase 1

1. Risiko dokumentasi kontrol tidak reliabel.
   - Jika checklist fase tidak sinkron dengan kondisi repo, maka review berikutnya mudah bias dan keputusan lanjut fase menjadi lemah.

2. Risiko reproducibility sejak awal.
   - Command inti yang tidak langsung jalan membuat eksekusi ulang oleh reviewer atau dosen menjadi tidak mulus.

3. Risiko literature review melebar atau dangkal.
   - Scope tema sudah luas: IoT, IDS, DoS/DDoS, ML, BoT-IoT, RT-IoT2022, dan *network forensics*.
   - Tanpa kriteria seleksi referensi yang lebih tegas, Fase 1 bisa berakhir menjadi kumpulan ringkasan paper tanpa gap riset yang tajam.

4. Risiko bias metodologi pada fase berikutnya belum diikat sejak awal.
   - Dataset audit belum mendefinisikan strategi antisipasi imbalance, split leakage, dan potensi duplikasi aliran trafik.
   - Ini memang belum harus selesai di Fase 0B, tetapi sebaiknya sudah disebut eksplisit sebagai fokus wajib Fase 2.

5. Risiko dashboard-spec dan implementasi belum sejajar.
   - [docs/dashboard-spec.md](/home/aqua/iot-dos-forensics-ids/docs/dashboard-spec.md:14) sudah menargetkan banyak section.
   - Implementasi saat ini di [dashboard/app.js](/home/aqua/iot-dos-forensics-ids/dashboard/app.js:1) baru menampilkan ringkasan proyek dan status.
   - Ini masih wajar untuk placeholder, tetapi statusnya perlu ditulis jelas sebagai “placeholder tahap scaffold”, bukan dipersepsikan sebagai dashboard fase lanjut.

## Saran Minor

1. Tambahkan satu bagian `Definition of Done` ringkas di README agar pembaca baru langsung paham output akhir yang diharapkan.

2. Tambahkan `results/README.md` atau placeholder serupa agar struktur artifact lebih mudah dipahami sejak awal.

3. Pertimbangkan menambahkan kolom `Jenis sumber` dan `Catatan kebocoran metodologi` pada literature matrix agar Fase 1 lebih tajam untuk kebutuhan reviewer akademik.

4. Gunakan bahasa status yang konsisten di seluruh repo.
   - Saat ini ada campuran `done conceptually`, `in progress`, `pending`, dan `scaffold created`.

5. Saat Fase 1 dimulai, segera isi `docs/research-log.md` paralel dengan literature matrix agar jejak seleksi referensi tidak hilang.

## Hasil Validasi Ringkas

- Struktur repo inti tersedia: `docs/`, `references/`, `prompts/`, `dashboard/`, `scripts/`, `results/`, `reports/`, `notebooks/`, `data/`.
- Script placeholder dashboard berhasil lolos kompilasi dengan `python3 -m py_compile scripts/generate_dashboard_data.py`.
- Baseline test belum ada; `python3 -m pytest -q` menghasilkan `no tests ran`.
- Dashboard data saat ini masih placeholder dan belum mengandung klaim eksperimen, yang untuk Fase 0B justru merupakan keputusan yang benar.

## Skor

**83/100**

## Verdict

**NEEDS REVISION**

## Kesimpulan

Fase 0A/0B ini **sudah layak sebagai fondasi awal secara konseptual**, tetapi **belum layak ditutup sebagai fase yang clean dan siap lanjut tanpa revisi**. Setelah sinkronisasi phase control, perbaikan instruksi reproducibility, penegasan workflow Git, dan penambahan baseline check minimal, repo ini akan cukup siap masuk Fase 1 literature review dengan risiko yang lebih terkendali.
