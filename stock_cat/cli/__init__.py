import click

from stock_cat.intrinsic_value.cli import command_intrinsic_value


@click.group()
def cli_stock_cat():
    pass


cli_stock_cat.add_command(command_intrinsic_value)


def main():
    cli_stock_cat()
