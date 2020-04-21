from algDev.models.backtest import Backtest
from algDev.models.trading_algorithm import TradingAlgorithm
from algDev.models.asset_strategy import AssetAllocation, AssetStrategy
import datetime

def run_test():

    pf_value = 1000000
    start_date = datetime.datetime(2018, 7, 13)
    end_date = datetime.datetime(2019, 1, 13)
    tickers = ["AAPL", "AMZN", "BRK-B"]
    features = [
        'macd_9_18'
    ]
    ta = TradingAlgorithm(tickers, features)

    aa = AssetAllocation(0.025, -0.15)
    a_s = AssetStrategy(aa)
    b = Backtest(ta, a_s, start_date, end_date, pf_value, True)

    print(b.simulate(False))

    # rtn = ((after_value - pf_value) / pf_value) * 100

    # print(str(rtn) + "%")

    # b.plot_value(pf_value, start_date, end_date)

run_test()