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
    fundamentals_table = recipe.get_ticker_fundamentals(as_table=True)

    click.secho(tabulate(fundamentals_table, tablefmt="github"), fg='green')
