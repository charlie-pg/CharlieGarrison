# Lab 06: Eli Lilly DCF Checkout

## Sources and Inputs

| Input | Value | Units | As-of date | Source/location |
|---|---:|---|---|---|
| Starting FCFF | 9,689.79 | $ millions | Year ended December 31, 2025 | Calculated as operating cash flow + after-tax interest - capital expenditures. Lilly 2025 10-K: Consolidated Statements of Cash Flows, p. 61; Note 11, p. 77; Note 14, p. 80. |
| Years 1–5 growth rates | 18%, 17%, 15%, 12%, 10% | Percent per year | Forecast after 2025 | Base-case estimate supported by Lilly 2025 10-K, Item 7 MD&A, pp. 48–52: product-driven revenue growth, improving gross margin, and elevated near-term capital expenditures. |
| WACC | 6.9% | Percent | September 10, 2026 | Base-case estimate using the September 10, 2026 10-year Treasury yield, LLY five-year beta, U.S. implied equity risk premium, Lilly debt costs, and capital structure. Sources: [U.S. Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202609&type=daily_treasury_yield_curve), [Yahoo Finance](https://finance.yahoo.com/quote/LLY/), [Damodaran](https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm), and Lilly filings. |
| Terminal growth | 2.5% | Percent per year | After forecast Year 5 | Base-case valuation assumption based on mature-company, long-run nominal economic growth. |
| Cash / debt / diluted shares | 8,950 / 54,908 / 893.7 | $ millions / $ millions / millions of shares | June 30, 2026 | [Lilly Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/59478/000005947826000081/lly-20260630.htm): cash and debt, Consolidated Condensed Balance Sheets, p. 7; diluted shares, Consolidated Condensed Statements of Operations, p. 5 (three months ended June 30, 2026). |

Market price: **$1,124.21 per share**, NYSE close on **September 9, 2026 at 4:00 p.m. EDT**. Source: [Stock Analysis](https://stockanalysis.com/stocks/lly/).

## Sensitivity Grid

Value per diluted share:

| WACC / Terminal Growth | 2.0% | 2.5% | 3.0% |
|---|---:|---:|---:|
| 5.9% | $436.19 | $499.78 | $585.28 |
| 6.9% | $333.93 | $371.59 | $418.91 |
| 7.9% | $266.41 | $290.96 | $320.53 |

## Reverse DCF

- Target price: **$1,124.21**
- Implied parallel growth-rate shift: **+27.38 percentage points**
- Implied Years 1–5 growth rates: **45.38%, 44.38%, 42.38%, 39.38%, 37.38%**

## Reasonableness

The base DCF value is **$371.59 per share** versus the **$1,124.21** market price. The DCF-to-market ratio is **0.33x**, or the market price is **3.03x** the DCF value. This is outside the professor's 0.5x–2.0x range.

The input to distrust most is the **Years 1–5 FCFF growth forecast** because Lilly's unusually strong incretin-driven growth could make the base-case growth path too low. No inputs were adjusted.

## Conditional Call

Initiate if Lilly demonstrates that incretin-driven growth, new product launches, and manufacturing expansion can support FCFF growth roughly 27.38 percentage points above the base-case forecast; otherwise, defer at the $1,124.21 market price versus the $371.59 DCF value.

Monitor Mounjaro and Zepbound volume growth and realized pricing.
