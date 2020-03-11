from models.equity import Equity
from models.indicators import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn import preprocessing

here = os.path.abspath(os.path.dirname(__file__))
data_directory = os.path.join(here, 'data')


def gen_features(equity_file, num_days, save=False, normalize = False):
    """
    Generates Data Frame of Features for models with Rows as follows for num_days = num_cols timepoints

    |Row 0   |Volumes                                                |
    |Row 1   |Prices                                                 |
    |Row 2   |SMA                                                    |
    |Row 3   |EMA                                                    |
    |Row 4   |Wilder MA                                              |
    |Row 5   |Upper Bolinger Band                                    |
    |Row 6   |Lower Bolinger Band                                    |
    |Row 7   |Accumulative Swing Index                               |
    |Row 8   |Average True Range                                     |
    |Row 9   |Balance of Power                                       |
    |Row 10  |Gopalakrishnan Range Index                             |
    |Row 11  |Price - Pivot Point                                    |
    |Row 12  |Pring's Know Sure Thing - SMA(Pring's Know Sure Thing) |
    |Row 13  |MACD - SMA(MACD)                                       |
    |Row 14  |d KST * d TRIX                                         |
    |Row 15  |TRIX - MA(TRIX)                                        |
    |Row 16  |RSI                                                    |
    |Row 17  |MA(OHLC/4, 1)                                          |
    |Row 18  |MA(OHLC/4, 3)                                          |
    |Row 19  |MA(OHLC/4, 5)                                          |
    |Row 20  |MA(OHLC/4, 7)                                          |
    |Row 21  |MA(OHLC/4, 9)                                          |
    |Row 22  |West Texas                                             |
    |Row 23  |Wilshire US Real Estate                                |
    |Row 24  |SNP                                                    |
    """

    '''
    option to normalize data by feature
    option to save df to file 

    '''
    
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
    sma_vec = np.array(Indicators.sma(closes, ma_period)[(-1 * num_days):])
    sma_vec = sma_vec.T
    ## Compute the ema on the last num_days + period days, then take the last num_days
    ## [num_days x 1]
    ema_vec = np.array(Indicators.ema(closes, ma_period)[(-1 * num_days):])
    ema_vec = ema_vec.T
    ## Compute the wilder ma on the last num_days + period days, then take the last num_days
    ## [num_days x 1]
    wilder_vec = np.array(Indicators.ema(closes, ma_period, 'wilder')[(-1 * num_days):])
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
    atr_vec = np.array(Indicators.average_true_range(e, atr_period)[(-1 * num_days):])
    atr_vec = atr_vec.T

    bop_vec = np.array(e.balance_of_power()[(-1 * num_days):])
    bop_vec = bop_vec.T

    gop_period = 10
    gop_vec = np.array(e.gop_range_index(gop_period)[(-1 * num_days):])
    gop_vec = gop_vec.T

    pivot_ind_vec = np.array(e.pivot_indicator()[(-1 * num_days):])
    pivot_ind_vec = pivot_ind_vec.T

    prings_vec = np.array(Indicators.prings_know_sure_thing(closes)[(-1 * num_days):])
    prings_vec = prings_vec.T

    macd_slow_period = 24
    macd_fast_period = 12
    macd_vec = np.array(Indicators.macd(closes, macd_slow_period, macd_fast_period)[(-1 * num_days):])
    macd_vec = macd_vec.T

    kst_trix_vec = np.array(Indicators.kst_trix_indicator(closes)[(-1 * num_days):])
    kst_trix_vec = kst_trix_vec.T

    trix_vec = np.array(Indicators.trix_indicator(closes)[(-1 * num_days):])
    trix_vec = trix_vec.T

    rsi_period = 20
    rsi_type = 'sma'
    rsi_vec = np.array(Indicators.rsi(closes, rsi_period, rsi_type)[(-1 * num_days):])
    resi_vec = rsi_vec.T

    ohlc_vec = e.ohlc()

    rainbow_vecs = Indicators.rainbow_ma(ohlc_vec, [1, 3, 5, 7, 9])

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

    wti_file = os.path.join(data_directory, 'commodities', 'OIL.xlsx')
    wti = Equity(wti_file)

    wti_closes = np.array(wti.closes[(-1 * num_days):])
    wti_closes = wti_closes.T

    reit_file = os.path.join(data_directory, 'indexes', 'RE.xlsx')
    reit_eq = Equity(reit_file)

    reit_closes = np.array(reit_eq.closes[(-1 * num_days):])
    reit_closes = reit_closes.T

    snp_file = os.path.join(data_directory, 'indexes', 'SNP.xlsx')
    snp_eq = Equity(snp_file)

    snp_closes = np.array(snp_eq.closes[(-1 * num_days):])
    snp_closes = snp_closes.T

    ### CREATE DATA FRAME ###

    features = pd.DataFrame()
    a_row = pd.Series(vol_vec)
    row1 = pd.DataFrame([a_row], index = ["Volumes"])

    b_row = pd.Series(close_vec)
    row2 = pd.DataFrame([b_row], index = ["Prices"])

    c_row = pd.Series(sma_vec)
    row3 = pd.DataFrame([c_row], index = ["SMA"])

    d_row = pd.Series(ema_vec)
    row4 = pd.DataFrame([d_row], index =["EMA"])

    e_row = pd.Series(wilder_vec)
    row5 = pd.DataFrame([e_row], index = ["Wilder MA"])

    f_row = pd.Series(upper_bol_vec)
    row6 = pd.DataFrame([f_row], index = ["Upper Bolinger Band"])

    g_row = pd.Series(lower_bol_vec)
    row7 = pd.DataFrame([g_row], index = ["Lower Bolinger Band"])

    h_row = pd.Series(accum_swing_vec)
    row8 = pd.DataFrame([h_row], index = ["Accumulative Swing Index"])

    i_row = pd.Series(atr_vec)
    row9 = pd.DataFrame([i_row], index = ["Average True Range"])

    j_row = pd.Series(bop_vec)
    row10 = pd.DataFrame([j_row], index = ["Balance of Power"])

    k_row = pd.Series(gop_vec)
    row11 = pd.DataFrame([k_row], index = ["Gopalakrishnan Range Index"])

    l_row = pd.Series(pivot_ind_vec)
    row12 = pd.DataFrame([l_row], index = ["Price - Pivot Point"])

    m_row = pd.Series(prings_vec)
    row13 = pd.DataFrame([m_row], index = ["Pring's Know Sure Thing - SMA(Pring's Know Sure Thing)"])

    n_row = pd.Series(macd_vec)
    row14 = pd.DataFrame([n_row], index = ["MACD - SMA(MACD)"])

    o_row = pd.Series(kst_trix_vec)
    row15 = pd.DataFrame([o_row], index = ["d KST * d TRIX "])

    p_row = pd.Series(trix_vec)
    row16 = pd.DataFrame([p_row], index = ["TRIX - MA(TRIX)"])

    q_row = pd.Series(rsi_vec)
    row17 = pd.DataFrame([q_row], index = ["RSI"])

    r_row = pd.Series(rainbow_vec_1)
    row18 = pd.DataFrame([r_row], index = ["MA(OHLC/4, 1)"])

    s_row = pd.Series(rainbow_vec_3)
    row19 = pd.DataFrame([s_row], index = ["MA(OHLC/4, 3)"])

    t_row = pd.Series(rainbow_vec_5)
    row20 = pd.DataFrame([t_row], index = ["MA(OHLC/4, 5)"])

    u_row = pd.Series(rainbow_vec_7)
    row21 = pd.DataFrame([u_row], index = ["MA(OHLC/4, 7)"])

    v_row = pd.Series(rainbow_vec_9)
    row22 = pd.DataFrame([v_row], index = ["MA(OHLC/4, 9)"])

    w_row = pd.Series(wti_closes)
    row23 = pd.DataFrame([w_row], index = ["West Texas"])

    x_row = pd.Series(reit_closes)
    row24 = pd.DataFrame([x_row], index = ["Wilshire US Real Estate"])

    y_row = pd.Series(snp_closes)
    row25 = pd.DataFrame([y_row], index = ["SNP"])


    df = pd.concat([features, row1, row2, row3, row4, row5, row6, row7, row8, row9, 
                              row10, row11,row12, row13, row14, row15, row16, row17, 
                              row18, row19, row20, row21, row22, row23, row24, row25], ignore_index=False)
    
    if save is True:
        name = input("What do you want to save this dataframe as? (Blank to not save) ")
        np.savetxt('features_df_%s.csv' % name, features, delimiter=',')
    
    if normalize is True:
        x = (df.values).T 
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        df = pd.DataFrame(x_scaled)

    return df                       