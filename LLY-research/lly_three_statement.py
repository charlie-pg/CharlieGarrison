# FIN 43900 - Project 1
# Eli Lilly (LLY) Three-Statement Financial Model
# All financial figures in USD millions unless noted.
# Source: Eli Lilly FY2025 Form 10-K

BASE_YEAR = 2025
FORECAST_YEARS = [2026, 2027, 2028, 2029, 2030]

historical_2025 = {
    "revenue": 65179.0,
    "gross_profit": 54127.0,
    "sga": 11094.0,
    "rd": 13337.0,
    "net_income": 20640.0,
    "cash": 7268.0,
    "inventory": 13744.0,
    "ppe_net": 24675.0,
    "current_debt": 1635.0,
    "long_term_debt": 40868.0,
    "equity": 26535.0,
    "capex": 7841.0,
}

print("Eli Lilly 2025 historical data loaded.")
print(f"2025 Revenue: ${historical_2025['revenue']:,.0f} million")

# ------------------------------------------
# 2026-2030 Operating Forecast
# ------------------------------------------

# Assumptions from LLY_ProForma_Assumptions.md
import os

base_revenue_growth = [0.32, 0.20, 0.15, 0.12, 0.10]

growth_adjustment = float(
    os.environ.get("LLY_GROWTH_ADJUSTMENT", "0")
)

assert -0.05 <= growth_adjustment <= 0.05, (
    "Revenue growth adjustment must be between -5 and +5 percentage points"
)

revenue_growth = [
    growth + growth_adjustment
    for growth in base_revenue_growth
]
gross_margin = 0.83
sga_to_gross_profit = 0.205
rd_to_revenue = historical_2025["rd"] / historical_2025["revenue"]

forecast = {}
previous_revenue = historical_2025["revenue"]

for year, growth in zip(FORECAST_YEARS, revenue_growth):
    revenue = previous_revenue * (1 + growth)
    gross_profit = revenue * gross_margin
    cost_of_sales = revenue - gross_profit
    sga = gross_profit * sga_to_gross_profit
    rd = revenue * rd_to_revenue
    operating_profit = gross_profit - sga - rd

    forecast[year] = {
        "revenue": revenue,
        "cost_of_sales": cost_of_sales,
        "gross_profit": gross_profit,
        "sga": sga,
        "rd": rd,
        "operating_profit": operating_profit,
    }

    previous_revenue = revenue

print("\nELI LILLY OPERATING FORECAST ($ millions)")
print(f"{'Year':<8}{'Revenue':>15}{'Operating Profit':>20}")

for year, data in forecast.items():
    print(
        f"{year:<8}"
        f"{data['revenue']:>15,.1f}"
        f"{data['operating_profit']:>20,.1f}"
    )


# ------------------------------------------
# 2025 Historical Balance Sheet
# Source: Lilly FY2025 Form 10-K, page 59
# USD millions
# ------------------------------------------

balance_sheet_2025 = {
    # Current assets
    "cash": 7268.0,
    "accounts_receivable": 17760.0,
    "other_receivables": 2395.0,
    "inventory": 13744.0,
    "prepaid_expenses": 14315.0,
    "other_current_assets": 147.0,

    # Noncurrent assets
    "investments": 2802.0,
    "goodwill": 5898.0,
    "intangibles": 6521.0,
    "deferred_tax_assets": 9959.0,
    "ppe_net": 24675.0,
    "other_noncurrent_assets": 6992.0,

    # Current liabilities
    "current_debt": 1635.0,
    "accounts_payable": 5379.0,
    "employee_compensation": 2375.0,
    "sales_rebates": 17382.0,
    "other_current_liabilities": 8457.0,

    # Noncurrent liabilities
    "long_term_debt": 40868.0,
    "long_term_taxes": 5875.0,
    "other_noncurrent_liabilities": 3970.0,

    # Equity
    "total_equity": 26535.0,
}

total_assets = 112476.0
total_liabilities = 85941.0
total_equity = balance_sheet_2025["total_equity"]

balance_check = total_assets - total_liabilities - total_equity

print("\n2025 BALANCE SHEET CHECK")
print(f"Total assets: ${total_assets:,.0f} million")
print(f"Total liabilities: ${total_liabilities:,.0f} million")
print(f"Total equity: ${total_equity:,.0f} million")
print(f"Balance difference: ${balance_check:,.0f} million")

