import numpy as np
from math import *

def gen_data(eq, days=500, look_back=19, label_range=5, verbose=False):

    train_size = int(0.8 * days)
    test_size = days - train_size

    features = np.array(gen_features(eq, days))

    train_features = features[0:train_size, :]
    test_features = features[train_size:len(features), :]
    labels = build_labels_string(eq)
    train_labels = labels[(-1 * days):((-1*days)+train_size)]
    
    test_labels = labels[((-1*days)+train_size):len(labels)]
    
    if verbose is True:
        print("Features Shape:")
        print(features.shape)
        print("Train Shape:")
        print(train_features.shape)
        print("Test Shape:")
        print(test_features.shape)
        print("Test Label Shape:")
        print(test_labels.shape)

    X_train, y_train = get_data_labelled(train_features, look_back, label_range)
    # #y_train = y_train.reshape(((train_size - look_back - 1), 1, 10)) #use for addition of middle dimension

    X_test, y_test = get_data_labelled(test_features, look_back, label_range)
    # y_test = y_test.reshape(((test_size - look_back - 1), 1, 10)) #use for addition of middle dimension

    return X_train, y_train, X_test, y_test


def gen_labels(p_0, p_1):
    dp = p_1 - p_0

    c = dp / p_0
    
    bounds = [[-.1, -.07], [-.07, -.05], [-.05, -.03], [-.03, -.01], [-.01, .01], [.01, .03], [.03, .05], [.05, .07],
              [.07, .09], [.09, 1]]

    y = [(1 if c >= bound[0] and c < bound[1] else 0) for bound in bounds]

    return y


def get_data_labelled(data, look_back, label_range):
    
    X, y = [], []
    for i in range(len(data) - look_back - 1):
        a = data[i:(i + look_back), :]
        X.append(a)
        p_0 = data[(i + look_back - label_range), 1]
        p_1 = data[(i + look_back), 1]
        y.append(gen_labels(p_0, p_1))
    X, y = np.array(X), np.array(y)

    return X, y

