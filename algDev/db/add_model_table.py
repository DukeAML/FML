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

create_table_query = '''
CREATE TABLE Models(
    ticker VARCHAR(10) NOT NULL,
    modelbinary bytea NOT NULL,
    epoch DECIMAL,
    title VARCHAR(100),
    metrics VARCHAR(1000),
    indicatorId VARCHAR(1000),
    PRIMARY KEY (ticker, title)
    ); '''

create_table_query2 = '''
CREATE TABLE ModelCollections(
    ticker VARCHAR(10) NOT NULL,
    modelIds VARCHAR(1000) NOT NULL,
    length BIGINT,
    upperthreshold DECIMAL,
    lowerthreshold DECIMAL,
    period BIGINT,
    PRIMARY KEY (ticker, modelIds)
    ); '''

cursor.execute(create_table_query)
cursor.execute(create_table_query2)

if(conn):
    cursor.close()
    conn.close()
    print("PostgreSQL connection is closed")