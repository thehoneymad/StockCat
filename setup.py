from setuptools import setup, find_packages

setup(
    name='stock_cat',
    version='0.1',
    description='collection of easy stock analysis tools for beginners',
    url='https://github.com/thehoneymad/StockCat',
    author='thehoneymad',
    license='MIT',
    packages=find_packages(),
    install_requires=['click', 'yfinance', 'yahoo-finance'],
    scripts=['bin/stock_cat'],
    zip_safe=False)
