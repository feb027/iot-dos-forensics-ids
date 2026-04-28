# Dataset Notes

## BoT-IoT (UNSW)

Official source: https://research.unsw.edu.au/projects/bot-iot-dataset

Status: pending audit.

Hal yang perlu diverifikasi:

- Format data yang akan dipakai.
- Ukuran dataset.
- Daftar fitur.
- Label normal/attack.
- Ketersediaan label DoS/DDoS.
- Apakah perlu subset.
- Risiko imbalance.
- Risiko leakage.

### Checklist Risiko Leakage untuk Fase 2

Saat dataset audit, cek minimal:

- Duplikasi flow/baris antar split.
- Split temporal vs random split; hindari train/test yang terlalu mirip secara waktu.
- Fitur yang terlalu dekat dengan label, misalnya field kategori serangan yang tidak boleh masuk fitur.
- Risiko memorisasi IP address, port, atau kombinasi host tertentu.
- Ketimpangan kelas normal vs DoS/DDoS.
- Apakah ada record generated/synthetic yang membuat model belajar pola simulator, bukan pola trafik umum.
- Apakah evaluasi perlu dilakukan dengan stratified split atau split berbasis skenario.

## RT-IoT2022 (UCI)

Official source: https://archive-beta.ics.uci.edu/dataset/942/rt-iot2022

Status: optional comparison; pending audit.
