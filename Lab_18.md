# Lab 18 — Legend Investor as Skill

Completed November 3, 2026. Previous lab files were left unchanged.

## Reusable skill and application

The `buffett-investor` skill contains YAML name/description metadata, instructions, and a bundled standard-library Python script. The workspace submission copy is [SKILL.md](lab18/buffett-investor/SKILL.md); the discoverable installation is `~/.codex/skills/buffett-investor/`.

The [Streamlit app](lab18/app.py) accepts a ticker, downloads SEC facts, charts owner earnings and net income, displays the financial table, tags and filing provenance, reports three checks, and displays an editable memo with unsupported-number warnings. Saved COST and JPM data can be viewed without another download. Other tickers require a live SEC download; their AI memos can be created with the skill and pasted into the app or saved under `lab18/memos/TICKER.md`.

The app includes the required text directly under its title:

> Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.

## Data and calculation rules

The script downloads company facts directly from [SEC EDGAR](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), without an API key. Requests identify Charlie Garrison and the email supplied during this session in the SEC User-Agent. Contact information is not saved in the data files.

The last five fiscal-year-end dates come from 10-K submissions, rather than the `fy` metadata on comparative XBRL facts. Only `10-K` facts are eligible; quarterly filings and amendments are excluded. Revenue, net income, operating cash flow, and capital spending must have annual durations of 350–380 days, accommodating 52/53-week fiscal years. Equity must be an instant at the fiscal-year-end date. The latest filing wins for a metric and period; professor tag priorities break ties in that filing. Ambiguous conflicting facts cause an error rather than an estimate.

| Metric | Allowed tags, in priority order |
|---|---|
| Revenue | RevenueFromContractWithCustomerExcludingAssessedTax; Revenues |
| Net income | NetIncomeLoss |
| Operating cash flow | NetCashProvidedByUsedInOperatingActivities |
| Capital spending | PaymentsToAcquirePropertyPlantAndEquipment; PaymentsToAcquireProductiveAssets |
| Equity | StockholdersEquity |

ROE = net income / year-end equity. Owner earnings = operating cash flow − capital spending. Missing source values and owner earnings are `not found`; a noncomputable ROE, including nonpositive equity, is `not known`. Missing inputs make the affected check `not known`. The growth check compares the first and last owner earnings; its displayed percentage uses the first year's positive owner earnings as the denominator.

Raw downloads, calculated JSON, and printed Markdown reports are preserved in `lab18/data/`. Every extracted cell records its tag, filing date, accession, and period. The cutoff used for the saved results was November 3, 2026. This is a latest-filing analysis, not an immutable historical SEC snapshot.

## Costco results and professor reference test

