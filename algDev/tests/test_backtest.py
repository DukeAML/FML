from algDev.models.backtest import Backtest
from algDev.models.trading_algorithm import TradingAlgorithm
from algDev.models.asset_strategy import AssetAllocation, AssetStrategy
from algDev.API.models import loadTradingAlgorithm
import datetime

def run_test():

    pf_value = 1234
    start_date = datetime.datetime(2020, 3, 4)
    end_date = datetime.datetime(2020, 3, 6)
    ta_id = '59f34827-33b8-4f6d-87aa-0455551ea59c'

    ta = loadTradingAlgorithm(ta_id)
    print(ta.eqs[0].closes)
    print(ta.models[0].accuracy)
    print(ta.models[0].models[0].metrics)
    aa = AssetAllocation(0.025, -0.15)
    a_s = AssetStrategy(aa)
    b = Backtest(ta, a_s, start_date, end_date, pf_value, True)

    print(b.simulate(False))

    # rtn = ((after_value - pf_value) / pf_value) * 100

    # print(str(rtn) + "%")

    # b.plot_value(pf_value, start_date, end_date)

run_test()