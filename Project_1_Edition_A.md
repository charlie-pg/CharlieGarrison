# Project 1 — Edition A

## Decision and user

**Decision:** Watch/defer. Do not initiate a position until the valuation, downside case, and key commercial assumptions are tested.

**Decision user:** The fund's investment committee, which must decide whether Eli Lilly and Company merits initiation in the portfolio and, if so, at what price and position size.

## Company and valuation date

- **Company:** Eli Lilly and Company
- **Ticker:** NYSE: LLY
- **CIK:** 0000059478
- **Valuation date:** September 1, 2026

## Initial thesis

**Watch/defer.** Lilly enters the research process with exceptional reported growth and a large operating base: FY2025 revenue was $65.179 billion, up from $45.043 billion in FY2024. That evidence supports further work, but it does not by itself establish an attractive investment at the valuation date. The available filing evidence is historical, the current market price and security count have not yet been fixed for the valuation, and no forecast, intrinsic-value range, or risk-adjusted return threshold has been completed. Initiation should therefore wait until the committee can compare a defensible valuation range with the market price and test whether growth and margin expectations already embedded in that price are achievable.

## Known evidence and sources

Unless otherwise stated, amounts are in USD millions and shares are in millions.

### Filing record

| Field | Recorded value | Filing evidence |
|---|---:|---|
| Entity | Eli Lilly and Company | 10-K cover; inline XBRL `dei:EntityRegistrantName` |
| Ticker / CIK | LLY / 0000059478 | 10-K cover; inline XBRL `dei:TradingSymbol` and `dei:EntityCentralIndexKey` |
| Form | 10-K | 10-K cover; inline XBRL `dei:DocumentType` |
| Filing / accession | 0000059478-26-000013 | Filing's embedded SEC source URL and SEC filing index |
| Reporting period | Jan. 1–Dec. 31, 2025 | Fiscal year ended Dec. 31, 2025; inline XBRL `dei:DocumentPeriodEndDate` |
| Filing date | Feb. 12, 2026 | SEC filing index |
| Currency | U.S. dollars (USD) | Inline XBRL unit reference `usd` |
| Presentation units | USD millions; shares millions | Financial-statement headings and inline XBRL scale of 6 |
| Diluted-share evidence | 899.3 million weighted-average diluted shares | FY2025 Consolidated Statements of Operations; inline XBRL `us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding`. This is EPS evidence, not a valuation-date share count. |
| Cash | $7,268 million | Cash and cash equivalents at Dec. 31, 2025; inline XBRL `us-gaap:CashAndCashEquivalentsAtCarryingValue` |
| Debt | $42,503 million | $1,635 million current debt plus $40,868 million long-term debt at Dec. 31, 2025 |
| Operating-value driver | FY2025 revenue of $65,179 million | Consolidated Statements of Operations; inline XBRL `us-gaap:Revenues` |

### Investment evidence

| Evidence | FY2025 / period-end value | Why it matters | Source |
|---|---:|---|---|
| Form and reporting period | Form 10-K; year ended Dec. 31, 2025 | Defines the primary evidence set | Eli Lilly 2025 Form 10-K, cover page |
| Filing identity | Accession 0000059478-26-000013; filed Feb. 12, 2026 | Makes the evidence reproducible | SEC filing index and the filing's embedded SEC source URL |
| Revenue | $65,179 | Primary operating-value driver | Form 10-K, Consolidated Statements of Operations; inline XBRL `us-gaap:Revenues` |
| Prior-year revenue | $45,043 | FY2025 growth was $20,136, or approximately 44.7% | Same source |
| Weighted-average diluted shares | 899.3 | Evidence for FY2025 diluted EPS; not a valuation-date share count | Form 10-K, Consolidated Statements of Operations; inline XBRL `us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding` |
| Cash and cash equivalents | $7,268 | Enterprise-to-equity value bridge | Form 10-K, Consolidated Balance Sheets; inline XBRL `us-gaap:CashAndCashEquivalentsAtCarryingValue` |
| Current debt | $1,635 | Enterprise-to-equity value bridge | Form 10-K, Consolidated Balance Sheets; inline XBRL `us-gaap:DebtCurrent` |
| Long-term debt | $40,868 | Enterprise-to-equity value bridge | Form 10-K, Consolidated Balance Sheets; inline XBRL `us-gaap:LongTermDebtNoncurrent` |
| Total balance-sheet debt | $42,503 | Current debt plus long-term debt | Calculation from the two filing values above |
| Net debt | $35,235 | Preliminary enterprise-to-equity value bridge | Total debt less cash; calculation from filing values above |

