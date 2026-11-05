"""One SEC fact set, three independent accounting screens."""
import sys
from pathlib import Path
from sec_facts import render_report

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "cathie-wood-investor/scripts"))
sys.path.insert(0, str(ROOT / "michael-burry-investor/scripts"))
import cathie_wood
import michael_burry

INVESTORS = ("Buffett", "Cathie Wood", "Burry")


def panel_checks(result, growth_threshold=cathie_wood.GROWTH_THRESHOLD):
    return {"Buffett": result["checks"], "Cathie Wood": cathie_wood.checks(result, growth_threshold),
            "Burry": michael_burry.checks(result)}


def panel_report(result, growth_threshold=cathie_wood.GROWTH_THRESHOLD):
    lines = [render_report(result), "## Legend panel", "| Investor | Check | Result |", "|---|---|---|"]
    for investor, checks in panel_checks(result, growth_threshold).items():
        lines.extend(f"| {investor} | {check} | {status} |" for check, status in checks.items())
    return "\n".join(lines) + "\n"
