import pandas as pd
import yfinance as yf

tickers = pd.read_csv("tickers.csv")

rows = []

for symbol in tickers["Symbol"]:

    try:

        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="1mo")
        income = ticker.income_stmt
        balance = ticker.balance_sheet

        # EBIT approximation
        ebit = income.loc["EBIT"].iloc[0] if "EBIT" in income.index else income.loc["Operating Income"].iloc[0]

        total_assets = balance.loc["Total Assets"].iloc[0]
        current_liab = balance.loc["Current Liabilities"].iloc[0]

        capital_employed = total_assets - current_liab

        roce = (ebit / capital_employed) * 100
        rows.append({
            "Symbol": symbol,
            "Price": info.get("currentPrice"),
           "Market Cap (₹ Cr)": round( info.get("marketCap") / 1e7, 0 ) if info.get("marketCap") is not None else None,
            "PE": info.get("trailingPE"),
            "ForwardPE": info.get("forwardPE"),
            "PB": info.get("priceToBook"),
             "ROE (%)": round( info.get("returnOnEquity") * 100, 2 ) if info.get("returnOnEquity") is not None else None,
            "ROCE (%)": round(roce, 2) if roce is not None else None,
            "DebtToEquity": info.get("debtToEquity"),
            # "DividendYield": info.get("dividendYield"),
            # "RevenueGrowth": info.get("revenueGrowth"),
            # "EarningsGrowth": info.get("earningsGrowth"),
            "30D High": hist["High"].max() if not hist.empty else None,
            "30D Low": hist["Low"].min() if not hist.empty else None,
            "52WeekHigh": info.get("fiftyTwoWeekHigh"),
            "52WeekLow": info.get("fiftyTwoWeekLow")
        })

        print(f"Success: {symbol}")

    except Exception as e:

        print(f"Failed: {symbol}")
        print(e)

df = pd.DataFrame(rows)

df.to_csv("stocks.csv", index=False)