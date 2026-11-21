# FIN 43900 Project 2 — Retirement Portfolio Decision

OpenAI Codex assisted with the repository audit, Python and Streamlit changes, data checks, automated tests and draft documentation. The analysis and investment decision are mine. This project is for education and is not investment advice. See [validation and AI use](docs/validation-and-ai-use.md).

**PILOT in the app only, with 0% funded.** This project evaluates a 30-year retirement strategy for a 25-year-old investor. The default portfolio satisfies the explicit cash floor and the proposed volatility limit. Issuer exposure remains unverified and the client’s numerical risk tolerance is unconfirmed. The committee can review the model and evidence in the app. See the [decision memo](docs/decision-memo.md) and [executed output](docs/executed-output.md).

## Run the app

Use Python 3.14.0, the tested version. The runtime uses the tracked price and ALFRED snapshots. Internet access is needed to install the pinned packages.

```sh
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest -v test_project2 test_project2_app
python -m streamlit run app.py
```

On Windows, use PowerShell from the repository root:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest -v test_project2 test_project2_app
python -m streamlit run app.py
```

Open the local URL printed by Streamlit. Leave the sidebar defaults unchanged and compare the three portfolios and six stress cases with the executed output. The displayed DGS10 vintage is fixed at September 30, 2026. The example runs without an upload or API key.

## Mandate and inputs

- **Objective and universe.** Grow retirement wealth over 30 years using BIL, IEF, LQD, VT and a separate cash sleeve. Gross exposures must be nonnegative and sum to 100%. Cash must be at least 5%. BIL is an ETF. The app counts only the cash sleeve, modeled at zero return and volatility.
- **Company cap.** A company can account for at most 10% of portfolio NAV. The checker combines each held fund's exposure using common issuer identifiers. A known breach fails even if other holdings are missing. Incomplete mapping is **UNVERIFIED**. The Lab 19 VT record is a partial example accessed after the decision date.
- **Benchmark and risk.** The strategic benchmark is 60% VT / 40% BIL, restored to target weights every month. Historical gross benchmark return and volatility use the same window as each scenario, before hypothetical shocks and costs. The app applies a proposed 15% annualized standard deviation limit to all candidate portfolios and stress scenarios. The 15% threshold is an illustrative analyst assumption. Lab 13 supplies no numerical client risk limit.
- **Estimates.** Yahoo Finance adjusted prices were downloaded via yfinance on October 22, 2026, per Lab 15. The 61 month-end-labeled prices cover September 2021 through September 2026 and use each month's last available trading observation. This is a retrospective snapshot. The app validates dates, columns, row count and positive finite prices before running.
- **Portfolio math.** The raw baselines use four ETFs. The constrained search uses five sleeves in five-percentage-point increments, prefers verified issuer coverage, and minimizes estimated volatility subject to the proposed volatility limit and a 6.5% first-year net expected-return hurdle. The hurdle is solely an illustrative modeling assumption and does not affect the mandate verdicts for the baselines. Simple monthly average returns are multiplied by 12 and sample volatility by √12. Trading costs are one-time basis points on ETF purchases from an all-cash starting account. Fund expenses already reflected in adjusted prices are not added again. The model does not estimate taxes, recurring advice fees, realized inflation or future returns.
- **DGS10.** The pinned ALFRED vintage makes the 10-year Treasury yield a point-in-time duration-risk monitor. It does not alter ETF estimates. A missing or stale signal blocks deployment. See the [data card and snapshot checks](docs/validation-and-ai-use.md).

### Optional holdings input

Upload a JSON object keyed by fund ticker. Each fund record has `holdings_date` and `available_on` in YYYY-MM-DD format, a `source` citation, an `issuer_weights` object keyed by canonical company ID, and numeric `noncompany_weight`. All weights are fractions of fund NAV. `available_on` is the date the source holdings were available to the analyst, at or before September 30, 2026. Normalize share classes, debt issuers and corporate parents consistently across funds. Include independently identified cash and sovereign exposures in `noncompany_weight`. Leave unidentified or nested holdings out of mapped coverage unless their underlying exposures were resolved. Complete mapped exposures must total 1.0 for each held fund. The checker does not authenticate uploads or resolve issuer names. Review source coverage and snapshot age before relying on any result.

## Repository map

| Path | Purpose |
|---|---|
| [app.py](app.py) and [project2.py](project2.py) | Streamlit interface, mandate checks, dated inputs and stress runs |
| [portfolio.py](portfolio.py) | Original Lab 14/15 math and legacy reproduction |
| [prices.csv](prices.csv) and [DGS10 vintage](data/dgs10-2026-09-30.csv) | Frozen run inputs |
| [Lab 13](Lab_13.md), [Lab 15](Lab_15.md), [Lab 17](Lab_17.md), [Lab 20](Lab_20.md) | Original mandate, model, signal and locked prediction evidence |
| [Decision memo](docs/decision-memo.md), [validation](docs/validation-and-ai-use.md), [manifest](docs/submission-manifest.md) | Submission artifacts and evidence |

The original Lab 15 record is intact. The [reconciliation](docs/validation-and-ai-use.md#lab-15-reconciliation) compares its reported figures with the committed code and prices. The Lab 18/19 investor screens remain separate.
