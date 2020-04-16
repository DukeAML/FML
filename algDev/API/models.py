import algDev.db.wrapper as db_wrapper

from algDev.models.trading_algorithm import TradingAlgorithm
from algDev.algorithms.model_collection import ModelCollection
from algDev.algorithms.svm import SVM
from algDev.algorithms.cnn import CNN
from algDev.algorithms.voter import Voter
from algDev.algorithms.asset_allocation import AssetAllocation

import pickle

def loadModelCollection(modelCollectionId):
    model_collection = db_wrapper.loadModelCollection()[0]
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
        metrics = model_res[3]

        new_model = SVM(model=model, title=title, metrics=metrics)

        models.append(new_model)
    params = {}
    params['length'] = length
    params['upper_threshold'] = uppertheshold
    params['lower_threshold'] = lowerthreshold
    params['period'] = period
    mc = ModelCollection(ticker, type, params = params, models = models)

    return mc

def loadTradingAlgorithm(tradingAlgorithmId):

    tradingAlgResult = db_wrapper.getTradingAlgorithm(tradingAlgorithmId)[0]
    tickers = tradingAlgResult[1].split(',')
    modelCollectionIds = tradingAlgResult[1].split(',')
    votingType = tradingAlgResult[2]
    mcs = []
    for modelCollectionId in modelCollectionIds:
        mc = loadModelCollection(modelCollectionId)
        mcs.append(mc)
    model_mc = mcs[0]
    features = model_mc.features
    t = model_mc.type
    length = model_mc.params['length']
    upper_threshold = model_mc.params['upper_threshold']
    lower_threshold = model_mc.params['lower_threshold']
    period = model_mc.params['period']
    ta = TradingAlgorithm(tickers=tickers, features=features, type=t, data_lookback_period=length, label_upper_threshold=upper_threshold, label_lower_threshold=lower_threshold, label_period=period, voting_type=votingType, models = mcs)

    return ta

def getTradingAlgorithms():
    tas = db_wrapper.loadTradingAlgorithms()

    trading_algorithms = []
    for ta in tas:
        trading_algorithms.append(loadTradingAlgorithm(ta[0]))
    
    return trading_algorithms


def getModels(ticker):
    
    models = db_wrapper.loadModelCollections(ticker)

    return models
