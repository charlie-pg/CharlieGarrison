"""Offline integration test, including one attack in each investor memo."""
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).parent
app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=60)
assert not app.exception, app.exception
assert len(app.columns) == 3
assert len(app.text_area) == 3
assert len(app.dataframe[0].value) == 5
assert list(app.dataframe[1].value["Result"]) == ["pass", "pass", "pass", "fail", "not known", "pass", "pass"]
assert not app.warning
for index in range(3):
    old = app.text_area[index].value
    app.text_area[index].set_value(old + "\nROE was 40.0%.").run(timeout=60)
    assert not app.exception, app.exception
    assert any("40.0%" in w.value for w in app.warning)
    app.text_area[index].set_value(old).run(timeout=60)
assert not app.warning
app.checkbox[0].check().run(timeout=60)
assert list(app.dataframe[1].value["Result"])[3:5] == ["pass", "not known"]
app.checkbox[0].uncheck().run(timeout=60)
assert list(app.dataframe[1].value["Result"])[3:5] == ["fail", "not known"]
app.text_input[0].set_value("NVDA").run(timeout=60)
assert not app.exception, app.exception
assert list(app.dataframe[1].value["Result"]) == ["pass", "pass", "pass", "pass", "pass", "fail", "pass"]
assert all("Verdict: WATCH" in memo.value for memo in app.text_area)
assert not app.warning
app.text_input[0].set_value("JPM").run(timeout=60)
assert not app.exception, app.exception
assert all(app.dataframe[0].value["Capital Spending"] == "not known")
app.text_input[0].set_value("UNKNOWN").run(timeout=60)
assert not app.exception, app.exception
assert any("No saved SEC data" in i.value for i in app.info)
print("PASS: COST and NVDA panels, three memo warnings, 5% probe, restored default, JPM gaps, unavailable ticker")