assert abs(balance_check) < 0.01, "Balance sheet does not balance!"

asset_keys = [
    "cash", "accounts_receivable", "other_receivables",
    "inventory", "prepaid_expenses", "other_current_assets",
    "investments", "goodwill", "intangibles",
    "deferred_tax_assets", "ppe_net", "other_noncurrent_assets"
]

liability_keys = [
    "current_debt", "accounts_payable", "employee_compensation",
    "sales_rebates", "other_current_liabilities",
    "long_term_debt", "long_term_taxes",
    "other_noncurrent_liabilities"
]

calculated_assets = sum(balance_sheet_2025[k] for k in asset_keys)
calculated_liabilities = sum(balance_sheet_2025[k] for k in liability_keys)

print("\nDETAILED 2025 BALANCE SHEET CHECK")
print(f"Calculated assets: ${calculated_assets:,.0f} million")
print(f"Calculated liabilities: ${calculated_liabilities:,.0f} million")
print(f"Assets discrepancy: ${calculated_assets - total_assets:,.0f} million")
print(f"Liabilities discrepancy: ${calculated_liabilities - total_liabilities:,.0f} million")
assert abs(calculated_assets - total_assets) < 0.01, "Historical asset detail does not reconcile"
assert abs(calculated_liabilities - total_liabilities) < 0.01, "Historical liability detail does not reconcile"
# ------------------------------------------
# 2026-2030 Balance Sheet Forecast
# Part 1: Inventory
# ------------------------------------------

# Inventory days from Lilly's 2025 historical ratio
inventory_days = 454.0

for year in FORECAST_YEARS:
    cost_of_sales = forecast[year]["cost_of_sales"]

    # Inventory = annual cost of sales × inventory days / 365
    forecast[year]["inventory"] = (
        cost_of_sales * inventory_days / 365
    )

print("\nELI LILLY INVENTORY FORECAST ($ millions)")
print(f"{'Year':<8}{'Inventory':>15}")

for year in FORECAST_YEARS:
    print(f"{year:<8}{forecast[year]['inventory']:>15,.1f}")

# ------------------------------------------
# 2026-2030 Accounts Receivable Forecast
# ------------------------------------------

receivables_to_revenue = (
    balance_sheet_2025["accounts_receivable"]
    / historical_2025["revenue"]
)

for year in FORECAST_YEARS:
    forecast[year]["accounts_receivable"] = (
        forecast[year]["revenue"] * receivables_to_revenue
    )

print("\nELI LILLY ACCOUNTS RECEIVABLE FORECAST ($ millions)")
print(f"{'Year':<8}{'Receivables':>15}")

for year in FORECAST_YEARS:
    print(f"{year:<8}{forecast[year]['accounts_receivable']:>15,.1f}")

# ------------------------------------------
# 2026-2030 PP&E and Depreciation Forecast
# ------------------------------------------

# Starting assumptions from Lab 10
capex_to_revenue = (
    historical_2025["capex"] / historical_2025["revenue"]
)
depreciation_rate = 0.081

previous_ppe = balance_sheet_2025["ppe_net"]

for year in FORECAST_YEARS:
    revenue = forecast[year]["revenue"]

    # Capital spending grows with revenue
    capex = revenue * capex_to_revenue

    # Depreciation based on beginning PP&E
    depreciation = previous_ppe * depreciation_rate

    # Ending PP&E roll-forward
    ending_ppe = previous_ppe + capex - depreciation

    forecast[year]["capex"] = capex
    forecast[year]["depreciation"] = depreciation
    forecast[year]["ppe_net"] = ending_ppe

    previous_ppe = ending_ppe

print("\nELI LILLY PP&E FORECAST ($ millions)")
print(f"{'Year':<8}{'Capex':>15}{'Depreciation':>18}{'Ending PP&E':>18}")

for year in FORECAST_YEARS:
    data = forecast[year]
    print(
        f"{year:<8}"
        f"{data['capex']:>15,.1f}"
        f"{data['depreciation']:>18,.1f}"
        f"{data['ppe_net']:>18,.1f}"
    )

# ------------------------------------------
# 2026-2030 Accounts Payable Forecast
# ------------------------------------------

