# Lab 16 — Provenance Gate

## Objective

Determine which data was actually available on March 31, 2026, and compare the resulting investment signals with signals calculated using information published later.

## Row Funnel

| Rule | Rows removed |
|---|---|
| Missing ticker | 11 |
| Exact duplicate | 7 |
| Published after decision date | 3, 8, 10 |
| Older revision replaced | 2 |

**Final as-of panel:** Rows 1, 4, 5, 6, 9, 12.

## Signal Comparison

| Ticker | As-of signal | Naive signal |
|---|---|---|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | −1.02% (February) | −5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February) |

All results match the instructor's known answers.

## Sanity Check

| Row | Yield | Problem |
|---|---|---|
| 1 | −0.99% | Negative yield |
| 4 | −2.91% | Negative yield |
| 5 | +2.04% | None |
| 6 | +3.09% | None |
| 9 | −9.09% | Negative yield; CCC priced above AAA and BBB |
| 12 | −9.91% | Negative yield; CCC priced above AAA and BBB |

Yield = 100 / price − 1.

## Later-Date Test

Changed the decision date to April 15, 2026. All three as-of signals matched their naive signals: AAA +5.83%, BBB −5.15%, and CCC +1.82%. Restored March 31 afterward.

## Learning and Reflection

**What is look-ahead bias?** Using information in a historical decision that was not actually available at the time.

**Why do publication dates and revisions matter?** A number can measure February but only become available in March or April. Revisions can also change the previously published value.

**AAA example:** The naive +5.83% uses March data published April 10, which was unavailable on March 31. The knowable signal was only +1.98%.

**Which rule mattered most?** Rule 3 prevented future publications from entering the historical decision. Rule 4 also mattered because it replaced AAA row 2 with the newer February revision, row 4.

**What would a naive backtest claim?** It would report returns based partly on future information, potentially creating misleading investment performance.

**What fifth rule is needed?** A financial sanity gate that quarantines negative-yield zero-coupon prices and credit-rating price-order violations, including rows 1, 4, 9, and 12.

## Conclusion

A provenance gate prevents look-ahead bias but does not guarantee economically sensible data. Both publication timing and financial sanity checks are necessary.