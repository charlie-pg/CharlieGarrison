import unittest

from streamlit.testing.v1 import AppTest

from project2 import ROOT


class Project2AppTest(unittest.TestCase):
    def test_default_app_shows_portfolios_and_rule_evidence(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=60)
        self.assertFalse(app.exception)
        summary = app.dataframe[0].value
        self.assertEqual(summary["Portfolio"].tolist(), ["Equal weight", "Inverse volatility", "Constrained"])
        self.assertEqual(summary["Mandate verdict"].tolist(), ["FAIL", "FAIL", "UNVERIFIED"])
        self.assertEqual(summary["Explicit cash"].tolist(), ["0.0%", "0.0%", "10.0%"])
        self.assertEqual(summary["Expected gross return"].tolist(), ["3.22%", "3.33%", "6.56%"])
        self.assertEqual(summary["Expected first-year net return"].tolist(), ["3.22%", "3.33%", "6.56%"])
        self.assertEqual(summary["Annualized volatility"].tolist(), ["7.50%", "1.40%", "6.02%"])

        details = {panel.label: panel for panel in app.expander}
        for name, verdict in zip(summary["Portfolio"], summary["Mandate verdict"]):
            rules = details[f"{name} · {verdict}"].table[0].value.set_index("Rule")
            self.assertEqual(rules.loc["Single-company exposure", "Status"], "UNVERIFIED")
            self.assertIn("coverage", rules.loc["Single-company exposure", "Evidence"])
        self.assertIn("DGS10 data card", details)
        self.assertIn("5.26%", [metric.value for metric in app.metric])
        self.assertTrue(any("0% funded" in message.value for message in app.info))
        self.assertTrue(any("Stop deployment" in message.value for message in app.error))

    def test_policy_labels_and_stress_results(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=60)
        self.assertFalse(app.exception)
        headings = [element.value for element in app.sidebar.subheader]
        self.assertEqual(headings, ["Client requirements", "Strategic benchmark", "Illustrative analyst assumptions"])
        sidebar_text = " ".join(element.value for element in app.sidebar.markdown)
        self.assertIn("60% VT / 40% BIL, rebalanced monthly", sidebar_text)
        self.assertIn("15% annualized", sidebar_text)
        self.assertIn("BIL excluded", sidebar_text)
        self.assertIn("6.5%", sidebar_text)

        scenarios = app.dataframe[1].value
        self.assertEqual(scenarios["Mandate verdict"].tolist(), ["UNVERIFIED"] * 6)
        self.assertEqual(scenarios["Expected first-year net return"].tolist(),
                         ["6.56%", "6.57%", "6.53%", "6.52%", "6.56%", "6.56%"])
        self.assertEqual(scenarios["Annualized volatility"].tolist(),
                         ["6.02%", "7.51%", "1.79%", "6.76%", "6.02%", "2.95%"])
        self.assertEqual(scenarios["Largest allocation change"].tolist(),
                         ["0 pp", "10 pp", "30 pp", "5 pp", "0 pp", "15 pp"])

        details = {panel.label: panel for panel in app.expander}
        gates = details["Scenario allocations and decision gates"].dataframe[0].value
        self.assertTrue(gates["Decision gate"].str.contains("UNVERIFIED").all())
        benchmark = details["Strategic benchmark by scenario"].dataframe[0].value
        self.assertEqual(benchmark["Benchmark gross"].tolist(),
                         ["8.57%", "8.57%", "13.89%", "8.57%", "8.57%", "13.89%"])
        self.assertEqual(benchmark["Benchmark volatility"].tolist(),
                         ["8.99%", "8.99%", "7.04%", "8.99%", "8.99%", "7.04%"])
