import streamlit as st

st.set_page_config(page_title="LLY Valuation Workbench", layout="wide")

st.title("Eli Lilly (LLY) — Valuation Workbench")
st.caption("FIN 43900 | Project 1 | Preliminary model")

st.sidebar.header("Model Assumptions")

wacc = st.sidebar.slider(
    "WACC",
    min_value=5.9,
    max_value=7.9,
    value=6.9,
    step=0.1,
    format="%.1f%%"
)

terminal_growth = st.sidebar.slider(
    "Terminal Growth",
    min_value=1.5,
    max_value=3.5,
    value=2.5,
    step=0.1,
    format="%.1f%%"
)
growth_adjustment = st.sidebar.slider(
    "Revenue Growth Adjustment (percentage points)",
    min_value=-5.0,
    max_value=5.0,
    value=0.0,
    step=0.5,
    format="%+.1f pp"
)
st.sidebar.write(f"Selected WACC: {wacc:.1f}%")
st.sidebar.write(f"Selected Terminal Growth: {terminal_growth:.1f}%")

# Import the forecast and valuation inputs from the existing model
import contextlib
import importlib
import io
import os

# Pass the selected growth adjustment to the financial model.
os.environ["LLY_GROWTH_ADJUSTMENT"] = str(growth_adjustment / 100)

# Rerun the existing model when a slider changes.
with contextlib.redirect_stdout(io.StringIO()):
    import lly_three_statement
    model = importlib.reload(lly_three_statement)

forecast = model.forecast
FORECAST_YEARS = model.FORECAST_YEARS
valuation_debt = model.valuation_debt
valuation_cash = model.valuation_cash
shares_outstanding = model.shares_outstanding

# Recalculate DCF using the selected sliders
selected_wacc = wacc / 100
selected_growth = terminal_growth / 100

pv_fcff = sum(
    forecast[year]["fcff"] / (1 + selected_wacc) ** period
    for period, year in enumerate(FORECAST_YEARS, start=1)
)

terminal_value = (
    forecast[2030]["fcff"] * (1 + selected_growth)
    / (selected_wacc - selected_growth)
)

pv_terminal = terminal_value / (1 + selected_wacc) ** 5
enterprise_value = pv_fcff + pv_terminal
equity_value = enterprise_value - valuation_debt + valuation_cash
share_price = equity_value / shares_outstanding

st.subheader("DCF Valuation Results")

col1, col2, col3 = st.columns(3)

col1.metric("Implied Share Price", f"${share_price:,.2f}")
col2.metric("Enterprise Value", f"${enterprise_value:,.0f}M")
col3.metric("Equity Value", f"${equity_value:,.0f}M")

st.caption(
    "Preliminary valuation linked to the five-year financial forecast. "
    "Adjust revenue growth, WACC, and terminal growth using the sidebar controls."
)

st.divider()
st.subheader("Five-Year Financial Forecast (2026–2030)")
st.caption("USD millions. Forecast updates when revenue growth changes.")

rows = []

for year in FORECAST_YEARS:
    f = forecast[year]
    rows.append({
        "Year": year,
        "Revenue ($M)": f.get("revenue"),
        "Gross Profit ($M)": f.get("gross_profit"),
        "EBIT ($M)": f.get("operating_profit"),
        "Net Income ($M)": f.get("net_income"),
        "FCFF ($M)": f.get("fcff"),
    })

st.dataframe(rows, hide_index=True, use_container_width=True)

st.divider()
st.subheader("Model Checks")
check_rows = []

for year in FORECAST_YEARS:
    difference = forecast[year]["balance_difference"]
    passed = abs(difference) < 0.01

    check_rows.append({
        "Year": year,
        "Balance Difference ($M)": round(difference, 4),
        "Status": "PASS" if passed else "FAIL",
    })

st.dataframe(check_rows, hide_index=True, use_container_width=True)

if all(row["Status"] == "PASS" for row in check_rows):
    st.success("PASS: All five forecast balance sheets reconcile.")
else:
    st.error("FAIL: One or more forecast balance sheets do not reconcile.")