from algDev.API.models import loadTradingAlgorithm
from algDev.models.backtest import Backtest
from algDev.models.trading_algorithm import TradingAlgorithm

from algDev.models.asset_strategy import AssetStrategy, AssetAllocation
import datetime

def run_backtest(start_date, end_date, pf_value, tradingAlgorithmId):
    
    trading_algorithm = loadTradingAlgorithm(tradingAlgorithmId)
    aa = AssetAllocation(trading_algorithm.params['upper_threshold'], trading_algorithm.params['lower_threshold'])
    asset_strategy = AssetStrategy(aa)
    
    b = Backtest(trading_algorithm, asset_strategy, start_date, end_date, pf_value, False)
    after_value, positions = b.simulate(False)

    #     let positions = [{'ticker': 'GS', 'values':[50,60,40], 'trades': [{'datePurchased': new Date('2020-04-03'), 'numShares': 50, 'sold': true, 'dateSold': new Date('2020-01-12')}]},
    #                 {'ticker': 'AAPL', 'values':[70,80,90], 'trades': [{'datePurchased': new Date('2020-04-06'), 'numShares': 50, 'sold': false, 'dateSold': null}]}
    #                 ]
    
    # let stats = [{'name': 'Total Returns', 'value': '5%'},{'name': 'Market Returns', 'value': '2%'},{'name': 'Beta', 'value': '69'},
    # {'name': 'Average Free Cash', 'value': 2000}, {'name': 'Log Returns', 'value': 1.5}, {'name': 'Average Free Cash', 'value': 2000}, {'name': 'Standard Deviation', 'value': 25}]
