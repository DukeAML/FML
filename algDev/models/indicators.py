import pandas as pd
import math
import numpy as np


class Indicators:
    """Contains commonly used technical indicators for various asset classes."""

    def __init__(self):

        self.length = len(self.data)
        self.shape = (self.length,)

    @staticmethod
    def sma(prices, period):
        """
        Function to calculate the Simple Moving Average for the equity at a given period
        @param: period = length of closing prices to look at for each equity
        @return: simple_ma = array of SMA values for each day, 0 until 'period'
        """
        simple_ma = np.zeros((len(prices),))
        for i, p in enumerate(prices):
            if i + period >= len(prices):
                break
            ma = sum(prices[i + j] for j in range(period)) / period
            simple_ma[i + period] = ma
        return simple_ma

    @staticmethod
    def ema(prices, period, type=''):
        """
        Function to calculate the Exponential Moving Average for the equity at a given period
        @param: period = length of closing prices to look at for each equity
        @return: exponential_ma = array of EMA values for each day, 0 until 'period'
        """

        exponential_ma = np.zeros((len(prices),))

        simple_ma = Indicators.sma(prices, period)

        base_sma = simple_ma[period]

        exponential_ma[period] = base_sma

        if type == 'wilder':
            multiplier = 1 / period
        else:
            multiplier = 2 / (period + 1)

        for i, close in enumerate(prices):
            if i + period + 1 >= len(prices):
                break

            exponential_ma[i + period + 1] = prices[i + period + 1] * multiplier + exponential_ma[i + period] * (
                    1 - multiplier)

        return exponential_ma

    @staticmethod
    def macd(prices, slow_period, fast_period):

        """
        Calculate the Moving Average Convergence Divergence
        @param: slow_period = number of days for longer period
        @param: fast_period = number of days for shorter period
        @requirement: slow_period > fast_period
        @return: macd = an array of the MACD to the same indexes close for the given period.
            For example, if 'fast_period' is 10 and 'slow_period' is 20, the ith 
            index will correspond to the difference between the ith EMA(20) and ith EMA(10). 
            indexes 0-19 will be 0
        """
        assert slow_period > fast_period
        return Indicators.ema(prices, slow_period) - Indicators.ema(prices, fast_period)

    @staticmethod
    def calc_moves(prices, period=1):
        """
        Calculate the movement between two periods
        @param: period = number of days between closes
        @return: moves = an array of the move relative to the same indexes close for the given period.
            For example, if  'period' is 10, the ith index will correspond 
            to the difference between the ith close and i - 10th close. 
            indexes 0-9 will be 0
        """
        moves = np.zeros((len(prices),))
        for i, close in enumerate(prices):
            index = i + period
            if index >= len(prices):
                break
            moves[index] = prices[index] - prices[index - period]

        return moves

    @staticmethod
    def rsi(prices, period=20, type='sma'):  # TODO: Rename type (shadows built-in)

        up, down = Indicators.calc_up_down(prices=prices)

        if type == 'sma':
            up_avg = Indicators.sma(up, period)
            down_avg = Indicators.sma(down, period)
        elif type == 'ema':
            up_avg = Indicators.ema(up, period, '')
            down_avg = Indicators.ema(down, period, '')
        else:
            up_avg = Indicators.ema(up, period, 'wilder')
            down_avg = Indicators.ema(down, period, 'wilder')

        rsi = np.zeros((len(up_avg),))
        for i, num in enumerate(up_avg):
            if down_avg[i] == 0:
                relative_strength = float('inf')
            else:
                relative_strength = up_avg[i] / down_avg[i]
            rsi[i] = 100 - (100 / (1 + relative_strength))

        return rsi

    @staticmethod
    def calc_up_down(prices, period=1):
        """
        Calculates the up-down of the equity for a given period\n @param: period = number of days between closes\n
        @return: up: an array of the move relative to the same indexes close for the given period. With a floor at
        0.\n @return: down: an array of the move relative to the same indexes close for the given period. With a
        cieling at 0.\n For example, if 'period' is 1, the ith index of 'up' will correspond to the difference
        between the ith close and i - 1 th close but negative entries will be 0. 'down' will be all negative entries
        with the positives as 0. index 0 will be 0
        """
        moves = Indicators.calc_moves(prices, period)

        up = np.zeros((len(prices),))
        down = np.zeros((len(prices),))

        for i, move in enumerate(moves):
            if move > 0:
                up[i] = move
            else:
                down[i] = -1 * move

        return up, down

    @staticmethod
    def macd_indicator(prices, slow_period, fast_period):
        macd_vals = Indicators.macd(prices, slow_period, fast_period)

        macd_smas = Indicators.sma(macd_vals, 9)
        macd_ind = np.array([(macd_val - macd_sma) for (macd_val, macd_sma) in zip(macd_vals, macd_smas)])

        return macd_ind

    @staticmethod
    def average_true_range(asset, period=10):
        true_ranges = np.zeros((len(asset.closes),))
        for i, close in enumerate(asset.closes):
            if i == 0:
                continue
            high = asset.highs[i]
            low = asset.lows[i]
            cp = asset.closes[i - 1]
            true_ranges[i] = np.max([high - low, np.abs(high - cp), np.abs(low - cp)])
        avg_tr = Indicators.calc_average_true_range(true_ranges, period)
        return avg_tr

    @staticmethod
    def calc_average_true_range(true_ranges, period=10):
        atr = np.zeros((len(true_ranges),))
        prevatr = true_ranges[0]
        for i, tr in enumerate(true_ranges):
            atr[i] = (prevatr * (period - 1) + true_ranges[i]) / period
            prevatr = atr[i]
        return atr

    @staticmethod
    def roc(prices):
        roc_vals = np.zeros((len(prices),))
        for i, price in enumerate(prices):
            if i is 0:
                continue
            roc_vals[i] = ((price / prices[i - 1]) - 1) * 100

        return roc_vals

    @staticmethod
    def kst(prices):
        tenp_roc = np.zeros((len(prices),))
        fifteenp_roc = np.zeros((len(prices),))
        twentyp_roc = np.zeros((len(prices),))
        thirtyp_roc = np.zeros((len(prices),))
        for i in range(len(prices)):
            if i < 10:
                continue
            tenp_roc[i] = (prices[i] - prices[i - 10]) / prices[i - 10]
            if i < 15:
                continue
            fifteenp_roc[i] = (prices[i] - prices[i - 15]) / prices[i - 15]
            if i < 20:
                continue
            twentyp_roc[i] = (prices[i] - prices[i - 20]) / prices[i - 20]
            if i < 30:
                continue
            thirtyp_roc[i] = (prices[i] - prices[i - 30]) / prices[i - 30]

        rcma_1 = Indicators.sma(tenp_roc, 10)
        rcma_2 = Indicators.sma(fifteenp_roc, 10)
        rcma_3 = Indicators.sma(twentyp_roc, 10)
        rcma_4 = Indicators.sma(thirtyp_roc, 15)

        kst_vals = np.zeros((len(prices),))
        for i in range(len(prices)):
            kst_vals[i] = rcma_1[i] + rcma_2[i] * 2 + rcma_3[i] * 3 + rcma_4[i] * 4
        return kst_vals

    @staticmethod
    def kst_trix_indicator(prices):
        kst_vals = Indicators.kst(prices)
        d_kst = Indicators.d_(kst_vals)

        trix_vals = Indicators.trix(prices)
        d_trix = Indicators.d_(trix_vals)

        ind = np.zeros((len(d_kst),))

        for i in range(len(ind)):
            ind[i] = d_kst[i] * d_trix[i]

        return ind

    @staticmethod
    def d_(prices):
        d_p = np.zeros((len(prices),))

        for i in range(len(d_p)):
            if i == 0:
                continue
            d_p[i] = prices[i] - prices[i - 1]

        return d_p

    @staticmethod
    def calc_pivot_points(high, low, close):
        pivot = (high + low + close) / 3

        r1 = (pivot * 2) - low
        r2 = pivot + (high - low)
        s1 = (pivot * 2) - high
        s2 = pivot - (high - low)

        return pivot, r1, r2, s1, s2

    @staticmethod
    def get_r(curr_high, curr_low, prev_close, prev_open):
        one = curr_high - prev_close
        two = curr_low - prev_close
        three = curr_high - curr_low

        if one >= two and one >= three:
            r = curr_high - prev_close - (0.5 * (curr_low - prev_close)) + (0.25 * (prev_close - prev_open))
        if two >= one and two >= three:
            r = curr_low - prev_close - (0.5 * (curr_high - prev_close)) + (0.25 * (prev_close - prev_open))
        if three >= one and three >= two:
            r = curr_high - curr_low + (0.25 * (prev_close - prev_open))

        return r

    @staticmethod
    def calc_std(prices, period):
        stds = np.zeros((len(prices),))

        for i in range(len(prices)):
            if i < period:
                continue
            stds[i] = np.std(prices[i - period:i])

        return stds

    @staticmethod
    def rainbow_ma(prices, periods=(1, 3, 5, 7, 9)):
        return [Indicators.sma(prices, period) for period in periods]

    @staticmethod
    def trix(prices):
        single_smoothed_ema = Indicators.ema(prices, 18)
        double_smoothed_ema = Indicators.ema(single_smoothed_ema, 18)
        triple_smoothed_ema = Indicators.ema(double_smoothed_ema, 18)

        trix_vals = np.zeros((len(triple_smoothed_ema),))

        for i in range(len(trix_vals)):
            if i is 0:
                continue
            if triple_smoothed_ema[i - 1] == 0:
                trix_vals[i] = 0
                continue

            trix_vals[i] = (triple_smoothed_ema[i] - triple_smoothed_ema[i - 1]) / triple_smoothed_ema[i - 1]

        return trix_vals

    @staticmethod
    def trix_indicator(prices):
        trix_vals = Indicators.trix(prices)
        t_ma = Indicators.ema(trix_vals, 9)

        return np.array([trix_vals[i] - t_ma[i] for i in range(len(trix_vals))])

    @staticmethod
    def prings_know_sure_thing(prices):
        kst_vec = Indicators.kst(prices)
        kst_sma = Indicators.sma(kst_vec, 9)

        return np.array([kst_vec[i] - kst_sma[i] for i in range(len(kst_sma))])
