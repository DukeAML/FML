import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import py_vollib.black_scholes as vol
import yfinance as yf
from pandas_datareader import data as pdr

tickers =["aapl", "goog", "nflx"]

div = pd.DataFrame()
for tckr in tickers:
    eq = yf.Ticker(tckr)
    hist = eq.history(period="max")
    div[tckr] = hist["Dividends"]

div = div.fillna(0)

paid=[]
for ii in range(len(div["aapl"])):
    if div["aapl"][ii] != 0: 
        paid.append(ii)



