from algDev.preprocessing.feature_generation import create_features, build_labels
from algDev.models.indicator import Indicator
import numpy as np

def parse_features(features):
    feature_set = []
    for feature in features:
        if 'rainbow' in feature:
            rainbows = feature.split('_')
            for i,rainbow in enumerate(rainbows):
                if i == 0:
                    continue
                feature_set.append('rainbow_'+rainbow)
        else:
            feature_set.append(feature)

    return feature_set
def get_subset(eq, feature_set, start_index, end_index, type):
    """Get a specific feature, instead of the whole features set
    
    Arguments:
        eq {Equity} -- Equity to look over
        feature_set {string array} -- Feature(s) that will be included
        start_index {int} -- starting index for feature
        end_index {int} -- ending index for feature
        threshold {float} -- see documentation on label threshold
        period {int} -- see documentation on label period
    
    Returns:
        [ndarray] -- one data point
    """
    features = create_features(eq, feature_set)

    if type=='cnn':
        X = features[start_index:end_index,:]
    elif type=='svm':
        X = features[start_index:end_index].reshape(1,-1)
    return X

def gen_cnn_data(eq, feature_set, length, threshold, period, split=0):
    """Generates the data to be used for a specific SVM
    
    Arguments:
        eq {Equity} -- equity to be used
        feature_set {string array} -- titles of features
        length {int} -- number of days to look back on for input
        threshold {float} -- see documentation on label threshold
        period {int} -- see documentation on label period
    
    Keyword Arguments:
        split {int} -- number of cnns to be used, number of data objects returned (default: {0})
    
    Returns:
        list of ndarray -- input and labels
    """
    features = create_features(eq, feature_set)

    X, y = format_data(eq.ticker, features, 'cnn', length, threshold, period)
    
    if split > 0:
        data_len = int(len(X)/split)
        Xs = []
        ys = []
        for i in range(split):
            start_index = i*data_len
            end_index = (i+1)*data_len
            Xs.append(X[start_index:end_index,:,:].reshape(data_len,X.shape[1],X.shape[2],1))
            ys.append(y[start_index:end_index])
        return Xs, ys
    else:
        return [X.reshape(X.shape[0],X.shape[1],X.shape[2],1)],[y]

def gen_svm_data(eq, feature, length, threshold, period):
    """Generates the data to be used for a specific SVM
    
    Arguments:
        eq {Equity} -- equity to be used
        feature {string array} -- feature title
        length {int} -- number of days to look back on for input
        threshold {float} -- see documentation on label threshold
        period {int} -- see documentation on label period
    
    Returns:
        ndarray -- input and labels
    """
    feature = create_features(eq, feature)
    
    X, y = format_data(eq.ticker, feature, 'svm', length, threshold, period)

    return X.reshape(X.shape[0],X.shape[1],),y

def unison_shuffled_copies(a, b):
    
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

def split_data(X, y, splits):
    """Splits the data for training and testing, also validation if necessary
    
    Arguments:
        X {ndarrray} -- input data
        y {ndarray} -- labels
        splits {float array} -- ratio of data for each type
    
    Returns:
        (ndarray) -- arrays of the data and labels splits up as requested
    """
    assert len(splits) <= 3 and len(splits) >= 2
    
    assert np.sum(splits) == 1

    X,y = unison_shuffled_copies(X,y)

    train_length = int(splits[0] * len(X))

    X_train = X[0:train_length]
    y_train = y[0:train_length]

    if(len(splits)==3):
        val_length = int(splits[1] * len(X))
        y_val = y[train_length:train_length+val_length]
        X_val = X[train_length:train_length+val_length]
        test_length = len(X) - train_length - val_length
        y_test = y[(-1 * test_length)]
        X_test = X[(-1 * test_length)]
        return X_train, y_train, X_val, y_val, X_test, y_test
    else:
        X_test = X[train_length:]
        y_test = y[train_length:]
        return X_train, y_train, X_test, y_test

def format_data(ticker, data, type, length, threshold, period):
    """Turn data into the format that will be used by the models
    
    Arguments:
        ticker {string} -- Securities ticker
        data {ndarray} -- array of raw features
        type {string} -- model type (cnn, svm)
        length {int} -- number of days to look back on for input
        threshold {float} -- see documentation for label threshold
        period {int} -- see documentation for label period
    
    Returns:
        (ndarray,ndarray) -- input and labels formatted as needed for the models
    """
    y = build_labels(ticker, period, threshold)[-(data.shape[0]-length):]
    if type=='cnn':
        X = np.zeros((data.shape[0]-length, length, data.shape[1]))
    elif type=='svm':
        X = np.zeros((data.shape[0]-length, length, 1))
    for i,d in enumerate(data):
            if i < length:
                continue
            if type=='cnn':
                X[i-length,:,:] = data[i-length:i,:]
            elif type=='svm':
                X[i-length,:] = data[i-length:i]
    if len(X) > len(y):
        y = y[0:len(X)]
    elif len(y) > len(X):
        X = X[0:len(y)]
    return X, y

    
