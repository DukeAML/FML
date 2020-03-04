# script to get open, high, low, close for stocks to update our historical db
# eventually gonna wanna just dockerize this?

import psycopg2
import credentials
from datetime import datetime, timedelta

def update():
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password)
    conn.autocommit = True
    cursor = conn.cursor()

    # first, get the most recent date that's in our DB
    getDateStatement = "SELECT DISTINCT date FROM Prices WHERE NOT (date < ANY(SELECT DISTINCT date FROM Prices))" # handle enumeration in the DB ya digg
    cursor.execute(getDateStatement)
    lastDate = cursor.fetchone()[0] # un-nest from list of tuples
    print(lastDate)

    # next, for each distinct ticker, insert everything between then and today from our API
    today = datetime.date(datetime.now())
    day_count = (today - lastDate).days + 1
    print(day_count)

    getTickersStatement = "SELECT DISTINCT ticker FROM Prices ORDER BY ticker"
    cursor.execute(getTickersStatement)
    tickers = cursor.fetchall()
    tickers = [ticker[0] for ticker in tickers]
    print(tickers)

    for ticker in tickers:
        for single_date in (lastDate + timedelta(n) for n in range(day_count)):
            print(single_date)
            #  THEN ==> 
            # price = getPrice(ticker, single_date)
            insertQuery = """ INSERT INTO Prices (ticker, date, open, high, low, close, volume, smavg) VALUES ('{}','{}',{},{},{},{},{},{})"""
            dateStr = str(single_date.year) + '-' + str(single_date.month) + '-' + str(single_date.day)

            # MAKE THE REST OF THE TUPLES HERE
            # THEN EXECUTE INSERT QUERY




if __name__ == '__main__':
    update()