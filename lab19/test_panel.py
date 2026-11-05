import json
from pathlib import Path
import unittest
from panel import panel_checks, panel_report, cathie_wood
from sec_facts import unsupported_numbers

ROOT = Path(__file__).parent


class PanelTests(unittest.TestCase):
    def setUp(self):
        self.result = json.loads((ROOT / "data/COST_result.json").read_text())

    def test_cost_seven_reference_checks(self):
        checks = panel_checks(self.result)
        self.assertEqual(list(checks["Buffett"].values()), ["pass"] * 3)
        self.assertEqual(list(checks["Cathie Wood"].values()), ["fail", "not known"])
        self.assertEqual(list(checks["Burry"].values()), ["pass"] * 2)
        self.assertEqual(round(self.result["revenue_cagr"] * 100, 2), 7.51)
        self.assertEqual([round(r["liabilities_to_equity"], 2) for r in self.result["rows"]], [2.11, 1.75, 1.96, 1.64, 1.49])
        self.assertTrue(all(r["rd_to_revenue"] == "not known" for r in self.result["rows"]))

    def test_five_percent_probe_preserves_other_screens(self):
        baseline = panel_checks(self.result)
        probe = panel_checks(self.result, .05)
        self.assertEqual(list(probe["Cathie Wood"].values()), ["pass", "not known"])
        for investor in ("Buffett", "Burry"):
            self.assertEqual(probe[investor], baseline[investor])
        self.assertEqual(panel_checks(self.result), baseline)
        self.assertEqual(cathie_wood.GROWTH_THRESHOLD, .15)

    def test_threshold_boundaries_and_missing(self):
        self.result["revenue_cagr"] = .15
        self.result["rows"][-1]["rd_to_revenue"] = .05
        self.result["rows"][-1]["liabilities_to_equity"] = 2
        checks = panel_checks(self.result)
        self.assertEqual(list(checks["Cathie Wood"].values()), ["pass", "pass"])
        self.assertEqual(list(checks["Burry"].values())[-1], "pass")
        self.result["revenue_cagr"] = "not known"
        self.result["rows"][-1]["rd_to_revenue"] = "not known"
        self.result["rows"][-1]["liabilities_to_equity"] = "not known"
        self.result["rows"][0]["operating_cash_flow"] = "not known"
        checks = panel_checks(self.result)
        self.assertEqual(list(checks["Cathie Wood"].values()), ["not known"] * 2)
        self.assertEqual(list(checks["Burry"].values()), ["not known"] * 2)

    def test_all_memos_and_injection(self):
        for path in sorted((ROOT / "memos").glob("*.md")):
            with self.subTest(memo=path.name):
                ticker = path.name.split("_")[0]
                result = json.loads((ROOT / f"data/{ticker}_result.json").read_text())
                report = panel_report(result)
                memo = path.read_text()
                self.assertEqual(unsupported_numbers(memo, report), [])
                self.assertIn("40.0%", unsupported_numbers(memo + "\nROE was 40.0%.", report))

    def test_bundled_extractors_match(self):
        canonical = (ROOT / "sec_facts.py").read_bytes()
        for folder in ("cathie-wood-investor", "michael-burry-investor"):
            self.assertEqual((ROOT / folder / "scripts/sec_facts.py").read_bytes(), canonical)

    def test_nvda_recalculates_from_raw_sec_facts(self):
        from sec_facts import analyze
        result = json.loads((ROOT / "data/NVDA_result.json").read_text())
        facts = json.loads((ROOT / "data/NVDA_companyfacts.json").read_text())
        recalculated = analyze(facts, [r["fiscal_year_end"] for r in result["rows"]], "NVDA", result["as_of"])
        self.assertEqual(recalculated["rows"], result["rows"])
        self.assertEqual([status for checks in panel_checks(recalculated).values() for status in checks.values()],
                         ["pass", "pass", "pass", "pass", "pass", "fail", "pass"])


if __name__ == "__main__":
    unittest.main()
