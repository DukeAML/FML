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

for div in div["aapl"]:
    if div != 0.0:
        print(div)

#create col with time since last div 
