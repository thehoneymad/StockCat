from os import getenv

import click
from pandas import DataFrame
from tabulate import tabulate

from stock_cat.intrinsic_value.intrinsic_value import IntrinsicValueRecipe

ALPHAVANTAGE_API_KEY_ENV = 'ALPHAVANTAGE_API_KEY'
ALPHAVANTAGE_API_KEY_URL = 'https://www.alphavantage.co/support/#api-key'


@click.command(name='intrinsic_value')
@click.option('--ticker', prompt='ticker', help='Stock ticker to analyze. For example, MSFT')
def command_intrinsic_value(ticker):
    av_api_key = getenv(ALPHAVANTAGE_API_KEY_ENV)
    if not av_api_key:
        av_api_key = click.prompt(click.style(
            f'Alpha Vantage API key not present in {ALPHAVANTAGE_API_KEY_ENV} env variable. \n'
            f'Please create a new one from {ALPHAVANTAGE_API_KEY_URL} if needed. \n'
            'Enter Alpha Vantage API key', fg='red'), type=str)
        click.echo(click.style(
            f'Execute `export ALPHAVANTAGE_API_KEY={av_api_key}` to stop this prompt.', fg='blue', blink=True))

    recipe = IntrinsicValueRecipe(ticker=ticker, av_api_key=av_api_key)

    click.echo(f'\nFetching {ticker} fundamentals \n')
    fundamentals_table = recipe.get_ticker_fundamentals(as_table=True)
    click.secho(tabulate(fundamentals_table, tablefmt='github'), fg='green')

    click.echo('\nFetching past 10 years EPS trend \n')
    past_eps_trend = recipe.get_past_eps_trend(max_years=10)
    click.secho(tabulate(past_eps_trend, tablefmt='github', headers="keys"), fg='yellow')

    avg_eps_growth_idx = 1
    avg_eps_growth = past_eps_trend.at[avg_eps_growth_idx, 'avgEpsGrowthPercent']

    avg_eps_growth_idx = click.prompt(
        '\nSelect average EPS growth percentage. Select index from the table above. \n'
        f'Current default is at index 0 : {avg_eps_growth}', default=avg_eps_growth_idx, type=int)

    avg_eps_growth = past_eps_trend.at[avg_eps_growth_idx, 'avgEpsGrowthPercent']
    eps = past_eps_trend.at[avg_eps_growth_idx, 'reportedEPS']
    click.secho(f'\nSelected average EPS growth for past 10 years is {avg_eps_growth}% \n', fg='yellow')
    click.secho(f'\nSelected last EPS for past 10 years is {eps}% \n', fg='yellow')

    discount_rate: float = recipe.get_default_discount_rate()
    discount_rate = click.prompt(f'What should be our discount rate?', default=discount_rate, type=float)
    click.secho(f'\nSelected discount rate {discount_rate}%', fg='blue')

    click.echo(f'\nFetching future 10 years EPS trend with last eps {eps} and average eps growth {avg_eps_growth}\n')
    future_eps_trend: DataFrame = recipe.get_future_eps_trend(eps=eps, avg_eps_growth_pct=avg_eps_growth,
                                                              discount_rate=discount_rate, years=75)
    click.secho(tabulate(future_eps_trend, tablefmt='github', headers="keys"), fg='yellow')

    intrinsic_value = recipe.get_intrinsic_value(
        discounted_present_value_series=(future_eps_trend['discountedPresentValue']))

    click.secho(f'\nCalculated intrinsic value of the stock is {intrinsic_value}', fg='red')