All amounts below are USD millions, except ROE. Values come from [the script's COST report](lab18/data/COST_report.md).

| Fiscal-year-end | Net income | Operating cash flow | Capital spending | Year-end equity | Owner earnings | Professor reference | ROE |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2022-08-28 | 5,844 | 7,392 | 3,891 | 20,642 | 3,501 | 3,501 | 28.3% |
| 2023-09-03 | 6,292 | 11,068 | 4,323 | 25,058 | 6,745 | 6,745 | 25.1% |
| 2024-09-01 | 7,367 | 11,339 | 4,710 | 23,622 | 6,629 | 6,629 | 31.2% |
| 2025-08-31 | 8,099 | 13,335 | 5,498 | 29,164 | 7,837 | 7,837 | 27.8% |
| 2026-08-30 | 9,226 | 15,817 | 6,435 | 35,803 | 9,382 | 9,382 | 25.8% |

**Test 1: PASS.** All five owner-earnings values match the professor's reference exactly. ROE is at least 15% every year, owner earnings are positive every year, and first-to-last owner earnings grow 168.0%; all three checks pass. Reference constants exist only in the validation script, never in the downloader, calculations, or app.

COST uses the first-priority revenue and capital-spending tags, together with the required net-income, operating-cash-flow, and equity tags. Each year's exact filing provenance is in the report.

## Missing-data and unsupported-claim tests

**Test 2 — JPM: PASS.** The latest five available annual fiscal ends are December 31, 2021–2025. Neither permitted capital-spending tag supplies the required facts. All five capital-spending and owner-earnings entries are `not found`. Both the positive-owner-earnings and owner-earnings-growth checks are `not known`. The independent ROE check fails because fiscal 2022 ROE is 12.9%. The script does not use an alternative bank-specific spending tag or infer zero spending. See [JPM report](lab18/data/JPM_report.md).

**Test 3 — unsupported 40.0% ROE: PASS.** The saved COST memo has no unsupported numerical tokens. Appending “ROE was 40.0%.” produces a warning identifying `40.0%`, even with the percent sign followed by sentence punctuation. The original saved memo remains unchanged. The app's editor runs the same audit on every edit.

The numerical audit compares normalized numbers and percent units with the script's printed report. It detects absent numerical claims; it does not verify whether an allowed number is attached to the correct year, metric, or unit. Manual review is still necessary.

Machine-readable results for these three assignment tests are saved in [validation.json](lab18/data/validation.json). Six additional extraction tests cover annual-period filtering, latest filing selection, tag priorities and fallback, missing capital spending, nonpositive equity, fiscal-end labels, and numerical auditing.

## Buffett verdict and my trust decision

The AI-selected verdict is **WATCH**. The [short COST business memo](lab18/memos/COST.md) uses only financial numbers printed by the Python script and uses no stock prices. Strong cash generation and ROE justify further research, but the accounting screen does not establish durable competitive advantage or attractive investment value.

**My decision: trust the verdict only as a starting point and verify independently.** I would check the underlying filings, investigate business durability and management's allocation of capital, and consider the limitations of the owner-earnings definition before making an investment decision. Passing the screen is evidence to investigate, not an automatic instruction to own the business.

## Reflection: code versus AI judgment

Code is useful for repeatable rules: selecting eligible periods, keeping missing values visible, applying formulas, retaining source tags, and checking the professor's reference. It can reproduce those calculations without changing its mind to fit a narrative.

AI judgment helps organize the business questions and choose a provisional verdict. It can also overstate what a table proves or attach the right number to the wrong claim. Separating the calculations from the memo makes errors easier to find, but neither a passing test nor a plausible memo replaces independent review.

## Run and verify

From the existing workspace, launch the app with:

```sh
lab18/.venv/bin/python -m streamlit run lab18/app.py
```

Streamlit prints a local URL, normally `http://localhost:8501`; open it in a browser. The included virtual environment has Streamlit installed. To recreate it on another computer:

```sh
python3 -m venv lab18/.venv
lab18/.venv/bin/python -m pip install -r lab18/requirements.txt
```

Refresh data with the app's SEC contact fields or run the script, which prompts for an email:

```sh
python3 lab18/buffett-investor/scripts/buffett.py COST --name "Charlie Garrison" --output lab18/data
python3 lab18/buffett-investor/scripts/buffett.py JPM --name "Charlie Garrison" --output lab18/data
python3 -m unittest discover -s lab18 -p 'test_*.py' -v
python3 lab18/validate_live.py
lab18/.venv/bin/python lab18/check_app.py
```

Live refreshes require internet access and may produce different data after later filings. The professor-reference test deliberately reports a failure if the latest five years eventually move beyond the reference window.

## Errors and submission limits

The sandbox initially blocked network requests; authorized network retries downloaded SEC data and installed dependencies successfully. The skill validator initially lacked PyYAML; it was installed in the isolated environment. A punctuation issue in the numerical warning was found by the injection test and corrected. These did not require modifying previous lab files.

The first Streamlit test exceeded its short startup timeout; rerunning with a longer startup allowance passed. Final Streamlit integration checks passed for the COST view, exact required caption, five-row table, saved memo, injected 40.0% warning, and JPM missing-data view. Streamlit reported no application exceptions. Its testing framework printed a benign missing-ScriptRunContext warning. Dependency consistency and the installed skill's validation also passed. Browser appearance was not manually inspected.

There are no known outstanding assignment failures. The app displays the saved AI memo and supports editing or pasting new memos; it does not call a paid AI API to generate a new verdict on each ticker entry. Qualitative business claims and numerical context still need human review. The number audit cannot establish semantic correctness.
