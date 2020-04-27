from algDev.models.trading_algorithm import TradingAlgorithm
from algDev.algorithms.model_collection import ModelCollection
from algDev.models.hyperparam_tst import hyper_param_haul
import datetime
import csv 

#Define tests to be called in run.py (in algDev)

def run_test_one():
    tickers = ['AAPL']
    features = ['macd_9_18','closes','prings','kst','kstTrix', 'rsi']
    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 15, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, voting_type = 'maj_rule', data_splits = [0.8, 0.2], cnn_split=0, model_params ={'gamma':100,"C":100}, verbose=True, test_mode = True)
    print(ta.models[0].accuracy)
    ta.generate_conf_matricies(datetime.datetime(2018,1,1), datetime.datetime(2019,1,1))
    # ta.plot_models_rocs()

def build_confusion_matrix():
    # one cm for whole alg 
    tickers = ['AAPL']
    features = ['macd_9_18','closes','prings','kst','kstTrix', 'rsi']
    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 15, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], model_params ={'gamma':100,"C":100}, cnn_split=0, verbose=True)
    print(ta.models[0].accuracy)
    ## At this point, the model is trained for everything. 
    ta.generate_conf_matricies(datetime.datetime(2018,1,1), datetime.datetime(2020,3,15))

def test_conf_matrix_model_coll():
    # one cm for each model 
    tickers = ['AAPL']
    features = ['macd_9_18','closes']
    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 10, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0, verbose=True, model_params ={'gamma':10,"C":1})
    
    ta.plot_model_cm(tickers[0])

def grid_search():
    tickers = ['AAPL']
    features = ['macd_9_18']
    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 15, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0, verbose=True)
    ta.grid_search(tickers[0], verbose= True)

def hyper_param_tuning():
    ticker_list = [['AAPL']]
    features_list = [['macd_9_18','macdSig','closes']]
    model_params = [{'gamma':.1, "C" :1},{'gamma':1, "C" :1},{'gamma':10, "C" : 1},{'gamma':100, "C" :1},{'gamma':.1, "C" :.1},{'gamma':1, "C" :.1},{'gamma':10, "C" :.1},{'gamma':100, "C" :.1},{'gamma':10, "C" :.001},{'gamma':100, "C" :.001}]
    hp = hyper_param_haul(features_list,ticker_list, model_params)
  