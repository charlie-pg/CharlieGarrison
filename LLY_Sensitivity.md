# Lab 11 - Eli Lilly Sensitivity Analysis

## Question
Which assumptions drive Eli Lilly's forecast and value, and what explains their effects?

## Drivers Tested

| Driver | Low | Base | High | Reason |
|---|---:|---:|---:|---|
| Revenue growth | Base - 5 percentage points | Base | Base + 5 percentage points | Tests slower or faster growth than my base forecast. |
| Gross margin | 81.0% | 83.0% | 85.0% | Tests the effect of lower or higher profitability on each dollar of revenue. |

Revenue growth base path for 2026-2030: 32%, 20%, 15%, 12%, 10%.

## What-If Results

Base 2030 operating profit: $66,588.8 million.

| Driver | Operating Profit Span |
|---|---:|
| Revenue growth | $28,485.8 million |
| Gross margin | $4,651.6 million |

Over these ranges, revenue growth was the larger driver of 2030 operating profit.

Higher revenue growth increases revenue throughout the forecast and compounds across multiple years, which then increases gross profit and operating profit. Gross margin also affects operating profit, but its effect was smaller over the range I tested.

FCFE and value per share are unavailable because my complete linked Lilly balance sheet and financing model from Lab 10 was unresolved. I did not create a terminal value or cash flow that my existing model could not support.

## Restored Base Check
Base before sensitivity: $66,588.8 million operating profit.

Base after sensitivity: $66,588.8 million operating profit.

Difference: $0.0 million.

Restored base check: PASS.

## Locked Changed-Input Record
I expected higher revenue growth to increase operating profit because higher revenue flows through gross profit and operating profit. The pre-run timestamped lock was not completed before the sensitivity was run, so I am recording that limitation rather than claiming it was locked beforehand.

Actual result: revenue growth produced a $28,485.8 million operating-profit span over the tested range.

## Partner Review
Partner question received: My partner asked why I expected revenue growth to have a larger effect on Lilly's results than gross margin.

My response: Revenue growth affects the entire revenue base and compounds across the forecast years. Gross margin also affects operating profit, but over the ranges I tested its effect was smaller.


Check I performed on my partner's analysis:  My partner's company was Amazon. We discussed free cash flow as one of the main drivers of his valuation, and I checked how changes in his operating assumptions would flow through to free cash flow.

Note: My partner left before we completed the final sensitivity-result comparison.

## Reflection
Revenue growth mattered most over the ranges I tested. The size of the difference surprised me because the revenue-growth span was much larger than the gross-margin span. This ranking depends on the ranges I chose and does not mean revenue growth will always be the more important driver.