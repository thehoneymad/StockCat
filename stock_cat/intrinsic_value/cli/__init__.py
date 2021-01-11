import os
from os import getenv

import click
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

    avg_eps_growth_idx = 0
    avg_eps_growth = past_eps_trend.at[avg_eps_growth_idx, 'avgEpsGrowthPercent']

    avg_eps_growth_idx = click.prompt(
        '\n Select average EPS growth percentage. Select index from the table above. \n'
        f'Current default is at index 0 : {avg_eps_growth}', default=0, type=int)

    avg_eps_growth = past_eps_trend.at[avg_eps_growth_idx, 'avgEpsGrowthPercent']
    click.secho(f'\nSelected average EPS growth for past 10 years is {avg_eps_growth}% \n', fg='yellow')
