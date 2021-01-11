# StockCat

StockCat is a personal journey to basic financial knowledge. This is a set of scripts
to automate basic financial insight.

To use, you will need a Alpha Vantage API key. To set it, execute
```bash
export ALPHAVANTAGE_API_KEY=<YOUR_API_KEY>
```

To install dependencies and what not of StockCat execute,
```bash
python3 setup.py install
```

You can also use 
```bash
python3 setup.py develop
```

To invoke StockCat execute,
```bash
bin/stock_cat
```

You will be greeted with a help guide like the following:
```bash
Usage: stock_cat [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  intrinsic_value
```

To see intrinsic value of a stock, execute
```bash
bin/stock_cat intrinsic_value --ticker <SYMBOL>
```
