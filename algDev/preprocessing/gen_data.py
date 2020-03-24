import numpy as np
from math import *
from preprocessing.feature_builder import gen_features, build_labels_string

def gen_data(eq, look_back=19, verbose=False):

    features = np.array(gen_features(eq,))
    train_size = int(0.8 * len(features))
    test_size = len(features) - train_size

    labels = np.array(build_labels_string(eq))
    assert(len(labels)==len(features))
    train_features = features[0:train_size, :]
    test_features = features[train_size:len(features), :]
    labels = build_labels_string(eq)
    train_labels = labels[0:train_size]
    test_labels = labels[train_size:len(labels)]
    print(len(train_features), len(train_labels))
    if verbose is True:
        print("Features Shape:")
        print(features.shape)
        print("Train Shape:")
        print(train_features.shape)
        print("Test Shape:")
        print(test_features.shape)
        print("Test Label Shape:")
        print(test_labels.shape)

    X_train, y_train = format_data(train_features, train_labels, look_back)
    # #y_train = y_train.reshape(((train_size - look_back - 1), 1, 10)) #use for addition of middle dimension

    X_test, y_test = format_data(test_features, test_labels, look_back)
    # y_test = y_test.reshape(((test_size - look_back - 1), 1, 10)) #use for addition of middle dimension
    return X_train, y_train, X_test, y_test


def format_data(data, labels, look_back):
    X = []
    y = []
    for i in range(len(data)):
        if i < look_back:
            continue

        a = data[(i-look_back):i, :]
        X.append(a)
        y.append(labels[i])
    X = np.array(X)
    y = np.array(y)

    return X, y

