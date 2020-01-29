import numpy as np
from math import *
from build_features import gen_features

def gen_data(eq, days=500, look_back=19, label_range=5, verbose=False):

    eq_path = r'./data/equities/%s.csv' % eq

    train_size = int(0.8 * days)
    test_size = days - train_size

    features = np.array(gen_features(eq_path, days))

    train = features[0:train_size, :]
    test = features[train_size:len(features), :]

    if verbose is True:
        print("Features Shape:")
        print(features.shape)
        print("Train Shape:")
        print(train.shape)
        print("Test Shape:")
        print(test.shape)

    X_train, y_train = get_data_labelled(train, look_back, label_range)
    X_test, y_test = get_data_labelled(test, look_back, label_range)

    return X_train, y_train, X_test, y_test

def gen_labels(p_0, p_1):
    dp = p_1 - p_0

    c = dp/p_0

    y = [c >= -0.1, c >= -0.07, c >= -0.04, c >= -0.01, c >= 0, c >= 0.01, c >= 0.04, c >= 0.07, c >= 0.1, c >= 0.15]

    return y

def get_data_labelled(data, look_back, label_range):
    X, y = [], []
    for i in range(len(data)-look_back-1):
        a = data[i:(i+look_back), :]
        X.append(a)
        p_0 = data[(i+look_back - label_range), 1]
        p_1 = data[(i+look_back), 1]
        y.append(gen_labels(p_0, p_1))
    X, y = np.array(X), np.array(y)
    print(X.shape)
    print(y.shape)
    return X,y
