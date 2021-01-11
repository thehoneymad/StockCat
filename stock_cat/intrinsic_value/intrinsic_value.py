import math
from datetime import datetime
from typing import Union, List, Any

import pandas
from alpha_vantage.fundamentaldata import FundamentalData
from pandas import DataFrame, Series

from stock_cat.alpha_vantage_ext.fundamentals_extensions import get_earnings_annual

ListTable = List[List[Any]]
DictTable = List[dict]


class IntrinsicValueRecipe:
    __summary_keys = ['Symbol', 'Name', 'Exchange', 'Currency', 'EPS', 'Beta', 'PERatio',
                      '200DayMovingAverage', '50DayMovingAverage']
    ___eps_growth_avg_window_years: int = 3

    # Discount rates can be also calculated automatically. For now, for simplicity we are using a hard coded
    # 9%. I haven't learned the intricacies to compute it better.
    # TODO: Implement an automated discount rate calculation method.
    ___default_discount_rate_percent: float = 9.0

    def __init__(self, ticker: str, av_api_key: str) -> None:
        self.__ticker = ticker
        self.__av_api_key = av_api_key

        fundamental_data = FundamentalData(key=av_api_key)
        # The current version of alpha_vantage library doesn't have all Alpha Vantage API. Adding the missing
        # get_earnings_annual method to the created FundamentalData object here so we can still use the Earnings API
        fundamental_data.get_earnings_annual = get_earnings_annual

        self.__fundamentals = fundamental_data

    def get_default_discount_rate(self) -> float:
        return self.___default_discount_rate_percent

    def get_ticker_fundamentals(self, as_table: bool = False) -> Union[dict, ListTable]:
        overview, _ = self.__fundamentals.get_company_overview(symbol=self.__ticker)

        if as_table:
            return [[x, overview[x]] for x in self.__summary_keys]
        return {x: overview[x] for x in self.__summary_keys}

    def get_past_eps_trend(self, max_years: int = 10) -> DataFrame:
        earnings, _ = self.__fundamentals.get_earnings_annual(self.__fundamentals, self.__ticker)
        trend_len = min(len(earnings), max_years + 1)

        past_eps_trend_df: DataFrame = earnings.head(trend_len).copy(deep=True)
        past_eps_trend_df['reportedEPS'] = past_eps_trend_df['reportedEPS'].astype(float)
        past_eps_trend_df.insert(len(past_eps_trend_df.columns), 'epsGrowthPercent', 0.0)
        past_eps_trend_df.insert(len(past_eps_trend_df.columns), 'avgEpsGrowthPercent', 0.0)

        for i in range(0, len(past_eps_trend_df) - 1):
            past_eps_trend_df.loc[i, 'epsGrowthPercent'] = \
                ((past_eps_trend_df.loc[i, 'reportedEPS'] / past_eps_trend_df.loc[i + 1, 'reportedEPS']) - 1.0) * 100

        for i in range(0, len(past_eps_trend_df) - self.___eps_growth_avg_window_years):
            past_eps_trend_df.loc[i, 'avgEpsGrowthPercent'] = \
                past_eps_trend_df.loc[i:i + self.___eps_growth_avg_window_years, 'epsGrowthPercent'].mean()

        ret = past_eps_trend_df.head(trend_len - 1)
        return ret

    def get_future_eps_trend(self, eps: float, avg_eps_growth_pct: float, discount_rate: float,
                             years: int = 75) -> DataFrame:
        curr_year: int = datetime.now().year
        future_years = [curr_year + x for x in range(0, years)]
        future_eps: list[float] = []
        discounted_present_values: list[float] = []

        curr_eps = eps
        curr_avg_eps_growth_pct = avg_eps_growth_pct
        for i in range(len(future_years)):
            computed_eps = curr_eps + curr_eps * (curr_avg_eps_growth_pct / 100)
            future_eps.append(computed_eps)
            # Present discounted EPS value = Future Value / (1+discount_rate)^n
            discounted_present_value = computed_eps / math.pow(1 + discount_rate / 100, i + 1)
            discounted_present_values.append(discounted_present_value)
            curr_eps = computed_eps
            if i % 10 == 0:
                # Divide current eps growth pct to 70% of its actual value to be pessimistic here
                curr_avg_eps_growth_pct = curr_avg_eps_growth_pct * 0.70

        data = {
            'years': future_years,
            'futureEps': future_eps,
            'discountedPresentValue': discounted_present_values
        }

        return pandas.DataFrame(data)

    def get_intrinsic_value(self, discounted_present_value_series: Series):
        return discounted_present_value_series.sum()
