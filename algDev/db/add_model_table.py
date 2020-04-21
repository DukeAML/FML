import psycopg2
from openpyxl import load_workbook
import credentials

from os import listdir
from os.path import isfile, join

conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
conn.autocommit = True
cursor = conn.cursor()

# Print PostgreSQL Connection properties
print ( conn.get_dsn_parameters(),"\n")

# Print PostgreSQL version
cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to - ", record,"\n")

drop_table_query = "DROP TABLE Models"
drop_table_query2 = "DROP TABLE ModelCollections"
drop_table_query3 = "DROP TABLE TradingAlgorithms"

try:
    cursor.execute(drop_table_query)
    print('dropped models table')
except:
    print("models table didn't exist, continuing...")
try:
    cursor.execute(drop_table_query2)
    print('dropped modelcollections table')
except:
    print("modelcollections table didn't exist, continuing...")
try:
    cursor.execute(drop_table_query3)
    print('dropped tradingalgorithms table')
except:
    print("tradingalgorithms table didn't exist, continuing...")
create_table_query = '''
CREATE TABLE Models(
    modelId uuid  NOT NULL,
    modelbinary bytea NOT NULL,
    title VARCHAR(100),
    metrics VARCHAR,
    PRIMARY KEY (modelId)
    ); '''

create_table_query2 = '''
CREATE TABLE ModelCollections(
    modelCollectionId uuid  NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    modelIds VARCHAR NOT NULL,
    length BIGINT,
    upperthreshold DECIMAL,
    lowerthreshold DECIMAL,
    period BIGINT,
    title VARCHAR(100),
    features VARCHAR,
    PRIMARY KEY (modelCollectionId)
    ); '''

create_table_query3 = '''
CREATE TABLE TradingAlgorithms(
    tradingAlgorithmId uuid  NOT NULL,
    tickers VARCHAR NOT NULL,
    features VARCHAR NOT NULL,
    length BIGINT,
    upperthreshold DECIMAL,
    lowerthreshold DECIMAL,
    period BIGINT,
    modelCollectionIds VARCHAR NOT NULL,
    votingType VARCHAR(10),
    title VARCHAR,
    PRIMARY KEY (tradingAlgorithmId)
    ); '''

cursor.execute(create_table_query)
cursor.execute(create_table_query2)
cursor.execute(create_table_query3)

if(conn):
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")