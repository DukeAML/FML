import math
import numpy as np
import pandas as pd
import datetime

from equity import Equity
from indicators import Indicators

def parse_type(type):
    if(type==''):
        return 0

    else:
        return 1

def build_labels(eq, period=1, threshold=.01, type=''):
    
    closes = eq.closes
    highs = eq.highs

    ## Should be a label for every close other than the ones we 
    ## wouldnt have a full sample.
    labels = np.zeros(len(closes)-period)
    # label_type = parse_type(type)

    for i,close in enumerate(closes):
        if i >= len(closes)-period:
            continue
        passed_threshold = False
        for j in range(period):
            if j + i >= len(closes):
                continue
            if(log_returns(highs[j + i], close) > threshold):
                passed_threshold = True
    
        labels[i] = 1 if passed_threshold else 0

    return labels


def log_returns(p_1, p_0):

    rtn = p_1/p_0

    lr = math.log(rtn)

    return lr

def build_features(eq, type=''):
    
    # feature_type = parse_type(type)

    macd_ind = Indicators.macd_indicator(eq.closes, 6, 18)



