from setuptools import setup

setup(
    name='stock_cat',
    version='0.1',
    description='collection of easy stock analysis tools for beginners',
    url='https://github.com/thehoneymad/StockCat',
    author='thehoneymad',
    license='MIT',
    packages=['stock_cat'],
    install_requires=['click', 'yfinance', 'yahoo-finance'],
    zip_safe=False)
