# Research Log — Fase 1 Literature Review

Tanggal mulai Fase 1: 2026-04-28T15:53:52+00:00

Metode pencarian:

- Pencarian utama memakai Exa melalui `mcporter` dengan query tentang BoT-IoT, RT-IoT2022, IoT IDS, DoS/DDoS, *network forensics*, dan risiko *data leakage*.
- Metadata DOI dicek melalui Crossref API untuk paper yang memiliki DOI.
- Halaman resmi dataset dicek dengan Jina Reader/curl: UNSW BoT-IoT dan UCI RT-IoT2022.
- Bukti pencarian mentah disimpan di `references/raw-search/`, `references/raw-sources/`, dan `references/raw-metadata/` sebagai audit trail awal.

## Ringkasan Seleksi

Target Fase 1 adalah minimal 10–15 referensi. Matrix saat ini berisi 18 sumber: 16 paper jurnal/prosiding, 1 dokumentasi resmi UNSW, dan 1 dataset resmi UCI. Sumber populer/blog tidak dipakai sebagai rujukan utama.

## Paper/Sumber Terpilih

### 1. Koroniotis et al. — BoT-IoT dataset

- Judul: Towards the development of realistic botnet dataset in the Internet of Things for network forensic analytics: BoT-IoT dataset
- Penulis: Nickolaos Koroniotis, Nour Moustafa, Elena Sitnikova, Benjamin Turnbull
- Tahun: 2019
- Venue/Publisher: Future Generation Computer Systems
- Link/DOI: https://doi.org/10.1016/j.future.2019.05.041
- Dataset: BoT-IoT
- Metode/Fokus: pembangunan dataset botnet IoT untuk *network forensic analytics*
- Hasil utama: sumber utama yang memperkenalkan BoT-IoT sebagai dataset untuk trafik normal dan serangan botnet pada lingkungan IoT
- Kelebihan: sangat relevan dengan judul karena menggabungkan IoT, serangan botnet, dan forensik jaringan
- Keterbatasan: dataset tetap perlu diaudit ulang sebelum eksperimen karena subset/format yang dipakai akan memengaruhi hasil
- Relevansi ke proyek: rujukan inti dataset utama dan latar belakang
- Catatan untuk naskah: cocok untuk BAB Pendahuluan, landasan dataset, dan metodologi dataset

### 2. UNSW Research — The Bot-IoT Dataset

- Judul: The Bot-IoT Dataset
- Penulis/Institusi: UNSW Research
- Tahun halaman: 2021 menurut hasil pencarian Exa
- Link: https://research.unsw.edu.au/projects/bot-iot-dataset
- Dataset: BoT-IoT
- Fokus: akses dataset, format file, kategori serangan, dan ketentuan penggunaan akademik
- Catatan utama: halaman resmi menyebut dataset tersedia sebagai PCAP, Argus, dan CSV, serta mencakup kategori serangan seperti DoS/DDoS
- Keterbatasan: dokumentasi halaman bukan paper eksperimen
- Relevansi ke proyek: sumber resmi untuk akses dan verifikasi dataset pada Fase 2

### 3. Sharmila & Nagapadma — RT-IoT2022 UCI

- Judul: RT-IoT2022 Dataset
- Penulis: B. S. Sharmila, Rohini Nagapadma
- Tahun: 2023; donated di UCI pada 2024-01-04
- Link/DOI: https://doi.org/10.24432/C5P338
- Dataset: RT-IoT2022
- Fokus: dataset real-time IoT untuk IDS
- Catatan dari UCI: 123117 instances, 83 features, tidak memiliki missing values menurut halaman UCI; label mencakup DOS_SYN_Hping, DDOS_Slowloris, dan normal pattern
- Keterbatasan: dipakai sebagai dataset alternatif, bukan target utama
- Relevansi ke proyek: opsi pembanding jika BoT-IoT terlalu berat

### 4. Alsaedi et al. — TON_IoT

- Judul: TON_IoT Telemetry Dataset: A New Generation Dataset of IoT and IIoT for Data-Driven Intrusion Detection Systems
- Tahun: 2020
- Venue: IEEE Access
- DOI: https://doi.org/10.1109/ACCESS.2020.3022862
- Fokus: dataset IoT/IIoT untuk IDS
- Relevansi: konteks perkembangan dataset IDS IoT selain BoT-IoT

