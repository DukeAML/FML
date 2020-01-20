import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

class equity:
    
    def initialize(self, data_file):
        
        data = pd.read_csv(data_file)

        self.opens = []
        self.closes = []
        self.highs = []
        self.lows = []
        self.dates = []
        self.volumes = []
        
        for index, row in data.iterrows():
            self.closes.append(float(row["Close"]))
            self.opens.append(float(row["Open"]))
            self.lows.append(float(row["Low"]))
            self.highs.append(float(row["High"]))
            self.dates.append(row["Date"])
            self.volumes.append(int(row["Volume"]))

        self.length = len(self.closes)
        self.shape = (self.length,)

    def __init__(self,data_file):
        self.initialize(data_file)
    
    def sma(self, period, prices):
        '''
        Function to calculate the Simple Moving Average for the equity at a given period
        @param: period = length of closing prices to look at for each equity
        @return: simple_ma = array of SMA values for each day, 0 until 'period'
        '''
        simple_ma = np.zeros((len(prices), ))
        for i, p in enumerate(prices):
            sum = 0
            if(i+period >= len(prices)):
                    break
            for j in range(period):
                sum = prices[i+j] + sum
            ma = sum/period
            simple_ma[i+period] = ma
        
        return simple_ma
    
    def ema(self, period):
        '''
        Function to calculate the Exponential Moving Average for the equity at a given period
        @param: period = length of closing prices to look at for each equity
        @return: exponential_ma = array of EMA values for each day, 0 until 'period'
        '''
       
        exponential_ma = np.zeros((len(prices), ))

        simple_ma = self.sma(period, prices)

        base_sma = simple_ma[period]
        print("Base SMA: ")
        print(base_sma)
        exponential_ma[period] = self.calc_ema(base_sma, prices[period],period)
        
        if(type=='wilder'):
            multiplier = 1/period
        else:
            multiplier = 2/(period+1)

        for i,close in enumerate(prices):
            if(i+period+1 >= len(prices)):
                break

            exponential_ma[i+period+1] = self.calc_ema(exponential_ma[i+period], self.closes[i+period+1], multiplier)
        
        for em in exponential_ma:
            if(em < 0):
                print(em)
        
        return exponential_ma

    def calc_ema(self, prev_ema, close, multiplier):
        '''
        Implements the Exponential Moving Average formula\n
        @param: prev_ema = EMA for the previous day.\n
        @param: close = current day's close\n
        @param: multiplier = weight for current data\n
        @return: ema = the value of the EMA for the given day\n
        '''
        ema = (close - prev_ema) * multiplier + prev_ema
        return ema

    def macd(self, slow_period, fast_period):

        '''
        Calculate the Moving Average Compounding Difference\n
        @param: slow_period = number of days for longer period\n
        @param: fast_period = number of days for shorter period\n
        @requirement: slow_period > fast_period\n
        @return: macd = an array of the MACD to the same indexes close for the given period.\n
            For example, if 'fast_period' is 10 and 'slow_period' is 20, the ith 
            index will correspond to the difference between the ith EMA(20) and ith EMA(10). 
            indexes 0-19 will be 0
        '''
        assert(slow_period > fast_period)

        slow_ema = self.ema(slow_period)
        fast_ema = self.ema(fast_period)

        macd = slow_ema - fast_ema
        return macd

    
    def calc_moves(self, prices, period=1):
        '''
        Calculate the movement between two periods\n
        @param: period = number of days between closes\n
        @return: moves = an array of the move relative to the same indexes close for the given period.\n
            For example, if  'period' is 10, the ith index will correspond 
            to the difference between the ith close and i - 10th close. 
            indexes 0-9 will be 0
        '''
        moves = np.zeros((len(prices),))
        for i,close in enumerate(prices):
            index = i+period
            if(index >= len(prices)):
                break
            moves[index] = prices[index] - prices[index-period]
        
        return moves

    def rsi(self, prices, period=20, type='sma'):
        
        up, down = self.calc_up_down(prices = prices)
       
        if(type=='sma'):
            up_avg = self.sma(period, up)
            down_avg = self.sma(period, down)
        elif(type=='ema'):
            up_avg = self.ema(period, up, '')
            down_avg = self.ema(period, down, '')
        else:
            up_avg = self.ema(period, up, 'wilder')
            down_avg = self.ema(period, down, 'wilder')

        rsi = np.zeros((len(up_avg), ))
        for i, num in enumerate(up_avg):
            if(down_avg[i]==0):
                relative_strength = float('inf')
            else:
                relative_strength = up_avg[i]/down_avg[i]
            rsi[i] = 100 - (100/(1+relative_strength))
        
        return rsi


    def calc_up_down(self, prices, period=1):
        '''
        Calculates the up-down of the equity for a given period\n
        @param: period = number of days between closes\n
        @return: up: an array of the move relative to the same indexes close for the given period. With a floor at 0.\n
        @return: down: an array of the move relative to the same indexes close for the given period. With a cieling at 0.\n
            For example, if 'period' is 1, the ith index of 'up' will correspond 
            to the difference between the ith close and i - 1 th close but negative 
            entries will be 0. 'down' will be all negative entries with the positives as 0.
            index 0 will be 0
        '''

        moves = self.calc_moves(prices, period)

        up = np.zeros(self.shape)
        down = np.zeros(self.shape)

        for i, move in enumerate(moves):
            if move > 0:
                up[i] = move
            else:
                down[i] = -1 * move

        return up, down

    



