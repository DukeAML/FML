import pandas as pd
import math
import numpy as np

from algDev.models.indicator import Indicator

class Indicators:
    
    """
    
    Contains commonly used technical indicators for various asset classes.
    
    """

    def __init__(self):
        
        self.length = len(self.data)
        self.shape = (self.length,)

    @staticmethod
    def sma(prices, period):
        """[
            Function to calculate the Simple Moving Average 
        for the equity at a given period
        ]
        
        Arguments:
            prices {[float[]]} -- [description]
            period {[int]} -- [length of closing prices to look at for each equity]
        
        Returns:
            [float[]] -- [array of SMA values for each day, 0 until 'period']
        """
        simple_ma = np.zeros((len(prices),))
        for i, p in enumerate(prices):
            if i + period - 1 >= len(prices):
                break
            ma = 0
            for j in range(period):
                ma = prices[i + j] + ma
            simple_ma[i] = ma/period
        return simple_ma[:(-1*(period))]

    @staticmethod
    def ema(prices, period, type=''):
        """
        [
            Function to calculate the Exponential Moving 
        Average for the equity at a given period
        ]
        
        Arguments:
            prices {[float[]]} -- [Prices to look at]
            period {[int]} -- [length of closing prices to look at for each equity]
        
        Keyword Arguments:
            type {str} -- [either reg or ema] (default: {''})
        
        Returns:
            [float[]] -- [the ema of the prices inputted as a vector]
        """
        
        exponential_ma = np.zeros((len(prices),))

        simple_ma = Indicators.sma(prices, period)

        base_sma = simple_ma[-1 * (period - 1)]
        
        if type == 'wilder':
            multiplier = (1 / period)
        else:
            multiplier = (2 / (period + 1))

        exponential_ma[-1 * (period - 1)] = Indicators.calc_ema(base_sma, prices[-period], multiplier)
        l = len(prices)
        for i, p in enumerate(prices):
            if l - i - period < 0:
                break
            ma = 0
            exponential_ma[l - i - period] = Indicators.calc_ema(exponential_ma[l - i - period + 1],
                                                                 prices[l - i - period],
                                                                 multiplier)

        return exponential_ma[:(-1*(period))]

    @staticmethod
    def calc_ema(prev_ema, close, multiplier):
        """[
            Implements the Exponential Moving Average formula
        ]
        @param: prev_ema = .\n
        @param: close = \n
        @param: multiplier = \n
        @return: ema = \n
        Arguments:
            prev_ema {[float]} -- [EMA for the previous day]
            close {[float]} -- [current day's close]
            multiplier {[float]} -- [weight for current data]
        
        Returns:
            [float -- [the value of the EMA for the given day]
        """

        return (close - prev_ema) * multiplier + prev_ema

    @staticmethod
    def macd(prices, slow_period, fast_period):

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
        return Indicators.ema(prices, slow_period) - Indicators.ema(prices, fast_period)[slow_period-fast_period:]

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

        return moves[:(-1*period)]

    @staticmethod
    def rsi(prices, period=20, type='ema'):  # TODO: Rename type (shadows built-in)

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
        
        macd_emas = Indicators.ema(macd_vals, 9)

        macd_ind = np.zeros((len(macd_vals),))
        for i,macd_val in enumerate(macd_vals):
            
            # print(macd_val, macd_vals[i+1], macd_emas[i], macd_emas[i+1])
            macd_ind[i] = Indicators.gen_macd_ind_lbl(macd_val, macd_vals[i+1], macd_emas[i], macd_emas[i+1])

        macd_ind = np.array([(macd_val - macd_ema) for (macd_val, macd_ema) in zip(macd_vals, macd_emas)])

        return macd_ind


    @staticmethod
    def gen_macd_ind_lbl(macd_val_0, macd_val_1, macd_ema_0, macd_ema_1):
        cross = Indicators.check_intersection(macd_val_0, macd_val_1, macd_ema_0, macd_ema_1)
        
        if cross is True:
            m = Indicators.get_slope(0,1,macd_val_0,macd_val_1)
            if m >=0:
                return 1

        ## For now just generating ones on buy and zeros else... eventually three classes might be good
        return 0

    @staticmethod
    def check_intersection(y_11, y_12, y_21, y_22):
        x11, x12, x21, x22 = 0, 1, 0, 1
        # print(y_11, y_12, y_21, y_22)
        m1 = Indicators.get_slope(0,1,y_11,y_12)
        m2 = Indicators.get_slope(0,1,y_21,y_22)

        b1 = y_11
        b2 = y_21

        A = np.array([[m1, -1],[m2, -1]]).reshape((2,2))
        b = np.array([b1, b2]).reshape((2,1))
        # print(A)
        # print(b)
        X = np.linalg.solve(A, b)

        x = X[0]
        y = X[1]
        cross = False
        if(x >= 0 and x <= 1):
            cross = True
        
        return cross

    @staticmethod
    def get_slope(x_0, x_1, y_0, y_1):
        m = (y_1 - y_0)/(x_1 - x_0)

        return m
    @staticmethod
    def average_true_range(asset, period=10):
        true_ranges = np.zeros((len(asset.closes),))
        for i, close in enumerate(asset.closes):
            if i + 1 >= len(asset.closes):
                break
            high = asset.highs[i]
            low = asset.lows[i]
            cp = asset.closes[i + 1]
            true_ranges[i] = np.max([high - low, np.abs(high - cp), np.abs(low - cp)])
        avg_tr = Indicators.calc_average_true_range(true_ranges, period)
        return avg_tr
    
    @staticmethod
    def calc_average_true_range(true_ranges, period=10):
        atr = np.zeros((len(true_ranges),))
        l = len(true_ranges)
        prevatr = true_ranges[-1]
        for i, tr in enumerate(true_ranges):
            atr[l - i - 1] = (prevatr * (period - 1) + true_ranges[l - i - 1]) / period
            prevatr = atr[l - i - 1]
        return atr[:-1]
    
    @staticmethod
    def roc(prices):
        roc_vals = np.zeros((len(prices),))
        for i, price in enumerate(prices):
            if i >= len(prices) - 1:
                break
            roc_vals[i] = ((price / prices[i + 1]) - 1) * 100
    
        return roc_vals[:-1]
    
    @staticmethod
    def kst(prices):
        tenp_roc = np.zeros((len(prices),))
        fifteenp_roc = np.zeros((len(prices),))
        twentyp_roc = np.zeros((len(prices),))
        thirtyp_roc = np.zeros((len(prices),))
        for i in range(len(prices)):
            if i + 10 >= len(prices):
                continue
            tenp_roc[i] = (prices[i] - prices[i+10])/prices[i+10]
            if i + 15 >= len(prices):
                continue
            fifteenp_roc[i] = (prices[i] - prices[i+15])/prices[i+15]
            if i + 20 >= len(prices):
                continue
            twentyp_roc[i] = (prices[i] - prices[i+20])/prices[i+20]
            if i + 30 >= len(prices):
                continue
            thirtyp_roc[i] = (prices[i] - prices[i+30])/prices[i+30]


        rcma_1 = Indicators.sma(tenp_roc, 10)
        rcma_2 = Indicators.sma(fifteenp_roc, 10)
        rcma_3 = Indicators.sma(twentyp_roc, 10)
        rcma_4 = Indicators.sma(thirtyp_roc, 15)
    
        kst_vals = np.zeros((len(rcma_4),))
        for i,p in enumerate(rcma_4):
            kst_vals[i] = rcma_1[i] + rcma_2[i] * 2 + rcma_3[i] * 3 + rcma_4[i] * 4
        return kst_vals
    
    @staticmethod
    def kst_trix_indicator(prices):
        kst_vals = Indicators.kst(prices)[:-94]
        d_kst = Indicators.d_(kst_vals)
    
        trix_vals = Indicators.trix(prices)
        d_trix = Indicators.d_(trix_vals)
        
        assert len(kst_vals)==len(trix_vals)
        
        ind = np.zeros((len(d_kst),))
    
        for i in range(len(ind)):
            ind[i] = np.sign(d_kst[i] * d_trix[i])
    
        return ind[:-1]
    
    @staticmethod
    def d_(prices):
        d_p = np.zeros((len(prices),))
    
        for i in range(len(d_p)):
            if i + 1 >= len(d_p):
                continue
            d_p[i] = prices[i] - prices[i + 1]
    
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
            if i + period >= len(prices):
                continue
            stds[i] = np.std(prices[i:i+period])
    
        return stds[:(-1*(period))]
    
    @staticmethod
    def rainbow_ma(prices, periods=(1, 3, 5, 7, 9)):
        
        return [Indicator(Indicators.sma(prices, period).T) for period in periods]
    
    @staticmethod
    def trix(prices):
        single_smoothed_ema = Indicators.ema(prices, 18)
        double_smoothed_ema = Indicators.ema(single_smoothed_ema, 18)
        triple_smoothed_ema = Indicators.ema(double_smoothed_ema, 18)
    
        trix_vals = np.zeros((len(triple_smoothed_ema),))
    
        for i in range(len(trix_vals)):
            if i + 1 >= len(trix_vals):
                continue
            if triple_smoothed_ema[i + 1] == 0:
                trix_vals[i] = 0
                continue
            
            trix_vals[i] = (triple_smoothed_ema[i] - triple_smoothed_ema[i + 1]) / triple_smoothed_ema[i + 1]
    
        return trix_vals[:-55]
    
    @staticmethod
    def trix_indicator(prices):
        trix_vals = Indicators.trix(prices)[:-9]
        t_ma = Indicators.ema(trix_vals, 9)
        assert len(trix_vals)==len(t_ma)
        return np.array([trix_vals[i] - t_ma[i] for i in range(len(trix_vals))])
    
    @staticmethod
    def prings_know_sure_thing(prices):

        kst_vec = Indicators.kst(prices)
        kst_sma = Indicators.sma(kst_vec, 9)
        kst_vec = kst_vec[:-9]
        assert len(kst_vec)==len(kst_sma)
        return np.array([kst_vec[i] - kst_sma[i] for i in range(len(kst_sma))])
