# Lab 19 — Legend Panel

Built November 5, 2026, continuing the completed Lab 18. Earlier lab files, the original app and the installed Buffett skill were preserved. The new app is [lab19/app.py](lab19/app.py); launch this version for Lab 19. No earlier Streamlit entry point was overwritten.

## Assignment and reusable skills

Implemented the professor's [Lab 19 instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md), including all seven checks. New reusable skills:

- [Cathie Wood](lab19/cathie-wood-investor/SKILL.md), adapted from [FAskills Cathie Wood](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/cathie_wood.md).
- [Michael Burry](lab19/michael-burry-investor/SKILL.md), adapted from [FAskills Michael Burry](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md).

Both source pages were read November 5. Both skills passed the skill validator and were installed under `~/.codex/skills/` with matching workspace copies. Each contains its own executable screen and bundled SEC extractor, so it can run independently. The app imports the investor checks and applies them to one shared fact set. Tests verify that the bundled extractors match the canonical [sec_facts.py](lab19/sec_facts.py).

The adaptation keeps Wood's innovation, adoption, cost-curve and reinvestment lens and Burry's cash backing, liabilities, footnotes and bear-case lens. Lab 19's narrower rules govern the actual calculations. The source pages' price targets, forecasts, holdings assertions and extensive JSON output are not imported into this SEC-only exercise. These are simulated analytical perspectives, not the investors' actual opinions.

## Shared facts and validation rules

COST and JPM are recalculated from the preserved Lab 18 raw companyfacts using its November 3, 2026 cutoff and original download timestamps. NVDA is a new SEC download with a November 5, 2026 filing cutoff. Raw NVDA companyfacts, submissions and archives are preserved in [lab19/data](lab19/data). The authorized contact name/email were used in the SEC User-Agent and are not saved in data files or source code.

The same selection rules remain: last five fiscal ends from 10-K submissions, only 10-K facts, no 10-Q or 10-K/A, annual duration 350–380 days, latest filing wins per metric/period, tag priority within that filing, and conflicting eligible facts raise an error. Comparative `fy` labels do not determine the year. Equity and added liabilities are fiscal-end instants. Every source cell retains its tag, start/end, filing date and accession. This is latest-filing analysis with a cutoff, not an immutable historical SEC snapshot.

Allowed tags remain revenue `RevenueFromContractWithCustomerExcludingAssessedTax` then `Revenues`; net income `NetIncomeLoss`; operating cash flow `NetCashProvidedByUsedInOperatingActivities`; capital spending `PaymentsToAcquirePropertyPlantAndEquipment` then `PaymentsToAcquireProductiveAssets`; equity `StockholdersEquity`. Added tags are exactly `Liabilities` and `ResearchAndDevelopmentExpense`. No substitute tags or inferred zero values.

ROE = net income / year-end equity; owner earnings = operating cash flow − capital spending. Revenue CAGR = (last revenue / first revenue)^(1/4) − 1 across five fiscal ends, requiring positive first revenue and nonnegative last revenue. R&D intensity = R&D / revenue, with positive revenue. Liabilities/equity requires positive equity. All missing or noncomputable Lab 19 values display **not known**. Lab 18's original `not found` displays were left untouched. Full-window checks require five years and their required inputs. Latest-year checks require their latest inputs. Year-over-year growth is also shown; the first displayed year is not known because no preceding year is included. CAGR is a separate metric and drives Wood's growth check.

## COST: all seven reference checks match

Computed results are in [COST_report.md](lab19/data/COST_report.md). Reference constants appear only in tests, not the extraction or app logic.

| Investor | Check | Computed result | Reference match |
|---|---|---|---|
| Buffett | ROE >=15% every year | pass | yes |
| Buffett | Positive owner earnings every year | pass | yes |
| Buffett | Owner earnings increased first to last | pass | yes |
| Cathie Wood | Revenue CAGR >=15% | fail; 7.51% | yes |
| Cathie Wood | Latest R&D/revenue >=5% | not known | yes |
| Burry | Operating cash flow >=net income every year | pass | yes |
| Burry | Latest liabilities/equity <=2 | pass; 1.49 rounded | yes |

All five liabilities/equity ratios also match the professor after rounding: **2.11, 1.75, 1.96, 1.64, 1.49**. R&D/revenue is not known in every year; missing R&D is not evidence of no innovation. The prior owner-earnings values still match Lab 18.

Saved AI verdicts: Buffett **WATCH**, Cathie Wood **PASS — decline for now**, Burry **WATCH**. Wood's PASS means passing on the investment under the innovation lens; her growth check fails and R&D remains not known. The [three COST memos](lab19/memos) explain the judgments using only printed numbers. Buffett's completed Lab 18 memo was copied without editing the original. The accounting checks are deterministic; verdicts are AI business judgments, not automatic pass-count rules.

## Cathie Wood threshold probe

**PASS:** lowering only the growth threshold from 15% to 5% changes COST's growth check from fail to pass at the same 7.51% CAGR; R&D stays not known, and Buffett/Burry checks do not change. Resetting the probe restores the default result. The app exposes a temporary checkbox and states that saved memo judgments do not regenerate automatically.

**Threshold retained: 15%, to preserve the professor's innovation screen; the 5% probe demonstrates sensitivity rather than new company evidence.** This line also appears under Wood's memo in the app. A change in screening status does not establish a stronger innovation thesis or automatically justify a different verdict.

## My company: VT's largest holding, verified before selecting it

