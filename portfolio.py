
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


if __name__ == "__main__":
    main()