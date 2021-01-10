import click


@click.command()
@click.option('--ticker', prompt='ticker', help='Stock ticker to analyze. For example, MSFT')
def stock_cat(ticker):
    click.echo(f'Selected stock ticker is {ticker}')


if __name__ == '__main__':
    stock_cat()
