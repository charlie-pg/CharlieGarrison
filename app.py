import io
import streamlit as st

from portfolio import (
    ASSETS,
    CORRELATIONS,
    find_lowest_risk,
    estimate_from_csv,
)

st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
st.title("Lab 15 — Portfolio Stability Decision")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

st.sidebar.header("Mandate")
objective_pct = st.sidebar.number_input(
    "Minimum expected return (%)", value=6.5, step=0.1
)
reserve_pct = st.sidebar.number_input(
    "Minimum reserve-eligible weight (%)", value=3.0, min_value=0.0, max_value=100.0
)
uploaded = st.sidebar.file_uploader("Upload prices.csv", type="csv")
last_36 = st.sidebar.toggle("Use only last 36 monthly returns", value=False)

if uploaded is None:
    base_assets = list(ASSETS)
    base_corr = [row[:] for row in CORRELATIONS]
    assets = list(base_assets)
    correlations = [row[:] for row in base_corr]
    st.info("Using Meridian training inputs from Lab 14.")
else:
    try:
        base_assets, base_corr = estimate_from_csv(
            io.StringIO(uploaded.getvalue().decode("utf-8-sig")),
            last_36=False,
        )
        assets, correlations = estimate_from_csv(
            io.StringIO(uploaded.getvalue().decode("utf-8-sig")),
            last_36=last_36,
        )
        st.info("Using historical price estimates from the uploaded CSV.")
    except Exception as error:
        st.error(f"Could not read prices.csv: {error}")
        st.stop()

st.subheader("Asset return estimates and reserve eligibility")
edited_assets = []
reserve_flags = []

for i, (name, ret, vol) in enumerate(assets):
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.write(name)
    with col2:
        edited_return = st.number_input(
            f"{name} estimated return (%)",
            value=float(round(ret * 100, 4)),
            step=0.1,
            key=f"return_{i}",
        )
    with col3:
        eligible = st.checkbox(
            f"Reserve eligible: {name}",
            value=(uploaded is None and i < 2),
            key=f"reserve_{i}",
        )
    edited_assets.append((name, edited_return / 100, vol))
    reserve_flags.append(eligible)

def display_result(result, asset_names):
    if result is None:
        st.warning("No mix meets the objective.")
        return

    st.metric("Expected return", f"{result['return'] * 100:.2f}%")
    st.metric("Volatility", f"{result['volatility'] * 100:.2f}%")
    st.metric("Reserve eligible", f"{result['reserve'] * 100:.2f}%")

    for name, weight in zip(asset_names, result["weights"]):
        st.write(f"**{name}:** {weight * 100:.0f}%")

try:
    current = find_lowest_risk(
        edited_assets,
        correlations,
        objective_pct / 100,
        reserve_pct / 100,
        reserve_flags,
    )

    baseline_flags = [
        i < 2 for i in range(len(base_assets))
    ] if uploaded is None else reserve_flags

    baseline = find_lowest_risk(
        base_assets,
        base_corr,
        objective_pct / 100,
        reserve_pct / 100,
        baseline_flags,
    )
except Exception as error:
    st.error(f"Portfolio calculation error: {error}")
    st.stop()

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Current inputs")
    display_result(current, [asset[0] for asset in edited_assets])

with right:
    st.subheader("As-loaded baseline")
    display_result(baseline, [asset[0] for asset in base_assets])

if current is not None and baseline is not None:
    largest_change = max(
        abs(a - b) * 100
        for a, b in zip(current["weights"], baseline["weights"])
    )
    st.metric("Largest weight change", f"{largest_change:.0f} percentage points")
else:
    st.write("Largest weight change: unavailable because one mix is infeasible.")