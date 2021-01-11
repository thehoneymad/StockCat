from alpha_vantage.alphavantage import AlphaVantage as av

@av._output_format
@av._call_api_on_func
def get_earnings_annual(self, symbol):
    """
    This API returns the annual and quarterly earnings (EPS) for the company of interest in an annual basis.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    _FUNCTION_KEY = 'EARNINGS'
    return _FUNCTION_KEY, 'annualEarnings', 'symbol'
