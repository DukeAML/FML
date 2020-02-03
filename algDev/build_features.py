from algDev.models.equity import Equity
from algDev.models.commodity import Commodity
from algDev.models.snp import SNP
from algDev.models.reit import REIT
from algDev.models.indicators import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

here = os.path.abspath(os.path.dirname(__file__))
data_directory = os.path.join(here, 'data')


def gen_features(equity_file, num_days, save=False):
    """
    Generates Set of Features for LSTM with Columns as follows for num_days timepoints

    |Vector 0   |Volumes                                                |
    |Vector 1   |Prices                                                 |
    |Vector 2   |SMA                                                    |
    |Vector 3   |EMA                                                    |
    |Vector 4   |Wilder MA                                              |
    |Vector 5   |Upper Bolinger Band                                    |
    |Vector 6   |Lower Bolinger Band                                    |
    |Vector 7   |Accumulative Swing Index                               |
    |Vector 8   |Average True Range                                     |
    |Vector 9   |Balance of Power                                       |
    |Vector 10  |Gopalakrishnan Range Index                             |
    |Vector 11  |Price - Pivot Point                                    |
    |Vector 12  |Pring's Know Sure Thing - SMA(Pring's Know Sure Thing) |
    |Vector 13  |MACD - SMA(MACD)                                       |
    |Vector 14  |d KST * d TRIX                                         |
    |Vector 15  |TRIX - MA(TRIX)                                        |
    |Vector 16  |RSI                                                    |
    |Vector 17  |MA(OHLC/4, 1)                                          |
    |Vector 18  |MA(OHLC/4, 3)                                          |
    |Vector 19  |MA(OHLC/4, 5)                                          |
    |Vector 20  |MA(OHLC/4, 7)                                          |
    |Vector 21  |MA(OHLC/4, 9)                                          |
    |Vector 22  |West Texas                                             |
    |Vector 23  |Wilshire US Real Estate                                |
    |Vector 24  |SNP                                                    |
    """
    e = Equity(equity_file)
    volumes = e.volumes
    closes = e.closes
    opens = e.opens
    highs = e.highs
    lows = e.lows

    ## Get the last num_days days of Volume Data
    ## vol_vec = [1 x num_days]
    vol_vec = np.array(volumes[(-1 * num_days):])
    vol_vec = vol_vec.T
    ## Get the last num_days days of Close Data
    ## close_vec = [1 x num_days]
    close_vec = np.array(closes[(-1 * num_days):])
    close_vec = close_vec.T
    ma_period = 9
    ## Compute the sma on the last num_days + period days, then take the last num_days
    ## [num_days x 1]
    sma_vec = np.array(sma(closes, ma_period)[(-1 * num_days):])
    sma_vec = sma_vec.T
    ## Compute the ema on the last num_days + period days, then take the last num_days
    ## [num_days x 1]
    ema_vec = np.array(ema(closes, ma_period)[(-1 * num_days):])
    ema_vec = ema_vec.T
    ## Compute the wilder ma on the last num_days + period days, then take the last num_days
    ## [num_days x 1]
    wilder_vec = np.array(ema(closes, ma_period, 'wilder')[(-1 * num_days):])
    wilder_vec = wilder_vec.T
    ## Compute the wilder ma on the last num_days + period days, then take the last num_days
    ## [num_days x 1]
    upper_bol_vec, lower_bol_vec = e.bollinger_bands()

    upper_bol_vec = np.array(upper_bol_vec[(-1 * num_days):])
    upper_bol_vec = upper_bol_vec.T

    lower_bol_vec = np.array(lower_bol_vec[(-1 * num_days):])
    lower_bol_vec = lower_bol_vec.T

    accum_swing_vec = np.array(e.accumulative_swing_index()[(-1 * num_days):])
    accum_swing_vec = accum_swing_vec.T

    atr_period = 10
    atr_vec = np.array(average_true_range(e, atr_period)[(-1 * num_days):])
    atr_vec = atr_vec.T

    bop_vec = np.array(e.balance_of_power()[(-1 * num_days):])
    bop_vec = bop_vec.T

    gop_period = 10
    gop_vec = np.array(e.gop_range_index(gop_period)[(-1 * num_days):])
    gop_vec = gop_vec.T

    pivot_ind_vec = np.array(e.pivot_indicator()[(-1 * num_days):])
    pivot_ind_vec = pivot_ind_vec.T

    prings_vec = np.array(prings_know_sure_thing(closes)[(-1 * num_days):])
    prings_vec = prings_vec.T

    macd_slow_period = 24
    macd_fast_period = 12
    macd_vec = np.array(macd_indicator(closes, macd_slow_period, macd_fast_period)[(-1 * num_days):])
    macd_vec = macd_vec.T

    kst_trix_vec = np.array(kst_trix_indicator(closes)[(-1 * num_days):])
    kst_trix_vec = kst_trix_vec.T

    trix_vec = np.array(trix_indicator(closes)[(-1 * num_days):])
    trix_vec = trix_vec.T

    rsi_period = 20
    rsi_type = 'sma'
    rsi_vec = np.array(rsi(closes, rsi_period, rsi_type)[(-1 * num_days):])
    resi_vec = rsi_vec.T

    ohlc_vec = e.ohlc()

    rainbow_vecs = rainbow_ma(ohlc_vec, [1, 3, 5, 7, 9])

    rainbow_vec_1 = np.array(rainbow_vecs[0][(-1 * num_days):])
    rainbow_vec_1 = rainbow_vec_1.T

    rainbow_vec_3 = np.array(rainbow_vecs[1][(-1 * num_days):])
    rainbow_vec_3 = rainbow_vec_3.T

    rainbow_vec_5 = np.array(rainbow_vecs[2][(-1 * num_days):])
    rainbow_vec_5 = rainbow_vec_5.T

    rainbow_vec_7 = np.array(rainbow_vecs[3][(-1 * num_days):])
    rainbow_vec_7 = rainbow_vec_7.T

    rainbow_vec_9 = np.array(rainbow_vecs[4][(-1 * num_days):])
    rainbow_vec_9 = rainbow_vec_9.T

    wti_file = os.path.join(data_directory, 'commodities', 'OIL.csv')
    wti = Commodity(wti_file)

    wti_closes = np.array(wti.closes[(-1 * num_days):])
    wti_closes = wti_closes.T

    reit_file = os.path.join(data_directory, 'indexes', 'RE.csv')
    reit_eq = REIT(reit_file)

    reit_closes = np.array(reit_eq.closes[(-1 * num_days):])
    reit_closes = reit_closes.T

    snp_file = os.path.join(data_directory, 'indexes', 'SNP.csv')
    snp_eq = SNP(snp_file)

    snp_closes = np.array(snp_eq.closes[(-1 * num_days):])
    snp_closes = snp_closes.T

    features = np.zeros((num_days, 25))
    features[:, 0] = vol_vec
    features[:, 1] = close_vec
    features[:, 2] = sma_vec
    features[:, 3] = ema_vec
    features[:, 4] = wilder_vec
    features[:, 5] = upper_bol_vec
    features[:, 6] = lower_bol_vec
    features[:, 7] = accum_swing_vec
    features[:, 8] = atr_vec
    features[:, 9] = bop_vec
    features[:, 10] = gop_vec
    features[:, 11] = pivot_ind_vec
    features[:, 12] = prings_vec
    features[:, 13] = macd_vec
    features[:, 14] = kst_trix_vec
    features[:, 15] = trix_vec
    features[:, 16] = rsi_vec
    features[:, 17] = rainbow_vec_1
    features[:, 18] = rainbow_vec_3
    features[:, 19] = rainbow_vec_5
    features[:, 20] = rainbow_vec_7
    features[:, 21] = rainbow_vec_9
    features[:, 22] = wti_closes
    features[:, 23] = reit_closes
    features[:, 24] = snp_closes

    if save is True:
        name = input("What do you want to save these features as? (Blank to not save) ")
        np.savetxt('features_%s.csv' % name, features, delimiter=',')

    return features


