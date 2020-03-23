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

for tckr in tickers:
    paid=[]
    for ii in range(len(div[tckr])):
        if div[tckr][ii] != 0: 
            paid.append(ii)
    if not paid:
        print(tckr + " has issued no derivatives")   
    else:

        count = [999 for ii in range(len(div[tckr]))]

        for ii in range(len(count)):
            if ii in paid: 
                count[ii] = 0
            else:
                if ii < min(paid):
                    count[ii] = "na"
                else:
                    c =0
                    tmp = ii
                    while ii not in paid and ii > min(paid):
                        ii -= 1 
                        c+=1
                    count[tmp] = c
            div["Passing Time: " + tckr] = count


print(div.head())



