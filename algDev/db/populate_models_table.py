from algDev.algorithms.model_collection import ModelCollection
from algDev.algorithms.svm import SVM

from algDev.algorithms.asset_allocation import AssetAllocation

from algDev.models.asset_strategy import AssetStrategy

from algDev.models.trading_algorithm import TradingAlgorithm

from algDev.db.wrapper import createTradingAlgorithm, getTradingAlgorithm, createModel, createModelCollection
def build_example_model():
    tickers = ['AAPL', 'GS', 'GOOG', 'AMZN', 'COST', 'INTC', 'IBM', 'PG', 'GE']
    
    features = [
        'macd_9_18',
        'upperbol',
        'lowerbol'
    ]

    look_back = 15
    lower_threshold = -0.1
    upper_threshold = 0.025
    label_period = 5

    ta = TradingAlgorithm(tickers, features, type='svm', data_lookback_period=look_back, label_lower_threshold=lower_threshold, label_upper_threshold=upper_threshold, label_period=label_period)

    createTradingAlgorithm(ta)

def get_tas():
    return getTradingAlgorithm()

def test_add_model():
    svm = SVM(metrics={'acc':0.9})

    createModel(svm)

def test_add_model_collection():
    mc = ModelCollection('AAPL','svm',features=['macd_9_18','closes'],params={'length':10, 'upper_threshold':0.015, 'lower_threshold':-0.1, 'period':10})

    createModelCollection(mc)
