import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from algDev.models.indicators import Indicators


class SNP(Indicators):

    def __init__(self, data_file):
        data = pd.read_csv(data_file)

        self.opens = []
        self.closes = []
        self.highs = []
        self.lows = []
        self.dates = []
        self.volumes = []

        for index, row in data.iterrows():
            row_data = row['Date,Open,High,Low,Close,Adj Close,Volume'].split(',')
            self.closes.append(float(row_data[4]))
            self.opens.append(float(row_data[1]))
            self.lows.append(float(row_data[3]))
            self.highs.append(float(row_data[2]))
            self.dates.append(row_data[0])
            self.volumes.append(int(row_data[6]))

        self.length = len(self.closes)
        self.shape = (self.length,)

    def ohlc(self):
        ohlc_vals = np.zeros(self.shape)
        for i in range(self.length):
            open = self.opens[i]
            high = self.highs[i]
            low = self.lows[i]
            close = self.closes[i]

            ohlc_vals[i] = (open + high + low + close) / 4

        return ohlc_vals

    def typical_prices(self):
        tp = np.zeros(self.shape)
        for i in range(self.length):
            high = self.highs[i]
            low = self.lows[i]
            close = self.closes[i]

            tp[i] = (high + low + close) / 3

        return tp
