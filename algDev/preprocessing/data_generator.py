from preprocessing.feature_generation import * 
from models.indicator import Indicator
import numpy as np

def gen_cnn_data(eq, feature_set, length, threshold, period):
    
    features = create_features(eq, feature_set)

    X, y = format_data(eq.ticker, features, 'cnn', length, threshold, period)
    print(X.shape)
    return X.reshape(X.shape[0],X.shape[1],X.shape[2],1),y

def split_data(X, y, splits):
    assert len(splits) <= 3 and len(splits) >= 2
    
    assert np.sum(splits) == 1

    train_length = int(splits[0] * len(X))

    X_train = X[0:train_length]
    y_train = y[0:train_length]

    if(len(splits)==3):
        val_length = int(splits[1] * len(X))
        y_val = y[train_length:train_length+val_length]
        X_val = X[train_length:train_length+val_length]
        test_length = len(X) - train_length - val_length
        y_test = y[(-1 * test_length):-1]
        X_test = X[(-1 * test_length):-1]
        return X_train, y_train, X_val, y_val, X_test, y_test
    else:
        X_test = X[train_length:-1]
        y_test = y[train_length:-1]
        return X_train, y_train, X_test, y_test

def format_data(ticker, data, type, length, threshold, period):

    y = build_labels(ticker, period, threshold)[-(data.shape[0]-length):]

    X = np.zeros((data.shape[0]-length, length, data.shape[1]))

    for i,d in enumerate(data):
        if i < length:
            continue
        
        X[i-length,:,:] = data[i-length:i,:]

    return X, y

    
