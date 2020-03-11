import numpy as np
import math 
import os
from build_dfFeatures import gen_features

def gen_labels(data, binary_category, threshold):
    '''
    this function generates labels for given data based on the following criterion
    inputs:
        data: list of price values for equity in question, length of list = look_back 
        binary category: one of "postive", "negative", or "window". positive establishes upper threshold, 
                        negative establishes lower threshold, and window establishes upper and lower threshold 
        threshold: limit of interest. (does return on equity surpass, fall beneath, etc. threshold)
    output:
        0: if equity return never meets criterion based on binary category and threshold
        1: if equity return does meet criterion based on binary category and threshold 

    '''
    
    #given data, will compute whether or not log return 
    # of that data ever surpasses threshold
    
    if binary_category == "positive":
        y = 0
        print(data)
        t0 = data[0]
        
        for ii in range(len(data)-1):
            delta = data[ii+1] - t0
            r = delta/ t0
            if r >= threshold:
                y = 1
        return y 
    
    #given data, will compute whether or not log return 
    # of that data ever falls below threshold
    elif binary_category == "negative":
        y = 0
        t0 = data[0]
        
        for ii in range(len(data)-1):
            delta = data[ii+1] - t0
            r = delta/ t0
            if r <= threshold:
                y = 1
        return y
    
    #given data, will compute whether or not log return 
    # of that data ever falls outside window of -(threshold), threshold
    elif binary_category == "window":
        
        y = 0
        t0 = data[0]
        
        for ii in range(len(data)-1):
            delta = data[ii+1] - t0
            r = delta/ t0
            if r >= threshold or r <= -(threshold):
                y = 1
        return y 

def get_data_labelled(data, look_back, binary_category, threshold):
    '''
    this function returns labelled data 
    inputs:
        data: (row) dataframe of equity price data, length = # days 
        look_back: period of interest for meeting return criterion (did eq return ever surpass 2% inc within look_back days)
        binary category: one of "postive", "negative", or "window". positive establishes upper threshold, 
                        negative establishes lower threshold, and window establishes upper and lower threshold 
        threshold: limit of interest. (does return on equity surpass, fall beneath, etc. threshold)
    outputs:
        2 arrays: X data (array of look_back periods), Y data (array of labels for look_back periods)

    '''
    X, y = [], []
    
    c=0
    d=0
    while len(data) - d > 10:
        temp = data[c:look_back+ d +1].tolist()
        X.append(temp)
        labels = gen_labels(temp, binary_category, threshold)
        y.append(labels)
        c+=1 
        d+=1

    X, y = np.array(X), np.array(y)

    return X, y


def gen_data(eq, features, days, look_back, binary_category, threshold):
    '''
    this function returns X data for given number of days formatted using look_back, 
    Y data (labels) formatted using binary category and threshold, using above helper functions
    
    inputs:
        eq: (string) ticker for equity of interest 
        features: (list of strings) all predictive features wanted for model 
        days: number of days to use
        look_back: period of interest for meeting return criterion (did eq return ever surpass 2% inc within look_back days)
        binary category: one of "postive", "negative", or "window". positive establishes upper threshold, 
                        negative establishes lower threshold, and window establishes upper and lower threshold 
        threshold: limit of interest. (does return on equity surpass, fall beneath, etc. threshold)
    outputs: 4 arrays below
        X_train: lists of data of size look_back for training
        y_train: labels for training data
        X_test: lists of data of size look_back for testing
        y_test: labels for test data

    '''
    
    rows = ["Volumes", "Prices","SMA","EMA", "Wilder MA","Upper Bolinger Band", 
                    "Lower Bolinger Band", "Accumulative Swing Index","Average True Range","Balance of Power", 
                    "Gopalakrishnan Range Index", "Price - Pivot Point","Pring's Know Sure Thing - SMA(Pring's Know Sure Thing)", 
                    "MACD - SMA(MACD)","d KST * d TRIX ", "TRIX - MA(TRIX)", "RSI", "MA(OHLC/4, 1)", "MA(OHLC/4, 3)","MA(OHLC/4, 5)", 
                    "MA(OHLC/4, 7)", "MA(OHLC/4, 9)", "West Texas", "Wilshire US Real Estate", "SNP"]
    row_dict0 ={}
    for ii in range(len(rows)):
        row_dict0[ii] = rows[ii]
    row_dict = {y:x for x,y in row_dict0.items()}

    here = os.path.abspath(os.path.dirname(__file__))
    eq_path = os.path.join(here, 'data', 'equities', '%s.xlsx' % eq)

    features = gen_features(eq_path, days, df= True)

    train_size = int(0.8 * days)
    test_size = days - train_size

    prices = features.iloc[row_dict["Prices"]]
    train = prices[0:train_size]
    test = prices[train_size:]

    X_train0, y_train = get_data_labelled(train, look_back, binary_category, threshold)
    X_test0, y_test = get_data_labelled(test, look_back, binary_category, threshold)

    X =[]
    for indicator in features:
        data = features.iloc[row_dict[indicator]]
        c = 0 
        d =0
        while len(data) - d > look_back:
            temp = data[c:look_back+ d +1].tolist()
            X.append(temp[0])
            c+=1 
            d+=1
    
    print(features.iloc[row_dict["SMA"]])
    print(len(X))

    train_size_I = int(0.8 * len(X))
    test_size_I = days - train_size_I

    X_train = np.array(X[0:train_size_I])
    X_test = np.array(X[train_size_I:])
   
    return X_train, y_train, X_test, y_test
