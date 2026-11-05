"""Lab 19's forensic screen; these checks cannot establish accounting integrity."""
import argparse
from pathlib import Path
from sec_facts import download, numeric, NOT_KNOWN, render_report


def checks(result):
    rows = result["rows"]
    complete = len(rows) == 5 and all(numeric(r["operating_cash_flow"]) and numeric(r["net_income"]) for r in rows)
    leverage = rows[-1]["liabilities_to_equity"] if rows else NOT_KNOWN
    return {
        "Operating cash flow at least net income every year":
            ("pass" if all(r["operating_cash_flow"] >= r["net_income"] for r in rows) else "fail") if complete else NOT_KNOWN,
        "Latest liabilities no more than twice equity":
            ("pass" if leverage <= 2 else "fail") if numeric(leverage) else NOT_KNOWN,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker")
    parser.add_argument("--name", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = download(args.ticker, args.name, args.email, args.output)
    report = render_report(result) + "\nBurry checks:\n" + "\n".join(f"- {k}: {v}" for k, v in checks(result).items()) + "\n"
    (args.output / f"{result['ticker']}_burry_report.md").write_text(report)
    print(report)
