# Final Verification Phase 7 BAB 4

Tanggal verifikasi: Fri May 1 03:31:15 PM UTC 2026

Draft diverifikasi: `reports/manuscript-draft-bab4.md`

## Score

**94/100**

## Verdict

**APPROVED**

## Ringkasan Final

BAB 4 sudah layak masuk tahap finalisasi naskah. Revisi minor dari review awal sudah diterapkan secara substansial: panjang naskah tidak lagi mepet batas bawah, Tabel 4.1 sudah membandingkan *baseline* dan *advanced* dengan MCC serta delta, Tabel 4.3 sudah memberi angka FP/FN yang jelas, istilah asing lebih rapi, dan URL *dashboard* sudah disertai tanggal akses.

Angka utama dataset, metrik model, *confusion matrix*, delta metrik, *feature importance*, dan SHAP konsisten dengan artifact yang diperiksa. Scope klaim juga aman: draft tidak mengklaim uji serangan pada perangkat IoT asli, tidak menyatakan sistem sebagai IDS produksi *real-time*, tidak mengklaim PCAP *replay* aktual, dan tidak membaca hasil Track B/C sebagai generalisasi dunia nyata.

## Checklist Revisi Review Awal

- **Panjang naskah tidak mepet bawah:** lulus. `wc -w` menunjukkan 1.994 kata, lebih aman dari batas minimum 1.900 kata.
- **Tabel 4.1 punya MCC Baseline dan delta:** lulus. Tabel memuat `MCC Baseline`, `MCC Advanced`, `Delta Macro F1`, dan `Delta MCC`.
- **Tabel 4.3 baris FP/FN spesifik:** lulus. Baris error mencantumkan `Decision Tree: FP=2, FN=13; LightGBM: FP=1, FN=4`.
- **Istilah asing lebih rapi:** lulus dengan catatan minor. Istilah utama seperti *dataset*, *baseline*, *advanced*, *track*, *macro F1*, *confusion matrix*, *feature importance*, *SHAP*, *dashboard*, *replay*, dan *real-time* sebagian besar sudah dimiringkan secara memadai.
- **URL dashboard punya tanggal akses:** lulus. URL `https://iot.aquarise.my.id/soc-demo/demo.html` ditulis dengan keterangan diakses pada 1 Mei 2026.

## Cek Angka Artifact

Lulus.

- Total data 3.668.522, train 2.934.817, test 733.705 sesuai `results/metrics/preprocessing_summary.json`.
- Track A sesuai `results/tables/baseline_dataset_tracks.csv`: train 2.861.833 = 370 normal + 2.861.463 DoS/DDoS; test 715.528 = 107 normal + 715.421 DoS/DDoS.
- Track B sesuai artifact: train 740 = 370 normal + 370 DoS/DDoS; test 214 = 107 normal + 107 DoS/DDoS.
- Track C sesuai artifact: train 1.110 = 370 normal + 740 DoS/DDoS; test 321 = 107 normal + 214 DoS/DDoS.
- Baseline Track A sesuai `results/metrics/baseline_summary.json`: Decision Tree, *macro F1* 0,9667, MCC 0,9344, TN=105, FP=2, FN=13, TP=715.408.
- Baseline Track B/C sesuai artifact: Random Forest dengan *macro F1* 1,0000 dan MCC 1,0000.
- Advanced Track A sesuai `results/metrics/advanced_summary.json`: LightGBM, *macro F1* 0,9885, MCC 0,9770, TN=106, FP=1, FN=4, TP=715.417, delta +0,0218/+0,0426.
- Advanced Track B sesuai artifact: XGBoost, *macro F1* 0,9953, MCC 0,9907, TN=107, FP=0, FN=1, TP=106, delta -0,0047/-0,0093.
- Advanced Track C sesuai artifact: XGBoost, *macro F1* 0,9965, MCC 0,9930, TN=107, FP=0, FN=1, TP=213, delta -0,0035/-0,0070.
- *Feature importance* Decision Tree Track A sesuai `results/tables/forensic_feature_importance.csv`: `N_IN_Conn_P_DstIP` 0,9689; `drate` 0,0096; `stddev` 0,0074; `proto=arp` 0,0054; `min` 0,0039.
- *Native feature importance* LightGBM Track A sesuai `results/tables/advanced_feature_importance.csv`: `N_IN_Conn_P_DstIP` 0,1455; `N_IN_Conn_P_SrcIP` 0,1380; `stddev` 0,1136; `min` 0,1132; `drate` 0,0984; `srate` 0,0884.
- SHAP LightGBM Track A sesuai `results/tables/advanced_shap_summary.csv`: `mean` 0,3218; `proto=udp` 0,1934; `state_number` 0,1909; `N_IN_Conn_P_DstIP` 0,0553; `stddev` 0,0519; sampel 3.000 baris.

## Cek Klaim/Scope

Lulus.

- Tidak ada klaim serangan terhadap perangkat IoT asli.
- Tidak ada klaim bahwa sistem merupakan IDS produksi *real-time*.
- Tidak ada klaim PCAP *replay* aktual; SOC *replay* dijelaskan sebagai representasi edukatif.
- Track B dan Track C dibatasi sebagai subset kecil terkontrol, bukan generalisasi dunia nyata.
- Akurasi tidak dijadikan klaim utama; pembahasan menekankan *macro F1*, MCC, *balanced accuracy*, *recall*, FP/FN, dan *confusion matrix*.
- *Feature importance* dan SHAP dipakai sebagai interpretasi berbasis artifact, bukan bukti kausal universal.

## Struktur dan Word Readiness

Lulus.

- Heading 4.1 sampai 4.7 lengkap dan urut.
- Tabel 4.1, Tabel 4.2, dan Tabel 4.3 ada.
- Gambar 4.1 sampai Gambar 4.4 memiliki placeholder dan caption yang urut.
- Format angka Indonesia konsisten untuk angka utama: koma sebagai desimal dan titik sebagai pemisah ribuan.
- Narasi BAB 4 konsisten dengan batasan BAB 1, landasan BAB 2, dan metode BAB 3.

## Sisa Catatan Minor

- Placeholder gambar masih perlu diganti dengan gambar/screenshot saat proses layout Word final, tetapi untuk draft Markdown yang diminta diverifikasi, urutan dan caption sudah siap.
- Beberapa istilah seperti Track A/B/C, Decision Tree, Random Forest, LightGBM, dan XGBoost wajar tidak dimiringkan karena dipakai sebagai nama skenario/model. Konsistensi istilah asing utama sudah cukup.

## Final Recommendation

**APPROVED untuk finalisasi BAB 4.** Tidak ada critical issue atau major issue. BAB 4 memenuhi gate approval karena score >= 90, angka sesuai artifact, klaim aman, struktur lengkap, dan revisi minor dari review awal sudah diterapkan.
