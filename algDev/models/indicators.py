import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from models.equity import equity

def sma(prices, period):
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

def ema(prices, period, type=''):
    '''
    Function to calculate the Exponential Moving Average for the equity at a given period
    @param: period = length of closing prices to look at for each equity
    @return: exponential_ma = array of EMA values for each day, 0 until 'period'
    '''
   
    exponential_ma = np.zeros((len(prices), ))
    simple_ma = sma(prices, period)
    base_sma = simple_ma[period]
    print("Base SMA: ")
    print(base_sma)
    
    if(type=='wilder'):
        multiplier = 1/period
    else:
        multiplier = 2/(period+1)

    exponential_ma[period] = calc_ema(base_sma, prices[period],multiplier)
    

    for i,close in enumerate(prices):
        if(i+period+1 >= len(prices)):
            break
        exponential_ma[i+period+1] = calc_ema(exponential_ma[i+period], prices[i+period+1], multiplier)
    
    return exponential_ma
def calc_ema(prev_ema, close, multiplier):
    '''
    Implements the Exponential Moving Average formula\n
    @param: prev_ema = EMA for the previous day.\n
    @param: close = current day's close\n
    @param: multiplier = weight for current data\n
    @return: ema = the value of the EMA for the given day\n
    '''
    ema = close * multiplier + prev_ema * (1-multiplier)
    if(ema < 0):
        print(ema)
        print(close)
        print(prev_ema)
        print(multiplier)
        print('---------------')
    return ema
def macd(prices, slow_period, fast_period):
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
    slow_ema = ema(prices, slow_period)
    fast_ema = ema(prices, fast_period)
    macd = slow_ema - fast_ema
    return macd

def calc_moves(prices, period=1):
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

def rsi(prices, period=20, type='sma'):
    
    up, down = calc_up_down(prices = prices)
   
    if(type=='sma'):
        up_avg = sma(up, period)
        down_avg = sma(down, period)
    elif(type=='ema'):
        up_avg = ema(up, period, '')
        down_avg = ema(down, period, '')
    else:
        up_avg = ema(up, period, 'wilder')
        down_avg = ema(down, period, 'wilder')
    rsi = np.zeros((len(up_avg), ))
    for i, num in enumerate(up_avg):
        if(down_avg[i]==0):
            relative_strength = float('inf')
        else:
            relative_strength = up_avg[i]/down_avg[i]
        rsi[i] = 100 - (100/(1+relative_strength))
    
    return rsi
def calc_up_down(prices, period=1):
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
    moves = calc_moves(prices, period)
    up = np.zeros((len(prices),))
    down = np.zeros((len(prices),))
    for i, move in enumerate(moves):
        if move > 0:
            up[i] = move
        else:
            down[i] = -1 * move
    return up, down

def true_range(asset, period=10):
    true_ranges = np.zeros((len(asset.closes),))
    for i, close in enumerate(asset.closes):
        if(i==0):
            continue
        high = asset.highs[i]
        low = asset.lows[i]
        cp = asset.closes[i-1]
        true_ranges[i] = np.max([high-low, np.abs(high-cp), np.abs(low-cp)])
    avg_tr = calc_average_true_range(true_ranges, period)
    return avg_tr

def calc_average_true_range(true_ranges, period=10):
    atr = np.zeros((len(true_ranges), ))
    prevatr = true_ranges[0]
    for i, tr in enumerate(true_ranges):
        atr[i] = (prevatr*(period-1) + true_ranges[i])/period
        prevatr = atr[i]
    return atr