cost_of_sales_2025 = (
    historical_2025["revenue"] - historical_2025["gross_profit"]
)

payables_to_cost_of_sales = (
    balance_sheet_2025["accounts_payable"] / cost_of_sales_2025
)

for year in FORECAST_YEARS:
    forecast[year]["accounts_payable"] = (
        forecast[year]["cost_of_sales"] * payables_to_cost_of_sales
    )

print("\nELI LILLY ACCOUNTS PAYABLE FORECAST ($ millions)")
print(f"{'Year':<8}{'Accounts Payable':>20}")

for year in FORECAST_YEARS:
    print(f"{year:<8}{forecast[year]['accounts_payable']:>20,.1f}")

# ------------------------------------------
# Remaining Operating Balance Sheet Accounts
# ------------------------------------------

# Forecast operating accounts as a percentage
# of revenue, based on 2025 historical values.
operating_accounts = [
    "other_receivables",
    "prepaid_expenses",
    "other_current_assets",
    "employee_compensation",
    "sales_rebates",
    "other_current_liabilities",
]

for year in FORECAST_YEARS:
    revenue_ratio = (
        forecast[year]["revenue"] / historical_2025["revenue"]
    )

    for account in operating_accounts:
        forecast[year][account] = (
            balance_sheet_2025[account] * revenue_ratio
        )

print("\nREMAINING OPERATING BALANCE SHEET FORECAST ($ millions)")
print(f"{'Year':<8}{'Other Receivables':>20}{'Sales Rebates':>18}")

for year in FORECAST_YEARS:
    print(
        f"{year:<8}"
        f"{forecast[year]['other_receivables']:>20,.1f}"
        f"{forecast[year]['sales_rebates']:>18,.1f}"
    )

# ------------------------------------------
# Noncurrent Assets and Financing Assumptions
# ------------------------------------------

fixed_accounts = [
    "investments",
    "goodwill",
    "intangibles",
    "deferred_tax_assets",
    "other_noncurrent_assets",
    "current_debt",
    "long_term_debt",
    "long_term_taxes",
    "other_noncurrent_liabilities",
]

for year in FORECAST_YEARS:
    for account in fixed_accounts:
        forecast[year][account] = balance_sheet_2025[account]

print("\nNONCURRENT AND FINANCING ASSUMPTIONS ($ millions)")
print(f"{'Year':<8}{'Total Debt':>18}")

for year in FORECAST_YEARS:
    total_debt = (
        forecast[year]["current_debt"]
        + forecast[year]["long_term_debt"]
    )
    print(f"{year:<8}{total_debt:>18,.1f}")

# ------------------------------------------
# 2026-2030 Net Income Forecast
# ------------------------------------------

# Preliminary financing assumption:
# 5% interest expense on outstanding debt.
# This rate must be validated against Lilly's filings.
interest_rate = 0.05
tax_rate = 0.198

for year in FORECAST_YEARS:
    data = forecast[year]

    total_debt = data["current_debt"] + data["long_term_debt"]
    interest_expense = total_debt * interest_rate

    pretax_income = data["operating_profit"] - interest_expense
    income_tax = max(pretax_income, 0) * tax_rate
    net_income = pretax_income - income_tax

    data["interest_expense"] = interest_expense
    data["pretax_income"] = pretax_income
    data["income_tax"] = income_tax
    data["net_income"] = net_income

print("\nELI LILLY NET INCOME FORECAST ($ millions)")
print(f"{'Year':<8}{'Interest':>15}{'Net Income':>18}")

for year in FORECAST_YEARS:
    data = forecast[year]
    print(
        f"{year:<8}"
        f"{data['interest_expense']:>15,.1f}"
        f"{data['net_income']:>18,.1f}"
    )

# ------------------------------------------
# 2026-2030 Cash Flow Forecast
# ------------------------------------------

previous_inventory = balance_sheet_2025["inventory"]
previous_receivables = balance_sheet_2025["accounts_receivable"]
previous_payables = balance_sheet_2025["accounts_payable"]

