import numpy as np
from math import *
from build_features import gen_features

def gen_data(eq, days=500, range=1, verbose=False):
    eq_path = r'./algDev/data/equities/%s.csv' % eq

    train_size = int(0.8 * days)
    test_size = days - train_size

    features = np.array(gen_features(eq_path, days))

    train = features[0:train_size, :]
    test = features[train_size:len(features), :]

    X_train, y_train = get_data_labelled(train, range)
    
    if verbose is True:
        print("Features Shape:")
        print(features.shape)
        print("Example Feature:")
        print(features[0])
        print("Train Shape:")
        print(train.shape)
        print("Example Label:")
        print(y_train[0])
        print("Test Shape:")
        print(test.shape)

    X_test, y_test = get_data_labelled(test, range)
    
    return X_train, y_train, X_test, y_test


def gen_labels(p_0, p_1):

    c = p_1 / p_0

    bounds = [[-1000, -0.7], [-0.7, -0.1], [-0.1, -0.07], [-.07, -.02], [-.02, 0], [0, .02], [.02, .05], [0.05, 0.08],
              [0.08, 0.11], [0.11, 1000]]

    y = [(1 if c >= bound[0] and c < bound[1] else 0) for bound in bounds]

    return y

def get_data_labelled(data, data_range):
    X, y = [], []
    for i in range(len(data) - data_range):
        a = data[i, :]
        X.append(a)
        p_0 = data[(i), 1]
        p_1 = data[(i + data_range), 1]
        y.append(gen_labels(p_0, p_1))
    X, y = np.array(X), np.array(y)

    return X, y


gen_data('VSLR', verbose=True)