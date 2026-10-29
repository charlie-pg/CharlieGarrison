# Lab 17 — Point-in-Time Audit

## Objective

Determine whether historical interest-rate data was actually available on the date an investment decision would have been made, and decide whether the series can safely be used in Project 2.

## Selected Series: DGS10

### Data Card

- **Series:** DGS10 — Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity
- **Source:** Federal Reserve Bank of St. Louis (FRED), with underlying data from the Board of Governors of the Federal Reserve System
- **Link:** https://fred.stlouisfed.org/series/DGS10
- **Download date:** October 29, 2026
- **What it measures:** The market yield on 10-year U.S. Treasury securities.
- **Units:** Percent per year.
- **Frequency:** Daily, generally on business days.
- **Publication lag:** The most recent trading day's observation may be the latest available at a decision time. On September 30, 2026, my app showed September 29 as the latest available observation.
- **Revisions:** My app detected zero revised observations when comparing the September 30 vintage with today's data.
- **Portfolio relevance:** Treasury yields influence bond prices, particularly the IEF Treasury bond ETF in my portfolio.

## Point-in-Time Results

**Decision date:** September 30, 2026

| Metric | Result |
|---|---|
| Last observation known | September 29, 2026 |
| Yield known then | 5.26% |
| Latest observation today | October 28, 2026 |
| Latest yield today | 5.05% |
| Later observations | 20 |
| Revised observations | 0 |

The September 30 vintage did not include the 20 observations that became available afterward. Using those later observations in a September 30 investment decision would introduce look-ahead bias.

## Known-Answer Validation

I tested my Streamlit application using the professor's October 5, 2026 reference date.

| Series | Last observation known | Value |
|---|---|---|
| BAA | September 2026 | 6.47 |
| FEDFUNDS | September 2026 | 3.75 |
| DGS10 | October 2, 2026 | 5.28 |
| MORTGAGE30US | October 1, 2026 | 7.28 |

**Result:** All four values matched the professor's expected answers.

### PAYEMS Revision Test

I added PAYEMS and changed the historical decision date to January 15, 2025.

- Last observation known: December 2024
- Value known then: 159,536
- Today's revised value for December 2024: 159,044
- Revised observations detected: 381

**Result:** The application successfully detected historical revisions. This confirms that the historical and current downloads are not simply displaying identical versions of the data.

## Three FRED Data Checks

**Official source:** https://fred.stlouisfed.org/series/DGS10

| Observation date | DGS10 yield |
|---|---|
| September 29, 2026 | 5.26% |
| October 2, 2026 | 5.28% |
| October 28, 2026 | 5.05% |

These three values were checked against the downloaded DGS10 data. The October 28 observation was also confirmed on the official FRED webpage. The September 29 and October 2 observations still require direct confirmation on the webpage.

The FRED webpage identifies the series as daily, measured in percent, and not seasonally adjusted.

## How the Application Prevents Look-Ahead Bias

The application uses two separate data sources:

1. **FRED:** Retrieves the series as it appears today.
2. **ALFRED:** Retrieves the historical version available on a selected date.

The historical download includes a `vintage_date` parameter specifying when the information had to be available.

The application compares the two datasets to identify:

- The latest observation available at the historical decision date.
- Observations published after that date.
- Historical observations whose values were subsequently revised.

These checks help prevent future information from entering a historical investment strategy.

Cleaning a dataset alone is not enough because a clean dataset may still contain information that was unavailable at the time. A data card also documents the source, units, publication timing, revisions, and limitations.

## Partner Review and Stress Test

I worked with my partner during class, but we did not complete the final partner-attack exchange before he left.

**Question examined:** Can we trust the publication timing of DGS10 when making investment decisions?

**Response:** My application showed that on September 30, 2026, the latest available DGS10 observation was September 29, with a yield of 5.26%. Therefore, Project 2 should use only observations available by each decision date rather than assuming the same day's interest rate was already published.

**Evidence:** The historical ALFRED vintage and the point-in-time comparison table in my Streamlit application.

## Project 2 Decision

**Decision: ADMIT CONDITIONALLY**

I would allow DGS10 into Project 2 because it is directly relevant to Treasury bond investments, is reported frequently, and showed no revisions in the tested historical comparison.

However, the following rule must be enforced:

**Only use DGS10 observations that were actually available on or before each investment decision date.**

If the data's publication timing cannot be verified, or historical revisions are discovered that affect the strategy, I would quarantine the series until the problem is resolved.

## Reflection

DGS10 is published daily, but the latest available observation can lag behind the decision date. My September 30 test demonstrated that the most recent known observation was from September 29.

A backtest using today's complete historical dataset could accidentally incorporate interest rates that had not yet been published when a trade was made. This could make a strategy appear more accurate or profitable than it would have been in real time.

The main lesson from this lab is that historical data must be evaluated based on when it became available, not simply when the underlying event occurred.

## Application

**Python file:** `asof_app.py`

The Streamlit application includes four default interest-rate series, support for additional FRED series IDs, historical date selection, charts, and a comparison table showing later observations and revisions.

**Data sources:** FRED and ALFRED, Federal Reserve Bank of St. Louis.

Built with AI assistance as an educational demonstration, not investment advice.