---
name: buffett-investor
description: Analyze a public US company's SEC 10-K financials and write a short Buffett-style own, watch, or pass business memo using audited script output, without stock prices.
---

Ask for the user's name and email if unavailable; SEC requests must identify both in User-Agent. Never invent contact information. No API key is needed.

Run the bundled script, relative to this skill directory:

```sh
python3 scripts/buffett.py COST --name "Your Name" --email "your@email.edu" --output /path/to/data
```

Use the script's Markdown output as the only source of financial numbers. It downloads SEC ticker metadata, submissions and companyfacts, selects the last five 10-K fiscal-year-end dates, and preserves the raw downloads and per-cell filing provenance. Annual duration facts must span 350–380 days (including 52/53-week years). Do not use the fact's `fy` field to label comparative years. Only 10-K is eligible, excluding 10-Q and 10-K/A. For a given metric and period, the latest filing wins; tag priority breaks ties within that filing. Missing values stay `not found`; ROE with nonpositive equity is `not known`. Never substitute other tags or estimate missing facts.

Write a short Markdown business memo with an AI-chosen **own**, **watch**, or **pass** verdict. Discuss business durability, capital allocation, the script's three checks, and limits of the evidence. Qualify business impressions as judgment; obtain primary-source evidence for factual qualitative claims not established by the output. Do not use stock prices or claim that passing these checks proves attractive valuation. All financial numbers must appear in the script's printed report. If data is incomplete, state that explicitly.

Audit the memo before handing it off:

```sh
python3 scripts/buffett.py --audit-memo /path/to/memo.md --report /path/to/data/COST_report.md
```

The audit is a numerical-token check, not a semantic fact checker: it cannot prove that an allowed number is attached to the correct metric, year, or unit. Review those associations manually. Do not change calculations to fit a reference answer; report discrepancies and unavailable fiscal years honestly.
