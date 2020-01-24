from models.equity import equity 
from models.commodity import commodity
from models.snp import snp
from models.reit import reit
from models.indicators import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

vslr_file = r'./data/equities/energy/VSLR.csv'
vslr = equity(vslr_file)

volumes = vslr.volumes
closes = vslr.closes
opens = vslr.opens
highs = vslr.highs
lows = vslr.lows

train_size = 100

## Get the last train_size days of Volume Data
## [train_size x 1]
vol_vec = volumes[(-1*train_size):] 

## Get the last train_size days of Close Data
## [train_size x 1]
close_vec = closes[(-1*train_size):] 

ma_period = 9
## Compute the sma on the last train_size + period days, then take the last train_size
## [train_size x 1]
sma_vec = sma(closes,ma_period)[(-1*train_size):]

## Compute the ema on the last train_size + period days, then take the last train_size
## [train_size x 1]
ema_vec = ema(closes,ma_period)[(-1*train_size):]

## Compute the wilder ma on the last train_size + period days, then take the last train_size
## [train_size x 1]
wilder_vec = ema(closes,ma_period,'wilder')[(-1*train_size):]

## Compute the wilder ma on the last train_size + period days, then take the last train_size
## [train_size x 1]
upper_bol_vec,lower_bol_vec = bolinger_bands(vslr)

upper_bol_vec = upper_bol_vec[(-1*train_size):]
lower_bol_vec = lower_bol_vec[(-1*train_size):]

accum_swing_vec = accumulative_swing_index(vslr)[(-1*train_size):]

atr_period = 10
atr_vec = average_true_range(vslr, atr_period)[(-1*train_size):]

bop_vec = balance_of_power(vslr)[(-1*train_size):]

gop_period = 10
gop_vec = gop_range_index(vslr, gop_period)[(-1*train_size):]

pivot_ind_vec = pivot_indicator(vslr)[(-1*train_size):]

prings_vec = prings_know_sure_thing(closes)[(-1*train_size):]

macd_slow_period = 24
macd_fast_period = 12
macd_vec = macd_indicator(closes, macd_slow_period, macd_fast_period)[(-1*train_size):]

kst_trix_vec = kst_trix_indicator(closes)[(-1*train_size):]

trix_vec = trix_indicator(closes)[(-1*train_size):]

rsi_period = 20
rsi_type = 'sma'
rsi_vec = rsi(closes, rsi_period, rsi_type)[(-1*train_size):]

ohlc_vec = vslr.ohlc()

rainbow_vecs = rainbow_ma(ohlc_vec, [1,3,5,7,9])

rainbow_vec_1 = rainbow_vecs[0][(-1*train_size):]
rainbow_vec_3 = rainbow_vecs[1][(-1*train_size):]
rainbow_vec_5 = rainbow_vecs[2][(-1*train_size):]
rainbow_vec_7 = rainbow_vecs[3][(-1*train_size):]
rainbow_vec_9 = rainbow_vecs[4][(-1*train_size):]

wti_file = r'./data/commodities/OIL.csv'
wti = commodity(wti_file)

wti_closes = wti.closes[(-1*train_size):]

reit_file = r'./data/indexes/RE.csv'
reit = reit(reit_file)

reit_closes = reit.closes[(-1*train_size):]

snp_file = r'./data/indexes/SNP.csv'
snp = snp(snp_file)

snp_closes = snp.closes[(-1*train_size):]

features = np.zeros((25, train_size))
features[0,:] = vol_vec
features[1,:] = close_vec
features[2,:] = sma_vec
features[3,:] = ema_vec
features[4,:] = wilder_vec
features[5,:] = upper_bol_vec
features[6,:] = lower_bol_vec
features[7,:] = accum_swing_vec
features[8,:] = atr_vec
features[9,:] = bop_vec
features[10,:] = gop_vec
features[11,:] = pivot_ind_vec
features[12,:] = prings_vec
features[13,:] = macd_vec
features[14,:] = kst_trix_vec
features[15,:] = trix_vec
features[16,:] = rsi_vec
features[17,:] = rainbow_vec_1
features[18,:] = rainbow_vec_3
features[19,:] = rainbow_vec_5
features[20,:] = rainbow_vec_7
features[21,:] = rainbow_vec_9
features[22,:] = wti_closes
features[23,:] = reit_closes
features[24,:] = snp_closes

np.savetxt('features_vslr.csv', features, delimiter=',')