for year in FORECAST_YEARS:
    data = forecast[year]

    change_inventory = data["inventory"] - previous_inventory
    change_receivables = data["accounts_receivable"] - previous_receivables
    change_payables = data["accounts_payable"] - previous_payables

    operating_cash_flow = (
        data["net_income"]
        + data["depreciation"]
        - change_inventory
        - change_receivables
        + change_payables
    )

    investing_cash_flow = -data["capex"]
    free_cash_flow = operating_cash_flow + investing_cash_flow

    data["operating_cash_flow"] = operating_cash_flow
    data["investing_cash_flow"] = investing_cash_flow
    data["free_cash_flow"] = free_cash_flow

    previous_inventory = data["inventory"]
    previous_receivables = data["accounts_receivable"]
    previous_payables = data["accounts_payable"]

print("\nELI LILLY PRELIMINARY CASH FLOW FORECAST ($ millions)")
print(f"{'Year':<8}{'Operating CF':>18}{'Free CF':>18}")

for year in FORECAST_YEARS:
    data = forecast[year]
    print(
        f"{year:<8}"
        f"{data['operating_cash_flow']:>18,.1f}"
        f"{data['free_cash_flow']:>18,.1f}"
    )

# ------------------------------------------
# Expanded Operating Working Capital Changes
# ------------------------------------------

working_capital_assets = [
    "accounts_receivable",
    "other_receivables",
    "inventory",
    "prepaid_expenses",
    "other_current_assets",
]

working_capital_liabilities = [
    "accounts_payable",
    "employee_compensation",
    "sales_rebates",
    "other_current_liabilities",
]

previous_balance = balance_sheet_2025.copy()

for year in FORECAST_YEARS:
    data = forecast[year]

    change_assets = sum(
        data[account] - previous_balance[account]
        for account in working_capital_assets
    )

    change_liabilities = sum(
        data[account] - previous_balance[account]
        for account in working_capital_liabilities
    )

    data["change_nwc"] = change_assets - change_liabilities

    previous_balance = data

print("\nELI LILLY CHANGE IN NET WORKING CAPITAL ($ millions)")
for year in FORECAST_YEARS:
    print(f"{year}: ${forecast[year]['change_nwc']:,.1f} million")

# ------------------------------------------
# Step 22: Updated Cash Flow Forecast
# ------------------------------------------

for year in FORECAST_YEARS:
    data = forecast[year]

    data["operating_cash_flow"] = (
        data["net_income"]
        + data["depreciation"]
        - data["change_nwc"]
    )

    data["investing_cash_flow"] = -data["capex"]

    data["free_cash_flow"] = (
        data["operating_cash_flow"]
        + data["investing_cash_flow"]
    )

print("\nUPDATED CASH FLOW FORECAST ($ millions)")
print(f"{'Year':<8}{'Operating CF':>18}{'Free CF':>18}")

for year in FORECAST_YEARS:
    data = forecast[year]
    print(
        f"{year:<8}"
        f"{data['operating_cash_flow']:>18,.1f}"
        f"{data['free_cash_flow']:>18,.1f}"
    )

# ------------------------------------------
# Step 23: Cash and Equity Roll-Forward
# ------------------------------------------

previous_cash = balance_sheet_2025["cash"]
previous_equity = balance_sheet_2025["total_equity"]

# Temporary assumption: no dividends, buybacks,
# new debt, or equity issuance.
# Must be revised to reflect Lilly's capital policy.
dividend_payout_ratio = 0.0

for year in FORECAST_YEARS:
    data = forecast[year]

    dividends = data["net_income"] * dividend_payout_ratio

    ending_cash = (
        previous_cash
        + data["operating_cash_flow"]
        + data["investing_cash_flow"]
        - dividends
    )

    ending_equity = (
        previous_equity
        + data["net_income"]
        - dividends
    )

    data["dividends"] = dividends
    data["cash"] = ending_cash
    data["total_equity"] = ending_equity

    previous_cash = ending_cash
    previous_equity = ending_equity

print("\nCASH AND EQUITY ROLL-FORWARD ($ millions)")
print(f"{'Year':<8}{'Ending Cash':>18}{'Ending Equity':>18}")

for year in FORECAST_YEARS:
    data = forecast[year]
    print(
        f"{year:<8}"
        f"{data['cash']:>18,.1f}"
        f"{data['total_equity']:>18,.1f}"
    )

# ------------------------------------------
# Step 24: Forecast Balance Sheet Check
# ------------------------------------------

