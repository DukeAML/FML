import psycopg2
import credentials
from datetime import datetime, timedelta

import yfinance as yf

def update():
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    # first, get the most recent date that's in our DB
    getDateStatement = "SELECT date FROM Prices WHERE NOT (date < ANY(SELECT DISTINCT date FROM Prices))" # handle enumeration in the DB ya digg
    cursor.execute(getDateStatement)
    lastDate = cursor.fetchone() # un-nest from list of tuples
    lastDate = lastDate[0]

    getTickersStatement = "SELECT DISTINCT ticker FROM Prices ORDER BY ticker"
    cursor.execute(getTickersStatement)
    tickers = cursor.fetchall()
    tickers = [ticker[0] for ticker in tickers]

    postgres_insert_query = """ INSERT INTO Prices (ticker, date, open, high, low, close, volume, smavg) VALUES ('{}','{}',{},{},{},{},{},{})"""

    for equity in tickers:
        tickerName = equity.upper()
        print('Updating:', tickerName)
        ticker = yf.Ticker(tickerName)
        hist = ticker.history(period="max")

        for row in hist.iterrows():
            try: 
                currentDate = row[0].to_pydatetime().date()
                if currentDate <= lastDate:
                    continue
                
                dateStr = str(currentDate.year) + '-' + str(currentDate.month) + '-' + str(currentDate.day)
                toUse = (equity, dateStr, row[1][0], row[1][1], row[1][2], row[1][3], row[1][4], "NULL")

                modified = False
                lst = list(toUse)
                for i in range(len(toUse)-1):
                    if not toUse[i]:
                        modified = True
                        lst[i] = "NULL"
                if modified:
                    toUse = tuple(lst)

                formatted = postgres_insert_query.format(*toUse)
                cursor.execute(formatted)
            
            except (Exception, psycopg2.Error) as error:
                print ("Error while connecting to PostgreSQL", error)

if(__name__ == "__main__"):
    update()