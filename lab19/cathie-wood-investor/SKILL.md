---
name: cathie-wood-investor
description: Analyze SEC annual facts and write a short Cathie Wood-inspired own, watch, or pass memo using printed financial numbers and Lab 19 checks, without stock prices.
---

Adapted from [the professor's FAskills Cathie Wood page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/cathie_wood.md), read November 5, 2026, and [Lab 19](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md). This is a simulated analytical lens, not the investor's actual opinion. Lab 19 limits this adaptation to SEC facts and a short memo rather than the source page's price targets, holdings claims or extensive JSON schema.

Consider disruptive innovation, expanding markets, cost curves, reinvestment and technology convergence as research questions. Historical growth and R&D intensity do not prove future disruption.

Run the bundled script relative to this skill directory:

```sh
python3 scripts/cathie_wood.py COST --name "Your Name" --email "your@email.edu" --output /path/to/data
```

Ask for a real contact name and email if unavailable. No API key. For panel use, read the existing printed panel report so every investor uses the same SEC facts and cutoff; do not download a different dataset for each memo.

Only 10-K facts, excluding amendments and quarterlies. Annual durations span 350–380 days; equity and liabilities are fiscal-end instants. Use submissions' last five fiscal-year-end dates, never comparative-fact fy metadata. Latest filing wins; within it use tag priority. Revenue tags: RevenueFromContractWithCustomerExcludingAssessedTax, then Revenues; capital spending: PaymentsToAcquirePropertyPlantAndEquipment, then PaymentsToAcquireProductiveAssets. Other tags: NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, StockholdersEquity, Liabilities, ResearchAndDevelopmentExpense. Reject ambiguous conflicts. Keep missing values and noncomputable ratios as not known; never estimate or substitute tags. Retain per-cell tag, dates and accession.

Revenue CAGR = (last revenue / first revenue) ** (1/4) - 1 across exactly five fiscal years, requiring a positive initial revenue and nonnegative final revenue; pass at >=15%. Latest R&D / revenue passes at >=5%, requiring positive revenue. Missing inputs remain not known. The 5% growth probe is a sensitivity test; retain the default 15% unless the user explicitly chooses otherwise.

Write a short Markdown memo with **Verdict: OWN**, **Verdict: WATCH**, or **Verdict: PASS**, chosen through AI judgment rather than automatically from the check count. Describe both checks, an interpretation through this lens, the bear case and what additional evidence could change the verdict. Qualify unsupported qualitative ideas as questions or scenarios. Use only financial numbers printed by the script; no stock prices, invented forecasts or confidence scores. Missing evidence must remain explicit.

Audit with the bundled helper:

```sh
python3 scripts/sec_facts.py --audit-memo /path/to/memo.md --report /path/to/data/COST_cathie_report.md
```

For a panel memo use the panel report path instead. Fix or report every unsupported-number warning. The token audit cannot verify year/metric/unit associations or qualitative claims; review those manually.
