import yfinance as yf
import math


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

    def get_history_data(stock_list):
        tickers = yf.Tickers(stock_list)
        return tickers.history(period="1y")["Close"]
