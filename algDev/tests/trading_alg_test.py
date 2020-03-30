from models.trading_algorithm import TradingAlgorithm

def run_test_one():
    tickers = ['AAPL']
    features = ['macd_9_18', 'closes', 'rainbow_4_6_12_14', 'oil', 'snp', 'reit']
    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 10, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0)
    print(ta.models)
