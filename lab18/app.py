"""Launch from the workspace: lab18/.venv/bin/python -m streamlit run lab18/app.py"""
import json
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "buffett-investor" / "scripts"))
from buffett import download, numeric, render_report, unsupported_numbers, display_value

st.set_page_config(page_title="Buffett Investor — Lab 18", layout="wide")
st.title("Buffett Investor — Lab 18")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("Company")
    ticker = st.text_input("Ticker", "COST").strip().upper()
    name = st.text_input("SEC contact name", "Charlie Garrison")
    email = st.text_input("SEC contact email", placeholder="Enter your email for live downloads")
    refresh = st.button("Download from SEC", type="primary")
    st.caption("No API key. Contact details are used only in the SEC User-Agent.")

if refresh:
    try:
        with st.spinner("Downloading SEC company facts and annual filing dates…"):
            st.session_state["result"] = download(ticker, name, email, ROOT / "data")
    except Exception as exc:
        st.error(f"SEC download failed: {exc}")

result = st.session_state.get("result")
if result is None or result["ticker"] != ticker:
    path = ROOT / "data" / f"{ticker}_result.json"
    result = json.loads(path.read_text()) if path.exists() else None
if result is None:
    st.info("Enter a ticker and your SEC contact details, then download. No saved SEC data exists for this ticker.")
    st.stop()

st.subheader(f"{result['ticker']} — {result['entity']}")
st.caption(f"Saved SEC download: {result['downloaded_at']}; filing cutoff: {result['as_of']}. Refresh to update.")
if len(result["rows"]) < 5:
    st.warning("Fewer than five fiscal years are available. Checks are not known.")

chart = pd.DataFrame([
    {"Fiscal-year-end": r["fiscal_year_end"],
     "Owner earnings": r["owner_earnings"] / 1e6 if numeric(r["owner_earnings"]) else None,
     "Net income": r["net_income"] / 1e6 if numeric(r["net_income"]) else None}
    for r in result["rows"]
]).set_index("Fiscal-year-end")
st.subheader("Annual earnings · USD millions")
if not chart.empty:
    st.line_chart(chart)
st.caption("Gaps indicate missing values; missing capital spending is never treated as zero.")

st.subheader("Financial table")
metrics = ["revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "owner_earnings", "roe"]
st.dataframe(pd.DataFrame([
    {"Fiscal-year-end": r["fiscal_year_end"], **{m.replace('_', ' ').title(): display_value(r[m], m == "roe") for m in metrics}}
    for r in result["rows"]
]), hide_index=True, width="stretch")
st.caption("USD millions, except ROE. ROE = net income / year-end equity. Owner earnings = operating cash flow − capital spending.")
for check, status in result["checks"].items():
    st.write(f"**{check}: {status}**")
st.write(f"First-to-last owner earnings growth: {display_value(result['owner_earnings_growth'], True)}")

report = render_report(result)
with st.expander("XBRL tags, filing provenance, and printed script report"):
    st.markdown(report)
st.download_button("Download script report", report, f"{ticker}_report.md")

st.subheader("Buffett-style business memo")
memo_path = ROOT / "memos" / f"{ticker}.md"
saved_memo = memo_path.read_text() if memo_path.exists() else ""
memo = st.text_area("Review or edit the AI memo", value=saved_memo, height=260, key=f"memo_{ticker}",
                    placeholder="Use the buffett-investor skill to write a memo from this script report, then paste it here.")
if memo:
    st.markdown(memo)
    unsupported = unsupported_numbers(memo, report)
    if unsupported:
        st.warning("Unsupported numerical claims (not printed by the script): " + ", ".join(unsupported))
    else:
        st.success("All numerical tokens appeared in the script report.")
    st.download_button("Download memo", memo, f"{ticker}_memo.md")
else:
    st.info("No AI memo saved for this ticker. The skill makes the business judgment after reviewing the script output.")
st.caption("The numerical check compares tokens, including percent units. It cannot verify that a supported number is attached to the correct year or metric, or validate qualitative claims.")
