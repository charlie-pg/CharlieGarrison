# Lab 11 - Eli Lilly Pro-Forma Sensitivity Analysis
# Company: Eli Lilly and Company (LLY)

YEARS = [2026, 2027, 2028, 2029, 2030]

# --------------------------------------------------
# BASE INPUTS
# --------------------------------------------------

BASE_REVENUE_2025 = 65179.0  # $ millions
BASE_GROWTH = [0.32, 0.20, 0.15, 0.12, 0.10]

BASE_GROSS_MARGIN = 0.830
SGA_TO_GROSS_PROFIT = 0.205

# 2025 R&D = $13,337m / $65,179m revenue
RD_TO_REVENUE = 13337.0 / 65179.0

TAX_RATE = 0.198

# Sensitivity ranges
GROWTH_SHIFT_LOW = -0.05   # -5 percentage points
GROWTH_SHIFT_HIGH = 0.05   # +5 percentage points

MARGIN_LOW = 0.810
MARGIN_BASE = 0.830
MARGIN_HIGH = 0.850


def run_model(growth_path, gross_margin):
    """
    Simplified Lilly operating pro-forma.
    FCFE is not calculated because the complete Lilly balance-sheet
    model was unresolved from Lab 10. No valuation is invented.
    """

    revenue = BASE_REVENUE_2025
    rows = []

    for year, growth in zip(YEARS, growth_path):

        revenue = revenue * (1 + growth)

        gross_profit = revenue * gross_margin
        sga = gross_profit * SGA_TO_GROSS_PROFIT
        rd = revenue * RD_TO_REVENUE

        operating_profit = gross_profit - sga - rd

        tax = max(0.0, operating_profit) * TAX_RATE
        after_tax_operating_profit = operating_profit - tax

        rows.append({
            "year": year,
            "revenue": revenue,
            "operating_profit": operating_profit,
            "after_tax_operating_profit": after_tax_operating_profit,
        })

    return rows


def final_outputs(rows):
    last = rows[-1]

    return {
        "operating_profit": last["operating_profit"],
        # Full FCFE unavailable because complete linked balance sheet
        # and financing schedule were unresolved.
        "fcfe": None,
        "value_per_share": None,
    }


def print_result(name, input_value, rows, base_outputs=None):
    outputs = final_outputs(rows)

    print(f"\n{name}")
    print(f"Input: {input_value}")
    print(f"2030 Operating profit: ${outputs['operating_profit']:,.1f}m")

    if outputs["fcfe"] is None:
        print("2030 FCFE: unavailable - complete linked balance sheet unresolved")

    if outputs["value_per_share"] is None:
        print("Value/share: unavailable - defensible FCFE valuation unresolved")

    if base_outputs is not None:
        change = outputs["operating_profit"] - base_outputs["operating_profit"]
        print(f"Change in operating profit vs base: ${change:+,.1f}m")

    return outputs


# --------------------------------------------------
# BASE CASE BEFORE SENSITIVITY
# --------------------------------------------------

print("ELI LILLY PRO-FORMA SENSITIVITY")
print("=" * 55)

base_rows_before = run_model(BASE_GROWTH.copy(), BASE_GROSS_MARGIN)
base_before = final_outputs(base_rows_before)

print("\nBASE CASE BEFORE SENSITIVITY")
print(f"2030 Revenue: ${base_rows_before[-1]['revenue']:,.1f}m")
print(f"2030 Operating profit: ${base_before['operating_profit']:,.1f}m")


# --------------------------------------------------
# DRIVER 1: REVENUE GROWTH
# One-at-a-time: gross margin remains at base
# --------------------------------------------------

print("\n" + "=" * 55)
print("DRIVER 1: REVENUE GROWTH")
print("Low/Base/High = -5pp / base / +5pp in every forecast year")

growth_low = [g + GROWTH_SHIFT_LOW for g in BASE_GROWTH]
growth_base = BASE_GROWTH.copy()
growth_high = [g + GROWTH_SHIFT_HIGH for g in BASE_GROWTH]

growth_results = {}

for label, path in [
    ("LOW", growth_low),
    ("BASE", growth_base),
    ("HIGH", growth_high),
]:
    rows = run_model(path.copy(), BASE_GROSS_MARGIN)
    growth_results[label] = print_result(
        f"Revenue Growth - {label}",
        [f"{g:.1%}" for g in path],
        rows,
        base_before,
    )


growth_values = [
    x["operating_profit"] for x in growth_results.values()
]

growth_span = max(growth_values) - min(growth_values)

print(
    f"\nRevenue-growth operating-profit span: "
    f"${growth_span:,.1f}m"
)


# --------------------------------------------------
# DRIVER 2: GROSS MARGIN
# One-at-a-time: growth remains at base
# --------------------------------------------------

print("\n" + "=" * 55)
print("DRIVER 2: GROSS MARGIN")
print("Low/Base/High = 81.0% / 83.0% / 85.0%")

margin_results = {}

for label, margin in [
    ("LOW", MARGIN_LOW),
    ("BASE", MARGIN_BASE),
    ("HIGH", MARGIN_HIGH),
]:
    rows = run_model(BASE_GROWTH.copy(), margin)
    margin_results[label] = print_result(
        f"Gross Margin - {label}",
        f"{margin:.1%}",
        rows,
        base_before,
    )


margin_values = [
    x["operating_profit"] for x in margin_results.values()
]

margin_span = max(margin_values) - min(margin_values)

print(
    f"\nGross-margin operating-profit span: "
    f"${margin_span:,.1f}m"
)


# --------------------------------------------------
# RESTORE BASE
# --------------------------------------------------

print("\n" + "=" * 55)
print("RESTORED BASE CHECK")

base_rows_after = run_model(BASE_GROWTH.copy(), BASE_GROSS_MARGIN)
base_after = final_outputs(base_rows_after)

difference = (
    base_after["operating_profit"]
    - base_before["operating_profit"]
)

print(
    f"Base before: ${base_before['operating_profit']:,.1f}m"
)

print(
    f"Base after:  ${base_after['operating_profit']:,.1f}m"
)

print(f"Difference:  ${difference:,.1f}m")

if abs(difference) < 0.01:
    print("RESTORED BASE CHECK: PASS")
else:
    print("RESTORED BASE CHECK: FAIL")


# --------------------------------------------------
# DRIVER COMPARISON
# --------------------------------------------------

print("\n" + "=" * 55)
print("DRIVER COMPARISON - OVER THESE RANGES")

print(
    f"Revenue growth operating-profit span: "
    f"${growth_span:,.1f}m"
)

print(
    f"Gross margin operating-profit span: "
    f"${margin_span:,.1f}m"
)

if growth_span > margin_span:
    print("Larger operating-profit driver over these ranges: Revenue growth")
else:
    print("Larger operating-profit driver over these ranges: Gross margin")

print(
    "\nNOTE: FCFE and value/share are unavailable because the complete "
    "Lilly balance-sheet and financing model from Lab 10 was unresolved. "
    "No terminal value or cash flow was invented."
)