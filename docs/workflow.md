# Workflow Hermes + Codex

## Operating Model

```text
Hermes = orchestrator
Codex = implementer/reviewer
GitHub = source of truth
Docs = progress memory
Artifacts = evidence
Dashboard = visual evidence viewer
```

## Standard Phase Loop

```text
1. Plan
2. Execute
3. Produce artifact
4. Update docs
5. Run Codex review
6. Fix issues
7. Commit and push
8. Move to next phase
```

## Codex Review Pattern

Preferred command pattern:

```bash
codex exec --dangerously-bypass-approvals-and-sandbox -C /path/to/repo   "Review the current phase. Write ONLY to docs/REVIEW_phaseX.md, then exit."
```

Use reviewer prompts from `prompts/`.

## Evidence-First Rule

No report claim without source.

Examples:

| Claim | Required Artifact |
|---|---|
| Model A has best F1 | `results/tables/model_comparison.csv` |
| DoS class dominates | `results/tables/class_distribution.csv` or EDA output |
| Feature X is important | `results/tables/feature_importance.csv` |
| Dashboard shows final result | `dashboard/data/dashboard-data.json` generated from results |

## When to Use Codex

Use Codex Implementer for:

- writing scripts,
- fixing bugs,
- generating dashboard,
- refactoring.

Use Codex Lecturer Reviewer for:

- literature review quality,
- methodology critique,
- scientific manuscript review,
- phase readiness.

Use Codex Technical Reviewer for:

- code correctness,
- reproducibility,
- leakage checks,
- dashboard-data consistency.

## Git Branch Policy

For future phases, prefer a phase branch, for example:

```text
phase-1-literature-review
phase-2-dataset-audit
phase-3-eda-preprocessing
```

Small scaffold/admin fixes may be committed directly to `main` when explicitly requested.

## Commit Policy

Commit after each stable phase or meaningful artifact.

Examples:

```text
docs: initialize IoT DoS project scaffold
research: add IoT IDS literature matrix
data: add BoT-IoT dataset audit notes
analysis: add dataset EDA figures
model: add baseline classifier comparison
forensics: add feature importance analysis
dashboard: add static results dashboard
paper: add scientific manuscript draft
```
