import yfinance as yf
import pandas as pd
import datetime


def normalize_officer(data):
    return [
        [officer.get("name"), officer.get("title")]
        for officer in data.get("companyOfficers")
    ]


class yahoo_finance:
    def get_indices(list):
        data = []
        for symbol in list:
            stock = yf.Ticker(symbol)
            data.append({"value": symbol, "label": stock.info.get("longName")})
        return data

    def get_performance_today(symbol):
        stock = yf.Ticker(symbol)
        close = stock.info.get("bid")
        stock_info = stock.info
        # print(stock.info)
        stock_hist = stock.history(
            period="1d",
        )
        if stock_hist.index[0].date() == datetime.datetime.today().date():
            traded = True
        else:
            traded = False
        close = stock_hist["Close"].item()
        open = stock_hist["Open"].item()
        volume = stock_hist["Volume"].item()

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
            "traded": traded,
        }
        # print(values)
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

    def get_company_data(value_inputs, stock_symbol):
        stock = yf.Ticker(stock_symbol)
        stock_info = stock.info

        data = {
            value: (
                normalize_officer(stock_info)
                if value == "companyOfficers"
                else stock_info.get(value)
            )
            for value in value_inputs
        }

        return data

    def get_current_company_price(symbol):
        stock = yf.Ticker(symbol)

        stock_history = stock.history(period="1d", interval="1m")
        return stock_history
