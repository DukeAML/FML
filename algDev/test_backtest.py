from models.backtest import Backtest
import datetime

def run_test():

    b = Backtest("AAPL", datetime.datetime(2016, 1, 1), 1000000)

    b.simulate({'lookback_period': 14, 'strategy_threshold': .015})


run_test()