from algDev.models.trading_algorithm import TradingAlgorithm
import datetime
def run_test_one():
    tickers = ['AAPL']
    features = ['macd_9_18', 'closes', 'rainbow_4_6_12_14']
    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 10, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0, verbose=True)
    print(ta.models[0].accuracy)
    ta.plot_models_rocs()

def build_confusion_matrix():
    tickers = ['AAPL']
    features = ['macd_9_18','closes']
    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 10, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0, verbose=True)
    print(ta.models[0].accuracy)
    ## At this point, the model is trained for everything. 
    ta.generate_conf_matricies(datetime.date(2018,1,1), datetime.date(2020,3,15),True)