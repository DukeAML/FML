
from algDev.models.trading_algorithm import TradingAlgorithm
from algDev.algorithms.model_collection import ModelCollection
import csv

def hyper_param_haul(features_list,ticker_list, model_params):
    acc_lst =[]
    with open('hyperparam_tst.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ticker", "features", "params", "acc", "confusion_matrix"])
        for ii in range(len(ticker_list)):
            ticker = tickers_list[ii]
            for jj in range(len(features_list)):
                features = features_list[jj]
                for kk in range(len(model_params)):
                    params = model_params[kk]
                    ta = TradingAlgorithm(ticker, features, type = 'svm', data_lookback_period = 10, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0, verbose=True, model_params = params)
                    cm = ta.plot_model_cm(ticker[0])
                    acc = ta.models[0].accuracy
                    acc_lst.append(acc)
                    writer.writerow([ticker, features, params, acc, cm)
    return max(acc_lst)
    
