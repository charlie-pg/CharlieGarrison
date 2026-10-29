
from datetime import date
from io import StringIO
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Point-in-Time Rates Audit", layout="wide")

SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}

@st.cache_data(ttl=3600)
def download_today(series_id):
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
    response = requests.get(url, params={"id": series_id}, timeout=30)
    response.raise_for_status()
    return parse_csv(response.text, series_id)

@st.cache_data(ttl=3600)
def download_asof(series_id, vintage):
    url = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
    response = requests.get(
        url,
        params={"id": series_id, "vintage_date": vintage},
        timeout=30,
    )
    response.raise_for_status()
    return parse_csv(response.text, series_id)

def parse_csv(text, series_id):
    df = pd.read_csv(StringIO(text), na_values=["."])
    if df.empty or len(df.columns) < 2:
        raise ValueError(f"No data found for {series_id}")
    df = df.iloc[:, :2].copy()
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna().sort_values("date").drop_duplicates("date", keep="last")

def latest(df):
    if df.empty:
        return None, None
    row = df.iloc[-1]
    return row["date"].strftime("%Y-%m-%d"), float(row["value"])

st.title("Lab 17 — Point-in-Time Rates Audit")
st.caption(
    "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, "
    f"downloaded {date.today()}; built with AI help, "
    "a learning demonstration, not investment advice."
)

with st.sidebar:
    selected = st.multiselect(
        "Rate series",
        options=list(SERIES),
        default=list(SERIES),
        format_func=lambda x: f"{x} — {SERIES[x]}",
    )
    extra = st.text_input("Add another FRED series ID (e.g., PAYEMS)").strip().upper()
    start = st.date_input("Start date", value=date(2020, 1, 1))
    asof_date = st.date_input(
        "As known on", value=date.today(), max_value=date.today()
    )

if extra and extra not in selected:
    selected.append(extra)

results = []

for series_id in selected:
    st.subheader(f"{series_id} — {SERIES.get(series_id, 'Custom series')}")
    st.markdown(f"[View source on FRED](https://fred.stlouisfed.org/series/{series_id})")

    try:
        current = download_today(series_id)
        historical = download_asof(series_id, asof_date.isoformat())

        # Do not count observations dated after the decision date.
        historical = historical[
            historical["date"] <= pd.Timestamp(asof_date)
        ]

        visible_current = current[current["date"] >= pd.Timestamp(start)]
        st.line_chart(visible_current.set_index("date")["value"])

        known_date, known_value = latest(historical)
        current_date, current_value = latest(current)

        st.write(
            f"Last observation known on {asof_date}: "
            f"**{known_date or 'None'} — {known_value if known_value is not None else 'N/A'}**"
        )

        if known_date is None:
            late_count = len(current)
            revised_count = 0
        else:
            cutoff = pd.Timestamp(known_date)
            late_count = int((current["date"] > cutoff).sum())

            comparison = historical.merge(
                current, on="date", suffixes=("_known", "_today")
            )
            revised_count = int(
                (
                    (comparison["value_known"] - comparison["value_today"]).abs()
                    > 1e-9
                ).sum()
            )

        results.append({
            "Series": f"https://fred.stlouisfed.org/series/{series_id}",
            "Last date known": known_date,
            "Value known": known_value,
            "Latest date today": current_date,
            "Latest value today": current_value,
            "Later observations": late_count,
            "Revised observations": revised_count,
        })

    except Exception as exc:
        st.error(f"Could not load {series_id}: {exc}")

st.subheader("Point-in-time comparison")
if results:
    st.dataframe(
        pd.DataFrame(results),
        column_config={
            "Series": st.column_config.LinkColumn(
                "Series / FRED page",
                display_text=r"https://fred\.stlouisfed\.org/series/(.*)"
            )
        },
        use_container_width=True,
        hide_index=True,
    )