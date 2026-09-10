"""Simple five-year discounted cash flow valuation (USD millions)."""

# Inputs (edit these values)
starting_fcff = 9689.79
growth_rates = [0.18, 0.17, 0.15, 0.12, 0.10]
wacc = 0.069
terminal_growth = 0.025
non_operating_cash = 8950.0
debt = 54908.0
diluted_shares = 893.7


if terminal_growth >= wacc:
    raise SystemExit("Error: terminal growth must be less than WACC.")

fcffs = []
fcff = starting_fcff
for growth_rate in growth_rates:
    fcff *= 1.0 + growth_rate
    fcffs.append(fcff)

present_value_explicit_fcff = sum(
    yearly_fcff / (1.0 + wacc) ** year
    for year, yearly_fcff in enumerate(fcffs, start=1)
)
terminal_value_year_5 = (
    fcffs[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)
)
present_value_terminal_value = terminal_value_year_5 / (1.0 + wacc) ** len(fcffs)
enterprise_value = present_value_explicit_fcff + present_value_terminal_value
equity_value = enterprise_value + non_operating_cash - debt
value_per_diluted_share = equity_value / diluted_shares
terminal_value_share = present_value_terminal_value / enterprise_value

for year, yearly_fcff in enumerate(fcffs, start=1):
    print(f"FCFF Year {year}: {yearly_fcff:.4f}")
print(f"Present value of five explicit FCFF: {present_value_explicit_fcff:.4f}")
print(f"Terminal value at Year 5: {terminal_value_year_5:.4f}")
print(f"Present value of terminal value: {present_value_terminal_value:.4f}")
print(f"Enterprise value: {enterprise_value:.4f}")
print(f"Equity value: {equity_value:.4f}")
print(f"Value per diluted share: {value_per_diluted_share:.4f}")
print(f"Present value of terminal value as share of enterprise value: {terminal_value_share:.4%}")


# Sensitivity grid: value per diluted share
print("\nSensitivity grid: value per diluted share")
sensitivity_growth_rates = [0.020, 0.025, 0.030]
print("WACC / Terminal Growth    2.0%    2.5%    3.0%")
for sensitivity_wacc in [0.059, 0.069, 0.079]:
    values = []
    for sensitivity_growth in sensitivity_growth_rates:
        sensitivity_pv_fcff = sum(
            yearly_fcff / (1.0 + sensitivity_wacc) ** year
            for year, yearly_fcff in enumerate(fcffs, start=1)
        )
        sensitivity_terminal_value = (
            fcffs[-1]
            * (1.0 + sensitivity_growth)
            / (sensitivity_wacc - sensitivity_growth)
        )
        sensitivity_enterprise_value = sensitivity_pv_fcff + (
            sensitivity_terminal_value / (1.0 + sensitivity_wacc) ** len(fcffs)
        )
        sensitivity_equity_value = (
            sensitivity_enterprise_value + non_operating_cash - debt
        )
        values.append(sensitivity_equity_value / diluted_shares)
    print(f"{sensitivity_wacc:.1%}                   " + "  ".join(f"{value:6.2f}" for value in values))


# Reverse DCF: parallel shift to all five growth rates
target_price = 1124.21


def price_from_growth_shift(growth_shift):
    reverse_fcffs = []
    reverse_fcff = starting_fcff
    for growth_rate in growth_rates:
        reverse_fcff *= 1.0 + growth_rate + growth_shift
        reverse_fcffs.append(reverse_fcff)

    reverse_pv_fcff = sum(
        yearly_fcff / (1.0 + wacc) ** year
        for year, yearly_fcff in enumerate(reverse_fcffs, start=1)
    )
    reverse_terminal_value = (
        reverse_fcffs[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)
    )
    reverse_enterprise_value = reverse_pv_fcff + (
        reverse_terminal_value / (1.0 + wacc) ** len(reverse_fcffs)
    )
    return (reverse_enterprise_value + non_operating_cash - debt) / diluted_shares


low_shift = -0.50
high_shift = 0.50
for _ in range(100):
    midpoint_shift = (low_shift + high_shift) / 2.0
    if price_from_growth_shift(midpoint_shift) < target_price:
        low_shift = midpoint_shift
    else:
        high_shift = midpoint_shift

implied_growth_shift = (low_shift + high_shift) / 2.0
print("\nReverse DCF")
print(f"Target price: ${target_price:.2f}")
print(f"Implied parallel growth-rate shift: {implied_growth_shift:+.2%}")
print(
    "Implied Years 1-5 growth rates: "
    + ", ".join(f"{growth_rate + implied_growth_shift:.2%}" for growth_rate in growth_rates)
)
