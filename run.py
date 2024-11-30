import yfinance as yf
import pandas as pd
from datetime import datetime, date

# Get S&P 500 YTD Return
sp500_ticker = "^GSPC"
sp500 = yf.Ticker(sp500_ticker)

today = date.today()
start_of_year = date(today.year, 1, 1)

sp500_hist = sp500.history(start=start_of_year, end=today)

sp500_start_price = sp500_hist['Close'].iloc[0]
sp500_end_price = sp500_hist['Close'].iloc[-1]
sp500_return = (sp500_end_price - sp500_start_price) / sp500_start_price

print(f"S&P 500 YTD Return: {sp500_return:.2%}")

# Get List of S&P 500 Companies
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
tables = pd.read_html(url)
sp500_companies = tables[0]
tickers = sp500_companies['Symbol'].tolist()
tickers = [ticker.replace('.', '-') for ticker in tickers]

# Find Underperforming Stocks
underperformers = []

for ticker in tickers:
    print(ticker)
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_of_year, end=today)

        if hist.empty:
            continue

        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        stock_return = (end_price - start_price) / start_price

        if stock_return < sp500_return:
            underperformers.append((ticker, stock_return))
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        continue

# Sort list of underperformers by return
underperformers = sorted(underperformers, key=lambda x: x[1], reverse=True)

# Display Results
print("\nStocks that underperformed the S&P 500 YTD:")
for ticker, ret in underperformers:
    print(f"{ticker}: {ret:.2%}")

# Output results to file
with open('output.txt', 'w+') as f:
    for ticker, ret in underperformers:
        f.write(f"{ticker}: {ret:.2%}\n")

