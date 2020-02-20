import yfinance as yf
import requests
from ftplib import FTP

msft = yf.Ticker("MSFT")

# get stock info
msft.info

# get historical market data
hist = msft.history(period="max")

# print(hist)

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
        print(tickers)

if __name__ == "__main__":
    getTickers()
