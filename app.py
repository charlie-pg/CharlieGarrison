"""Project 2 Streamlit entry point, extended from the Lab 15 app."""
import json

import streamlit as st

from project2 import (
    AS_OF, NAMES, ROOT, RETURN_HURDLE, SIGNAL_MAX_AGE, VOLATILITY_LIMIT,
    allocation_stop, compare, load_prices,
    read_signal, stress_cases, validate_holdings,
)

st.set_page_config(page_title="Project 2 Portfolio Decision", layout="wide")
st.title("Retirement Portfolio Decision")
st.caption("Built with OpenAI Codex assistance. Educational analysis, not investment advice.")

with st.sidebar:
    st.header("Portfolio policy")
    st.subheader("Client requirements")
    st.markdown("- Long only, with no borrowing or short selling\n"
                "- **5% minimum explicit cash** (BIL excluded)\n"
                "- **10% maximum single-company exposure**")
    st.subheader("Strategic benchmark")
    st.write("60% VT / 40% BIL, rebalanced monthly.")
    st.subheader("Illustrative analyst assumptions")
    st.markdown(f"- **{VOLATILITY_LIMIT:.0%} annualized volatility limit** for the portfolio analysis\n"
                f"- **{RETURN_HURDLE:.1%} first-year net expected-return hurdle** for the constrained search")
    st.caption("Lab 13 supplies no numerical risk limit or return hurdle.")
    upload = st.file_uploader("Optional as-of issuer holdings JSON", type="json")
    st.caption("See README for the holdings schema and source requirements.")

try:
    text = load_prices((ROOT / "prices.csv").read_text())
    holdings = validate_holdings(json.loads(upload.getvalue()), AS_OF) if upload else {}
    portfolios, benchmark = compare(text, holdings)
except (OSError, ValueError, TypeError, AttributeError, KeyError) as error:
    st.error(f"Allocation stopped: invalid input. {error}")
    st.stop()

if holdings:
    st.subheader("Uploaded holdings sources")
    st.table([{"Fund": fund, "Holdings date": data["holdings_date"],
               "Available on": data["available_on"], "Source": data["source"]}
              for fund, data in holdings.items()])
else:
    st.info("No eligible issuer snapshots loaded. The Lab 19 VT example is partial and was accessed after the decision date.")
st.subheader("Portfolio comparison")
summary = []
for name, result in portfolios.items():
    summary.append({
        "Portfolio": name,
        "Mandate verdict": result["verdict"] if result else "FAIL",
        "Explicit cash": f"{result['weights'][-1]:.1%}" if result else "—",
        "Expected gross return": f"{result['gross']:.2%}" if result else "—",
        "Expected first-year net return": f"{result['net']:.2%}" if result else "—",
        "Annualized volatility": f"{result['vol']:.2%}" if result else "—",
    })
st.dataframe(summary, hide_index=True, width="stretch")
st.caption("Open a portfolio below for its allocation and the evidence behind each verdict.")
for name, result in portfolios.items():
    with st.expander(f"{name} · {result['verdict'] if result else 'FAIL'}"):
        if result is None:
            st.error("No candidate satisfies the search constraints.")
            continue
        st.write(" · ".join(f"{ticker} {weight:.1%}" for ticker, weight in zip(NAMES, result["weights"])))
        st.table([{"Rule": rule, "Status": status, "Evidence": reason}
                  for rule, (status, reason) in result["checks"].items()])
st.caption(f"Strategic benchmark · 60% VT / 40% BIL, rebalanced monthly · "
           f"Historical annualized gross return {benchmark['gross']:.2%} · "
           f"Annualized volatility {benchmark['vol']:.2%}")

st.subheader("Point-in-time Treasury signal")
signal_age = None
try:
    observed, yield_percent, signal_age = read_signal((ROOT / "data/dgs10-2026-09-30.csv").read_text(), AS_OF)
    st.metric(f"10-year Treasury yield known on {AS_OF}", f"{yield_percent:.2f}%")
    st.write(f"Latest published observation {observed}. Observation age {signal_age} calendar day(s).")
except (OSError, ValueError, TypeError, KeyError) as error:
    st.warning(f"Vintage unavailable: {error}")
with st.expander("DGS10 data card"):
    st.write("Board of Governors 10-year Treasury constant maturity yield, via FRED and ALFRED. "
             "Business daily, percent per year, not seasonally adjusted. The saved September 30 vintage "
             "defines what was available; current FRED values can include later observations or revisions. "
             "Monitor IEF duration risk. This yield does not forecast ETF returns or change weights.")
    st.write(f"Pilot freshness rule: no more than {SIGNAL_MAX_AGE} calendar days since the latest observation.")
    st.markdown("[FRED series](https://fred.stlouisfed.org/series/DGS10) · "
                "[Saved vintage source](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-09-30&cosd=2026-09-01&coed=2026-09-30)")

st.subheader("Stress testing")
cases = stress_cases(text, holdings)
reference, _ = cases["Reference"]
stress_summary = []
stress_details = []
benchmark_rows = []
for label, (result, yardstick) in cases.items():
    stop = allocation_stop(result, signal_age)
    largest_change = "—"
    if result is not None and reference is not None:
        change = max(abs(a - b) for a, b in zip(reference["weights"], result["weights"]))
        largest_change = f"{change * 100:.0f} pp"
    stress_summary.append({
        "Scenario": label,
        "Expected first-year net return": f"{result['net']:.2%}" if result else "—",
        "Annualized volatility": f"{result['vol']:.2%}" if result else "—",
        "Largest allocation change": largest_change,
        "Mandate verdict": result["verdict"] if result else "FAIL",
    })
    detail = {"Scenario": label}
    if result is not None:
        detail.update({name: f"{weight:.0%}" for name, weight in zip(NAMES, result["weights"])})
    detail["Decision gate"] = stop or "Scenario cleared"
    stress_details.append(detail)
    benchmark_rows.append({
        "Scenario": label,
        "Benchmark gross": f"{yardstick['gross']:.2%}",
        "Benchmark volatility": f"{yardstick['vol']:.2%}",
    })
st.dataframe(stress_summary, hide_index=True, width="stretch")
st.caption("Allocation changes are measured against the reference portfolio. Trading costs apply "
           "once to one-way turnover from an all-cash starting account.")
with st.expander("Scenario allocations and decision gates"):
    st.dataframe(stress_details, hide_index=True, width="stretch")
with st.expander("Strategic benchmark by scenario"):
    st.dataframe(benchmark_rows, hide_index=True, width="stretch")
    st.caption("Historical annualized statistics use each scenario’s window and monthly rebalancing, "
               "before hypothetical shocks or costs.")

st.info("PILOT ONLY · Paper account · 0% funded.")
if any(allocation_stop(result, signal_age) for result, _ in cases.values()):
    st.error("Stop deployment while any required stress or verification gate is open.")
else:
    st.write("Modeled gates cleared. Confirm client risk tolerance and obtain committee approval before any funding.")
