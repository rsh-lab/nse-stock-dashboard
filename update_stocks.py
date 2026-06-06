import pandas as pd
import yfinance as yf

tickers = pd.read_csv("tickers.csv")

rows = []

for symbol in tickers["Symbol"]:

    try:

        ticker = yf.Ticker(symbol)
        info = ticker.info

        rows.append({
            "Symbol": symbol,
            "Price": info.get("currentPrice"),
           "Market Cap (₹ Cr)": round( info.get("marketCap") / 1e7, 0 ) if info.get("marketCap") is not None else None,
            "PE": info.get("trailingPE"),
            "ForwardPE": info.get("forwardPE"),
            "PB": info.get("priceToBook"),
             "ROE (%)": round( info.get("returnOnEquity") * 100, 2 ) if info.get("returnOnEquity") is not None else None,
            "DebtToEquity": info.get("debtToEquity"),
            "DividendYield": info.get("dividendYield"),
            "RevenueGrowth": info.get("revenueGrowth"),
            "EarningsGrowth": info.get("earningsGrowth"),
            "52WeekHigh": info.get("fiftyTwoWeekHigh"),
            "52WeekLow": info.get("fiftyTwoWeekLow")
        })

        print(f"Success: {symbol}")

    except Exception as e:

        print(f"Failed: {symbol}")
        print(e)

df = pd.DataFrame(rows)

df.to_csv("stocks.csv", index=False)