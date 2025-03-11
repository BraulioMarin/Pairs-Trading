import pandas as pd
from Stocks import download_data, load_data, plot_normalized, plot_prices
from cointegration_test import test_cointegration_johansen,test_cointegration_ols
from signalgenerator import generate_trading_signals
from backtesting import backtest_strategy
from plotsignals import plot_trading_signals

if __name__ == "__main__":
    tickers = ["UNP", "CSX"]

   
    download_data(tickers)
    data = load_data().dropna()

    
    stock1, stock2 = data[tickers[0]], data[tickers[1]]
    plot_prices(data)
    plot_normalized(data,tickers)

    
    eigenvector = test_cointegration_johansen(stock1, stock2)

    initial_hedge_ratio = test_cointegration_ols(stock1, stock2)[1]
    
    signals = generate_trading_signals(stock1, stock2, initial_hedge_ratio=initial_hedge_ratio)


    plot_trading_signals(stock1, stock2, signals)
    backtest_strategy(signals)

    