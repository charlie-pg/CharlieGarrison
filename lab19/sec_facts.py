"""SEC-only financial extraction and deterministic checks; Python standard library."""
import argparse
from datetime import date, datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
import re
import time
from urllib.request import Request, urlopen

TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
    "equity": ["StockholdersEquity"],
    "liabilities": ["Liabilities"],
    "research_and_development": ["ResearchAndDevelopmentExpense"],
}
NOT_FOUND = "not known"
NOT_KNOWN = "not known"


def get_json(url, user_agent):
    time.sleep(0.2)  # Sequential requests, comfortably below SEC's rate limit.
    request = Request(url, headers={"User-Agent": user_agent, "Accept": "application/json"})
    with urlopen(request, timeout=45) as response:
        return json.load(response)


def annual_records(block, as_of):
    return [dict(zip(block, values)) for values in zip(*block.values())
            if dict(zip(block, values)).get("form") == "10-K"
            and dict(zip(block, values)).get("filingDate", "9999") <= as_of]


def fiscal_ends(records):
    return sorted({r["reportDate"] for r in records if r.get("reportDate")})[-5:]


def choose_fact(facts, metric, end, as_of):
    candidates = []
    for priority, tag in enumerate(TAGS[metric]):
        for fact in facts.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", []):
            if fact.get("form") != "10-K" or fact.get("end") != end or fact.get("filed", "9999") > as_of:
                continue
            if metric not in {"equity", "liabilities"}:
                if not fact.get("start"):
                    continue
                days = (date.fromisoformat(end) - date.fromisoformat(fact["start"])).days
                if not 350 <= days <= 380:
                    continue
            elif fact.get("start"):
                continue
            candidates.append((fact.get("filed", ""), -priority, fact.get("accn", ""), tag, fact))
    if not candidates:
        return {"value": NOT_FOUND, "tag": NOT_FOUND}
    newest = max(candidates, key=lambda x: x[:3])
    same = [c for c in candidates if c[:3] == newest[:3]]
    if len({(c[4].get("start"), c[4]["val"]) for c in same}) > 1:
        raise ValueError(f"Ambiguous SEC facts for {metric} ending {end}; inspect raw data.")
    fact = newest[4]
    return {"value": fact["val"], "tag": newest[3], "filed": fact["filed"],
            "accession": fact.get("accn"), "start": fact.get("start"), "end": end}


def numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def analyze(facts, ends, ticker, as_of):
    rows = []
    for end in ends:
        cells = {metric: choose_fact(facts, metric, end, as_of) for metric in TAGS}
        row = {"fiscal_year_end": end, "sources": cells}
        row.update({metric: cell["value"] for metric, cell in cells.items()})
        ni, eq, ocf, capex = (row[m] for m in ("net_income", "equity", "operating_cash_flow", "capital_spending"))
        row["roe"] = ni / eq if numeric(ni) and numeric(eq) and eq > 0 else NOT_KNOWN
        row["owner_earnings"] = ocf - capex if numeric(ocf) and numeric(capex) else NOT_FOUND
        rows.append(row)
    for index, row in enumerate(rows):
        previous = rows[index - 1]["revenue"] if index else NOT_KNOWN
        current = row["revenue"]
        row["revenue_growth"] = current / previous - 1 if numeric(current) and numeric(previous) and previous > 0 else NOT_KNOWN
        rd = row["research_and_development"]
        row["rd_to_revenue"] = rd / current if numeric(rd) and numeric(current) and current > 0 else NOT_KNOWN
        liabilities, equity = row["liabilities"], row["equity"]
        row["liabilities_to_equity"] = liabilities / equity if numeric(liabilities) and numeric(equity) and equity > 0 else NOT_KNOWN
    roe = [r["roe"] for r in rows]
    oe = [r["owner_earnings"] for r in rows]
    complete = len(rows) == 5
    checks = {
        "ROE at least 15% every year": ("pass" if all(x >= .15 for x in roe) else "fail")
        if complete and all(map(numeric, roe)) else NOT_KNOWN,
        "Positive owner earnings every year": ("pass" if all(x > 0 for x in oe) else "fail")
        if complete and all(map(numeric, oe)) else NOT_KNOWN,
        "Owner earnings growth, first to last year": ("pass" if oe[-1] > oe[0] else "fail")
        if complete and numeric(oe[0]) and numeric(oe[-1]) else NOT_KNOWN,
    }
    revenues = [r["revenue"] for r in rows]
    revenue_cagr = (revenues[-1] / revenues[0]) ** .25 - 1 if complete and numeric(revenues[0]) and numeric(revenues[-1]) and revenues[0] > 0 and revenues[-1] >= 0 else NOT_KNOWN
    growth = (oe[-1] / oe[0] - 1) if complete and numeric(oe[0]) and numeric(oe[-1]) and oe[0] > 0 else NOT_KNOWN
    return {"ticker": ticker, "entity": facts.get("entityName", ticker), "as_of": as_of,
            "rows": rows, "checks": checks, "revenue_cagr": revenue_cagr, "owner_earnings_growth": growth,
            "downloaded_at": datetime.now(timezone.utc).isoformat()}


