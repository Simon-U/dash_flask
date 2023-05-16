import datetime

import yfinance as yf
import pandas as pd


def normalize_officer(data):
    return [
        [officer.get("name"), officer.get("title")]
        for officer in data.get("companyOfficers")
    ]


class yahoo_finance:
    def get_indices(list):
        """_summary_
        List of indec
        Args:
            list (list): Symbols for the indecies

        Returns:
            dict: Returns dicktionary with the Symbol and name
        """
        data = []
        for symbol in list:
            stock = yf.Ticker(symbol)
            data.append({"value": symbol, "label": stock.info.get("longName")})
        return data

    def get_performance_today(symbol):
        """_summary_
        Calculates the stocks performance based on the symbol
        Args:
            symbol (string): Symbol for the stock/index

        Returns:
            dict: Returns dict with different values
        """
        stock = yf.Ticker(symbol)
        close = stock.info.get("bid")
        stock_info = stock.info
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
        return values

    def get_history_data(stock_list):
        """_summary_
        Method to retrieve the data for the historic data plot in the index page
        Args:
            stock_list (list): List of the stocks mentioned in the string

        Returns:
            dataframe: _description_
        """
        stock_string = " ".join([dict.get("value") for dict in stock_list])
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
        """_summary_
        MEthod to retrive different values fabout a certain company
        Args:
            value_inputs (dict): values you with to retrive
            stock_symbol (string): Company symbol

        Returns:
            returns: Dictinary with the selected values
        """
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
        """_summary_
        Method to return the current stock data within a 1 day moving frame and a 1m intervall
        Args:
            symbol (string): Company symbol

        Returns:
            dataframe: the timeseries
        """
        stock = yf.Ticker(symbol)

        stock_history = stock.history(period="1d", interval="1m")
        return stock_history
