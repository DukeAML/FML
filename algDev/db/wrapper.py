import psycopg2
from openpyxl import load_workbook
import credentials

from os import listdir
from os.path import isfile, join



def getData(ticker):
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password)
    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT * FROM Prices WHERE ticker = '{}'"
    cursor.execute(query.format(ticker))
    result = cursor.fetchall()
    return result

def getTickers():
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password)
    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT DISTINCT ticker FROM Prices ORDER BY ticker"
    cursor.execute(query)

    result = cursor.fetchall()
    result = [item[0] for item in result]

    return result