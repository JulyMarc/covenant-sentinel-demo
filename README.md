# Covenant Sentinel — Synthetic Private Credit Monitoring Demo

A public-safe portfolio artifact for Applied AI / Forward Deployed AI / fintech document workflows.

> Framing: a synthetic prototype built to explore document-intelligence and covenant-monitoring workflows: deterministic math first, cited values, explicit refusal, audit log, and human approval gate.

## Why this exists

Many regulated finance workflows do not need an autonomous “AI analyst”. They need a reliable support tool that:

1. extracts values from controlled documents;
2. shows exactly where each value came from;
3. performs deterministic calculations;
4. flags inconsistencies and missing data;
5. refuses unsupported questions;
6. leaves an audit trail for human review.

This demo applies that pattern to a small synthetic private-credit monitoring pack.

## What it demonstrates

- deterministic covenant calculations;
- cited source values and evidence quotes from a synthetic corpus;
- headroom / watch / breach flags;
- monitoring drift versus prior period;
- tie-out and consistency checks;
- refusal behavior for real/private/out-of-corpus questions;
- a human approval gate;
- 20 deterministic eval cases;
- a Markdown report and Dockerfile.

## What it does **not** claim

- No real borrower, lender, customer data, portfolio holding or confidential document is used.
- No private-debt underwriting judgement is claimed.
- No investment recommendation, default prediction or credit score is produced.
- No model call is required in this MVP: covenant conclusions are deterministic Python over cited synthetic values.
- The corpus is deliberately simplified; domain assumptions should be reviewed by credit professionals.

## Run

From this directory:

```bash
python3 covenant_sentinel.py report --out reports/demo_report.md
python3 covenant_sentinel.py eval
python3 covenant_sentinel.py ask "Is net leverage near the covenant limit?"
python3 covenant_sentinel.py ask "What is NordicCo's real sponsor and live market valuation?"
```

Expected eval result:

```text
20/20 PASS
```

Docker smoke:

```bash
docker build -t covenant-sentinel-demo .
docker run --rm covenant-sentinel-demo
```

## Demo corpus

- `data/docs/nordicco_financial_statements.md`
- `data/docs/nordicco_credit_agreement_extract.md`
- `data/docs/nordicco_monitoring_update_2026q2.md`
- `data/extractions.json` — curated synthetic extraction layer with citations and evidence quotes

## Current intentional findings

- **Net leverage:** `WATCH` — `(EUR 92.0m debt - EUR 10.0m cash) / EUR 24.0m EBITDA = 3.42x` versus `4.00x` maximum.
- **Interest coverage:** `WATCH` — `EUR 24.0m EBITDA / EUR 8.0m cash interest = 3.00x` versus `2.50x` minimum.
- **Minimum liquidity:** `BREACH` — `EUR 10.0m` versus `EUR 15.0m` required.
- **Tie-out issue:** senior debt does not tie: financial statements show `EUR 90.0m`, compliance certificate shows `EUR 92.0m`.
- **Monitoring drift:** net leverage deteriorates from `2.61x` in FY2025 to `3.42x` in 2026Q2.

## Eval coverage

The 20-case eval pack checks:

- covenant status correctness;
- formula/numeric fidelity;
- citation and evidence-quote presence;
- tie-out detection;
- monitoring drift;
- refusal for real borrower / valuation / default-prediction questions;
- human approval gate wording;
- model-call transparency;
- synthetic-data disclaimer.

Run:

```bash
python3 covenant_sentinel.py eval
```

## Governance posture

See `GOVERNANCE.md` for the full model-risk and human-in-the-loop framing.

Short version:

- deterministic calculations are separated from any language generation;
- every conclusion must be traceable to a cited value, evidence quote and formula;
- unsupported questions must refuse instead of extrapolating;
- a human reviewer must approve any borrower communication or investment interpretation;
- failures and limitations are part of the artifact, not hidden.

## Files

```text
covenant_sentinel.py                 # CLI, deterministic covenant engine, Q&A/refusal, eval runner
data/docs/*.md                       # synthetic source documents
data/extractions.json                # cited extracted values with evidence quotes
eval_cases.json                      # 20 deterministic eval cases
reports/demo_report.md               # generated covenant report
GOVERNANCE.md                        # human-in-loop / model-risk framing
```

## License and citation

Code and documentation are released under the Apache License 2.0. See `LICENSE`.

If you use or adapt this demo, please cite the repository. Citation metadata is provided in `CITATION.cff`.

## Interview framing

> I built this as a synthetic prototype to explore the workflow, not to claim private-credit underwriting expertise. The point is the reliability pattern: cited values, deterministic calculations, tie-outs, refusal behavior, evals, and a human approval gate. I would expect credit professionals to challenge and correct the domain assumptions.