Primary source: [Eli Lilly 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/lly-20251231.htm). Filing metadata: [SEC filing index](https://www.sec.gov/Archives/edgar/data/59478/000005947826000013/).

## Consequential assumptions

These are hypotheses to test, not established facts:

1. Demand for Lilly's diabetes and obesity medicines can support durable volume growth after the initial adoption surge.
2. Manufacturing capacity can expand quickly enough to convert demand into revenue without unacceptable execution costs or shortages.
3. Net pricing will remain sufficient despite payer negotiation, competitive entrants, rebates, and broader access efforts.
4. Revenue growth will translate into sustainable operating cash flow and margin expansion rather than being absorbed by manufacturing, commercialization, and R&D spending.
5. Pipeline productivity and lifecycle management will offset patent, concentration, and single-franchise risks over the valuation horizon.
6. The valuation-date diluted share count can be estimated without material dilution beyond currently disclosed equity awards.
7. Cash and debt can be normalized into a complete enterprise-value bridge after reviewing investments, leases, pensions, noncontrolling interests, and other non-operating claims.

## Unknowns

- The market price and fully diluted security count to use on September 1, 2026.
- The growth, margin, reinvestment, and terminal assumptions implied by that market price.
- Product-level volume, realized net price, geographic mix, and payer-access outlook.
- Capacity ramp timing, utilization, capital requirements, and execution risk.
- Competitive impact from existing and forthcoming obesity and diabetes therapies.
- Probability-adjusted value of the pipeline and the cost of clinical or regulatory failures.
- Sustainable tax rate, working-capital needs, capital expenditure, and free-cash-flow conversion.
- A normalized enterprise-value bridge and the appropriate cost of capital.
- The fund's required return, maximum position size, risk budget, and time horizon.

## Research plan

1. Fix the valuation-date market data: closing price, basic shares, options and awards, convertibles, cash, debt, and other enterprise-value adjustments.
2. Reconcile three years of reported financials and build product-level revenue, operating-margin, tax, reinvestment, and free-cash-flow forecasts.
3. Model the diabetes and obesity franchise using patient volumes, net pricing, access, supply, market share, persistence, and geographic expansion.
4. Map manufacturing projects and capacity milestones to forecast supply, capital expenditure, and gross-margin outcomes.
5. Build probability-adjusted scenarios for the pipeline, competition, regulation, safety, patent exposure, and pricing pressure.
6. Value Lilly with a DCF and relevant trading/transaction multiples; reconcile enterprise value to equity value and calculate per-share value using a valuation-date diluted count.
7. Produce bull, base, and bear cases with explicit catalysts, falsifiers, sensitivities, expected returns, and downside.
8. Compare the resulting risk-adjusted return with the fund's hurdle rate and alternatives before recommending initiation and position size.

## Risk assessment

**Overall preliminary risk: High.** Lilly's operating momentum is strong, but the investment case may depend on sustaining exceptional growth from a concentrated diabetes and obesity franchise while meeting the expectations embedded in the valuation-date share price. A probability-weighted valuation and current market evidence are still outstanding, so this rating concerns uncertainty and potential loss severity rather than predicting a negative outcome.

| Risk | Preliminary likelihood | Potential impact | Evidence or test required |
|---|---|---|---|
| Valuation / expectations | High | High | Reverse-engineer the growth, margin, and duration implied by the Sept. 1, 2026 market price; compare bull, base, and bear values with the price. |
| Franchise concentration | Medium–high | High | Measure revenue and profit dependence on diabetes and obesity products and model slower adoption, share loss, and indication-level setbacks. |
| Competition | High | High | Compare efficacy, safety, dosing, supply, access, and expected launch timing for incumbent and pipeline competitors. |
| Pricing and payer access | Medium–high | High | Test net-price pressure, rebates, coverage restrictions, government policy, and the trade-off between broader access and unit economics. |
| Manufacturing and supply execution | Medium | High | Map capacity additions, ramp timing, utilization, capital expenditure, shortages, and quality risks to achievable sales volumes. |
| Clinical, regulatory, and safety | Medium | High | Probability-weight major pipeline programs and assess label limitations, trial failures, adverse events, and post-market findings. |
| Margin and cash conversion | Medium | Medium–high | Determine whether manufacturing, commercialization, R&D, working capital, and capital expenditure prevent revenue growth from becoming free cash flow. |
| Balance sheet / capital allocation | Low–medium | Medium | Reconcile the $42.503 billion debt balance, $7.268 billion cash balance, maturity schedule, interest burden, and acquisition or shareholder-return plans. |
| Dilution / share-count error | Medium | Medium | Replace the 899.3 million FY2025 weighted-average diluted share count with a valuation-date fully diluted count, including equity awards and other claims. |

The watch/defer decision changes only after the research establishes an adequate margin of safety under the base case and tolerable permanent-loss exposure under the bear case.

## Partner-generated falsification question

> What FY2026–2028 evidence would demonstrate that Lilly's obesity and diabetes franchise cannot sustain the volume growth, pricing, and margin expansion required to justify its valuation?

No answer is supplied in Edition A; the question is reserved for subsequent research and testing.