vslr_file = os.path.join(data_directory, 'equities', 'VSLR.csv')
vslr = Equity(vslr_file)

volumes = vslr.volumes
closes = vslr.closes
opens = vslr.opens
highs = vslr.highs
lows = vslr.lows

train_size = 100

## Get the last train_size days of Volume Data
## [train_size x 1]
vol_vec = volumes[(-1 * train_size):]

## Get the last train_size days of Close Data
## [train_size x 1]
close_vec = closes[(-1 * train_size):]

ma_period = 9
## Compute the sma on the last train_size + period days, then take the last train_size
## [train_size x 1]
sma_vec = Indicators.sma(prices=closes, period=ma_period)[(-1 * train_size):]

## Compute the ema on the last train_size + period days, then take the last train_size
## [train_size x 1]
ema_vec = Indicators.ema(prices=closes, period=ma_period)[(-1 * train_size):]

## Compute the wilder ma on the last train_size + period days, then take the last train_size
## [train_size x 1]
wilder_vec = ema(closes, ma_period, 'wilder')[(-1 * train_size):]

## Compute the wilder ma on the last train_size + period days, then take the last train_size
## [train_size x 1]
upper_bol_vec, lower_bol_vec = vslr.bollinger_bands()

upper_bol_vec = upper_bol_vec[(-1 * train_size):]
lower_bol_vec = lower_bol_vec[(-1 * train_size):]

