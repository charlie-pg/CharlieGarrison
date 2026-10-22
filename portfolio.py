
import math

# Lab 14 — Portfolio Baselines
# All returns and volatilities are decimals.
ASSETS = [
    ("Treasury bills", 0.035, 0.005),
    ("Treasury 10-year note", 0.043, 0.07),
    ("Investment-grade bond fund", 0.05, 0.06),
    ("Global equity index fund", 0.08, 0.16),
]

CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]

OBJECTIVE = 0.065


def validate_correlations(correlations):
    n = len(ASSETS)
    if len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table must be 4 by 4.")

    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not -1 <= value <= 1:
                raise ValueError("Invalid correlation: must be between -1 and 1.")
            if not math.isclose(value, correlations[j][i], abs_tol=1e-10):
                raise ValueError("Correlation table must be symmetric.")
        if not math.isclose(correlations[i][i], 1.0, abs_tol=1e-10):
            raise ValueError("Diagonal correlations must equal 1.")


def covariance_matrix(assets, correlations):
    return [
        [
            correlations[i][j] * assets[i][2] * assets[j][2]
            for j in range(len(assets))
        ]
        for i in range(len(assets))
    ]


def inverse_volatility_weights(assets):
    inverse = [1 / asset[2] for asset in assets]
    total = sum(inverse)
    return [value / total for value in inverse]


def expected_return(weights, assets):
    return sum(w * asset[1] for w, asset in zip(weights, assets))


def portfolio_volatility(weights, covariance):
    variance = sum(
        weights[i] * weights[j] * covariance[i][j]
        for i in range(len(weights))
        for j in range(len(weights))
    )
    return math.sqrt(variance)


def reserve_weight(weights):
    return weights[0] + weights[1]


def meets_objective(portfolio_return, objective):
    return portfolio_return >= objective


def calculate_portfolio(weights, assets, covariance, objective):
    ret = expected_return(weights, assets)
    vol = portfolio_volatility(weights, covariance)
    reserve = reserve_weight(weights)
    return ret, vol, reserve, meets_objective(ret, objective)


def main():
    validate_correlations(CORRELATIONS)
    covariance = covariance_matrix(ASSETS, CORRELATIONS)

    portfolios = {
        "Benchmark": [0.0, 0.0, 0.4, 0.6],
        "Equal weight": [0.25] * 4,
        "Inverse volatility": inverse_volatility_weights(ASSETS),
    }

    for name, weights in portfolios.items():
        ret, vol, reserve, meets = calculate_portfolio(
            weights, ASSETS, covariance, OBJECTIVE
        )
        print(f"\n{name}")
        print("Weights (%):", " / ".join(f"{w * 100:.1f}" for w in weights))
        print(f"Expected return: {ret * 100:.2f}%")
        print(f"Volatility: {vol * 100:.2f}%")
        print(f"Reserve eligible: {reserve * 100:.1f}%")
        print(f"Meets 6.5% objective: {'yes' if meets else 'no'}")


def find_lowest_risk(assets, correlations, objective, reserve_minimum=0.03,
                     reserve_flags=None):
    from itertools import product

    n = len(assets)
    if reserve_flags is None:
        reserve_flags = [i < 2 for i in range(n)]

    validate_correlations_for_assets(correlations, n)
    covariance = covariance_matrix(assets, correlations)
    best = None

    for allocation in product(range(0, 101, 5), repeat=n - 1):
        final_weight = 100 - sum(allocation)
        if final_weight < 0 or final_weight % 5 != 0:
            continue

        weights = [x / 100 for x in (*allocation, final_weight)]
        ret = expected_return(weights, assets)
        reserve = sum(w for w, flag in zip(weights, reserve_flags) if flag)

        if ret < objective - 1e-12 or reserve < reserve_minimum - 1e-12:
            continue

        vol = portfolio_volatility(weights, covariance)

        if best is None or vol < best["volatility"] - 1e-12:
            best = {
                "weights": weights,
                "return": ret,
                "volatility": vol,
                "reserve": reserve,
            }

    return best


def validate_correlations_for_assets(correlations, n):
    if len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table has incorrect dimensions.")

    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not -1 <= value <= 1:
                raise ValueError("Correlation must be between -1 and 1.")
            if not math.isclose(value, correlations[j][i], abs_tol=1e-10):
                raise ValueError("Correlation table must be symmetric.")
        if not math.isclose(correlations[i][i], 1, abs_tol=1e-10):
            raise ValueError("Diagonal correlations must equal 1.")


def estimate_from_csv(csv_file, last_36=False):
    import csv
    import statistics

    rows = list(csv.reader(csv_file))
    tickers = rows[0][1:]
    prices = [[float(value) for value in row[1:]] for row in rows[1:] if row]

    if last_36:
        prices = prices[-37:]

    if len(prices) < 3:
        raise ValueError("Not enough monthly prices.")

    monthly = [
        [prices[t][i] / prices[t - 1][i] - 1 for i in range(len(tickers))]
        for t in range(1, len(prices))
    ]

    columns = [[row[i] for row in monthly] for i in range(len(tickers))]
    assets = [
        (ticker, statistics.mean(col) * 12,
         statistics.stdev(col) * math.sqrt(12))
        for ticker, col in zip(tickers, columns)
    ]

    correlations = []
    for a in columns:
        row = []
        for b in columns:
            mean_a, mean_b = statistics.mean(a), statistics.mean(b)
            numerator = sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b))
            denominator = math.sqrt(
                sum((x - mean_a) ** 2 for x in a)
                * sum((y - mean_b) ** 2 for y in b)
            )
            row.append(numerator / denominator if denominator else 0.0)
        correlations.append(row)

    for i in range(len(tickers)):
        correlations[i][i] = 1.0

    return assets, correlations

if __name__ == "__main__":
    main()