import click


@click.command(name='intrinsic_value')
@click.option('--ticker', prompt='ticker', help='Stock ticker to analyze. For example, MSFT')
def command_intrinsic_value(ticker):
    click.echo(f'Selected stock ticker is {ticker}')
