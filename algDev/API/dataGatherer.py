# USE BLOOMBERG INSTEAD ==> YAHOO IS A MESS 
# seeking alpha - go through their news site
# dividend table in DB ==> ISIN as link/relation
# change to every stock on the S&P 500 instead of everything


# download, install interactive brokers and pyAPI, get that historical data for the ISIN's
# new data can also be gotten from there
# "problem" is that it goes back two years, but that's not an issue
# use Bloomberg for older historical data ==> pull that data ONCE rather than using a subscription -- historical data,
# so we only need to get it once

# DO THIS BY TUESDAY

import yfinance as yf
import requests
from ftplib import FTP
import numpy as np

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max 
def getPrices(ticker, period):
    tickerObj = yf.Ticker(ticker.upper())
    history = tickerObj.history(period=period)
    days = list(history['Close'])
    jsonList = []

    for i in range(len(days)):
        if np.isnan(days[i]):
            continue
        tempObj = {}
        tempObj["name"] = i
        tempObj["value"] = days[i]
        jsonList.append(tempObj)
    
    return jsonList


def getTickers():
    tickers = []

    def processTicker(ticker):
        if(ticker[:6] == 'Symbol'):
            return
        else:
            tickers.append(ticker.split('|')[0])


    with FTP('ftp.nasdaqtrader.com') as ftp:
        ftp.login()
        ftp.cwd('SymbolDirectory')
        # ftp.retrlines('LIST')
        test = ftp.retrlines('RETR nasdaqlisted.txt', processTicker)
    
    return tickers

if __name__ == "__main__":
    msft = yf.Ticker("MSFT")

    # get stock info
    msft.info

    # get historical market data
    hist = msft.history(period="1mo")

    print(list(hist['Close']))
