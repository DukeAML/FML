import pandas as pd
import math
import numpy as np


class Indicators:
    """Contains commonly used technical indicators for various asset classes."""

    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)
        self.data['Close'].astype(dtype=float)
        # self.data['Close'].replace({'.': np.nan, '#N/A': np.nan}, inplace=True)
        self.closes = self.data['Close'].ffill().values  # fills close with last price if given '.'
        self.dates = self.data['Date'].values
        self.length = len(self.data)
        self.shape = (self.length,)

    @staticmethod
    def sma(period, prices):
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
    def ema(period, prices):
        """
        Function to calculate the Exponential Moving Average for the equity at a given period
        @param: period = length of closing prices to look at for each equity
        @return: exponential_ma = array of EMA values for each day, 0 until 'period'
        """

        exponential_ma = np.zeros((len(prices),))

        simple_ma = Indicators.sma(period, prices)

        base_sma = simple_ma[period]
        print("Base SMA: ")
        print(base_sma)
        exponential_ma[period] = Indicators.calc_ema(base_sma, prices[period], period)

        if type == 'wilder':
            multiplier = 1 / period
        else:
            multiplier = 2 / (period + 1)

        for i, close in enumerate(prices):
            if i + period + 1 >= len(prices):
                break

            exponential_ma[i + period + 1] = Indicators.calc_ema(exponential_ma[i + period],
                                                                 self.closes[i + period + 1],
                                                                 multiplier)

        for em in exponential_ma:
            if em < 0:
                print(em)

        return exponential_ma

    @staticmethod
    def calc_ema(prev_ema, close, multiplier):
        """
        Implements the Exponential Moving Average formula\n
        @param: prev_ema = EMA for the previous day.\n
        @param: close = current day's close\n
        @param: multiplier = weight for current data\n
        @return: ema = the value of the EMA for the given day\n
        """
        return (close - prev_ema) * multiplier + prev_ema

    def macd(self, slow_period, fast_period):

        """
        Calculate the Moving Average Compounding Difference\n
        @param: slow_period = number of days for longer period\n
        @param: fast_period = number of days for shorter period\n
        @requirement: slow_period > fast_period\n
        @return: macd = an array of the MACD to the same indexes close for the given period.\n
            For example, if 'fast_period' is 10 and 'slow_period' is 20, the ith 
            index will correspond to the difference between the ith EMA(20) and ith EMA(10). 
            indexes 0-19 will be 0
        """
        assert slow_period > fast_period
        return self.ema(slow_period) - self.ema(fast_period)

    @staticmethod
    def calc_moves(prices, period=1):
        """
        Calculate the movement between two periods\n
        @param: period = number of days between closes\n
        @return: moves = an array of the move relative to the same indexes close for the given period.\n
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
    def rsi(self, prices, period=20, type='sma'):  # TODO: Rename type (shadows built-in)

        up, down = self.calc_up_down(prices=prices)

        if type == 'sma':
            up_avg = self.sma(period, up)
            down_avg = self.sma(period, down)
        elif type == 'ema':
            up_avg = self.ema(period, up, '')
            down_avg = self.ema(period, down, '')
        else:
            up_avg = self.ema(period, up, 'wilder')
            down_avg = self.ema(period, down, 'wilder')

        rsi = np.zeros((len(up_avg),))
        for i, num in enumerate(up_avg):
            if down_avg[i] == 0:
                relative_strength = float('inf')
            else:
                relative_strength = up_avg[i] / down_avg[i]
            rsi[i] = 100 - (100 / (1 + relative_strength))

        return rsi

    @staticmethod
    def calc_up_down(self, prices, period=1):
        """
        Calculates the up-down of the equity for a given period\n @param: period = number of days between closes\n
        @return: up: an array of the move relative to the same indexes close for the given period. With a floor at
        0.\n @return: down: an array of the move relative to the same indexes close for the given period. With a
        cieling at 0.\n For example, if 'period' is 1, the ith index of 'up' will correspond to the difference
        between the ith close and i - 1 th close but negative entries will be 0. 'down' will be all negative entries
        with the positives as 0. index 0 will be 0
        """
        moves = self.calc_moves(prices, period)

        up = np.zeros(self.shape)
        down = np.zeros(self.shape)

        for i, move in enumerate(moves):
            if move > 0:
                up[i] = move
            else:
                down[i] = -1 * move

        return up, down

    @staticmethod
    def macd_indicator(prices, slow_period, fast_period):
        macd_vals = macd(prices, slow_period, fast_period)

        macd_sma = sma(macd_vals, 9)
        macd_ind = np.array([macd_val - macd_sma for (macd_val, macd_sma) in (macd_vals, macd_smas)])

        return macd_ind


def average_true_range(asset, period=10):
    true_ranges = np.zeros((len(asset.closes),))
    for i, close in enumerate(asset.closes):
        if i == 0:
            continue
        high = asset.highs[i]
        low = asset.lows[i]
        cp = asset.closes[i - 1]
        true_ranges[i] = np.max([high - low, np.abs(high - cp), np.abs(low - cp)])
    avg_tr = calc_average_true_range(true_ranges, period)
    return avg_tr


def calc_average_true_range(true_ranges, period=10):
    atr = np.zeros((len(true_ranges),))
    prevatr = true_ranges[0]
    for i, tr in enumerate(true_ranges):
        atr[i] = (prevatr * (period - 1) + true_ranges[i]) / period
        prevatr = atr[i]
    return atr


def roc(prices):
    roc_vals = np.zeros((len(prices),))
    for i, price in enumerate(prices):
        if i is 0:
            continue
        roc_vals[i] = ((price / prices[i - 1]) - 1) * 100

    return roc_vals


def kst(prices):
    rcma_1 = rcma(prices)
    rcma_2 = rcma(prices, 10)
    rcma_3 = rcma(prices, 10)
    rcma_4 = rcma(prices, 15)

    kst_vals = np.zeros((len(prices),))
    for i in range(len(prices)):
        kst_vals[i] = rcma_1[i] + rcma_2[i] * 2 + rcma_3[i] * 3 + rcma_4[i] * 4
    return kst_vals


def kst_trix_indicator(prices):
    kst_vals = kst(prices)
    d_kst = d_(kst_vals)

    trix_vals = trix(prices)
    d_trix = d_(trix_vals)

    ind = np.zeros((len(d_kst),))

    for i in range(len(ind)):
        ind[i] = d_kst[i] * d_trix[i]

    return ind


def d_(prices):
    d_p = np.zeros((len(prices),))

    for i in range(len(d_p)):
        if i == 0:
            continue
        d_p[i] = prices[i] - prices[i - 1]

    return d_p


def rcma(prices, sma_period=10):
    return sma(prices, sma_period)


def calc_pivot_points(high, low, close):
    pivot = (high + low + close) / 3

    r1 = (pivot * 2) - low
    r2 = pivot + (high - low)
    s1 = (pivot * 2) - high
    s2 = pivot - (high - low)

    return pivot, r1, r2, s1, s2


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


def calc_std(prices, period):
    stds = np.zeros((len(prices),))

    for i in range(len(prices)):
        if i < period:
            continue
        stds[i] = np.std(prices[i - period:i])

    return stds


def rainbow_ma(prices, periods=(1, 3, 5, 7, 9)):
    return [sma(prices, period) for period in periods]


def trix(prices):
    single_smoothed_ema = ema(prices, 18)
    double_smoothed_ema = ema(single_smoothed_ema, 18)
    triple_smoothed_ema = ema(double_smoothed_ema, 18)

    trix_vals = np.zeros((len(triple_smoothed_ema),))

    for i in range(len(trix_vals)):
        if i is 0:
            continue
        if triple_smoothed_ema[i - 1] == 0:
            trix_vals[i] = 0
            continue

        trix_vals[i] = (triple_smoothed_ema[i] - triple_smoothed_ema[i - 1]) / triple_smoothed_ema[i - 1]

    return trix_vals


def trix_indicator(prices):
    trix_vals = trix(prices)
    t_ma = ema(trix_vals, 9)

    return np.array([trix_vals[i] - t_ma[i] for i in range(len(trix_vals))])


def prings_know_sure_thing(prices):
    kst_vec = kst(prices)
    kst_sma = sma(kst_vec, 9)

    return np.array([kst_vec[i] - pkst[i] for i in range(len(kst_sma))])
