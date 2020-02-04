import math
import numpy as np
import pandas as pd
import datetime

from models.indicators import Indicators

class Equity:

    def __init__(self, data_file):
        self.parse_data(data_file)

    def parse_data(self, data_file):
        self.data = pd.read_csv(data_file)
        
        if 'Close' in self.data.columns:
            self.data['Close'].astype(dtype=float)
            self.closes = self.data['Close'].ffill().values  # fills values if not NaN
        
        if 'Open' in self.data.columns:
            self.data['Open'].astype(dtype=float)
            self.opens = self.data['Open'].ffill().values  # fills values if not NaN
        
        if 'High' in self.data.columns:
            self.data['High'].astype(dtype=float)
            self.highs = self.data['High'].ffill().values  # fills values if not NaN
        
        if 'Low' in self.data.columns:
            self.data['Low'].astype(dtype=float)
            self.lows = self.data['Low'].ffill().values  # fills values if not NaN
            
        if 'Volume' in self.data.columns:
            self.data['Volume'].astype(dtype=int)
            self.volumes = self.data['Volume'].ffill().values

        if 'Date' in self.data.columns:
            self.data['Date'].astype(dtype=str)
            self.dates = self.data['Date'].values

        for i in range(len(self.closes)):
            ### Case for missing values
            if(self.closes[i]==0):
                # This line could end up fucking up, might not be worth fixing
                arr = [c if c > 0 else 0 for c in self.closes[i-3:i+3]]
                li = np.array(list(filter((0).__ne__, arr)))
                self.closes[i] = np.sum(li)/len(li)

    def ohlc(self):
        return (self.opens + self.highs + self.lows + self.closes) / 4

    def typical_prices(self):
        return (self.highs + self.lows + self.closes) / 3

    def balance_of_power(self):
        return (self.closes - self.opens) / (self.highs - self.lows)

    def bollinger_bands(self, period=20, stds=2):
        tp = self.typical_prices()
        ma = Indicators.sma(prices=tp, period=period)
        std = Indicators.calc_std(prices=tp, period=period)

        bolu = np.array([ma[i] + stds * std[i] for i in range(len(tp))])
        bold = np.array([ma[i] + stds * std[i] for i in range(len(tp))])

        return bolu, bold

    def accumulative_swing_index(self):
        asi = np.zeros((len(self.closes),))
        for i in range(len(self.closes)):
            if i is 0:
                continue
            curr_close = self.closes[i]
            prev_close = self.closes[i - 1]
            curr_open = self.opens[i]
            prev_open = self.opens[i - 1]
            curr_high = self.highs[i]
            prev_high = self.highs[i - 1]
            curr_low = self.lows[i]
            prev_low = self.lows[i - 1]
            k = np.max([(prev_high - curr_close), (prev_low - curr_close)])
            t = curr_high - curr_low
            kt = k / t

            num = (prev_close - curr_close + (0.5 * (prev_close - prev_open)) + (0.25 * (curr_close - curr_open)))

            r = Indicators.get_r(curr_high, curr_low, prev_close, prev_open)

            body = num / r

            asi[i] = 50 * body * kt
        return asi

    def gop_range_index(self, period=10):
        gop = np.zeros((len(self.closes),))

        for i in range(len(self.closes)):
            if i < period:
                continue
            highest = np.max(self.highs[i - period:i])
            lowest = np.min(self.lows[i - period:i])
            price_range = highest - lowest
            gop[i] = math.log(price_range) / math.log(period)

        return gop

    def pivot_points(self):
        closes = self.closes
        highs = self.highs
        lows = self.lows

        pivots = np.zeros((len(closes),))
        r1s = np.zeros((len(closes),))
        r2s = np.zeros((len(closes),))
        s1s = np.zeros((len(closes),))
        s2s = np.zeros((len(closes),))

        for i in range(len(closes)):
            pivot, r1, r2, s1, s2 = Indicators.calc_pivot_points(highs[i], lows[i], closes[i])
            pivots[i] = pivot
            r1s[i] = r1
            r2s[i] = r2
            s1s[i] = s1
            s2s[i] = s2

        return pivots, r1s, r2s, s1s, s2s

    def pivot_indicator(self):
        pivots, *_ = self.pivot_points()

        ind = np.zeros((len(pivots),))
        for i in range(len(pivots)):
            ind[i] = self.closes[i] - pivots[i]

        return ind
