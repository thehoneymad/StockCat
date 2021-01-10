from typing import Union, List, Any

from alpha_vantage.fundamentaldata import FundamentalData

Table = List[List[Any]]


class IntrinsicValueRecipe:
    __summary_keys = ['Symbol', 'Name', 'Exchange', 'Currency', 'EPS', 'Beta', 'PERatio',
                      '200DayMovingAverage', '50DayMovingAverage']

    def __init__(self, ticker: str, av_api_key: str) -> None:
        self.__ticker = ticker
        self.__av_api_key = av_api_key
        self.__fundamentals = FundamentalData(key=av_api_key)

    def get_ticker_fundamentals(self, as_table: False) -> Union[dict, Table]:
        overview, _ = self.__fundamentals.get_company_overview(symbol=self.__ticker)

        if as_table:
            return [[x, overview[x]] for x in self.__summary_keys]
        return {x: overview[x] for x in self.__summary_keys}

    def get_intrinsic_value(self):
        pass
