"""Retirement portfolio analysis layered on the Lab 14/15 calculations."""
import csv
import math
from calendar import monthrange
from collections import defaultdict
from datetime import date
from io import StringIO
from itertools import combinations
from pathlib import Path
from statistics import mean, stdev

from portfolio import covariance_matrix, estimate_from_csv, expected_return
from portfolio import inverse_volatility_weights, portfolio_volatility

ROOT = Path(__file__).resolve().parent
ETF_NAMES = ("BIL", "IEF", "LQD", "VT")
NAMES = (*ETF_NAMES, "Cash")
AS_OF = date(2026, 9, 30)
CASH_MIN = 0.05
ISSUER_MAX = 0.10
EPS = 1e-9
VOLATILITY_LIMIT = 0.15
RETURN_HURDLE = 0.065
BENCHMARK = (0.4, 0, 0, 0.6)
SIGNAL_MAX_AGE = 7


def load_prices(text):
    rows = list(csv.reader(StringIO(text)))
    if not rows or tuple(rows[0]) != ("Date", *ETF_NAMES):
        raise ValueError("Expected columns Date,BIL,IEF,LQD,VT in that order.")
    if len(rows) != 62:
        raise ValueError("Expected exactly 61 monthly price rows.")
    for index, row in enumerate(rows[1:]):
        if len(row) != 5:
            raise ValueError(f"Incorrect number of fields at CSV row {index + 2}.")
        year, month = divmod(2021 * 12 + 8 + index, 12)
        month += 1
        month_end = date(year, month, monthrange(year, month)[1])
        if date.fromisoformat(row[0]) != month_end:
            raise ValueError(f"Expected month-end {month_end} at CSV row {index + 2}.")
        if any(not math.isfinite(price) or price <= 0 for price in map(float, row[1:])):
            raise ValueError(f"Prices must be positive and finite at CSV row {index + 2}.")
    return text


def read_signal(text, decision_date):
    rows = csv.DictReader(StringIO(text))
    if rows.fieldnames != ["observation_date", f"DGS10_{decision_date:%Y%m%d}"]:
        raise ValueError("DGS10 file must match the requested vintage.")
    observations = {}
    for row in rows:
        observed = date.fromisoformat(row["observation_date"])
        if observed > decision_date:
            raise ValueError("DGS10 vintage contains an observation after the decision date.")
        if observed in observations:
            raise ValueError("Duplicate DGS10 observation date.")
        value = row[rows.fieldnames[1]]
        observations[observed] = None if value in ("", ".") else float(value)
        if observations[observed] is not None and not math.isfinite(observations[observed]):
            raise ValueError("Nonfinite DGS10 observation.")
    known = [(d, v) for d, v in observations.items() if v is not None]
    if not known:
        raise ValueError("No published DGS10 observations in the vintage.")
    observed, value = max(known)
    return observed, value, (decision_date - observed).days


def validate_holdings(document, decision_date):
    """Accept dated, long-only exposures expressed as fractions of fund NAV."""
    if not isinstance(document, dict) or set(document) - set(ETF_NAMES):
        raise ValueError("Holdings must be an object keyed by supported fund ticker.")
    for ticker, snapshot in document.items():
        holdings_date = date.fromisoformat(snapshot["holdings_date"])
        available_on = date.fromisoformat(snapshot["available_on"])
        if not holdings_date <= available_on <= decision_date:
            raise ValueError(f"{ticker}: holdings availability must be known by {decision_date}.")
        if not snapshot["source"].strip():
            raise ValueError(f"{ticker}: source is required.")
        issuers = snapshot["issuer_weights"]
        if any(not name.strip() for name in issuers):
            raise ValueError(f"{ticker}: issuer names cannot be blank.")
        weights = [snapshot["noncompany_weight"], *issuers.values()]
        if any(isinstance(w, bool) or not math.isfinite(w) or w < 0 for w in weights):
            raise ValueError(f"{ticker}: weights must be finite, nonnegative fractions.")
        if sum(weights) > 1 + EPS:
            raise ValueError(f"{ticker}: mapped holdings exceed 100% of fund NAV.")
    return document


def issuer_check(weights, holdings, limit):
    exposures = defaultdict(float)
    gaps = []
    for ticker, weight in zip(ETF_NAMES, weights):
        if weight <= EPS:
            continue
        snapshot = holdings.get(ticker)
        if snapshot is None:
            gaps.append(ticker)
            continue
        issuers = snapshot["issuer_weights"]
        for issuer, fraction in issuers.items():
            exposures[issuer] += weight * fraction
        if sum(issuers.values()) + snapshot["noncompany_weight"] < 1 - EPS:
            gaps.append(ticker)
    breaches = [f"{i} {w:.2%}" for i, w in sorted(exposures.items()) if w > limit + EPS]
    if breaches:
        return "FAIL", f"Above {limit:.2%}: {', '.join(breaches)}."
    if gaps:
        return "UNVERIFIED", f"Incomplete as-of issuer coverage: {', '.join(gaps)}."
    return "PASS", f"Largest mapped company exposure {max(exposures.values(), default=0):.2%} (cap {limit:.2%})."


