import click
from tabulate import tabulate

from stock_cat.intrinsic_value.intrinsic_value import IntrinsicValueRecipe


@click.command(name='intrinsic_value')
@click.option('--ticker', prompt='ticker', help='Stock ticker to analyze. For example, MSFT')
def command_intrinsic_value(ticker):
    recipe = IntrinsicValueRecipe(ticker)
    ticker_summary_table = recipe.get_ticker_summary(as_table=True)

    click.secho(tabulate(ticker_summary_table, tablefmt="github"), fg='green')