print("\nFORECAST BALANCE SHEET CHECK ($ millions)")

for year in FORECAST_YEARS:
    data = forecast[year]

    assets = sum(data[account] for account in asset_keys)
    liabilities = sum(data[account] for account in liability_keys)
    equity = data["total_equity"]

    difference = assets - liabilities - equity

    data["total_assets"] = assets
    data["total_liabilities"] = liabilities
    data["balance_difference"] = difference

    print(
        f"{year}: Assets ${assets:,.1f}M | "
        f"Liabilities ${liabilities:,.1f}M | "
        f"Equity ${equity:,.1f}M | "
        f"Difference ${difference:,.1f}M"
    )

# ------------------------------------------
# Step 24: Forecast Balance Sheet Check
# ------------------------------------------

print("\nFORECAST BALANCE SHEET CHECK ($ millions)")

for year in FORECAST_YEARS:
    data = forecast[year]

    assets = sum(data[account] for account in asset_keys)
    liabilities = sum(data[account] for account in liability_keys)
    equity = data["total_equity"]

    difference = assets - liabilities - equity

    data["total_assets"] = assets
    data["total_liabilities"] = liabilities
    data["balance_difference"] = difference

    print(
        f"{year}: Assets ${assets:,.1f}M | "
        f"Liabilities ${liabilities:,.1f}M | "
        f"Equity ${equity:,.1f}M | "
        f"Difference ${difference:,.1f}M"
    )

# Step 25: Automatic Balance Sheet Validation
for year in FORECAST_YEARS:
    difference = forecast[year]["balance_difference"]

    assert abs(difference) < 0.01, (
        f"{year} balance sheet does not balance!"
    )

print("\nPASS: All five forecast balance sheets balance.")

# ------------------------------------------
# Step 26: Free Cash Flow to the Firm (FCFF)
# ------------------------------------------

print("\nFREE CASH FLOW TO THE FIRM ($ millions)")

for year in FORECAST_YEARS:
    data = forecast[year]

    fcff = (
        data["operating_profit"] * (1 - tax_rate)
        + data["depreciation"]
        - data["capex"]
        - data["change_nwc"]
    )

    data["fcff"] = fcff

    print(f"{year}: ${fcff:,.1f} million")

# ------------------------------------------
# Step 27: Discount Forecast FCFF
# ------------------------------------------

wacc = 0.069

print("\nDISCOUNTED FREE CASH FLOWS ($ millions)")

pv_forecast_fcff = 0.0

for period, year in enumerate(FORECAST_YEARS, start=1):
    fcff = forecast[year]["fcff"]

    discount_factor = 1 / (1 + wacc) ** period
    present_value = fcff * discount_factor

    forecast[year]["pv_fcff"] = present_value
    pv_forecast_fcff += present_value

    print(f"{year}: ${present_value:,.1f} million")

print(f"\nTotal PV of forecast FCFF: ${pv_forecast_fcff:,.1f} million")

# ------------------------------------------
# Step 28: Terminal Value
# ------------------------------------------

terminal_growth = 0.025

final_year_fcff = forecast[2030]["fcff"]

terminal_value = (
    final_year_fcff * (1 + terminal_growth)
    / (wacc - terminal_growth)
)

pv_terminal_value = terminal_value / (1 + wacc) ** 5

enterprise_value = pv_forecast_fcff + pv_terminal_value

print("\nDCF TERMINAL VALUE ($ millions)")
print(f"2030 FCFF: ${final_year_fcff:,.1f} million")
print(f"Terminal Value: ${terminal_value:,.1f} million")
print(f"PV of Terminal Value: ${pv_terminal_value:,.1f} million")
print(f"Enterprise Value: ${enterprise_value:,.1f} million")

# ------------------------------------------
# Step 29: Enterprise Value to Equity Value
# ------------------------------------------

valuation_cash = balance_sheet_2025["cash"]

valuation_debt = (
    balance_sheet_2025["current_debt"]
    + balance_sheet_2025["long_term_debt"]
)

equity_value = (
    enterprise_value
    - valuation_debt
    + valuation_cash
)

