"""Recalculate preserved Lab 18 data; save reproducible validation evidence."""
import json
from pathlib import Path
import unittest
from sec_facts import analyze, unsupported_numbers
from panel import panel_checks, panel_report

ROOT = Path(__file__).resolve().parent


def rebuild(ticker):
    old_dir = ROOT.parent / "lab18/data"
    old = json.loads((old_dir / f"{ticker}_result.json").read_text())
    facts = json.loads((old_dir / f"{ticker}_companyfacts.json").read_text())
    result = analyze(facts, [r["fiscal_year_end"] for r in old["rows"]], ticker, old["as_of"])
    result.update(downloaded_at=old["downloaded_at"], urls=old["urls"],
                  data_origin=f"Recalculated preserved lab18/data/{ticker}_companyfacts.json; not a new download")
    (ROOT / f"data/{ticker}_result.json").write_text(json.dumps(result, indent=2) + "\n")
    (ROOT / f"data/{ticker}_report.md").write_text(panel_report(result))
    return result


if __name__ == "__main__":
    result = rebuild("COST")
    rebuild("JPM")
    suite = unittest.defaultTestLoader.discover(str(ROOT), pattern="test_*.py")
    tests = unittest.TextTestRunner(verbosity=2).run(suite)
    evidence = {
        "unit_tests": {"run": tests.testsRun, "passed": tests.wasSuccessful()},
        "cost_default": panel_checks(result), "cost_five_percent_probe": panel_checks(result, .05),
        "retained_growth_threshold": .15, "revenue_cagr": result["revenue_cagr"],
        "liabilities_to_equity": [r["liabilities_to_equity"] for r in result["rows"]],
        "memo_audits": {},
    }
    for path in sorted((ROOT / "memos").glob("*.md")):
        ticker = path.name.split("_")[0]
        data = json.loads((ROOT / f"data/{ticker}_result.json").read_text())
        report = panel_report(data)
        evidence["memo_audits"][path.name] = {
            "baseline_warnings": unsupported_numbers(path.read_text(), report),
            "injected_warnings": unsupported_numbers(path.read_text() + "\nROE was 40.0%.", report),
        }
    (ROOT / "data/validation.json").write_text(json.dumps(evidence, indent=2) + "\n")
    raise SystemExit(0 if tests.wasSuccessful() else 1)
