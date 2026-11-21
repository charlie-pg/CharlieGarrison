import math
import unittest
from datetime import date

import asof
from portfolio import ASSETS, CORRELATIONS, covariance_matrix
from project2 import (
    AS_OF, ROOT, allocation_stop, benchmark_metrics, compare, issuer_check, load_prices, mandate_checks,
    metrics, read_signal, stress_cases, validate_holdings, verdict,
)


class Project2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (ROOT / "prices.csv").read_text()
        cls.prices = load_prices(cls.raw)

    def test_lab14_equal_weight(self):
        result = metrics((0.25,) * 4 + (0.0,), [*ASSETS, ("Cash", 0, 0)],
                         [row + [0] for row in covariance_matrix(ASSETS, CORRELATIONS)] + [[0] * 5], 0)
        self.assertAlmostEqual(result["gross"], 0.052)
        self.assertEqual(round(result["vol"] * 100, 2), 5.21)

    def test_cash_and_risk_boundaries(self):
        for cash, cash_status in [(0.05, "PASS"), (0.049, "FAIL")]:
            result = {"weights": (1 - cash, 0, 0, 0, cash), "vol": 0.15}
            checks = mandate_checks(result, {}, 0.10)
            self.assertEqual(checks["Cash minimum"][0], cash_status)
            self.assertEqual(checks["Proposed annualized volatility limit"][0], "PASS")
            self.assertEqual(checks["Single-company exposure"][0], "UNVERIFIED")
            self.assertEqual(verdict(checks), "UNVERIFIED" if cash_status == "PASS" else "FAIL")

        result["vol"] = 0.1501
        self.assertEqual(mandate_checks(result, {}, 0.10)["Proposed annualized volatility limit"][0], "FAIL")

    def test_monthly_rebalanced_benchmark(self):
        prices = "Date,BIL,IEF,LQD,VT\na,100,100,100,100\nb,110,100,100,100\nc,110,100,100,110\n"
        benchmark = benchmark_metrics(prices, 2)
        # Fixed weights give +4% and +6%; a buy-and-hold benchmark would drift.
        self.assertAlmostEqual(benchmark["gross"], 0.60)
        self.assertAlmostEqual(benchmark["vol"], math.sqrt(12) * 0.02 / math.sqrt(2))

    def test_issuer_overlap_and_boundary(self):
        holdings = {
            "LQD": {"issuer_weights": {"Issuer A": 0.20}, "noncompany_weight": 0.80},
            "VT": {"issuer_weights": {"Issuer A": 0.20}, "noncompany_weight": 0.80},
        }
        self.assertEqual(issuer_check((0, 0, .25, .25, .50), holdings, .10)[0], "PASS")
        self.assertEqual(issuer_check((0, 0, .26, .25, .49), holdings, .10)[0], "FAIL")
        del holdings["LQD"]
        self.assertEqual(issuer_check((0, 0, .25, .25, .50), holdings, .10)[0], "UNVERIFIED")
        self.assertEqual(issuer_check((0, 0, .04, .60, .36), holdings, .10)[0], "FAIL")

    def test_holdings_require_availability_and_coverage(self):
        snapshot = {"holdings_date": "2026-09-29", "available_on": "2026-10-01",
                    "source": "synthetic test source", "issuer_weights": {"Issuer A": 0.04},
                    "noncompany_weight": 0.80}
        with self.assertRaisesRegex(ValueError, "availability"):
            validate_holdings({"VT": snapshot}, AS_OF)
        snapshot["available_on"] = AS_OF.isoformat()
        holdings = validate_holdings({"VT": snapshot}, AS_OF)
        self.assertEqual(issuer_check((0, 0, 0, .5, .5), holdings, .10)[0], "UNVERIFIED")
        snapshot["noncompany_weight"] = 1
        with self.assertRaisesRegex(ValueError, "exceed 100%"):
            validate_holdings(holdings, AS_OF)

    def test_monthly_data_validation(self):
        for bad in [self.raw.replace("2021-10-31", "2021-09-30"),
                    self.raw.replace("2021-10-31", "2021-11-30"),
                    "Date,VT,IEF,LQD,BIL\n" + self.raw.split("\n", 1)[1],
                    self.raw.replace(self.raw.splitlines()[1].split(",")[1], "nan", 1)]:
            with self.subTest():
                with self.assertRaises(ValueError):
                    load_prices(bad)

    def test_signal_vintage_and_future_row(self):
        raw = (ROOT / "data/dgs10-2026-09-30.csv").read_text()
        self.assertEqual(read_signal(raw, AS_OF), (date(2026, 9, 29), 5.26, 1))
        with self.assertRaisesRegex(ValueError, "after the decision date"):
            read_signal(raw.rstrip() + "\n2026-10-01,5.20\n", AS_OF)
        with self.assertRaisesRegex(ValueError, "requested vintage"):
            read_signal(raw, date(2026, 10, 1))

    def test_lab16_point_in_time_known_answers(self):
        unique = {row[1:]: row for row in reversed(asof.DATA) if row[1]}
        rows, _ = asof.latest_vintages([r for r in unique.values() if r[3] <= asof.DECISION_DATE])
        self.assertEqual([r[0] for r in rows], [1, 4, 5, 6, 9, 12])
        values = asof.signals(rows)
        self.assertEqual({t: round(v, 2) for t, (v, _) in values.items()},
                         {"AAA": 1.98, "BBB": -1.02, "CCC": 0.91})

    def test_cost_and_infeasibility(self):
        result = metrics((.60, .40), [("ETF", .08, .1), ("Cash", 0, 0)],
                         [[.01, 0], [0, 0]], .005)
        self.assertAlmostEqual(result["net"], .045)
        portfolios, _ = compare(self.prices, {}, hurdle=1)
        self.assertIsNone(portfolios["Constrained"])
        self.assertIn("No candidate", allocation_stop(None, 1))

    def test_stress_runs_and_funding_gate(self):
        rows = stress_cases(self.prices, {})
        self.assertEqual(len(rows), 6)
        for name, (result, _) in rows.items():
            if result is not None:
                self.assertGreaterEqual(result["weights"][-1], .10 if name in
                                        ("10% cash / 8% company", "Combined adverse") else .05)
                self.assertEqual(result["verdict"], "UNVERIFIED")
                self.assertEqual(result["checks"]["Proposed annualized volatility limit"][0], "PASS")
        self.assertIn("UNVERIFIED", allocation_stop(rows["Reference"][0], 1))
        self.assertIn("stale", allocation_stop({"verdict": "PASS"}, 8))
        self.assertIsNone(allocation_stop({"verdict": "PASS"}, 1))


if __name__ == "__main__":
    unittest.main()
