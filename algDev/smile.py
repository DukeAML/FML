import io
import ftplib
import pandas
import requests
import requests_html
import ssl
import numpy as np
from yahoo_fin import options
from yahoo_fin import stock_info as si
import matplotlib.pyplot as plt
import py_vollib.black_scholes as vol
import yfinance as yf

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

# plt.show() 

coord = []
for jj in range(len(strike)):
    (x,y) = (strike[jj], iv[jj])
    coord.append((x,y))

slopes = []
d = (len(coord)//5) -1
c =0
for ii in range(d):
    x1 = coord[c]
    x2 = coord[c+5]
    m = (x2[1] - x1[1])/ (x2[0] - x1[0])
    slopes.append(m)
    c+=5

# print(slopes)
