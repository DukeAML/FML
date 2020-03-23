import math
import numpy as np
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt

from models.equity import Equity
from models.indicators import Indicators
from models.indicator import Indicator
from preprocessing import utils
here = os.path.abspath(os.path.dirname(__file__))

def macd_raw_feature(eq, slow_period, fast_period):
    """
    Generates a feature vector of macd_raw for the last num_days
    """
    macd_raw_vec = np.array(Indicators.macd(eq.closes, slow_period, fast_period))
    macd_raw_vec = macd_raw_vec.T

    return [Indicator(macd_raw_vec)]

def macd_signal(eq, slow_period, fast_period):
    macd_sig = np.array(Indicators.ema(np.array(Indicators.macd(eq.closes, slow_period, fast_period)), 9))
    macd_sig = macd_sig.T

    return [Indicator(macd_sig)]

def kst_trix_vec_feature(eq):
    kst_trix_vec = np.array(Indicators.kst_trix_indicator(eq.closes))
    kst_trix_vec = kst_trix_vec.T

    return [Indicator(kst_trix_vec)]

def trix_vec_feature(eq):
    trix_vec = np.array(Indicators.trix_indicator(eq.closes))
    trix_vec = trix_vec.T
    return [Indicator(trix_vec)]

def rsi_feature(eq, period = 20, type = 'sma'):
    rsi_vec = np.array(Indicators.rsi(eq.closes, period, type))
    rsi_vec = rsi_vec.T
    return [Indicator(rsi_vec)]

def prings_feature(eq):
    prings_vec = np.array(Indicators.prings_know_sure_thing(eq.closes))
    prings_vec = prings_vec.T
    return [Indicator(prings_vec)]

def olhc_feature(eq):
    ohlc_vec = eq.ohlc()
    return [Indicator(ohlc_vec)]

def rainbow_feature(eq, smas):

    ohlc_vec = olhc_feature(eq)[0].values
    rainbow_vecs = Indicators.rainbow_ma(ohlc_vec, smas)

    return rainbow_vecs

def oil_feature():
    wti_file = os.path.join('../', 'commodities', 'OIL')
    wti = Equity(wti_file)

    wti_closes = np.array(wti.closes)
    wti_closes = wti_closes.T

    return [Indicator(wti_closes)]
    
def reit_feature():
    reit_file = os.path.join('../', 'indexes', 'RE')
    reit_eq = Equity(reit_file)

    reit_closes = np.array(reit_eq.closes)
    reit_closes = reit_closes.T

    return [Indicator(reit_closes)]

def snp_feature():
    snp_file = os.path.join('../', 'indexes', 'SNP')
    snp_eq = Equity(snp_file)

    snp_closes = np.array(snp_eq.closes)
    snp_closes = snp_closes.T

    return [Indicator(snp_closes)]

def gop_feature(eq, period):
    gop_vec = np.array(eq.gop_range_index(period))
    gop_vec = gop_vec.T

    return [Indicator(gop_vec)]

def bop_feature(eq):
    bop_vec = np.array(eq.balance_of_power())
    bop_vec = bop_vec.T

    return [Indicator(bop_vec)]

def volume_feature(eq):
    
    vol_vec = np.array(eq.volumes)
    vol_vec = vol_vec.T

    return [Indicator(vol_vec)]

def close_feature(eq):
    close_vec = np.array(eq.closes)
    close_vec = close_vec.T

    return [Indicator(close_vec)]

def sma_feature(eq, period):
    sma_vec = np.array(Indicators.sma(eq.closes, period))
    sma_vec = sma_vec.T

    return [Indicator(sma_vec)]

def ema_feature(eq, period):
    
    ema_vec = np.array(Indicators.ema(eq.closes, period))
    ema_vec = ema_vec.T

    return [Indicator(ema_vec)]
def wilder_feature(eq, period):
    wilder_vec = np.array(Indicators.ema(eq.closes, period, 'wilder'))
    wilder_vec = wilder_vec.T

    return [Indicator(wilder_vec)]

def upper_bollinger_feature(eq, period=20, stds=2):
    upper_bol_vec, _ = eq.bollinger_bands(period, stds)

    upper_bol_vec = np.array(upper_bol_vec)
    upper_bol_vec = upper_bol_vec.T

    return [Indicator(upper_bol_vec)]

def lower_bollinger_feature(eq, period=20, stds=2):
    _, lower_bol_vec = eq.bollinger_bands(period, stds)

    lower_bol_vec = np.array(lower_bol_vec)
    lower_bol_vec = lower_bol_vec.T

    return [Indicator(lower_bol_vec)]

