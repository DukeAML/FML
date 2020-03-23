def gen_features(ticker, save=False, normalize=False):
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

    if normalize is True:
        for i in range(features.shape[1]):
            features[:,i] = norm(features[:,i])

    if save is True:
        name = input("What do you want to save these features as? (Blank to not save) ")
        np.savetxt('features_%s.csv' % name, features, delimiter=',')

    return features




    