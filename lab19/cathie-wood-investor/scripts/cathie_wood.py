"""Lab 19's innovation screen; judgment belongs in a separate memo."""
import argparse
from pathlib import Path
from sec_facts import download, numeric, NOT_KNOWN, render_report

GROWTH_THRESHOLD = 0.15
RD_THRESHOLD = 0.05


def checks(result, growth_threshold=GROWTH_THRESHOLD):
    growth = result["revenue_cagr"]
    latest = result["rows"][-1] if result["rows"] else {}
    rd = latest.get("rd_to_revenue", NOT_KNOWN)
    return {
        f"Annualized revenue growth at least {growth_threshold:.0%}":
            ("pass" if growth >= growth_threshold else "fail") if numeric(growth) else NOT_KNOWN,
        f"Latest R&D/revenue at least {RD_THRESHOLD:.0%}":
            ("pass" if rd >= RD_THRESHOLD else "fail") if numeric(rd) else NOT_KNOWN,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker")
    parser.add_argument("--name", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = download(args.ticker, args.name, args.email, args.output)
    report = render_report(result) + "\nCathie Wood checks:\n" + "\n".join(f"- {k}: {v}" for k, v in checks(result).items()) + "\n"
    (args.output / f"{result['ticker']}_cathie_report.md").write_text(report)
    print(report)
