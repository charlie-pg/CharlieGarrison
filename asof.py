
from datetime import date

# Editable inputs
DECISION_DATE = "2026-03-31"

# Row number, ticker, month measured, published on, price
DATA = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]


def latest_vintages(rows):
    """Keep the latest publication for each ticker and measured month."""
    latest = {}
    replaced = []

    for row in rows:
        number, ticker, month, published, price = row
        key = (ticker, month)

        if key not in latest:
            latest[key] = row
        elif published > latest[key][3]:
            replaced.append(latest[key][0])
            latest[key] = row
        else:
            replaced.append(number)

    return sorted(latest.values(), key=lambda r: (r[1], r[2])), sorted(replaced)


def signals(rows):
    """Calculate the latest month-over-month price change per ticker."""
    results = {}
    tickers = sorted({row[1] for row in rows})

    for ticker in tickers:
        history = sorted(
            (row for row in rows if row[1] == ticker),
            key=lambda r: r[2]
        )

        if len(history) < 2:
            results[ticker] = None
            continue

        previous = history[-2]
        current = history[-1]
        change = (current[4] / previous[4] - 1) * 100
        results[ticker] = (change, current[2])

    return results


def main():
    decision = date.fromisoformat(DECISION_DATE)

    # Rule 1: quarantine rows without tickers.
    missing = [r[0] for r in DATA if not r[1].strip()]
    rows = [r for r in DATA if r[1].strip()]

    # Rule 2: remove exact duplicates, keeping the first row.
    seen = set()
    duplicates = []
    unique = []

    for row in rows:
        identity = row[1:]  # Ignore row number when checking duplicates.
        if identity in seen:
            duplicates.append(row[0])
        else:
            seen.add(identity)
            unique.append(row)

    # Rule 3: remove publications after the decision date.
    future = [
        r[0] for r in unique
        if date.fromisoformat(r[3]) > decision
    ]
    available = [
        r for r in unique
        if date.fromisoformat(r[3]) <= decision
    ]

    # Rule 4: keep the latest available revision per ticker/month.
    panel, older = latest_vintages(available)

    print(f"DECISION DATE: {DECISION_DATE}")
    print("\nROW FUNNEL")
    print(f"1. Missing ticker: {len(missing)} removed {missing}")
    print(f"2. Exact duplicate: {len(duplicates)} removed {duplicates}")
    print(f"3. Published too late: {len(future)} removed {future}")
    print(f"4. Older revision: {len(older)} removed {older}")

    print("\nAS-OF PANEL")
    print("Row  Ticker  Month    Published    Price")
    for number, ticker, month, published, price in panel:
        print(f"{number:<4} {ticker:<6}  {month}  {published}  {price:.1f}")

    # Naive: latest publication for each ticker/month, ignoring timing.
    naive_panel, _ = latest_vintages(
        [r for r in DATA if r[1].strip()]
    )

    asof_results = signals(panel)
    naive_results = signals(naive_panel)

    print("\nSIGNALS")
    print("Ticker  As-of signal          Naive signal")
    for ticker in sorted(asof_results):
        asof = asof_results[ticker]
        naive = naive_results[ticker]

        def format_signal(result):
            if result is None:
                return "Not enough months"
            change, month = result
            return f"{change:+.2f}% ({month})"

        print(
            f"{ticker:<6}  "
            f"{format_signal(asof):<22}"
            f"{format_signal(naive)}"
        )


if __name__ == "__main__":
    main()
