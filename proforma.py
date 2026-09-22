# Lab 09 - Pro-Forma Build: ABG Known Answer

YEARS = [2026, 2027, 2028, 2029, 2030]

# Assumptions
growth = 0.018
gross_margin = 0.1705
sga_ratios = [0.665, 0.655, 0.645, 0.645, 0.645]
depr_ratio = 82.4 / 3070.4
impairment = 120.0
capex = 250.0
tax_rate = 0.255
inventory_days = 2135.8 / (17999.0 - 3071.7) * 365
floorplan_ratio = 2027.0 / 2135.8
other_wc_rate = 0.008
minimum_cash = 25.0
revolver_limit = 850.0
revolver_rate = 0.06
debt_repayment = 150.0
buyback = 150.0
floorplan_rate = 0.0467
debt_rate = 0.0544
cost_of_equity = 0.10
terminal_growth = 0.025
shares = 17.951349

# FY2025 opening balance sheet
revenue = 17999.0
inventory = 2135.8
ppe = 3070.4
other_assets = 6371.6
cash = 40.4
floorplan = 2027.0
debt = 3572.0
other_liabilities = 2127.5
equity = 3891.7
revolver = 0.0

results = []

for i, year in enumerate(YEARS):
    opening_revenue = revenue
    opening_inventory = inventory
    opening_ppe = ppe
    opening_cash = cash
    opening_floorplan = floorplan
    opening_debt = debt
    opening_revolver = revolver

    # Income statement
    revenue = opening_revenue * (1 + growth)
    gross_profit = revenue * gross_margin
    sga = gross_profit * sga_ratios[i]
    depreciation = opening_ppe * depr_ratio
    operating_income = gross_profit - sga - depreciation - impairment

    interest = (
        opening_floorplan * floorplan_rate
        + opening_debt * debt_rate
        + opening_revolver * revolver_rate
    )

    pretax = operating_income - interest
    tax = max(0, pretax) * tax_rate
    net_income = pretax - tax

    # Balance sheet except cash
    inventory = (revenue - gross_profit) * inventory_days / 365
    floorplan = inventory * floorplan_ratio
    ppe = opening_ppe + capex - depreciation

    revenue_change = revenue - opening_revenue
    other_wc = other_wc_rate * revenue_change
    other_assets = other_assets + other_wc - impairment

    debt = opening_debt - debt_repayment
    equity = equity + net_income - buyback

    # Cash flow
    change_inventory = inventory - opening_inventory
    change_floorplan = floorplan - opening_floorplan

    fcfe = (
        net_income
        + depreciation
        + impairment
        - capex
        - change_inventory
        - other_wc
        + change_floorplan
        - debt_repayment
    )

    cash_before_revolver = opening_cash + fcfe - buyback

    # Revolver logic
    if cash_before_revolver < minimum_cash:
        draw = minimum_cash - cash_before_revolver
        if opening_revolver + draw > revolver_limit:
            raise ValueError(f"{year}: revolver limit exceeded")
        revolver = opening_revolver + draw
        cash = minimum_cash
    else:
        repayment = min(opening_revolver, cash_before_revolver - minimum_cash)
        revolver = opening_revolver - repayment
        cash = cash_before_revolver - repayment

    assets = cash + inventory + ppe + other_assets
    liabilities_equity = floorplan + debt + revolver + other_liabilities + equity
    balance_gap = assets - liabilities_equity

    results.append({
        "year": year,
        "revenue": revenue,
        "operating_income": operating_income,
        "net_income": net_income,
        "fcfe": fcfe,
        "cash": cash,
        "gap": balance_gap,
    })


def assert_balanced(rows):
    for row in rows:
        if abs(row["gap"]) > 0.1:
            raise ValueError(
                f'FY{row["year"]}E balance sheet does not balance: '
                f'gap = {row["gap"]:.1f}'
            )
        if row["cash"] < minimum_cash:
            raise ValueError(
                f'FY{row["year"]}E cash below minimum'
            )


def print_line(label, key):
    values = " | ".join(f'{r[key]:,.1f}' for r in results)
    print(f"{label:<32} | {values}")


print("ABG Pro-Forma")
print("Years                            | " + " | ".join(str(y) for y in YEARS))
print_line("Revenue", "revenue")
print_line("Operating income", "operating_income")
print_line("Net income", "net_income")
print_line("Free cash flow to equity", "fcfe")
print_line("Cash, year end", "cash")
print_line("Assets - liabilities - equity", "gap")

assert_balanced(results)

# Equity valuation
pv_fcfe = sum(
    row["fcfe"] / ((1 + cost_of_equity) ** (i + 1))
    for i, row in enumerate(results)
)

terminal_fcfe = results[-1]["fcfe"] + debt_repayment
terminal_value = (
    terminal_fcfe * (1 + terminal_growth)
    / (cost_of_equity - terminal_growth)
)

pv_terminal = terminal_value / ((1 + cost_of_equity) ** 5)
equity_value = pv_fcfe + pv_terminal
terminal_share = pv_terminal / equity_value
value_per_share = equity_value / shares

print(f"\nEquity value: ${equity_value:,.1f} million")
print(f"Share of value after 2030: {terminal_share:.1%}")
print(f"Value per share: ${value_per_share:.2f}")