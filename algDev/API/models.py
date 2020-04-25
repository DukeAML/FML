import algDev.db.wrapper as db_wrapper

from algDev.models.trading_algorithm import TradingAlgorithm
from algDev.algorithms.model_collection import ModelCollection
from algDev.algorithms.svm import SVM
from algDev.algorithms.cnn import CNN
from algDev.algorithms.voter import Voter
from algDev.algorithms.asset_allocation import AssetAllocation
from algDev.API.indicators import get_indicator_value
import datetime
import pickle

def parse_metrics(metric_string):
    metrics = {}

    metric_string = metric_string.replace('{','')
    metric_string = metric_string.replace('}','')

    metric_arr = metric_string.split(',')

    for m in metric_arr:
        k_v = m.split(':')
        v = float(k_v[1].strip())
        k = k_v[0].split('\"')[1]
        metrics[k] = v

    return metrics

def loadModelCollection(modelCollectionId):
    model_collection = db_wrapper.loadModelCollection(modelCollectionId)
    ticker = model_collection[1]
    modelIds = model_collection[2]
    length = model_collection[3]
    uppertheshold = model_collection[4]
    lowerthreshold = model_collection[5]
    period = model_collection[6]
    title = model_collection[7]
    features = model_collection[8]
    
    type = title.split(' - ')[0]
    models = []
    features = features.split(',')
    for modelId in modelIds.split(','):
        model_res = db_wrapper.getModel(modelId)[0]

        modelbinary = bytes(model_res[1])
        model = pickle.loads(modelbinary)
        title = model_res[2]
        metrics = parse_metrics(model_res[3])
        
        new_model = SVM(model=model, title=title, metrics=metrics)

        models.append(new_model)
    params = {}
    params['length'] = int(length)
    params['upper_threshold'] = float(uppertheshold)
    params['lower_threshold'] = float(lowerthreshold)
    params['period'] = int(period)
    mc = ModelCollection(ticker, type, features = features, params = params, models = models)
    
    return mc

def loadTradingAlgorithm(tradingAlgorithmId):

    tradingAlgResult = db_wrapper.getTradingAlgorithm(tradingAlgorithmId)
    
    tickers = tradingAlgResult[1].split(',')
    features = tradingAlgResult[2].split(',')
    length = int(tradingAlgResult[3])
    upper_threshold = float(tradingAlgResult[4])
    lower_threshold = float(tradingAlgResult[5])
    period = int(tradingAlgResult[6])
    modelCollectionIds = tradingAlgResult[7].split(',')
    votingType = tradingAlgResult[8]
    mcs = []
    for modelCollectionId in modelCollectionIds:
        mc = loadModelCollection(modelCollectionId)
        
        mcs.append(mc)
    model_mc = mcs[0]
    features = model_mc.features
    t = model_mc.type
    
    ta = TradingAlgorithm(tickers=tickers, features=features, type=t, data_lookback_period=length, label_upper_threshold=upper_threshold, label_lower_threshold=lower_threshold, label_period=period, voting_type=votingType, models = mcs)

    return ta

def getTradingAlgorithms():
    tas = db_wrapper.getTradingAlgorithms()

    trading_algorithms = []
    for ta in tas:
        trading_algorithms.append(loadTradingAlgorithm(ta[0]))
    
    return trading_algorithms


def getModels(ticker):
    
    models = db_wrapper.loadModelCollections(ticker)

    return models


def loadModelResult(modelCollectionId):

    mc = loadModelCollection(modelCollectionId)

    lookback = mc.params['length']
    features = mc.features

    preds = mc.predict(datetime.datetime.now())
    result = []

    for i,f in enumerate(features):
        vals = get_indicator_value(mc.ticker, f)[0:lookback]
        pred = preds[i]
        res = {'name': f, 'values': vals, 'prediction':pred}
        result.append(res)
    ## Get a list of all indicators, the values for the last t days
    ## Get the predicted value for each individual svm

    # result : [{'name':'indicator_name', 'values':[10,23,...,n], 'prediction':0},{...},{...},...]
    return result