accum_swing_vec = vslr.accumulative_swing_index()[(-1 * train_size):]

atr_period = 10
atr_vec = average_true_range(vslr, atr_period)[(-1 * train_size):]

bop_vec = vslr.balance_of_power()[(-1 * train_size):]

gop_period = 10
gop_vec = vslr.gop_range_index(gop_period)[(-1 * train_size):]

pivot_ind_vec = vslr.pivot_indicator()[(-1 * train_size):]

prings_vec = prings_know_sure_thing(closes)[(-1 * train_size):]

macd_slow_period = 24
macd_fast_period = 12
macd_vec = macd_indicator(closes, macd_slow_period, macd_fast_period)[(-1 * train_size):]

kst_trix_vec = kst_trix_indicator(closes)[(-1 * train_size):]

trix_vec = trix_indicator(closes)[(-1 * train_size):]

rsi_period = 20
rsi_type = 'sma'
rsi_vec = rsi(closes, rsi_period, rsi_type)[(-1 * train_size):]

ohlc_vec = vslr.ohlc()

rainbow_vecs = rainbow_ma(ohlc_vec, [1, 3, 5, 7, 9])

rainbow_vec_1 = rainbow_vecs[0][(-1 * train_size):]
rainbow_vec_3 = rainbow_vecs[1][(-1 * train_size):]
rainbow_vec_5 = rainbow_vecs[2][(-1 * train_size):]
rainbow_vec_7 = rainbow_vecs[3][(-1 * train_size):]
rainbow_vec_9 = rainbow_vecs[4][(-1 * train_size):]

wti_file = os.path.join(data_directory, 'commodities', 'OIL.csv')
wti = Commodity(wti_file)

wti_closes = wti.closes[(-1 * train_size):]

reit_file = os.path.join(data_directory, 'indexes', 'RE.csv')
reit = REIT(reit_file)

reit_closes = reit.closes[(-1 * train_size):]

snp_file = os.path.join(data_directory, 'indexes', 'SNP.csv')
snp = SNP(snp_file)

snp_closes = snp.closes[(-1 * train_size):]

np.savetxt('features_vslr.csv', features, delimiter=',')
