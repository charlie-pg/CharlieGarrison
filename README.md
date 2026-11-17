# Project 2 — Portfolio Stability

This repository contains a Streamlit portfolio tool developed in Lab 15. It searches allocations in 5-percentage-point increments and displays the lowest-volatility mix that meets a minimum expected return and reserve requirement. The current recorded decision is **pilot, not adopt**, pending further checks; see [Lab 15](Lab_15.md). This is an educational demonstration, not investment advice.

## Setup and run

From a terminal in a fresh clone of this repository, with Python 3 installed:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install 'streamlit>=1.40,<2'
python -m streamlit run app.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. Open the local URL printed by Streamlit. To stop the app, press Ctrl+C in the terminal.

## Reproduce the recorded historical comparison

1. Upload the repository's `prices.csv` in the sidebar. It contains monthly adjusted prices for BIL, IEF, LQD and VT from September 2021 through September 2026.
2. Leave the minimum expected return at 6.5% and the minimum reserve-eligible weight at 3%. Mark BIL and IEF as reserve eligible; uploaded assets are not selected automatically.
3. With the 36-month toggle off, read the current allocation, expected return and volatility. Then turn on **Use only last 36 monthly returns** and compare the current results with the full-period as-loaded baseline.
4. [Lab 15](Lab_15.md) records 30% BIL, 0% IEF, 5% LQD and 65% VT in both windows, with volatility of 10.12% and 7.89%, respectively. These are recorded results, not a claim that a fresh run has been verified today.

Without an upload, the app uses the built-in Meridian training inputs. You can change estimated returns and reserve eligibility in the app; the as-loaded baseline uses the original returns and the current mandate settings. With an uploaded file, it also uses the currently selected reserve flags. Estimates are historical inputs, not guaranteed future outcomes.

## Client mandate and limitations

[Lab 13](Lab_13.md) records an initial Project 2 mandate for a 25-year-old saving for retirement over 30 years: no borrowing or short selling, at least 5% cash, and no more than 10% in one company. Risk tolerance still needs confirmation.

The app's default 6.5% return and 3% reserve thresholds are **Meridian training assumptions**, not confirmed requirements for this client. Its grid uses nonnegative weights summing to 100%, but the configurable reserve rule does not specifically enforce 5% cash, and the app does not check the 10% company limit or look through fund holdings. [mandate.py](mandate.py) is a separate Meridian exercise, not a client-mandate checker. Consequently, the recorded allocation is not established as compliant with the Project 2 mandate.

[Lab 20](Lab_20.md) contains the readiness evidence template. The separate [Lab 19 investor panel](Lab_19.md) is a screening tool and is not integrated into this portfolio app.
