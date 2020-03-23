from preprocessing.feature_generation import * 
from models.indicator import Indicator
import numpy as np

def gen_cnn_data(eq, length, threshold, period):
    feature_set = ['macd_9_18', 'volumes', 'rainbow_1_5_9_13', 'oil', 'snp', 'reit','accumSwing']
    features = create_features(eq, feature_set)

    X, y = format_data(eq.ticker, features, 'cnn', length, threshold, period)

    print(X.shape)
    print(y.shape)


def format_data(ticker, data, type, length, threshold, period):

    y = build_labels(ticker, period, threshold)[-(data.shape[0]-length):]
    X = np.zeros((length, data.shape[1], data.shape[0]-length))

    for i,d in enumerate(data):
        if i < length:
            continue
        
        X[:,:,i-length] = data[i-length:i,:]

    return X, y

    
