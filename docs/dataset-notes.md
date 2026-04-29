# Dataset Notes

## BoT-IoT (UNSW)

Official source: https://research.unsw.edu.au/projects/bot-iot-dataset

Working audit mirror: https://huggingface.co/datasets/Mireu-Lab/UNSW-IoT

Audit date: 2026-04-29

Status: **audited for Fase 2** using CSV train/test files from the public Hugging Face mirror. Raw CSV files are stored under `data/raw/bot-iot-hf/` and intentionally not committed.

## Dataset Source and Size

| Item | Value |
|---|---:|
| Local files audited | 2 |
| Total rows audited | 3.668.522 |
| Total bytes audited | 461.384.981 |
| Columns in audited CSV | 19 |
| Candidate model features after exclusions | 10 |

Official source states that BoT-IoT provides PCAP, Argus, and CSV formats. The official page reports PCAP files of 69.3 GB, extracted CSV flow traffic of 16.7 GB, and a 5% subset of about 1.07 GB across 4 files. Fase 2 uses the mirror CSV split only for practical audit and reproducible scripts.

## Audited Files

| Split | Rows | Bytes | Exact duplicate rows | Duplicate `pkSeqID` | SHA256 |
|---|---:|---:|---:|---:|---|
| train | 2.934.817 | 369.103.929 | 0 | 0 | `047e577cd9c7f8f61d44ac170114497904c33091bf80d1dd5e682e353a69c15b` |
| test | 733.705 | 92.281.052 | 0 | 0 | `8617de2ac5d6ca4c2f77272c7409253a396f2a9e667c29c8e797ab9f57a1868e` |


## Column Roles

Audited columns:

```text
pkSeqID, proto, saddr, sport, daddr, dport, seq, stddev, N_IN_Conn_P_SrcIP, min, state_number, mean, N_IN_Conn_P_DstIP, drate, srate, max, attack, category, subcategory
```

Recommended baseline feature columns:

```text
proto, stddev, N_IN_Conn_P_SrcIP, min, state_number, mean, N_IN_Conn_P_DstIP, drate, srate, max
```

Recommended excluded/leakage columns:

```text
attack, category, daddr, dport, pkSeqID, saddr, seq, sport, subcategory
```

Rationale:

- `attack`, `category`, and `subcategory` are labels, not input features.
- `pkSeqID` and `seq` are identifiers/order fields.
- `saddr`, `sport`, `daddr`, and `dport` can make the model memorize lab topology, host identity, or service-specific patterns instead of learning generalizable traffic behavior.

## Label Mapping

| Task | Mapping |
|---|---|
| Binary attack | `attack=0` → normal; `attack=1` → attack |
| DoS scope | `category in {DoS, DDoS}` → `dos_or_ddos`; `attack=0` or `category=Normal` → `normal`; other categories → `other_attack` |
| Optional multiclass | Use `category` for coarse attack class or `subcategory` for protocol/subtype analysis. |

## Category Distribution

### Train Split

| Category | Count | Rate |
|---|---:|---:|
| DDoS | 1.541.315 | 52.5183% |
| DoS | 1.320.148 | 44.9823% |
| Normal | 370 | 0.0126% |
| Reconnaissance | 72.919 | 2.4846% |
| Theft | 65 | 0.0022% |


### Test Split

| Category | Count | Rate |
|---|---:|---:|
| DDoS | 385.309 | 52.5155% |
| DoS | 330.112 | 44.9925% |
| Normal | 107 | 0.0146% |
| Reconnaissance | 18.163 | 2.4755% |
| Theft | 14 | 0.0019% |


## DoS/DDoS Scope Distribution

| Split | Label | Count | Rate |
|---|---|---:|---:|
| train | dos_or_ddos | 2.861.463 | 97.5006% |
| train | normal | 370 | 0.0126% |
| train | other_attack | 72.984 | 2.4868% |
| test | dos_or_ddos | 715.421 | 97.5080% |
| test | normal | 107 | 0.0146% |
| test | other_attack | 18.177 | 2.4774% |


## Missing Values

The audited CSV profiles show zero missing values in all audited columns. Detailed per-column profile is stored in:

```text
results/tables/column_profile.csv
```

## Leakage and Split Risks

| Check | Value | Interpretation |
|---|---:|---|
| pkSeqID overlap train/test | 0 | Should be 0 for clean split identifiers. |
| Exact full-row overlap train/test | 0 | Should be 0 to avoid direct duplicate leakage. |
| Model-feature signature overlap train/test excluding ids/network ids/labels | 327.338 | Non-zero can occur in aggregated flow features; high values mean random split similarity risk and should be disclosed. |


Important interpretation:

1. No `pkSeqID` overlap and no exact full-row overlap were found between train and test.
2. However, many model-feature signatures overlap after excluding IDs, network identifiers, and labels. This does not prove direct duplicate leakage, but it is a warning that the split may be highly similar because the dataset is generated from repeated aggregated flow patterns.
3. Normal traffic is extremely underrepresented. A naive model can look excellent while failing to learn meaningful normal-vs-attack boundaries.

## Duplicate Model-Feature Signature Within Split

Selain overlap antar train/test, audit juga menemukan banyak signature fitur model yang berulang di dalam masing-masing split setelah `pkSeqID`, `seq`, network identifier, dan label dikeluarkan:

| Split | Duplicate model-feature rows excluding IDs/network IDs/labels |
|---|---:|
| train | 1.487.901 |
| test | 202.630 |

Interpretasi: ini bukan exact duplicate row karena `pkSeqID` dan/atau field lain dapat berbeda, tetapi pola fitur agregat yang sama muncul berulang. Pada Fase 3, ini harus diperlakukan sebagai risiko sampling/evaluasi: model bisa terlihat sangat kuat karena banyak pola agregat berulang, bukan karena benar-benar generalisasi ke trafik IoT baru.

## Fase 2 Decision

Proceed to Fase 3 only with these constraints:

- Use the audited train/test split as a first reproducible baseline, but report the imbalance and split-similarity limitation.
- Do not include label columns or network identifiers as model inputs.
- For the main `normal` vs `DoS/DDoS` task, filter to `normal` and `dos_or_ddos`; document that `other_attack` rows are excluded from the binary scope.
- Use metrics beyond accuracy: precision, recall, F1, confusion matrix, and false positive/false negative discussion.
- Consider class weighting or controlled sampling because normal rows are only 477 across the audited split.

## RT-IoT2022 (UCI)

Official source: https://archive-beta.ics.uci.edu/dataset/942/rt-iot2022

Status: optional comparison. Fase 2 did not audit RT-IoT2022 files because the approved primary dataset is BoT-IoT and the primary audit already found enough constraints for the next modeling phase. RT-IoT2022 remains useful if BoT-IoT normal-class imbalance becomes too limiting for the final manuscript.