### 5. Neto et al. — CICIoT2023

- Judul: CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment
- Tahun: 2023
- Venue: Sensors
- DOI: https://doi.org/10.3390/s23135941
- Fokus: dataset dan benchmark serangan IoT skala besar
- Relevansi: konteks dataset IoT IDS yang lebih baru; bukan target eksperimen utama

### 6. Alosaimi & Almutairi — IDS Using BoT-IoT

- Judul: An Intrusion Detection System Using BoT-IoT
- Tahun: 2023
- Venue: Applied Sciences
- DOI: https://doi.org/10.3390/app13095427
- Fokus: IDS berbasis BoT-IoT
- Relevansi: pembanding langsung untuk metode IDS pada dataset yang sama

### 7. Kalakoti et al. — Feature Selection for Botnet Detection

- Judul: In-Depth Feature Selection for the Statistical Machine Learning-Based Botnet Detection in IoT Networks
- Tahun: 2022
- Venue: IEEE Access
- DOI: https://doi.org/10.1109/ACCESS.2022.3204001
- Fokus: *feature selection* untuk deteksi botnet IoT
- Relevansi: dasar Fase 5 untuk analisis fitur penting dan interpretasi forensik

### 8. Sadhwani et al. — Lightweight DDoS ML

- Judul: A Lightweight Model for DDoS Attack Detection Using Machine Learning Techniques
- Tahun: 2023
- Venue: Applied Sciences
- DOI: https://doi.org/10.3390/app13179937
- Fokus: model ringan untuk deteksi DDoS
- Relevansi: justifikasi penggunaan baseline ML ringan pada proyek UAS

### 9. Sharmila & Nagapadma — QAE RT-IoT2022

- Judul: Quantized autoencoder (QAE) intrusion detection system for anomaly detection in resource-constrained IoT devices using RT-IoT2022 dataset
- Tahun: 2023
- Venue: Cybersecurity
- DOI: https://doi.org/10.1186/s42400-023-00178-5
- Fokus: anomaly detection berbasis QAE pada RT-IoT2022
- Relevansi: bukti RT-IoT2022 sudah dipakai untuk riset IDS; metode lebih kompleks dari baseline awal

### 10. Jamalipour & Murali — Taxonomy of ML IDS for IoT

- Judul: A Taxonomy of Machine-Learning-Based Intrusion Detection Systems for the Internet of Things: A Survey
- Tahun: 2022
- Venue: IEEE Internet of Things Journal
- DOI: https://doi.org/10.1109/JIOT.2021.3126811
- Fokus: taksonomi IDS IoT berbasis ML
- Relevansi: landasan teori IDS IoT dan posisi penelitian

### 11. Jayalaxmi et al. — ML/DL IDS Survey

- Judul: Machine and Deep Learning Solutions for Intrusion Detection and Prevention in IoTs: A Survey
- Tahun: 2022
- Venue: IEEE Access
- DOI: https://doi.org/10.1109/ACCESS.2022.3220622
- Fokus: review solusi ML/DL untuk IDS/IPS IoT
- Relevansi: memperkuat BAB II tentang pendekatan ML dan DL

### 12. Kikissagbe & Adda — ML IDS Comprehensive Review

- Judul: Machine Learning-Based Intrusion Detection Methods in IoT Systems: A Comprehensive Review
- Tahun: 2024
- Venue: Electronics
- DOI: https://doi.org/10.3390/electronics13183601
- Fokus: review metode ML untuk IDS IoT
- Relevansi: referensi baru untuk state-of-the-art ML IDS IoT

### 13. Rahman et al. — Survey IDS in IoT Networks

- Judul: A survey on intrusion detection system in IoT networks
- Tahun: 2025
- Venue: Cyber Security and Applications
- DOI: https://doi.org/10.1016/j.csa.2024.100082
- Fokus: survey IDS pada jaringan IoT
- Relevansi: sumber terbaru untuk konteks umum IDS IoT

