from algDev.models.trading_algorithm import TradingAlgorithm
from algDev.algorithms.model_collection import ModelCollection
import datetime
def run_test_one():
    tickers = ['AAPL']
    features = ['macd_9_18', 'macdSig', 'prings', 'kstTrix']
    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 10, label_lower_threshold = -0.15, label_upper_threshold = 0.005, label_period = 1, data_splits = [0.8, 0.2], cnn_split=0, verbose=True)
    print(ta.models[0].accuracy)
    ta.generate_conf_matricies(datetime.date(2018,1,1), datetime.date(2019,1,1))
    ta.plot_models_rocs()

def build_confusion_matrix():
    tickers = ['NFLX']
    features = ['macd_9_18','closes']
    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 15, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0, verbose=True)
    print(ta.models[0].accuracy)
    ## At this point, the model is trained for everything. 
    ta.generate_conf_matricies(datetime.date(2018,1,1), datetime.date(2020,3,15))

def test_conf_matrix_model_coll():
    tickers = ['AAPL']
    features = ['macd_9_18','closes']
    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 10, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0, verbose=True)
    
    ta.plot_model_cm(tickers[0])

def plot_hyperparam_viz():
    tickers = ['AAPL']
    features = ['closes']
    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 10, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0, verbose=True)
    ta.plot_models_hyperparam_viz(tickers)


