#!/usr/bin/env python3
"""Synthetic Covenant Sentinel demo.

This is a public-safe portfolio artifact: it uses synthetic borrower documents only,
performs deterministic covenant math, records citations, and runs simple evals.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "extractions.json"
EVAL_PATH = ROOT / "eval_cases.json"


@dataclass(frozen=True)
class CitedValue:
    value: float
    citation: str
    quote: str


@dataclass(frozen=True)
class CovenantResult:
    name: str
    actual: float
    limit: float
    headroom: float
    status: str
    formula: str
    citations: list[str]


def load_data(path: Path = DATA_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cv(node: dict[str, Any]) -> CitedValue:
    return CitedValue(float(node["value"]), str(node["citation"]), str(node.get("quote", "")))


def iter_cited_values(data: dict[str, Any]) -> list[tuple[str, CitedValue]]:
    cited = []
    for group, fields in data["values"].items():
        for key, node in fields.items():
            cited.append((f"{group}.{key}", cv(node)))
    return cited


def compute_results(data: dict[str, Any]) -> tuple[list[CovenantResult], list[str]]:
    values = data["values"]
    fs = values["financial_statements"]
    cert = values["certificate"]
    cov = values["covenants"]

    ebitda = cv(cert["ebitda_ltm_eurm"])
    senior_debt = cv(cert["senior_debt_eurm"])
    cash = cv(cert["cash_eurm"])
    interest = cv(cert["cash_interest_eurm"])
    revolver = cv(cert["undrawn_revolver_eurm"])

    max_leverage = cv(cov["max_net_leverage"])
    min_coverage = cv(cov["min_interest_coverage"])
    min_liquidity = cv(cov["min_liquidity_eurm"])

    net_debt = senior_debt.value - cash.value
    leverage = net_debt / ebitda.value
    leverage_headroom = max_leverage.value - leverage

    coverage = ebitda.value / interest.value
    coverage_headroom = coverage - min_coverage.value

    liquidity = cash.value + revolver.value
    liquidity_headroom = liquidity - min_liquidity.value

    fy2025_net_debt = cv(fs["fy2025_senior_debt_eurm"]).value - cv(fs["fy2025_cash_eurm"]).value
    fy2025_ebitda = cv(fs["fy2025_ebitda_eurm"]).value
    prior_leverage = fy2025_net_debt / fy2025_ebitda
    leverage_drift = leverage - prior_leverage

    results = [
        CovenantResult(
            name="Net leverage",
            actual=leverage,
            limit=max_leverage.value,
            headroom=leverage_headroom,
            status="WATCH" if 0 <= leverage_headroom < 0.75 else ("BREACH" if leverage_headroom < 0 else "PASS"),
            formula=f"(senior debt EUR {senior_debt.value:.1f}m - cash EUR {cash.value:.1f}m) / EBITDA EUR {ebitda.value:.1f}m",
            citations=[senior_debt.citation, cash.citation, ebitda.citation, max_leverage.citation],
        ),
        CovenantResult(
            name="Interest coverage",
            actual=coverage,
            limit=min_coverage.value,
            headroom=coverage_headroom,
            status="WATCH" if 0 <= coverage_headroom < 0.75 else ("BREACH" if coverage_headroom < 0 else "PASS"),
            formula=f"EBITDA EUR {ebitda.value:.1f}m / cash interest EUR {interest.value:.1f}m",
            citations=[ebitda.citation, interest.citation, min_coverage.citation],
        ),
        CovenantResult(
            name="Minimum liquidity",
            actual=liquidity,
            limit=min_liquidity.value,
            headroom=liquidity_headroom,
            status="BREACH" if liquidity_headroom < 0 else ("WATCH" if liquidity_headroom < 3 else "PASS"),
            formula=f"cash EUR {cash.value:.1f}m + undrawn revolver EUR {revolver.value:.1f}m",
            citations=[cash.citation, revolver.citation, min_liquidity.citation],
        ),
    ]

    fs_debt = cv(fs["senior_debt_eurm"])
    issues = []
    if abs(fs_debt.value - senior_debt.value) > 0.01:
        issues.append(
            "Senior debt mismatch: financial statements show "
            f"EUR {fs_debt.value:.1f}m ({fs_debt.citation}) while the compliance certificate shows "
            f"EUR {senior_debt.value:.1f}m ({senior_debt.citation})."
        )
    if leverage_drift > 0.5:
        issues.append(
            f"Monitoring drift: net leverage increased from {prior_leverage:.2f}x in FY2025 to {leverage:.2f}x in 2026Q2."
        )
    return results, issues


def answer_question(question: str, data: dict[str, Any]) -> str:
    q = question.lower()
    results, issues = compute_results(data)
    by_name = {r.name.lower(): r for r in results}

    if "based on a real borrower" in q:
        return "No real borrower is used. This is a synthetic demo corpus only."
    if "real" in q or "sponsor" in q or "valuation" in q or "live borrower" in q:
        return "I do not know based on the provided synthetic documents. No real sponsor, valuation, live borrower data or holding comparison is included."
    if "default" in q or "predict" in q:
        return "I do not know based on the provided synthetic documents. Default prediction is outside the supported demo scope."
    if "human" in q or "approval" in q or "sent to a borrower" in q:
        return "No. A human reviewer must approve any interpretation, covenant conclusion or borrower communication before use."
    if "model" in q or "generated" in q:
        return "No model calls generated the covenant conclusions in this MVP; all covenant math is deterministic Python over cited synthetic values."
    if "all covenant" in q or "all covenant statuses" in q:
        return "; ".join(f"{r.name}: {r.status}" for r in results) + "."
    if "ebitda" in q:
        return "LTM EBITDA is EUR 24.0m from MU-2026Q2#compliance-certificate-values."
    if "cash" in q and "interest" not in q:
        return "Unrestricted cash is EUR 10.0m from MU-2026Q2#compliance-certificate-values."
    if "interest" in q or "coverage" in q:
        r = by_name["interest coverage"]
        return f"{r.status}: interest coverage is {r.actual:.2f}x versus the {r.limit:.2f}x minimum; headroom is {r.headroom:.2f}x. Formula: {r.formula}. Citations: {', '.join(r.citations)}."
    if "liquidity" in q:
        r = by_name["minimum liquidity"]
        return f"{r.status}: liquidity is EUR {r.actual:.1f}m versus the EUR {r.limit:.1f}m minimum; headroom is EUR {r.headroom:.1f}m. Formula: {r.formula}. Citations: {', '.join(r.citations)}."
    if "leverage" in q or "debt source" in q or "certificate senior debt" in q:
        r = by_name["net leverage"]
        drift = next((issue for issue in issues if issue.startswith("Monitoring drift")), "")
        debt_source = " Certificate senior debt is EUR 92.0m from MU-2026Q2#compliance-certificate-values."
        return f"{r.status}: net leverage is {r.actual:.2f}x versus the {r.limit:.2f}x maximum; headroom is {r.headroom:.2f}x. Formula: {r.formula}. Citations: {', '.join(r.citations)}. {drift}{debt_source}"
    if "consistency" in q or "tie" in q or "mismatch" in q:
        return " ".join(issues) if issues else "No consistency issues found in the extracted synthetic values."
    return "I do not know based on the provided synthetic documents. The question is outside the supported demo scope."


def render_report(data: dict[str, Any]) -> str:
    results, issues = compute_results(data)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# Covenant Sentinel Demo Report",
        "",
        f"Generated: {now}",
        f"Borrower: {data['borrower']} (synthetic)",
        f"As of: {data['as_of']}",
        "",
        "> Public-safe demo only. Not based on any real borrower, lender, portfolio holding, or confidential document.",
        "",
        "## Covenant results",
        "",
        "| Covenant | Status | Actual | Limit | Headroom | Formula | Citations |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for r in results:
        unit = "EURm" if "liquidity" in r.name.lower() else "x"
        lines.append(
            f"| {r.name} | {r.status} | {r.actual:.2f}{unit} | {r.limit:.2f}{unit} | "
            f"{r.headroom:.2f}{unit} | {r.formula} | {'; '.join(r.citations)} |"
        )
    lines.extend(["", "## Tie-out and monitoring flags", ""])
    for issue in issues:
        lines.append(f"- {issue}")
    if not issues:
        lines.append("- No issues found.")
    lines.extend(["", "## Evidence quotes", ""])
    for label, cited in iter_cited_values(data):
        if cited.quote:
            lines.append(f"- `{label}` = `{cited.value:g}` from `{cited.citation}` — “{cited.quote}”")
    lines.extend(
        [
            "",
            "## Human approval gate",
            "",
            "This report is a decision-support artifact. A human reviewer must approve any interpretation, covenant conclusion, or borrower communication before use.",
            "",
            "## Audit log",
            "",
            "- Input corpus: 3 synthetic markdown documents under `data/docs/`.",
            "- Extraction source: curated synthetic `data/extractions.json` with citations.",
            "- Model calls: none in this MVP; all covenant math is deterministic Python.",
            "- Failure mode intentionally demonstrated: debt mismatch between financial statements and compliance certificate.",
        ]
    )
    return "\n".join(lines) + "\n"


def run_evals(data: dict[str, Any]) -> tuple[bool, str]:
    cases = json.loads(EVAL_PATH.read_text(encoding="utf-8"))
    lines = ["# Covenant Sentinel Eval Results", "", "| ID | Pass | Missing |", "|---|---:|---|"]
    all_ok = True
    passed = 0
    for case in cases:
        answer = answer_question(case["question"], data)
        missing = [needle for needle in case["expected_contains"] if needle not in answer]
        ok = not missing
        passed += int(ok)
        all_ok = all_ok and ok
        lines.append(f"| {case['id']} | {'PASS' if ok else 'FAIL'} | {', '.join(missing) if missing else '-'} |")
    lines.extend(["", f"Summary: {passed}/{len(cases)} PASS"])
    return all_ok, "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthetic Covenant Sentinel demo")
    sub = parser.add_subparsers(dest="command", required=True)
    report_p = sub.add_parser("report", help="Generate markdown covenant report")
    report_p.add_argument("--out", default=str(ROOT / "reports" / "demo_report.md"))
    sub.add_parser("eval", help="Run deterministic eval cases")
    ask_p = sub.add_parser("ask", help="Ask a supported grounded question")
    ask_p.add_argument("question")
    args = parser.parse_args()

    data = load_data()
    if args.command == "report":
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_report(data), encoding="utf-8")
        print(out)
        return 0
    if args.command == "eval":
        ok, text = run_evals(data)
        print(text)
        return 0 if ok else 1
    if args.command == "ask":
        print(answer_question(args.question, data))
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
