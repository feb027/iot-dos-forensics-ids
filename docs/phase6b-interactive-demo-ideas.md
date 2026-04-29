# Fase 6B Interactive Demo Ideas

Status: brainstorm/backlog sebelum Fase 7 manuscript.

## Catatan dari diskusi model insight

Hasil modeling tidak perlu berhenti sebagai leaderboard model. Nilai akademik bisa diperkuat dengan:

1. Track A error reduction analysis:
   - Decision Tree baseline Track A: FP 2, FN 13, Macro F1 0.9667, MCC 0.9344.
   - LightGBM Track A: FP 1, FN 4, Macro F1 0.9885, MCC 0.9770.
   - Narasi utama: advanced model mengurangi error yang relevan untuk IDS, terutama FN attack-as-normal.

2. Feature ablation:
   - Uji ulang performa saat top forensic feature seperti `N_IN_Conn_P_DstIP` dan `N_IN_Conn_P_SrcIP` dihapus.
   - Tujuan: mengukur apakah model terlalu bergantung pada connection-count features atau tetap robust dengan fitur statistik flow lain.

3. Threshold / FP-FN trade-off:
   - Tampilkan bagaimana threshold memengaruhi false positive dan false negative.
   - Tujuan: membuat pembahasan IDS lebih realistis karena biaya FN dan FP berbeda.

## Ide demo interaktif yang lebih menarik

### Opsi A — AI SOC Analyst / Incident Replay Demo

Konsep: dashboard berubah dari sekadar chart menjadi simulasi kerja analis SOC.

Alur demo:
1. User memilih skenario trafik: Normal, DoS, DDoS, atau borderline/error case.
2. Dashboard menampilkan replay timeline trafik IoT.
3. Model memprediksi normal vs DoS/DDoS.
4. Panel evidence menampilkan:
   - prediction confidence,
   - top SHAP/evidence features,
   - confusion outcome jika sample berasal dari FP/FN/TP/TN,
   - rekomendasi tindakan analis.
5. Panel "AI SOC Analyst" menghasilkan ringkasan investigasi bergaya security analyst:
   - apa yang terjadi,
   - kenapa model curiga,
   - fitur bukti utama,
   - risiko FP/FN,
   - rekomendasi mitigasi.

Nilai SOTA:
- Terinspirasi tren agentic AI SOC / Security Copilot: alert triage, contextual enrichment, investigation summary, evidence chain, human-in-the-loop.
- Bisa dibuat static/deterministic tanpa mengirim data ke API eksternal.

### Opsi B — What-if Attack Simulator

Konsep: user mengubah parameter flow secara manual dan melihat prediksi berubah.

Kontrol interaktif:
- `N_IN_Conn_P_DstIP`
- `N_IN_Conn_P_SrcIP`
- `srate`
- `stddev`
- `state_number`
- `mean/max/min`
- `proto`

Output:
- prediksi normal/DoS,
- confidence,
- risk score,
- top contributing features,
- warning jika input menyerupai pola DoS.

Catatan implementasi:
- Model asli tidak perlu dijalankan di browser jika berat.
- Bisa pakai surrogate rule/lookup grid dari artifact LightGBM/SHAP untuk demo edukatif, dengan label jelas: "interactive simulation, not live production model".

### Opsi C — Attack Timeline / Forensic Storyboard

Konsep: membuat cerita investigasi dari dataset.

Panel:
- timeline peningkatan koneksi,
- target concentration ke destination IP,
- packet/source rate spike,
- model decision point,
- analyst note,
- recommended mitigation.

Nilai demo:
- Paling aman dan kuat untuk presentasi dosen karena mudah dijelaskan.
- Tidak butuh backend atau model live.

### Opsi D — LLM/RAG Evidence Chatbot

Konsep: chat kecil di dashboard yang menjawab pertanyaan tentang hasil eksperimen.

Contoh pertanyaan:
- Kenapa accuracy tidak dijadikan klaim utama?
- Apa arti FP dan FN dalam IDS?
- Kenapa Track A lebih penting daripada Track B/C?
- Fitur apa yang paling mendukung bukti DoS?
- Apa batasan dataset BoT-IoT?

Implementasi aman:
- Static Q&A berbasis artifact terlebih dulu.
- Optional local LLM/Ollama untuk demo lokal, bukan wajib di GitHub Pages.

### Opsi E — MITRE ATT&CK-style Mapping Panel

Konsep: mapping hasil DoS/DDoS ke bahasa taktik/teknik keamanan.

Contoh:
- Impact / Network Denial of Service style narrative.
- Evidence: connection concentration, packet rate, abnormal flow statistics.
- Analyst actions: rate limiting, firewall rule, device isolation, traffic shaping, monitoring target IP.

Catatan:
- Jangan overclaim mapping ATT&CK jika data tidak cukup untuk attribution.
- Gunakan sebagai educational/security framing, bukan bukti aktor/teknik spesifik.

## Rekomendasi pilihan terbaik

Paling cocok untuk UAS dan demo:

**AI SOC Analyst / Incident Replay Demo + What-if Attack Simulator**

Kenapa:
- Interaktif dan gampang didemokan.
- Masih nyambung langsung ke hasil modeling saat ini.
- Terlihat modern/SOTA karena mengikuti tren AI SOC copilot dan human-in-the-loop investigation.
- Tidak membutuhkan hardware.
- Bisa tetap static GitHub Pages.

## Sumber tren SOTA yang relevan untuk disebut di planning

- Microsoft Security Copilot / Defender: agentic AI untuk investigasi SOC, chat berbasis konteks, dan supporting evidence.
- D3 Morpheus AI SOC: autonomous alert investigation, attack path discovery, evidence chain.
- Securonix Sam AI SOC Analyst: triage, enrichment, investigation summaries, human-led AI.
- Cisco XDR Agentic AI: local/fine-tuned security model dan agent tools untuk incident investigation.
- XAI IDS 2025/2026: SHAP/LIME, visual explanation for FP/FN, human-centered explainable IDS.

## Safety / academic boundaries

- Demo harus diberi label jelas sebagai prototype educational dashboard.
- Jika pakai generated SOC narrative, nyatakan narasi berasal dari artifact/model explanation, bukan bukti forensik real-world penuh.
- Jangan klaim real-time production IDS jika hanya replay/static sample.
- Jangan pakai raw dataset besar di frontend.
