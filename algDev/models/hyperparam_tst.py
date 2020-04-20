
from algDev.models.trading_algorithm import TradingAlgorithm
from algDev.algorithms.model_collection import ModelCollection
import csv
'''
def hyper_param_haul(features_list,ticker_list, model_params):
    acc_lst =[]
    with open('hyperparam_tst.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["tickers", "features", "params", "acc", "confusion_matrix"])
        for ii in range(len(ticker_list)):
            tickers = ticker_list[ii]
            for jj in range(len(features_list)):
                features = features_list[jj]
                for kk in range(len(model_params)):
                    params = model_params[kk]
                    print(tickers, features, params)
                    ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 30, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0, verbose=True, model_params = params)
                    # cm = ta.plot_model_cm(ticker[0])
                    acc = ta.models[0].accuracy
                    acc_lst.append(acc)
                    writer.writerow([tickers, features, params, acc])
    return max(acc_lst)
    '''
    
def hyper_param_haul(features_list,ticker_list, model_params):
    acc_lst =[]
    cm_lst = []
    file = open('hyperparam_tst.txt', 'w')
    writer = csv.writer(file)
    writer.writerow(["tickers", "features", "params", "acc", "confusion_matrix"])
    for ii in range(len(ticker_list)):
        tickers = ticker_list[ii]
        for jj in range(len(features_list)):
            features = features_list[jj]
            for kk in range(len(model_params)):
                params = model_params[kk]
                ta = TradingAlgorithm(tickers, features, type = 'svm', data_lookback_period = 30, label_lower_threshold = -0.15, label_upper_threshold = 0.015, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0, verbose=True, model_params = params)
                cm = ta.plot_model_cm(tickers[0])
                cm_lst += cm
                acc = ta.models[0].accuracy
                acc_lst.append(acc)   
                writer.writerow([tickers, features, params, acc])
                for ii in range(len(cm_lst)):
                    for jj in range(len(cm_lst[ii])):
                        file.write(str(cm_lst[ii][jj]))
                        file.write("\n")

    file.close()

    return max(acc_lst)