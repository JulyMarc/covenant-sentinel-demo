# Governance and Model-Risk Notes

This demo is intentionally conservative: it treats AI/document automation as decision support, not autonomous credit judgement.

## Scope boundary

Allowed in this artifact:

- cite source values from provided documents;
- compute deterministic covenant metrics;
- flag mathematical headroom, breach/watch/pass status and tie-out inconsistencies;
- refuse questions not supported by the synthetic corpus;
- produce a Markdown report for human review.

Not allowed in this artifact:

- real borrower analysis;
- investment recommendations;
- default prediction;
- private-credit underwriting conclusions;
- use of confidential documents;
- per-company risk views on any live borrower or credit.

## Control design

### 1. Deterministic core

Covenant conclusions come from deterministic formulas in `covenant_sentinel.py`, not free-form generation.

Examples:

- Net leverage = `(senior debt - cash) / EBITDA`
- Interest coverage = `EBITDA / cash interest expense`
- Liquidity = `cash + undrawn committed revolver`

### 2. Citation requirement

Every numeric value in the extraction layer has a citation pointer and a short evidence quote such as:

```text
MU-2026Q2#compliance-certificate-values — Senior debt outstanding | EUR 92.0m
CA-2025#minimum-liquidity-covenant — The borrower must maintain Liquidity of at least EUR 15.0 million
```

A production version would replace these short quote anchors with exact source spans, page numbers and document checksums.

### 3. Human approval gate

This report is not a borrower communication or investment decision. A human reviewer must approve:

- extracted values;
- covenant interpretation;
- treatment of mismatches;
- any external communication;
- any portfolio-monitoring escalation.

### 4. Refusal behavior

The CLI refuses unsupported questions about:

- real sponsors;
- live valuations;
- real borrowers or holdings;
- default predictions;
- information not present in the synthetic corpus.

### 5. Eval harness

`eval_cases.json` includes 20 deterministic checks covering:

- calculation status;
- formula fidelity;
- citation and evidence-quote presence;
- tie-out issue detection;
- monitoring drift;
- synthetic-data disclaimers;
- refusal behavior;
- human approval wording.

Run:

```bash
python3 covenant_sentinel.py eval
```

## Known limitations

- The extraction layer is curated JSON, not a full parser/OCR/RAG pipeline.
- The synthetic covenant language is simplified.
- The demo does not model covenant EBITDA adjustments, cures, baskets, incurrence tests, add-backs or reporting-calendar nuance.
- Evidence quotes are included, but no full exact source-span highlighter/page-coordinate UI exists yet.
- CI currently runs syntax checks, deterministic evals and report generation; it does not yet run linting or container builds.
- No confidential or real transaction data is used.

## Production-hardening path

If this were expanded, the next controls would be:

1. exact source-span extraction with document checksums;
2. schema validation for extracted values;
3. independent calculation replay tests;
4. double-entry tie-out checks across statement tables;
5. reviewer workflow with sign-off state;
6. immutable audit logs;
7. evaluation set with deliberately adversarial documents;
8. role-based access and redaction for confidential materials.

## Presentation rule

When discussing this artifact, say:

> Synthetic decision-support prototype. It demonstrates a reliability pattern, not private-credit expertise or live-borrower analysis.
