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
    modelMetrics = str(model.metrics).replace("'","\"")

    sql = "INSERT INTO models (modelId, modelbinary, title, metrics) VALUES ('{}',{},'{}','{}')"
    cursor.execute(sql.format(modelId, psycopg2.Binary(modelData), modelTitle, modelMetrics))

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
        modelIds.append(str(modelId))

    modelIds = ','.join(modelIds)
    
    period = int(modelCollection.params['period'])
    length = int(modelCollection.params['length'])
    upper_threshold = float(modelCollection.params['upper_threshold'])
    lower_threshold = float(modelCollection.params['lower_threshold'])
    title = input("Enter name for modelCollection ")
    if title=='':
        title='default'
    features = ','.join(modelCollection.features)
    if title=='':
        title = str(modelCollection.features)
    title = modelCollection.type + ' - ' + title
    sql = "INSERT INTO ModelCollections (modelCollectionId, ticker, modelIds, length, upperthreshold, lowerthreshold, period, title, features) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')"
    cursor.execute(sql.format(id, ticker, modelIds, length, upper_threshold, lower_threshold, period, title, features))

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
        modelIds.append(str(modelCollectionId))
    
    
    features = ','.join(tradingAlgorithm.features)
    length = tradingAlgorithm.params['length']
    upperthreshold = tradingAlgorithm.params['upper_threshold']
    lowerthreshold = tradingAlgorithm.params['lower_threshold']
    period = tradingAlgorithm.params['period']

    modelIds = ','.join(modelIds)

    votingType = tradingAlgorithm.voter.voting_type
    title = input("Trading Algorithm Name")
    if title=='':
        title='Default'
    sql = "INSERT INTO TradingAlgorithms (tradingAlgorithmId, tickers, features, length, upperthreshold, lowerthreshold, period, modelCollectionIds, votingType, title) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"
    cursor.execute(sql.format(id, tickers, features, length, upperthreshold, lowerthreshold, period, modelIds, votingType, title))

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

    query = "SELECT * FROM TradingAlgorithms WHERE tradingAlgorithmId = '{}'"
    cursor.execute(query.format(tradingAlgId))
    result = cursor.fetchone()
    
    return result

def loadModelCollection(modelCollId):
    
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT * FROM ModelCollections WHERE modelCollectionId = '{}'"
    cursor.execute(query.format(modelCollId))
    result = cursor.fetchone()
    
    return result

def getFirstDate():
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    getDateStatement = "SELECT date FROM Prices WHERE NOT (date > ANY(SELECT DISTINCT date FROM Prices))" # handle enumeration in the DB ya digg
    cursor.execute(getDateStatement)
    firstDate = cursor.fetchone() # un-nest from list of tuples
    firstDate = firstDate[0]

    return firstDate

def getMostRecentDate():
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    getDateStatement = "SELECT date FROM Prices WHERE NOT (date < ANY(SELECT DISTINCT date FROM Prices))" # handle enumeration in the DB ya digg
    cursor.execute(getDateStatement)
    lastDate = cursor.fetchone() # un-nest from list of tuples
    lastDate = lastDate[0]

    return lastDate

def getTradingAlgorithms():
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT * FROM TradingAlgorithms"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def getModelCollections():
    conn = psycopg2.connect(host="localhost",database="postgres", user=credentials.username, password=credentials.password, port=credentials.port)
    conn.autocommit = True
    cursor = conn.cursor()

    query = "SELECT * FROM ModelCollections"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

