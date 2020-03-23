from models.indicators import Indicators
import numpy as np
import  matplotlib.pyplot as plt

def plot_prices(ax, prices, line_style):
    i = np.arange(len(prices))
    ax.plot(ax, prices, line_style)

    return ax

def plot_macd(ax, prices, slow_period, fast_period, line_style='k-'):
    macd = Indicators.macd(prices, slow_period, fast_period)[slow_period - 1:]
    i = np.arange(len(prices))[slow_period-1:]
    ax.plot(i, macd, line_style)

    return ax

def plot_ema(ax, prices, period, line_style='k-'):
    ema = Indicators.ema(prices, period)[period-1:]
    i = np.arange(len(prices))[period-1:]

    ax.plot(i, ema, line_style)

    return ax