print("\nDCF EQUITY VALUATION ($ millions)")
print(f"Enterprise Value: ${enterprise_value:,.1f}M")
print(f"Less Debt: ${valuation_debt:,.1f}M")
print(f"Add Cash: ${valuation_cash:,.1f}M")
print(f"Equity Value: ${equity_value:,.1f}M")

# ------------------------------------------
# Step 30: Implied Value Per Share
# ------------------------------------------

shares_outstanding = 893.7  # Millions; verify source/date

implied_share_price = equity_value / shares_outstanding

print("\nDCF IMPLIED SHARE PRICE")
print(f"Shares Outstanding: {shares_outstanding:,.1f} million")
print(f"Implied Share Price: ${implied_share_price:,.2f}")

# ------------------------------------------
# Step 31: WACC and Terminal Growth Sensitivity
# ------------------------------------------

wacc_values = [0.059, 0.064, 0.069, 0.074, 0.079]
growth_values = [0.015, 0.020, 0.025, 0.030, 0.035]

print("\nDCF SENSITIVITY: IMPLIED SHARE PRICE ($)")
print(f"{'WACC / g':<12}", end="")

for g in growth_values:
    print(f"{g:.1%}".rjust(12), end="")
print()

for test_wacc in wacc_values:
    print(f"{test_wacc:.1%}".ljust(12), end="")

    for g in growth_values:
        pv_cash_flows = sum(
            forecast[year]["fcff"] / (1 + test_wacc) ** period
            for period, year in enumerate(FORECAST_YEARS, start=1)
        )

        tv = forecast[2030]["fcff"] * (1 + g) / (test_wacc - g)
        pv_tv = tv / (1 + test_wacc) ** 5

        ev = pv_cash_flows + pv_tv
        eq = ev - valuation_debt + valuation_cash
        price = eq / shares_outstanding

        print(f"{price:>12,.2f}", end="")

    print()

# ------------------------------------------
# Step 32: Terminal Value Dependence
# ------------------------------------------

terminal_value_share = pv_terminal_value / enterprise_value

print("\nDCF TERMINAL VALUE DEPENDENCE")
print(f"Terminal Value Share: {terminal_value_share:.1%}")
print(f"Forecast Cash Flow Share: {1 - terminal_value_share:.1%}")

# ------------------------------------------
# Step 33: Low / Base / High DCF Scenarios
# ------------------------------------------

scenarios = {
    "Low":  {"wacc": 0.079, "growth": 0.015},
    "Base": {"wacc": 0.069, "growth": 0.025},
    "High": {"wacc": 0.059, "growth": 0.035},
}

print("\nLOW / BASE / HIGH DCF SCENARIOS")

for name, assumptions in scenarios.items():
    scenario_wacc = assumptions["wacc"]
    scenario_growth = assumptions["growth"]

    pv_fcff = sum(
        forecast[year]["fcff"] / (1 + scenario_wacc) ** period
        for period, year in enumerate(FORECAST_YEARS, start=1)
    )

    terminal_fcff = forecast[2030]["fcff"] * (1 + scenario_growth)

    scenario_tv = terminal_fcff / (
        scenario_wacc - scenario_growth
    )

    scenario_pv_tv = scenario_tv / (1 + scenario_wacc) ** 5

    scenario_ev = pv_fcff + scenario_pv_tv
    scenario_equity = scenario_ev - valuation_debt + valuation_cash
    scenario_price = scenario_equity / shares_outstanding

    print(
        f"{name}: ${scenario_price:,.2f} per share "
        f"(WACC {scenario_wacc:.1%}, growth {scenario_growth:.1%})"
    )

# ------------------------------------------
# Step 34: Reverse DCF - Required FCFF Scale
# ------------------------------------------

reference_price = 1124.21  # Historical reference; verify date/source

target_equity_value = reference_price * shares_outstanding
target_enterprise_value = (
    target_equity_value + valuation_debt - valuation_cash
)

required_fcff_multiplier = target_enterprise_value / enterprise_value
required_fcff_increase = required_fcff_multiplier - 1

print("\nREVERSE DCF: REQUIRED CASH FLOW SCALE")
print(f"Reference Share Price: ${reference_price:,.2f}")
print(f"Required FCFF Multiplier: {required_fcff_multiplier:.2f}x")
print(f"Required FCFF Increase: {required_fcff_increase:.1%}")