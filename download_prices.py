
import yfinance as yf
import pandas as pd
from datetime import date

# Four real ETFs for Lab 15
tickers = ["BIL", "IEF", "LQD", "VT"]

# Download daily adjusted prices, then take the last
# available trading price of each completed month.
data = yf.download(
    tickers,
    start="2021-09-01",
    end="2026-10-01",
    auto_adjust=True,
    progress=False,
)

prices = data["Close"].resample("ME").last()

# Use the last 61 completed months:
# 61 prices produce 60 monthly returns (5 years).
prices = prices.dropna().tail(61)
prices = prices[tickers]
prices.index.name = "Date"

if len(prices) < 61:
    raise ValueError(
        f"Only {len(prices)} complete months found; need 61."
    )

prices.to_csv("prices.csv", date_format="%Y-%m-%d")

print("Created prices.csv successfully!")
print("Source: Yahoo Finance via yfinance")
print("Downloaded:", date.today())
print("ETFs:", ", ".join(tickers))
print("Months:", len(prices))
print("First date:", prices.index[0].date())
print("Last date:", prices.index[-1].date())
print(prices.tail())