def estimates(text, months, equity_shock=0):
    assets, correlations = estimate_from_csv(StringIO(text), last_36=months == 36)
    if any(vol <= EPS for _, _, vol in assets):
        raise ValueError("Inverse volatility requires nonzero volatility for all ETFs.")
    assets = [(ticker, ret + (equity_shock if ticker == "VT" else 0), vol)
              for ticker, ret, vol in assets]
    covariance = covariance_matrix(assets, correlations)
    return [*assets, ("Cash", 0.0, 0.0)], [row + [0.0] for row in covariance] + [[0.0] * 5]


def metrics(weights, assets, covariance, cost):
    gross = expected_return(weights, assets)
    # One-way turnover from a pre-trade portfolio held entirely in cash.
    turnover = 1 - weights[-1]
    return {"weights": weights, "gross": gross, "net": gross - turnover * cost,
            "vol": portfolio_volatility(weights, covariance), "turnover": turnover}


def verdict(checks):
    statuses = [status for status, _ in checks.values()]
    if "FAIL" in statuses:
        return "FAIL"
    return "UNVERIFIED" if "UNVERIFIED" in statuses else "PASS"


def mandate_checks(result, holdings, issuer_limit, cash_floor=CASH_MIN):
    weights = result["weights"]
    funded = min(weights) >= -EPS and abs(sum(weights) - 1) <= EPS
    return {
        "Long only and fully invested": ("PASS" if funded else "FAIL", f"Total {sum(weights):.2%}; minimum weight {min(weights):.2%}."),
        "Cash minimum": ("PASS" if weights[-1] >= cash_floor - EPS else "FAIL", f"Cash {weights[-1]:.2%}; minimum {cash_floor:.2%}."),
        "Single-company exposure": issuer_check(weights, holdings, issuer_limit),
        "Proposed annualized volatility limit": (
            "PASS" if result["vol"] <= VOLATILITY_LIMIT + EPS else "FAIL",
            f"{result['vol']:.2%}; analyst assumption {VOLATILITY_LIMIT:.2%}.",
        ),
    }


def grid_weights():
    # Four separators divide 20 five-point units into five sleeves.
    for cuts in combinations(range(24), 4):
        endpoints = (-1, *cuts, 24)
        yield tuple((right - left - 1) / 20 for left, right in zip(endpoints, endpoints[1:]))


def benchmark_metrics(text, months):
    """Use the fixed benchmark weights at the start of every monthly period."""
    rows = list(csv.reader(StringIO(text)))[-(months + 1):]
    prices = [tuple(map(float, row[1:])) for row in rows]
    monthly_returns = [
        sum(weight * (end / start - 1)
            for weight, start, end in zip(BENCHMARK, previous, current))
        for previous, current in zip(prices, prices[1:])
    ]
    return {"gross": mean(monthly_returns) * 12,
            "vol": stdev(monthly_returns) * math.sqrt(12)}


def compare(text, holdings, *, months=60, equity_shock=0, cost=0,
            cash_floor=CASH_MIN, issuer_limit=ISSUER_MAX, hurdle=RETURN_HURDLE):
    assets, covariance = estimates(text, months, equity_shock)
    portfolios = {
        "Equal weight": metrics((0.25,) * 4 + (0.0,), assets, covariance, cost),
        "Inverse volatility": metrics((*inverse_volatility_weights(assets[:4]), 0.0), assets, covariance, cost),
    }
    cash_floor = max(CASH_MIN, cash_floor)
    issuer_limit = min(ISSUER_MAX, issuer_limit)
    best = None
    best_key = (math.inf, math.inf)
    for weights in grid_weights():
        if weights[-1] < cash_floor - EPS:
            continue
        result = metrics(weights, assets, covariance, cost)
        if result["net"] < hurdle - EPS or result["vol"] > VOLATILITY_LIMIT + EPS:
            continue
        issuer_status, _ = issuer_check(weights, holdings, issuer_limit)
        if issuer_status == "FAIL":
            continue
        key = (issuer_status == "UNVERIFIED", result["vol"])
        if key < best_key:
            best, best_key = result, key
    portfolios["Constrained"] = best
    for result in portfolios.values():
        if result is not None:
            result["checks"] = mandate_checks(result, holdings, issuer_limit, cash_floor)
            result["verdict"] = verdict(result["checks"])
    return portfolios, benchmark_metrics(text, months)


def stress_cases(text, holdings):
    scenarios = {
        "Reference": {},
        "VT expected return −2 pp": {"equity_shock": -0.02},
        "Last 36 monthly returns": {"months": 36},
        "50 bp trading cost": {"cost": 0.005},
        "10% cash / 8% company": {"cash_floor": 0.10, "issuer_limit": 0.08},
        "Combined adverse": {"equity_shock": -0.02, "months": 36, "cost": 0.005,
                             "cash_floor": 0.10, "issuer_limit": 0.08},
    }
    results = {}
    for label, changes in scenarios.items():
        portfolios, benchmark = compare(text, holdings, **changes)
        results[label] = (portfolios["Constrained"], benchmark)
    return results


def allocation_stop(candidate, signal_age):
    if candidate is None:
        return "No candidate satisfies the modeled scenario constraints."
    if candidate["verdict"] != "PASS":
        return f"Retirement mandate verdict is {candidate['verdict']}."
    if signal_age is None or signal_age > SIGNAL_MAX_AGE:
        return "DGS10 vintage is missing or stale for the decision date."
    return None
