"""Run: lab18/.venv/bin/python -m streamlit run lab19/app.py"""
import json
from pathlib import Path
import pandas as pd
import streamlit as st
from sec_facts import download, numeric, display_value, unsupported_numbers
from panel import INVESTORS, panel_checks, panel_report

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Legend Panel — Lab 19", layout="wide")
st.title("Legend Panel — Lab 19")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
with st.sidebar:
    ticker = st.text_input("Ticker", "COST").strip().upper()
    name = st.text_input("SEC contact name", "Charlie Garrison")
    email = st.text_input("SEC contact email")
    refresh = st.button("Download from SEC", type="primary")
    probe = st.checkbox("Probe Cathie Wood growth at 5%", value=False)
    st.caption("Default growth threshold retained: 15%. The probe is temporary.")
if refresh:
    try:
        with st.spinner("Downloading SEC facts…"):
            st.session_state["result"] = download(ticker, name, email, ROOT / "data")
    except Exception as exc:
        st.error(f"SEC download failed: {exc}")
result = st.session_state.get("result")
if result is None or result["ticker"] != ticker:
    path = ROOT / "data" / f"{ticker}_result.json"
    result = json.loads(path.read_text()) if path.exists() else None
if result is None:
    st.info("No saved SEC data for this ticker. Enter contact details and download.")
    st.stop()
st.subheader(f"{ticker} — {result['entity']}")
st.caption(f"SEC download: {result['downloaded_at']}; filing cutoff: {result['as_of']}.")
if len(result["rows"]) < 5:
    st.warning("Fewer than five fiscal years; full-window checks are not known.")
st.subheader("Annual earnings · USD millions")
st.line_chart(pd.DataFrame([
    {"Fiscal-year-end": r["fiscal_year_end"], **{m.replace('_', ' ').title(): r[m] / 1e6 if numeric(r[m]) else None for m in ("owner_earnings", "net_income")}}
    for r in result["rows"]
]).set_index("Fiscal-year-end"))
st.caption("Gaps indicate missing values; missing capital spending is never zero.")
metrics = ["revenue", "net_income", "operating_cash_flow", "capital_spending", "equity", "liabilities", "research_and_development", "owner_earnings", "roe", "revenue_growth", "rd_to_revenue", "liabilities_to_equity"]
st.subheader("Financial table")
st.dataframe(pd.DataFrame([
    {"Fiscal-year-end": r["fiscal_year_end"], **{m.replace('_', ' ').title():
        (f"{r[m]:.2f}x" if m == "liabilities_to_equity" and numeric(r[m]) else display_value(r[m], m in {"roe", "revenue_growth", "rd_to_revenue"})) for m in metrics}}
    for r in result["rows"]
]), hide_index=True, width="stretch")
st.caption("USD millions; ROE, year-over-year growth and R&D/revenue in percent; liabilities/equity in multiples. ROE uses year-end equity. Owner earnings = operating cash flow − capital spending.")
growth = result["revenue_cagr"]
st.write("Annualized revenue growth, first to last: " + (f"{growth:.2%}" if numeric(growth) else "not known"))
threshold = .05 if probe else .15
checks = panel_checks(result, threshold)
st.subheader("Investor × check")
st.dataframe(pd.DataFrame([{"Investor": investor, "Check": check, "Result": status}
    for investor, items in checks.items() for check, status in items.items()]), hide_index=True, width="stretch")
report = panel_report(result, threshold)
with st.expander("Printed script report, XBRL tags and filing provenance"):
    st.markdown(report)
st.download_button("Download script report", report, f"{ticker}_panel_report.md")
st.caption("Saved memos are AI judgments from the default screen. During the probe, review and edit their reasoning and verdicts; they do not regenerate automatically.")
for col, investor in zip(st.columns(3), INVESTORS):
    with col:
        st.subheader(investor)
        for check, status in checks[investor].items():
            st.write(f"**{check}: {status}**")
        path = ROOT / "memos" / f"{ticker}_{investor.lower().replace(' ', '_')}.md"
        saved = path.read_text() if path.exists() else ""
        memo = st.text_area(f"{investor} memo", saved, height=350, key=f"memo_{ticker}_{investor}")
        if memo:
            st.markdown(memo)
            warnings = unsupported_numbers(memo, report)
            if warnings:
                st.warning(f"{investor} unsupported numerical claims: " + ", ".join(warnings))
            else:
                st.success("All numerical tokens appeared in the script report.")
            st.download_button(f"Download {investor} memo", memo, f"{ticker}_{investor}_memo.md")
        else:
            st.info("Verdict: not known. Use this investor's skill with the printed report, then paste the memo here.")
        if investor == "Cathie Wood":
            st.caption("Retained growth threshold: 15%, to preserve the assignment's innovation screen. The 5% probe demonstrates threshold sensitivity; missing R&D remains not known.")
st.caption("The numerical audit covers every memo. It checks tokens, not metric, year, unit associations or qualitative claims. Review manually. Edits are temporary; use Download memo to retain them. No paid AI API is called.")
