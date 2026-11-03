"""Streamlit integration checks using saved SEC data; no network requests."""
from pathlib import Path
from streamlit.testing.v1 import AppTest

root = Path(__file__).parent
app = AppTest.from_file(str(root / "app.py")).run(timeout=60)
assert not app.exception, app.exception
assert app.title[0].value == "Buffett Investor — Lab 18"
assert any("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice." == c.value for c in app.caption)
assert len(app.dataframe) == 1
assert len(app.dataframe[0].value) == 5
assert app.text_area[0].value == (root / "memos/COST.md").read_text()
assert not app.warning
app.text_area[0].set_value(app.text_area[0].value + "\nROE was 40.0%.\n").run(timeout=60)
assert not app.exception, app.exception
assert any("40.0%" in warning.value for warning in app.warning)
app.text_input[0].set_value("JPM").run(timeout=60)
assert not app.exception, app.exception
table = app.dataframe[0].value
assert all(table["Capital Spending"] == "not found")
assert all(table["Owner Earnings"] == "not found")
assert sum("not known" in item.value and "Owner earnings" in item.value or
           "not known" in item.value and "Positive owner earnings" in item.value
           for item in app.markdown) >= 2
print("PASS: COST view, required caption, five rows, saved memo, injected warning, JPM missing-data view.")
