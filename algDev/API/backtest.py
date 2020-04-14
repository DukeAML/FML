from algDev.API.models import loadTradingAlgorithm
from algDev.models.backtest import Backtest
from algDev.models.trading_algorithm import TradingAlgorithm

from algDev.models.asset_strategy import AssetStrategy, AssetAllocation
import datetime

def run_backtest(start_date, end_date, pf_value, equities, tradingAlgorithmId):
    
    trading_algorithm = loadTradingAlgorithm(tradingAlgorithmId)
    aa = AssetAllocation(trading_algorithm.params['upper_threshold'], trading_algorithm.params['lower_threshold'])
    asset_strategy = AssetStrategy(aa)
    
    b = Backtest(equities, trading_algorithm, asset_strategy, start_date, end_date, pf_value, False)

    after_value, positions = b.simulate(False)