The user selected **VT**, from the Lab 15 portfolio. [Stock Analysis's VT holdings table](https://stockanalysis.com/etf/vt/holdings/) is dated **September 30, 2026**, accessed November 5, 2026. It ranks **NVIDIA Corporation (NVDA) first at a displayed 4.54%**, followed by Apple at 4.11% and Microsoft at 3.25%. The page identifies Finnhub as provider. This is a dated secondary source; Vanguard's issuer page returned no readable holdings. The selection was verified from the dated table rather than assumed. [Source record](lab19/data/VT_holding_source.json) preserves the date, ranking and limitation. Holdings can change after this date.

NVDA files 10-Ks, so no next-largest-company substitution was needed. [NVDA_report.md](lab19/data/NVDA_report.md) shows fiscal ends January 30, 2022 through January 25, 2026 and full filing provenance.

| Investor | Results | Saved AI verdict |
|---|---|---|
| Buffett | ROE pass; positive owner earnings pass; first-to-last owner earnings growth pass | WATCH |
| Cathie Wood | Revenue CAGR 68.30%: pass; latest R&D/revenue 8.6%: pass | WATCH |
| Burry | Cash flow >=net income every year: fail; latest liabilities/equity 0.315x: pass | WATCH |

Latest operating cash flow is **$102,718.00 million**, below net income of **$120,067.00 million**. The divergence is a research concern, not proof of misconduct. The [NVDA memos](lab19/memos) explain why favorable profitability and growth screens coexist with the cash-conversion concern. All three provisional WATCH verdicts share a research condition but reach it through different checks; identical verdict labels do not mean identical evidence or reasoning.

**Draft bull case:** Positive owner earnings throughout the window and strong recorded growth justify further research into durable earnings power. Reported research intensity also clears the innovation screen, supporting investigation of continued reinvestment.

**Draft bear case:** The cash-backing check fails despite reported profitability. If weaker cash conversion persists, historical growth and a passing liability ratio may give an incomplete view of earnings quality.

## Personal reflection after the partner discussion

I completed the partner discussion with Shrey. My personal decision is that I agree with Buffett: Costco looks like an attractive company worth watching, but I would research its valuation before investing. I would use the three-investor panel for Project 2 only as an initial screening tool, not as a final investment decision.

The NVDA bull and bear cases above remain AI-assisted drafts. This reflection records my own decision about Costco and how I would use the panel; the computed results remain unchanged.

## Verification

- **16 unit tests pass:** annual filtering, filing/tag selection, ambiguity rejection, instant liabilities, missing values, nonpositive equity, CAGR and invalid endpoints, thresholds including equality, all seven COST checks, all five leverage references, 5% probe and default restoration, raw-data NVDA recalculation, matching skill extractors, and numerical auditing of every COST/NVDA memo.
- **Streamlit integration passes:** five-year financial table, seven-row panel, three columns and saved memos, COST and NVDA results, separate unsupported `40.0%` injection in each investor memo, probe and reset, JPM missing capital spending, and an unavailable ticker. No application exceptions. The test runner prints a benign missing-ScriptRunContext warning.
- **All six saved memos:** no unsupported numerical tokens; injecting `ROE was 40.0%.` is flagged. Machine-readable evidence: [validation.json](lab19/data/validation.json).
- **Both skills validate** and installed copies match. Earlier tracked lab/app files have no git diff.

The number audit checks normalized tokens and percent units against the printed report. It cannot confirm the right metric, year, scale or unit association, and cannot verify qualitative claims. Source context still needs human review. The app displays editable saved AI memos; it does not call a paid AI API. Downloads preserve edits; editing the textbox alone does not save to disk. Browser appearance has not been manually inspected.

## Run and reproduce

From the workspace:

```sh
lab18/.venv/bin/python -m streamlit run lab19/app.py
python3 lab19/validate.py
lab18/.venv/bin/python lab19/check_app.py
```

The first command prints a local browser URL. Enter COST or NVDA to load saved results without network access; JPM demonstrates missing inputs. For a fresh environment, create `lab19/.venv` and install `lab19/requirements.txt`.

For a live refresh, enter your contact details in the sidebar, or run the extractor (it prompts for your email):

```sh
python3 lab19/sec_facts.py NVDA --name "Charlie Garrison" --output lab19/data
```

Live refreshes can change the fiscal window and reference results. The validation command deliberately rebuilds COST/JPM from preserved Lab 18 inputs and does not redownload NVDA. The standalone extractor prints the financial report and Buffett checks; the app assembles all seven investor checks through `panel.py`. The standalone new-skill scripts print their own checks and support the memo audit.

## What I still need to do manually

1. Open the new app and inspect COST and NVDA side by side; review each memo's interpretation and numerical context. Restart Codex if the newly installed skills are not yet listed.
2. Explain Wood's `checks` function in [cathie_wood.py](lab19/cathie-wood-investor/scripts/cathie_wood.py) to a partner line by line without AI, including missing-input behavior. Discuss what each lens would do during a sell-off without claiming actual investor trades.
3. Partner discussion with Shrey and my personal screening decision are complete, as recorded above. Review the draft NVDA bull/bear wording and the threshold-probe explanation before submission.
4. Complete the Lab 19 Brightspace quiz and individually submit GitHub links to this document, app, skills and supporting files. The quiz and Brightspace submission remain manual tasks.

No known automated assignment check remains failing. Browser review, any remaining code-explanation work and submission remain manual tasks.
