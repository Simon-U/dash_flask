import yfinance as yf
import pandas as pd


class yahoo_finance:
    def get_indices(list):
        data = []
        for symbol in list:
            stock = yf.Ticker(symbol)
            data.append({"value": symbol, "label": stock.info.get("longName")})
        return data

    def get_performance_today(symbol):
        stock = yf.Ticker(symbol)
        close = stock.info.get("currentPrice")
        stock_info = stock.info
        if close is None:
            stock_hist = stock.history(period="1d")
            close = stock_hist["Close"].item()
            open = stock_hist["Open"].item()
            volume = stock_hist["Volume"].item()
        else:
            close = stock_info.get("currentPrice")
            open = stock_info.get("open")
            volume = stock_info.get("volume")
        performance = round(
            (close - open) / open * 100,
            3,
        )
        change = round(close - open, 2)

        values = {
            "open": round(close, 2),
            "close": round(close, 2),
            "volume": volume,
            "performance": performance,
            "change": change,
            "name": stock_info.get("longName"),
            "currency": stock_info.get("currency"),
            "symbol": stock_info.get("symbol"),
        }

        return values

    def get_history_data(stock_string, stock_list):
        tickers = yf.Tickers(stock_string)
        values = [
            "longName",
            "symbol",
            "currentPrice",
            "targetLowPrice",
            "targetMeanPrice",
            "targetHighPrice",
            "currency",
        ]
        columns = [
            "Company name",
            "Symbol",
            "Current Price",
            "Target Low",
            "Target Mean",
            "Target High",
            "Currency",
        ]
        data = pd.DataFrame(columns=columns)
        if len(stock_list) == 1:
            company_data = [
                tickers.tickers[stock_list[0].get("value")].info.get(item)
                for item in values
            ]
            data.loc[0] = company_data
            return (
                tickers.tickers[stock_list[0].get("value")].history(period="1y")[
                    "Close"
                ],
                data,
            )

        for stock in stock_list:
            company_data = [
                tickers.tickers[stock.get("value")].info.get(item) for item in values
            ]
            position = len(data) + 1
            data.loc[position] = company_data
        return tickers.history(period="1y")["Close"], data
