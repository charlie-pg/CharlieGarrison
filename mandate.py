
# Lab 13 — Portfolio Mandate Defense

RESERVE_SIZE = 100.0  # USD millions
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5
MIN_LIQUID_SHARE = 90.0
ISSUER_LIMIT = 8.0

# Holding: (issuer, redemption days, reserve eligible)
HOLDINGS = {
    "Cash": (None, 0, True),
    "Treasury bills": ("U.S. Treasury", 1, True),
    "Treasury 10-year note": ("U.S. Treasury", 1, True),
    "Global equity index fund": ("diversified fund", 2, False),
    "Investment-grade bond fund": ("diversified fund", 3, False),
    "Private real estate fund": ("diversified fund", 90, False),
    "Acme Corp bonds": ("Acme Corp", 4, False),
    "Acme Corp stock": ("Acme Corp", 1, False),
}

CANDIDATES = {
    "A": [2, 2, 10, 60, 26, 0, 0, 0],
    "B": [1, 0, 0, 55, 20, 15, 5, 4],
    "C": [1, 1, 0, 70, 20, 0, 0, 8],
    "D": [100, 0, 0, 0, 0, 0, 0, 0],
}

EXEMPT_ISSUERS = {None, "U.S. Treasury", "diversified fund"}


def check_portfolio(name, weights, reserve_minimum):
    holdings = list(HOLDINGS.items())
    total = sum(weights)
    lowest = min(weights)

    reserve = sum(
        weight for weight, (_, (_, _, eligible))
        in zip(weights, holdings) if eligible
    )

    liquid = sum(
        weight for weight, (_, (_, days, _))
        in zip(weights, holdings) if days <= LIQUIDITY_WINDOW
    )

    company_weights = {}
    for weight, (_, (issuer, _, _)) in zip(weights, holdings):
        if issuer not in EXEMPT_ISSUERS:
            company_weights[issuer] = company_weights.get(issuer, 0) + weight

    largest_company = max(company_weights.values(), default=0)

    checks = [
        ("Weights sum to 100", total, abs(total - 100) < 1e-9),
        ("Long-only (lowest weight)", lowest, lowest >= 0),
        ("Reserve eligible", reserve, reserve >= reserve_minimum),
        ("Redeemable in 5 days", liquid, liquid >= MIN_LIQUID_SHARE),
        ("Largest single company", largest_company,
         largest_company <= ISSUER_LIMIT),
    ]

    print(f"\nCandidate {name}")
    failures = 0
    for label, value, passed in checks:
        print(f"  {label}: {value:.1f} — {'pass' if passed else 'FAIL'}")
        failures += not passed

    print("  Calendar-year loss: requires CIO clarification")
    print(
        "  Verdict: passes every checkable rule"
        if failures == 0 else f"  Verdict: fails {failures} rule(s)"
    )


reserve_minimum = (
    QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION
    / RESERVE_SIZE * 100
)

print(f"Reserve minimum: {reserve_minimum:.1f}%")

for name, weights in CANDIDATES.items():
    check_portfolio(name, weights, reserve_minimum)