def display_value(value, percent=False):
    if not numeric(value):
        return value
    return f"{value * 100:.1f}%" if percent else f"{value / 1_000_000:,.2f}"


def render_report(result):
    metrics = list(TAGS) + ["owner_earnings", "roe", "revenue_growth", "rd_to_revenue", "liabilities_to_equity"]
    lines = [f"# {result['ticker']} — {result['entity']}",
             f"As of {result['as_of']}. USD millions; ROE, revenue growth and R&D/revenue in percent; liabilities/equity in multiples. No stock prices.",
             "| Fiscal-year-end | " + " | ".join(m.replace('_', ' ') for m in metrics) + " |",
             "|---|" + "---|" * len(metrics)]
    for row in result["rows"]:
        lines.append("| " + row["fiscal_year_end"] + " | " + " | ".join((f"{row[m]:.3f}x" if m == "liabilities_to_equity" and numeric(row[m]) else display_value(row[m], m in {"roe", "revenue_growth", "rd_to_revenue"})) for m in metrics) + " |")
    lines += ["", "Checks:"] + [f"- {k}: **{v}**" for k, v in result["checks"].items()]
    lines += [f"- Annualized revenue growth (first to last): {(f"{result['revenue_cagr'] * 100:.2f}%" if numeric(result['revenue_cagr']) else NOT_KNOWN)}", f"- Owner earnings growth: {display_value(result['owner_earnings_growth'], True)}", "", "XBRL tags and filing provenance:"]
    for row in result["rows"]:
        lines.append(f"\n{row['fiscal_year_end']}:")
        for metric, source in row["sources"].items():
            lines.append(f"- {metric}: {source['tag']} (filed {source.get('filed', NOT_FOUND)}; accession {source.get('accession', NOT_FOUND)}; start {source.get('start') or 'instant'})")
    if len(result["rows"]) < 5:
        lines.append("\nWARNING: Fewer than five annual filings found; checks are not known.")
    return "\n".join(lines) + "\n"


NUMBER = re.compile(r"(?<![\w.])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[ \t]*%)?(?!\w|\.\d|%)")


def number_key(token):
    token = token.strip().replace(',', '').replace('−', '-').replace(' ', '')
    percent = token.endswith('%')
    return Decimal(token.rstrip('%')), percent


def unsupported_numbers(memo, report):
    allowed = {number_key(m.group()) for m in NUMBER.finditer(report)}
    return sorted({m.group().strip() for m in NUMBER.finditer(memo) if number_key(m.group()) not in allowed})


def download(ticker, name, email, output, as_of=None):
    if not name.strip() or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise ValueError("Supply your real name and email for the SEC User-Agent.")
    ticker = ticker.strip().upper()
    if not re.fullmatch(r"[A-Z0-9.-]{1,12}", ticker):
        raise ValueError("Enter a valid ticker.")
    as_of = as_of or date.today().isoformat()
    date.fromisoformat(as_of)
    user_agent = f"{name.strip()} {email} FIN439 learning demonstration"
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    tickers = get_json("https://www.sec.gov/files/company_tickers.json", user_agent)
    match = next((v for v in tickers.values() if v["ticker"] == ticker), None)
    if match is None:
        raise ValueError(f"Ticker {ticker} not found in SEC ticker metadata.")
    cik = str(match['cik_str']).zfill(10)
    submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    submissions = get_json(submissions_url, user_agent)
    facts = get_json(facts_url, user_agent)
    records = annual_records(submissions["filings"]["recent"], as_of)
    archives = []
    for extra in submissions["filings"].get("files", []):
        if len(fiscal_ends(records)) >= 5:
            break
        block = get_json("https://data.sec.gov/submissions/" + extra["name"], user_agent)
        archives.append(block)
        records += annual_records(block, as_of)
    result = analyze(facts, fiscal_ends(records), ticker, as_of)
    result["urls"] = {"facts": facts_url, "submissions": submissions_url}
    for suffix, value in [("companyfacts", facts), ("submissions", submissions), ("archives", archives), ("result", result)]:
        (output / f"{ticker}_{suffix}.json").write_text(json.dumps(value, indent=2) + "\n")
    (output / f"{ticker}_report.md").write_text(render_report(result))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker", nargs="?")
    parser.add_argument("--name", default="Charlie Garrison")
    parser.add_argument("--email")
    parser.add_argument("--output", default="lab19/data")
    parser.add_argument("--as-of", help="YYYY-MM-DD; filter filing dates, not a historical SEC snapshot")
    parser.add_argument("--audit-memo", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        if args.audit_memo:
            if not args.report:
                parser.error("--audit-memo requires --report")
            unsupported = unsupported_numbers(args.audit_memo.read_text(), args.report.read_text())
            print("WARNING: Unsupported numerical claims: " + ", ".join(unsupported) if unsupported else "PASS: All numerical tokens appeared in the script report.")
            return 1 if unsupported else 0
        if not args.ticker:
            parser.error("a ticker is required")
        email = args.email or input("Email for SEC User-Agent: ").strip()
        print(render_report(download(args.ticker, args.name, email, args.output, args.as_of)))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
