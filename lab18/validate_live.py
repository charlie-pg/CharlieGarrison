"""Validate saved SEC outputs against the assignment, without changing extraction."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location("buffett", ROOT / "buffett-investor/scripts/buffett.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def run():
    results = []
    cost_path = ROOT / "data/COST_result.json"
    if cost_path.exists():
        cost = json.loads(cost_path.read_text())
        expected = dict(zip(range(2022, 2027), [3501, 6745, 6629, 7837, 9382]))
        actual = {int(r["fiscal_year_end"][:4]): r["owner_earnings"] / 1e6
                  if b.numeric(r["owner_earnings"]) else r["owner_earnings"] for r in cost["rows"]}
        comparison = {str(y): {"expected_millions": e, "actual_millions": actual.get(y, "not found"),
                              "matches": actual.get(y) == e} for y, e in expected.items()}
        passed = all(c["matches"] for c in comparison.values()) and all(s == "pass" for s in cost["checks"].values())
        results.append({"test": "COST professor reference", "status": "pass" if passed else "FAIL", "comparison": comparison, "checks": cost["checks"]})
        memo = (ROOT / "memos/COST.md").read_text() if (ROOT / "memos/COST.md").exists() else ""
        report = b.render_report(cost)
        baseline = b.unsupported_numbers(memo, report)
        attacked = b.unsupported_numbers(memo + "\nROE was 40.0%.\n", report)
        results.append({"test": "Unsupported 40.0% ROE injection", "status": "pass" if "40.0%" in attacked and not baseline and memo else "FAIL", "baseline_warnings": baseline, "injected_warnings": attacked})
    else:
        results.append({"test": "COST professor reference and memo injection", "status": "NOT RUN", "reason": "No SEC download"})
    jpm_path = ROOT / "data/JPM_result.json"
    if jpm_path.exists():
        jpm = json.loads(jpm_path.read_text())
        missing = len(jpm["rows"]) == 5 and all(r["capital_spending"] == "not found" and r["owner_earnings"] == "not found" for r in jpm["rows"])
        checks = list(jpm["checks"].values())[1:]
        results.append({"test": "JPM missing capital spending", "status": "pass" if missing and checks == ["not known"] * 2 else "FAIL", "checks": jpm["checks"], "capital_spending": [r["capital_spending"] for r in jpm["rows"]]})
    else:
        results.append({"test": "JPM missing capital spending", "status": "NOT RUN", "reason": "No SEC download"})
    (ROOT / "data/validation.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return 0 if all(r["status"] == "pass" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(run())
