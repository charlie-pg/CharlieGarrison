import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).parent / "sec_facts.py"
spec = importlib.util.spec_from_file_location("buffett", SCRIPT)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def fixture():
    """Synthetic data for behavioral tests only; never used by the app or reports."""
    facts = {"facts": {"us-gaap": {}}}
    ends = [f"{y}-12-31" for y in range(2022, 2027)]
    for metric, tags in b.TAGS.items():
        units = []
        for i, end in enumerate(ends):
            value = {"revenue": 1000, "net_income": 20, "equity": 100,
                     "operating_cash_flow": 50 + i, "capital_spending": 10,
                     "liabilities": 200, "research_and_development": 50}[metric]
            fact = {"end": end, "val": value, "form": "10-K", "filed": "2027-02-01", "accn": "a"}
            if metric not in {"equity", "liabilities"}:
                fact["start"] = end[:4] + "-01-01"
            units.append(fact)
        facts["facts"]["us-gaap"][tags[0]] = {"units": {"USD": units}}
    return facts, ends


class ExtractionTests(unittest.TestCase):
    def test_annual_and_latest_filing(self):
        facts, ends = fixture()
        units = facts["facts"]["us-gaap"]["NetIncomeLoss"]["units"]["USD"]
        units += [dict(units[0], val=999, form="10-Q", filed="2027-03-01"),
                  dict(units[0], val=888, start="2022-10-01", filed="2027-03-01"),
                  dict(units[0], val=777, form="10-K/A", filed="2027-03-01"),
                  dict(units[0], val=30, filed="2027-02-02")]
        row = b.analyze(facts, ends, "TEST", "2027-04-01")["rows"][0]
        self.assertEqual(row["net_income"], 30)
        self.assertEqual(row["roe"], .3)

    def test_priority_fallback_and_newest(self):
        facts, ends = fixture()
        gaap = facts["facts"]["us-gaap"]
        primary = gaap[b.TAGS["revenue"][0]]["units"]["USD"][0]
        gaap["Revenues"] = {"units": {"USD": [dict(primary, val=2000)]}}
        self.assertEqual(b.choose_fact(facts, "revenue", ends[0], "2027-04-01")["value"], 1000)
        gaap["Revenues"]["units"]["USD"][0]["filed"] = "2027-03-01"
        self.assertEqual(b.choose_fact(facts, "revenue", ends[0], "2027-04-01")["value"], 2000)
        self.assertEqual(b.choose_fact(facts, "revenue", ends[0], "2027-02-01")["value"], 1000)

    def test_missing_capex(self):
        facts, ends = fixture()
        del facts["facts"]["us-gaap"][b.TAGS["capital_spending"][0]]
        result = b.analyze(facts, ends, "TEST", "2027-04-01")
        self.assertTrue(all(r["capital_spending"] == "not known" and r["owner_earnings"] == "not known" for r in result["rows"]))
        self.assertEqual(list(result["checks"].values())[1:], ["not known", "not known"])

    def test_checks_and_nonpositive_equity(self):
        facts, ends = fixture()
        self.assertEqual(list(b.analyze(facts, ends, "TEST", "2027-04-01")["checks"].values()), ["pass"] * 3)
        facts["facts"]["us-gaap"]["StockholdersEquity"]["units"]["USD"][0]["val"] = 0
        result = b.analyze(facts, ends, "TEST", "2027-04-01")
        self.assertEqual(result["rows"][0]["roe"], "not known")
        self.assertEqual(list(result["checks"].values())[0], "not known")
        self.assertEqual(list(b.analyze(facts, ends[:4], "TEST", "2027-04-01")["checks"].values()), ["not known"] * 3)

    def test_added_metrics_and_missing_data(self):
        facts, ends = fixture()
        result = b.analyze(facts, ends, "TEST", "2027-04-01")
        self.assertEqual(result["rows"][0]["liabilities_to_equity"], 2)
        self.assertEqual(result["rows"][0]["rd_to_revenue"], .05)
        self.assertEqual(result["rows"][0]["revenue_growth"], "not known")
        self.assertEqual(result["rows"][1]["revenue_growth"], 0)
        del facts["facts"]["us-gaap"]["ResearchAndDevelopmentExpense"]
        result = b.analyze(facts, ends, "TEST", "2027-04-01")
        self.assertEqual(result["rows"][0]["research_and_development"], "not known")
        self.assertEqual(result["rows"][0]["rd_to_revenue"], "not known")

    def test_cagr_formula_and_uncomputable_inputs(self):
        facts, ends = fixture()
        revenue = facts["facts"]["us-gaap"][b.TAGS["revenue"][0]]["units"]["USD"]
        revenue[-1]["val"] = 1000 * 1.15 ** 4
        self.assertAlmostEqual(b.analyze(facts, ends, "TEST", "2027-04-01")["revenue_cagr"], .15)
        self.assertEqual(b.analyze(facts, ends[:4], "TEST", "2027-04-01")["revenue_cagr"], "not known")
        revenue[0]["val"] = 0
        self.assertEqual(b.analyze(facts, ends, "TEST", "2027-04-01")["revenue_cagr"], "not known")
        revenue[0]["val"] = 1000
        revenue[-1]["val"] = -1
        self.assertEqual(b.analyze(facts, ends, "TEST", "2027-04-01")["revenue_cagr"], "not known")

    def test_liabilities_must_be_instant(self):
        facts, ends = fixture()
        unit = facts["facts"]["us-gaap"]["Liabilities"]["units"]["USD"][0]
        unit["start"] = "2022-01-01"
        self.assertEqual(b.choose_fact(facts, "liabilities", ends[0], "2027-04-01")["value"], "not known")

    def test_ambiguity_is_rejected(self):
        facts, ends = fixture()
        units = facts["facts"]["us-gaap"]["Liabilities"]["units"]["USD"]
        units.append(dict(units[0], val=999))
        with self.assertRaises(ValueError):
            b.analyze(facts, ends, "TEST", "2027-04-01")

    def test_memo_numeric_audit(self):
        self.assertEqual(b.unsupported_numbers("ROE was 40.0%", "ROE 20.0%; revenue 40.00"), ["40.0%"])
        self.assertEqual(b.unsupported_numbers("ROE was 40.0%.", "ROE 20.0%; revenue 40.00"), ["40.0%"])
        self.assertEqual(b.unsupported_numbers("Income 1,000.00; ROE 20%", "1,000.00 20.0%"), [])

    def test_fiscal_end_not_fact_fy(self):
        records = [{"reportDate": f"{y}-08-31"} for y in range(2019, 2027)]
        self.assertEqual(b.fiscal_ends(records), [f"{y}-08-31" for y in range(2022, 2027)])
        facts, ends = fixture()
        for tag in facts["facts"]["us-gaap"].values():
            for fact in tag["units"]["USD"]:
                fact["fy"] = 2026
        self.assertEqual([r["fiscal_year_end"] for r in b.analyze(facts, ends, "TEST", "2027-04-01")["rows"]], ends)


if __name__ == "__main__":
    unittest.main()
