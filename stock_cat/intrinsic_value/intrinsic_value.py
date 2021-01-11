from typing import Union, List, Any

import numpy as np
from alpha_vantage.fundamentaldata import FundamentalData
from pandas import DataFrame

from stock_cat.alpha_vantage_ext.fundamentals_extensions import get_earnings_annual

ListTable = List[List[Any]]
DictTable = List[dict]


class IntrinsicValueRecipe:
    __summary_keys = ['Symbol', 'Name', 'Exchange', 'Currency', 'EPS', 'Beta', 'PERatio',
                      '200DayMovingAverage', '50DayMovingAverage']

    def __init__(self, ticker: str, av_api_key: str) -> None:
        self.__ticker = ticker
        self.__av_api_key = av_api_key

        fundamental_data = FundamentalData(key=av_api_key)
        # The current version of alpha_vantage library doesn't have all Alpha Vantage API. Adding the missing
        # get_earnings_annual method to the created FundamentalData object here so we can still use the Earnings API
        fundamental_data.get_earnings_annual = get_earnings_annual

        self.__fundamentals = fundamental_data

    def get_ticker_fundamentals(self, as_table: False) -> Union[dict, ListTable]:
        overview, _ = self.__fundamentals.get_company_overview(symbol=self.__ticker)

        if as_table:
            return [[x, overview[x]] for x in self.__summary_keys]
        return {x: overview[x] for x in self.__summary_keys}

    def get_past_eps_trend(self, max_years=10) -> DataFrame:
        earnings, _ = self.__fundamentals.get_earnings_annual(self.__fundamentals, self.__ticker)
        trend_len = min(len(earnings), max_years + 1)

        past_eps_trend_df: DataFrame = earnings.head(trend_len).copy(deep=True)
        past_eps_trend_df.insert(2, "epsGrowthPercent", 0.0)

        for i in range(0, len(past_eps_trend_df) - 1):
            past_eps_trend_df.loc[i, 'epsGrowthPercent'] = \
            ((float(past_eps_trend_df.loc[i, 'reportedEPS'])
              / float(past_eps_trend_df.loc[i + 1, 'reportedEPS'])) - 1.0) * 100

        return past_eps_trend_df.head(trend_len - 1)
