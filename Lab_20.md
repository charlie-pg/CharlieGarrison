# Lab 20 — Project 2 Readiness

**Status: evidence pending.** The starting point is the [Lab 15 portfolio app](app.py); [README](README.md) provides setup, reproduction steps and mandate limitations. Do not treat the placeholders below as completed work.

## Existing decision and mandate gaps

The recorded Lab 15 decision is **pilot, not adopt**: the historical allocation was stable across the two windows, but estimated volatility changed, and the return estimates, data quality and mandate needed further review. The recorded comparison used Meridian training thresholds, not a confirmed Project 2 mandate. The app does not specifically enforce the client's 5% cash minimum or 10% single-company limit; risk tolerance remains unconfirmed. See [Lab 13](Lab_13.md), [Lab 15](Lab_15.md), and the README.

## Partner run — successful with assistance

I sent my GitHub repository link to **Max Puntill**, and he successfully ran the Project 2 app. I gave him a little help at the beginning; otherwise, everything ran smoothly. This was a successful assisted run, not a fully independent cold run.

The date, commit tested, environment, commands, elapsed time and specifics of the initial help were not recorded. This run does not establish that a stranger can complete the process without assistance.

## Locked Changed-Input Record — personal prediction before the experiment

**Prediction date:** November 17, 2026. This is my personal AI-off prediction, not a measured result.

- **Old required reserve:** 3% of the portfolio.
- **New required reserve:** 5% of the portfolio.
- **My prediction:** The portfolio's expected return will decrease because a larger share must be held in lower-return reserve assets.
- **Expected decision effect:** My current **PILOT** recommendation will likely remain **PILOT**, but I expect a lower projected return.

The prediction was committed and pushed before the experiment in [commit 2d6b05c](https://github.com/charlie-pg/CharlieGarrison/commit/2d6b05c3ea497b39a9f7d5b9d37905ca35feb2fe).

## Changed-input result — measured after the push

**Test date:** November 17, 2026. Tested the portfolio code and `prices.csv` at commit `2d6b05c`, after the prediction was pushed. The full historical price window, 6.5% minimum expected return, BIL and IEF as reserve eligible, and 5-percentage-point allocation grid were held constant. The calculation uses the app's rounding of displayed asset return inputs.

| Result | Before: 3% reserve minimum | After: 5% reserve minimum |
|---|---:|---:|
| BIL / IEF / LQD / VT | 60% / 0% / 0% / 40% | 60% / 0% / 0% / 40% |
| Expected return | 6.91% | 6.91% |
| Volatility | 6.04% | 6.04% |
| Reserve-eligible allocation | 60% | 60% |
| App's tested return and reserve requirements | Meets both | Meets both |
| Retirement client mandate | Not established | Not established |

The predicted decrease in expected return **did not occur**. The original optimum already held 60% in reserve-eligible BIL, so neither minimum was binding. These are model estimates, not realized returns. Meeting the app's two tested requirements is not a full retirement-mandate verdict: the app does not specifically check the 5% cash rule or the 10% single-company limit, including fund holdings.

**Decision effect:** Retain **PILOT, not adopt**. This test gives no reason to change the recommendation, and the client mandate and other checks remain unresolved. The measured full-window result also differs from Lab 15's recorded 30% BIL / 5% LQD / 65% VT, 6.50% return and 10.12% volatility; the cause has not been established and should be investigated before adoption.

To reproduce in the app, upload `prices.csv`, leave the 36-month toggle off, select BIL and IEF as reserve eligible, keep the 6.5% return minimum and all asset estimates unchanged, and compare results with the reserve minimum at 3% and 5%. The experiment above called the same `estimate_from_csv` and `find_lowest_risk` functions with those settings.

## Fix or documented clean run — pending

- Issue found, or evidence that the run was clean: **pending**
- Fix and retest evidence, if needed: **pending**
- Remaining limitations: **pending**

## Decision and reversal condition

**PILOT, not adopt:** Do not adopt until the retirement mandate is enforced, the Lab 15 discrepancy is reconciled, and the results pass independent validation.