def accum_swing_feature(eq):
    accum_swing_vec = np.array(eq.accumulative_swing_index())
    accum_swing_vec = accum_swing_vec.T

    return [Indicator(accum_swing_vec)]

def atr_feature(eq, period):
    atr_vec = np.array(Indicators.average_true_range(eq, period))
    atr_vec = atr_vec.T

    return [Indicator(atr_vec)]

def plot_features(eq, features, ax, range=-1):
    feature_set = get_feature_set(eq, features)
    fs = concat_indicators(feature_set)

    for i,f in enumerate(fs):
        f.plot(ax, utils.get_style(i), range)
    
    return ax

def plot_labels(eq, period, threshold, ax, type='', range=-1):
    labels = build_labels(eq.ticker, period, threshold, type)[:range]
    i = np.arange(len(labels))
    p = labels[:] == 1
    n = labels[:] == 0
    ax.plot(i[p], labels[p], 'bo')
    ax.plot(i[n], labels[n], 'ro')

    return ax

def concat_indicators(feature_set):
    num_features = len(feature_set)
    print(feature_set)
    lens = np.array([f.len for f in feature_set])
    min_len = np.min(lens)
    print(min_len)

    for i in range(num_features):
        
        feature_set[i].trim_vals(end_index=min_len)
    
    return feature_set

def concat_features(feature_set):
    num_features = len(feature_set)

    lens = np.array([f.len for f in feature_set])
    min_len = np.min(lens)
    
    features = np.zeros((min_len, num_features))

    for i in range(num_features):
        
        feature = feature_set[i].trim_vals(end_index=min_len).values

        features[:,i] = feature
    
    return features

def create_features(eq, features, normalize = True, save = False):
    
    feature_set = get_feature_set(eq, features)
    fs = concat_features(feature_set)
    
    if normalize is True:
        for i in range(fs.shape[1]):
            f = utils.norm(fs[:,i])
            fs[:,i] = f

    if save is True:
        name = input("What do you want to save these features as? (Blank to not save) ")
        np.savetxt('features_%s.csv' % name, fs, delimiter=',')

    return fs

def get_feature_set(eq, features):
    feature_set = []
    for feature in features:
        f = get_feature(eq, feature)
        for feat in f:
            feature_set.append(feat)

    return feature_set

def get_feature(eq, feature_arg):
    args = feature_arg.split('_')
    feature = args[0]

    if len(args)==1:
        args.append('9')
    if len(args)==2:
        args.append('18')

    fast_period = int(args[1])
    slow_period = int(args[2])
    all_periods = [int(i) for i in args[1:]]

    ## Come up with good way to parse an input for a feature and return correct function call
    if(feature=='sma'):
        return sma_feature(eq, fast_period)
    elif(feature=='ema'):
        return ema_feature(eq, fast_period)
    elif(feature=='wilder'):
        return wilder_feature(eq, fast_period)
    elif(feature=='macd'):
        return macd_raw_feature(eq, slow_period, fast_period)
    elif(feature=='macdSig'):
        return macd_signal(eq, slow_period, fast_period)
    elif(feature=='kst'):
        return ''
    elif(feature=='trix'):
        return ''
    elif(feature=='kstTrix'):
        return kst_trix_vec_feature(eq)
    elif(feature=='rsi'):
        return rsi_feature(eq)
    elif(feature=='prings'):
        return prings_feature(eq)
    elif(feature=='olhc'):
        return olhc_feature(eq)
    elif(feature=='rainbow'):
        return rainbow_feature(eq, all_periods)
    elif(feature=='oil'):
        return oil_feature()
    elif(feature=='snp'):
        return snp_feature()
    elif(feature=='reit'):
        return reit_feature()
    elif(feature=='gop'):
        return gop_feature(eq, fast_period)
    elif(feature=='bop'):
        return bop_feature(eq)
    elif(feature=='volumes'):
        return volume_feature(eq)
    elif(feature=='closes'):
        return close_feature(eq)
    elif(feature=='upperBol'):
        return upper_bollinger_feature(eq)
    elif(feature=='lowerBol'):
        return lower_bollinger_feature(eq)
    elif(feature=='accumSwing'):
        return accum_swing_feature(eq)
    elif(feature=='atr'):
        return atr_feature(eq, fast_period)
    
    return ''

def build_labels(ticker, period=10, threshold=.015, type=''):
    
    eq = Equity(ticker)
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
            if(utils.log_returns(highs[j + i], close) > threshold):
                passed_threshold = True
    
        labels[i] = 1 if passed_threshold else 0

    return labels
