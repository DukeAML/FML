import io
import ftplib
import pandas
import requests
import requests_html
import ssl
import numpy
from yahoo_fin import options
from yahoo_fin import stock_info as si
import matplotlib.pyplot as plt
import py_vollib.black_scholes as vol


tickers = ["aapl", "nflx"]

dow_data = {}
for ticker in tickers:
    try:
        dow_data[ticker] = options.get_options_chain(ticker)
    except Exception:
        print(ticker + " failed")

print(dow_data["aapl"]["calls"].keys())

for ticker in tickers:
    iv_dec = []
    calls = dow_data[ticker]['calls']
    volatility = calls["Implied Volatility"]
    for ii in range(len(volatility)):
        x = volatility[ii]
        dec = float(x.strip('%').replace(',',''))/100
        iv_dec.append(dec)
        
    dow_data[ticker]['calls']["iv_dec"] = iv_dec

strike = dow_data["nflx"]['calls']["Strike"]
iv = dow_data["nflx"]['calls']["iv_dec"]

plt.plot(strike, iv) 
plt.xlabel('strike') 
plt.ylabel("iv") 
plt.title('smile of aapl') 

plt.show() 
