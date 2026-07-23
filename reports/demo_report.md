# Covenant Sentinel Demo Report

Generated: 2026-07-23T18:54:10+00:00
Borrower: NordicCo (synthetic)
As of: 2026Q2

> Public-safe demo only. Not based on any real borrower, lender, portfolio holding, or confidential document.

## Covenant results

| Covenant | Status | Actual | Limit | Headroom | Formula | Citations |
|---|---:|---:|---:|---:|---|---|
| Net leverage | WATCH | 3.42x | 4.00x | 0.58x | (senior debt EUR 92.0m - cash EUR 10.0m) / EBITDA EUR 24.0m | MU-2026Q2#compliance-certificate-values; MU-2026Q2#compliance-certificate-values; MU-2026Q2#compliance-certificate-values; CA-2025#net-leverage-covenant |
| Interest coverage | WATCH | 3.00x | 2.50x | 0.50x | EBITDA EUR 24.0m / cash interest EUR 8.0m | MU-2026Q2#compliance-certificate-values; MU-2026Q2#compliance-certificate-values; CA-2025#interest-coverage-covenant |
| Minimum liquidity | BREACH | 10.00EURm | 15.00EURm | -5.00EURm | cash EUR 10.0m + undrawn revolver EUR 0.0m | MU-2026Q2#compliance-certificate-values; MU-2026Q2#compliance-certificate-values; CA-2025#minimum-liquidity-covenant |

## Tie-out and monitoring flags

- Senior debt mismatch: financial statements show EUR 90.0m (FS-2026Q2#balance-sheet-highlights) while the compliance certificate shows EUR 92.0m (MU-2026Q2#compliance-certificate-values).
- Monitoring drift: net leverage increased from 2.61x in FY2025 to 3.42x in 2026Q2.

## Evidence quotes

- `financial_statements.ebitda_ltm_eurm` = `24` from `FS-2026Q2#income-statement-highlights` — “LTM 2026Q2 | Revenue EURm 119.0 | EBITDA EURm 24.0 | Cash Interest EURm 8.0”
- `financial_statements.senior_debt_eurm` = `90` from `FS-2026Q2#balance-sheet-highlights` — “LTM 2026Q2 | Cash EURm 10.0 | Senior Debt EURm 90.0 | Current Assets EURm 47.0 | Current Liabilities EURm 31.0 | Equity EURm 36.0”
- `financial_statements.cash_eurm` = `10` from `FS-2026Q2#balance-sheet-highlights` — “LTM 2026Q2 | Cash EURm 10.0 | Senior Debt EURm 90.0 | Current Assets EURm 47.0 | Current Liabilities EURm 31.0 | Equity EURm 36.0”
- `financial_statements.cash_interest_eurm` = `8` from `FS-2026Q2#income-statement-highlights` — “LTM 2026Q2 | Revenue EURm 119.0 | EBITDA EURm 24.0 | Cash Interest EURm 8.0”
- `financial_statements.fy2025_ebitda_eurm` = `28` from `FS-2026Q2#income-statement-highlights` — “FY2025A | Revenue EURm 124.0 | EBITDA EURm 28.0 | Cash Interest EURm 7.5”
- `financial_statements.fy2025_senior_debt_eurm` = `85` from `FS-2026Q2#balance-sheet-highlights` — “FY2025A | Cash EURm 12.0 | Senior Debt EURm 85.0 | Current Assets EURm 50.0 | Current Liabilities EURm 28.0 | Equity EURm 42.0”
- `financial_statements.fy2025_cash_eurm` = `12` from `FS-2026Q2#balance-sheet-highlights` — “FY2025A | Cash EURm 12.0 | Senior Debt EURm 85.0 | Current Assets EURm 50.0 | Current Liabilities EURm 28.0 | Equity EURm 42.0”
- `certificate.ebitda_ltm_eurm` = `24` from `MU-2026Q2#compliance-certificate-values` — “Consolidated EBITDA | EUR 24.0m”
- `certificate.senior_debt_eurm` = `92` from `MU-2026Q2#compliance-certificate-values` — “Senior debt outstanding | EUR 92.0m”
- `certificate.cash_eurm` = `10` from `MU-2026Q2#compliance-certificate-values` — “Unrestricted cash | EUR 10.0m”
- `certificate.cash_interest_eurm` = `8` from `MU-2026Q2#compliance-certificate-values` — “Cash interest expense | EUR 8.0m”
- `certificate.undrawn_revolver_eurm` = `0` from `MU-2026Q2#compliance-certificate-values` — “Undrawn committed revolver | EUR 0.0m”
- `covenants.max_net_leverage` = `4` from `CA-2025#net-leverage-covenant` — “The borrower must not permit Net Debt divided by Consolidated EBITDA to exceed 4.00x on any quarterly test date.”
- `covenants.min_interest_coverage` = `2.5` from `CA-2025#interest-coverage-covenant` — “The borrower must maintain Consolidated EBITDA divided by cash interest expense of at least 2.50x on any quarterly test date.”
- `covenants.min_liquidity_eurm` = `15` from `CA-2025#minimum-liquidity-covenant` — “The borrower must maintain Liquidity of at least EUR 15.0 million on any quarterly test date.”

## Human approval gate

This report is a decision-support artifact. A human reviewer must approve any interpretation, covenant conclusion, or borrower communication before use.

## Audit log

- Input corpus: 3 synthetic markdown documents under `data/docs/`.
- Extraction source: curated synthetic `data/extractions.json` with citations.
- Model calls: none in this MVP; all covenant math is deterministic Python.
- Failure mode intentionally demonstrated: debt mismatch between financial statements and compliance certificate.
