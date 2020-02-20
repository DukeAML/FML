import yfinance as yf
import requests
from ftplib import FTP

def getPrices(ticker):
    tickerObj = yf.Ticker(ticker.upper())
    history = tickerObj.history(period="1mo")
    days = list(history['Close'])
    jsonList = []

    for i in range(len(days)):
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
