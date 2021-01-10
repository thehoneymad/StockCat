from typing import Union, List, Any

import yfinance as yf
from yfinance import Ticker

Table = List[List[Any]]


class IntrinsicValueRecipe:
    __summary_keys = ['symbol', 'bid', 'currency', 'previousClose', 'dayHigh', 'dayLow', 'trailingEps']

    def __init__(self, ticker: str) -> None:
        self.__ticker = ticker

    def get_ticker_summary(self, as_table: False) -> Union[dict, Table]:
        yf_ticker: Ticker = yf.Ticker(self.__ticker)
        if as_table:
            return [[x, yf_ticker.info[x]] for x in self.__summary_keys]
        return {x: yf_ticker.info[x] for x in self.__summary_keys}

    def get_intrinsic_value(self):
        pass
