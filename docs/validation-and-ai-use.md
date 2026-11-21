# Validation and AI use

OpenAI Codex assisted with auditing Lab 13–20, implementing the Streamlit extension, retrieving and checking the official ALFRED vintage, writing tests, and drafting the documentation. Charlie Garrison owns the analysis and decision. Student review and the independently checked AI output for Video 1 are pending. The checks below identify what was executed and what remains to be validated.

## Locked Changed-Input Record

The [Lab 20 record](../Lab_20.md) preserves the November 17, 2026 human AI-off prediction and reports the pre-run GitHub push. The [prediction commit, 2d6b05c](https://github.com/charlie-pg/CharlieGarrison/commit/2d6b05c3ea497b39a9f7d5b9d37905ca35feb2fe), precedes the [measured result, 5078444](https://github.com/charlie-pg/CharlieGarrison/commit/507844471df97e316d8a815c03fda64467e716e2). Charlie predicted that raising the reserve floor from 3% to 5% would lower expected return and leave the recommendation at PILOT.

The full price window, estimated returns rounded to the app input precision, 6.5% return hurdle, BIL/IEF eligibility, and five-point grid were held constant. Both runs produced 60% BIL, 40% VT, 6.91% expected return, 6.04% annualized volatility, and 60% eligible reserve. The higher floor was nonbinding and the predicted return decrease did not occur. PILOT was retained. This evidence predates the explicit cash check and test of the company cap.

The [partner record, 98760e1](https://github.com/charlie-pg/CharlieGarrison/commit/98760e1abe350b612ff1346391b0c3e843e6fc0a), documents a successful assisted run by Max Puntill. Revision, commands, environment, timing and details of the initial help were not recorded. An independent stranger run of this version remains open.

## Lab 15 reconciliation

Executed the original portfolio engine and price file from Git commit [6546c53](https://github.com/charlie-pg/CharlieGarrison/commit/6546c53). The original and current legacy engine and price files are identical. Used 6.5% return, 3% reserve and BIL/IEF eligibility. Raw and app-rounded inputs returned the same weights and displayed metrics.

| Window | Lab 15 report BIL / IEF / LQD / VT | Reported return / vol | Replayed weights | Replayed return / vol |
|---|---|---|---|---|
| Full | 30 / 0 / 5 / 65% | 6.50% / 10.12% | 60 / 0 / 0 / 40% | 6.91% / 6.04% |
| 36 months | 30 / 0 / 5 / 65% | 6.50% / 7.89% | 85 / 0 / 0 / 15% | 6.75% / 1.79% |

The original settings that produced the Lab 15 report are unknown. The replay rules out drift in the tracked engine and price bytes and the app's return rounding for the documented configuration. The legacy replay shows a 25-point weight change. The [Project 2 results](executed-output.md) add explicit cash and are a distinct analysis.

## Frozen inputs and DGS10 data card

- [Prices](../prices.csv), Yahoo Finance via yfinance, October 22, 2026 per Lab 15. Monthly adjusted closes in USD, last available trading price each month. Historical estimates include 60 or 36 simple monthly returns and no point-in-time claim is made for the price snapshot. SHA-256 `254c7a6e20280b65fd4f7840baa4c16cf581a0cca34cd922c9c80270c89372a4`.
- [DGS10 vintage](../data/dgs10-2026-09-30.csv), retrieved November 20, 2026 from ALFRED. Board of Governors series, daily business observations, percent per year, not seasonally adjusted. Latest value at the decision date was 5.26% dated September 29. Blank observations are omitted from the latest-value calculation. Publication timing is determined by the supplied vintage and can lag the observation date. Later vintages may include new or revised observations. The signal monitors IEF duration risk and does not set expected returns. The 7-calendar-day freshness stop is a pilot assumption. The official vintage confirms the September 29 observation. The Lab 17 October 2 observation and other reference cases were not rerun here. SHA-256 `f7ebe7165fd9a7349b3b91f53141e57a9b32a35d0ec888576eff215c443e1adb`. [FRED data card](https://fred.stlouisfed.org/series/DGS10) · [ALFRED download](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-09-30&cosd=2026-09-01&coed=2026-09-30)
- Issuer holdings are absent from the default run. The [Lab 19 VT record](../lab19/data/VT_holding_source.json) identifies one dated secondary disclosure accessed after the decision date. It cannot establish combined equity and corporate bond exposures. The synthetic holdings in tests validate the checker only.

## Current model policy and funding gate

The strategic benchmark is 60% VT / 40% BIL, rebalanced monthly. For each scenario window, the benchmark monthly return is 60% of VT’s monthly return plus 40% of BIL’s. The annualized benchmark figures are historical and gross of modeled trading costs. The same fixed weights apply across the window, estimates, costs and constraints stresses.

Every portfolio is assessed against a minimum of 5% explicit cash, excluding BIL, and a 10% single-company exposure cap. The tighter constraint stress raises the explicit cash floor to 10% and lowers the issuer cap to 8%. Missing look-through coverage remains UNVERIFIED under either cap. The 15% annualized volatility threshold is an illustrative analyst assumption that applies to both baselines, the constrained portfolio and all stress runs. Lab 13 supplies no client numerical risk limit. The 6.5% first-year net expected-return hurdle is used only in modeling the constrained search. It is not a client mandate. The committee recommendation remains a paper-account PILOT with 0% funded until issuer coverage and the remaining deployment requirements are verified.

## Checks and stress evidence

On November 20, 2026, all 12 Project 2 tests, six Lab 18 tests and 16 Lab 19 tests passed under Python 3.14.0 and Streamlit 1.67.0. The separate Lab 18 and Lab 19 offline Streamlit checks also passed. The Project 2 suite includes a hand-calculated monthly rebalancing case and tests at and just above the 15% volatility threshold. `pip check` found no broken requirements. The local Streamlit health endpoint and app page both returned HTTP 200. Verification used the existing pinned environment. A fresh dependency install and an independent cold run remain pending.

Run `python -m unittest -v test_project2 test_project2_app` with the pinned environment. The tests cover the Lab 14 equal-weight calculation, Lab 16 funnel and signals, Lab 17 saved signal and date guard, adjusted-price file validation, 5% cash and 10% shared issuer boundaries, incomplete exposures, one-way cost math, infeasibility, decision stops and the Streamlit default and stress displays. See [executed output](executed-output.md) for the measured four-factor stress and combined case. For an admissible funded pilot, verify issuer sources and confirm the client’s numerical risk tolerance and rerun the stress suite.

Candidate AI-output check for student review. Codex flagged that the Lab 15 stability claim was not reproducible under the documented settings. The validation here reran the historical Git blobs. Independently rerun the reference and short window yourself, then record what you accepted, qualified or rejected. This is a suggested check, not a completed student attestation.
