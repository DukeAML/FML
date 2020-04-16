import psycopg2
from openpyxl import load_workbook
import pickle
import algDev.db.credentials as credentials
import uuid
from os import listdir
from os.path import isfile, join


def getData(ticker):
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT * FROM Prices WHERE ticker = '{}' ORDER BY Date DESC"
    cursor.execute(query.format(ticker))
    result = cursor.fetchall()
    return result

def getTickers():

    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)

    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT DISTINCT ticker FROM Prices ORDER BY ticker"
    cursor.execute(query)

    result = cursor.fetchall()
    result = [item[0] for item in result]

    return result

def createModel(model):
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)

    conn.autocommit = True
    cursor = conn.cursor()

    modelId = uuid.uuid4()
    modelData = pickle.dumps(model.model)
    modelTitle = model.title
    modelMetrics = str(model.metrics)

    sql = "INSERT INTO models (modelId, modelbinary, title, metrics) VALUES (%s)"
    cursor.execute(sql, (modelId, psycopg2.BINARY(modelData), modelTitle, modelMetrics))

    return modelId

def createModelCollection(modelCollection):
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)

    conn.autocommit = True
    cursor = conn.cursor()
    id = uuid.uuid4()
    ticker = modelCollection.eq.ticker
    modelIds = []
    for model in modelCollection.models:
        modelId = createModel(model)
        modelIds.append(modelId)
    modelIds = ','.join(modelIds)
    
    period = int(modelCollection.params['period'])
    length = int(modelCollection.params['length'])
    upper_threshold = float(modelCollection.params['upper_threshold'])
    lower_threshold = float(modelCollection.params['lower_threshold'])
    title = input("Enter name for modelCollection ")
    features = ','.join(modelCollection.features)
    if title=='':
        title = str(modelCollection.features)
    title = modelCollection.type + ' - ' + title
    sql = "INSERT INTO Models (modelCollectionId, ticker, modelIds, length, upperthreshold, lowerthreshold, period, title, features) VALUES (%s)"
    cursor.execute(sql, (id, ticker, modelIds, length, upper_threshold, lower_threshold, period, title, features))

    return id

def createTradingAlgorithm(tradingAlgorithm):
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)

    conn.autocommit = True
    cursor = conn.cursor()

    id = uuid.uuid4()

    tickers = ','.join(tradingAlgorithm.tickers)

    modelIds = []
    for model in tradingAlgorithm.models:

        modelCollectionId = createModelCollection(model)
        modelIds.append(modelCollectionId)

    modelIds = ','.join(modelIds)

    votingType = tradingAlgorithm.voter.voting_type

    sql = "INSERT INTO Models (tradingAlgorithmId, tickers, modelCollectionIds, votingType=) VALUES (%s)"
    cursor.execute(sql, (id, tickers, modelIds, votingType))

    return id

def loadModelCollections(ticker):

    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT * FROM ModelCollections WHERE ticker = '{}'"
    cursor.execute(query.format(ticker))
    result = cursor.fetchall()
    return result

def getModel(modelId):

    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT * FROM Models WHERE modelId = '{}'"
    cursor.execute(query.format(modelId))
    result = cursor.fetchall()
    return result

def getTradingAlgorithm(tradingAlgId):

    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT * FROM TradingAlgorithm WHERE tradingAlgorithmId = '{}'"
    cursor.execute(query.format(tradingAlgId))
    result = cursor.fetchall()

    return result

def loadModelCollection(modelCollId):
    
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT * FROM ModelConnections WHERE modelCollectionId = '{}'"
    cursor.execute(query.format(modelCollId))
    result = cursor.fetchall()

    return result

def getFirstDate():
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    getDateStatement = "SELECT date FROM Prices WHERE NOT (date > ANY(SELECT DISTINCT date FROM Prices))" # handle enumeration in the DB ya digg
    cursor.execute(getDateStatement)
    firstDate = cursor.fetchone() # un-nest from list of tuples
    firstDate = firstDate[0]
    print('firstDate', firstDate)

    return firstDate

def getMostRecentDate():
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    getDateStatement = "SELECT date FROM Prices WHERE NOT (date < ANY(SELECT DISTINCT date FROM Prices))" # handle enumeration in the DB ya digg
    cursor.execute(getDateStatement)
    lastDate = cursor.fetchone() # un-nest from list of tuples
    lastDate = lastDate[0]
    print('lastDate', lastDate)

    return lastDate

def getTradingAlgorithm():
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT * FROM TradingAlgorithms"
    cursor.execute(query)
    result = cursor.fetchall()
    return result
