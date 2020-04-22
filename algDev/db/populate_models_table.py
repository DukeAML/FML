from algDev.algorithms.model_collection import ModelCollection
from algDev.algorithms.svm import SVM

from algDev.algorithms.asset_allocation import AssetAllocation

from algDev.models.asset_strategy import AssetStrategy

from algDev.models.trading_algorithm import TradingAlgorithm

from algDev.db.wrapper import createTradingAlgorithm, getTradingAlgorithms, createModel, createModelCollection
def build_example_model():
    tickers = ['AAPL', 'IBM']
    
    features = [
        'closes',
    ]

    look_back = 10
    lower_threshold = -0.15
    upper_threshold = 0.03
    label_period = 10

    ta = TradingAlgorithm(tickers, features, type='svm', data_lookback_period=look_back, label_lower_threshold=lower_threshold, label_upper_threshold=upper_threshold, label_period=label_period)
    print("Trading Alg Build")
    createTradingAlgorithm(ta)

def get_tas():
    return getTradingAlgorithms()

def test_add_model():
    svm = SVM(metrics={'acc':0.9})

    createModel(svm)

def test_add_model_collection():
    mc = ModelCollection('AAPL','svm',features=['macd_9_18','closes'],params={'length':10, 'upper_threshold':0.015, 'lower_threshold':-0.1, 'period':10})

    createModelCollection(mc)
