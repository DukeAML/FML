import psycopg2
import xlrd



conn = psycopg2.connect(host="localhost",database="postgres", user="postgres", password="daddyluke123")

cursor = conn.cursor()
# Print PostgreSQL Connection properties
print ( conn.get_dsn_parameters(),"\n")

# Print PostgreSQL version
cursor.execute("SELECT version();")
record = cursor.fetchone()
print("You are connected to - ", record,"\n")

# create_table_query = '''
# CREATE TABLE Prices
#     (ticker VARCHAR(10) NOT NULL,
#     date DATE NOT NULL,
#     open DECIMAL,
#     high DECIMAL,
#     low DECIMAL,
#     close DECIMAL,
#     adjClose DECIMAL,
#     volume INTEGER
#     PRIMARY KEY (ticker,date)
#     ); '''
# 
# cursor.execute(create_table_query)

pathToData = "../../algDev/data/"
xl_workbook = xlrd.open_workbook(pathToData + '/indexes/RE.xls')

sheet_names = xl_workbook.sheet_names()
print('Sheet Names', sheet_names)

postgres_insert_query = """ INSERT INTO Prices (ticker, date, open, high, low, close, adjClose, volume) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

# record_to_insert = (5, 'One Plus 6', 950)
# cursor.execute(postgres_insert_query, record_to_insert)

# conn.commit()
# count = cursor.rowcount
# print (count, "Record inserted successfully into mobile table")

# need to actually run it now


# except (Exception, psycopg2.Error) as error :
#     print ("Error while connecting to PostgreSQL", error)
# finally:
#     #closing database connection.
#         if(conn):
#             cursor.close()
#             conn.close()
#             print("PostgreSQL connection is closed")