### 14. Pakmehr et al. — DDoS Detection Techniques in IoT

- Judul: DDoS attack detection techniques in IoT networks: a survey
- Tahun: 2024
- Venue: Cluster Computing
- DOI: https://doi.org/10.1007/s10586-024-04662-6
- Fokus: teknik deteksi DDoS pada jaringan IoT
- Relevansi: rujukan langsung untuk teori DoS/DDoS pada proyek

### 15. Shukla et al. — IoT Traffic-Based DDoS Review

- Judul: IoT traffic-based DDoS attacks detection mechanisms: A comprehensive review
- Tahun: 2024
- Venue: The Journal of Supercomputing
- DOI: https://doi.org/10.1007/s11227-023-05843-7
- Fokus: deteksi DDoS berbasis trafik IoT
- Relevansi: mendukung argumen bahwa fitur trafik dapat dianalisis untuk deteksi dan forensik

### 16. Bouke & Abdullah — Leakage-Free Evaluation

- Judul: An empirical assessment of ML models for 5G network intrusion detection: A data leakage-free approach
- Tahun: 2024
- Venue: e-Prime - Advances in Electrical Engineering, Electronics and Energy
- DOI: https://doi.org/10.1016/j.prime.2024.100590
- Fokus: evaluasi ML untuk IDS dengan pendekatan bebas *data leakage*
- Relevansi: prinsip metodologi untuk mencegah evaluasi yang terlalu optimistis pada Fase 2–4

### 17. Wu et al. — IoT Network Traffic Analysis for Forensic Investigators

- Judul: IoT network traffic analysis: Opportunities and challenges for forensic investigators?
- Penulis: Tina Wu, Frank Breitinger, Stephen Niemann
- Tahun: 2021
- Venue: Forensic Science International: Digital Investigation
- DOI: https://doi.org/10.1016/j.fsidi.2021.301123
- Fokus: analisis trafik perangkat IoT sebagai sumber artefak forensik
- Relevansi: memperkuat aspek Digital Forensics pada naskah, terutama penggunaan metadata/traffic flow sebagai bukti investigasi

### 18. Koroniotis et al. — Network Forensic Framework for IoT

- Judul: A new network forensic framework based on deep learning for Internet of Things networks: A particle deep framework
- Penulis: Nickolaos Koroniotis, Nour Moustafa, Elena Sitnikova
- Tahun: 2020
- Venue: Future Generation Computer Systems
- DOI: https://doi.org/10.1016/j.future.2020.03.042
- Fokus: kerangka network forensic berbasis deep learning untuk jaringan IoT
- Relevansi: menjembatani BoT-IoT, flow analysis, dan digital forensics; dipakai sebagai landasan konsep, bukan target performa proyek

## Gap Sementara untuk Proyek

Dari sumber yang terkumpul, gap yang paling aman untuk proyek UAS ini bukan membuat metode baru yang terlalu kompleks, melainkan membuat pipeline yang rapi dan auditable:

1. BoT-IoT dipakai sebagai dataset utama, tetapi sebelum model dilatih perlu audit label, fitur, subset, imbalance, dan potensi leakage.
2. Model baseline klasik tetap relevan karena proyek berfokus pada analisis DoS/DDoS dan interpretasi fitur, bukan hanya mengejar performa tertinggi.
3. Bagian forensik diperkuat dengan sumber khusus *network traffic analysis* dan *network forensic framework*, lalu diterapkan secara realistis melalui fitur penting, confusion matrix, dan pola kesalahan model, bukan sekadar melaporkan akurasi.
4. RT-IoT2022 diposisikan sebagai dataset alternatif/pembanding jika BoT-IoT terlalu berat atau jika dibutuhkan validasi tambahan.

## Catatan untuk Fase 2

- Jangan memasukkan kolom label seperti `Attack_type` ke fitur.
- Cek duplikasi flow/baris sebelum split.
- Cek apakah split random membuat train/test terlalu mirip.
- Catat distribusi kelas normal vs DoS/DDoS dari subset yang benar-benar dipakai.
- Dokumentasikan alasan memilih subset agar tidak terlihat memilih data demi hasil bagus.
