from algDev.preprocessing.feature_generation import *
from algDev.preprocessing import data_generator
import matplotlib.pyplot as plt
import numpy as np
from algDev.models.equity import Equity
from algDev.algorithms.cnn import CNN
from algDev.algorithms.svm import SVM
from algDev.API.indicators import get_indicator_value
from algDev.db.wrapper import *
from algDev.tests import trading_alg_test, asset_alloc_test, test_svm
from algDev.db.populate_models_table import build_example_model, get_tas, test_add_model, test_add_model_collection
from algDev.API.models import loadTradingAlgorithm, loadModelResult
from algDev.tests.test_backtest import run_test
from algDev.tests.hyperparam_tst import hyper_param_haul

def test_one():
    eq = Equity('QCOM')
    print(eq.opens)
    print(eq.dates)
    print(getTickers())

def test_two():
    eq = Equity('AAPL')
    feature_set = ['prings']
    length = 10
    threshold = 0.015
    period = 10
    fig, ax = plt.subplots()
    ax = plot_features(eq, feature_set, ax, 255)
    # # ax = plot_labels(eq, 10, .015, ax, range=255)
    plt.show()

    # X,y = data_generator.gen_svm_data(eq, feature_set, length, threshold, period)

    # svm = SVM(X, y)
    # svm.train([0.8,0.2])
    # cnn.train_model(X_train,y_train,X_test,y_test)

    print(get_indicator_value('AAPL', 'lowerBol'))

def test_three():
    
    trading_alg_test.run_test_one()

def test_four():
    asset_alloc_test.run_test_one()

def test_five():
    trading_alg_test.build_confusion_matrix()

def test_six():
    trading_alg_test.test_conf_matrix_model_coll()

def test_seven():
    ticker_list = [['AAPL']]
    features_list = [['macd_9_18','macdSig','closes']]
    model_params = [{'gamma':.1, "C" :1},{'gamma':1, "C" :1},{'gamma':10, "C" : 1},{'gamma':100, "C" :1},{'gamma':.1, "C" :.1},{'gamma':1, "C" :.1},{'gamma':10, "C" :.1},{'gamma':100, "C" :.1},{'gamma':10, "C" :.001},{'gamma':100, "C" :.001}]
    hp = hyper_param_haul(features_list,ticker_list, model_params)

def test_eight():
    test_svm.run_3()

def test_nine():
    build_example_model()
    # test_add_model()
    # test_add_model_collection()

def test_ten():
    print(get_tas())

def test_eleven():
    trading_alg_test.grid_search()

def test_twelve():
    ta_entity = getTradingAlgorithms()
    ta_id = ta_entity[0][0]
    trading_alg = loadTradingAlgorithm(ta_id)

    print(trading_alg)

def backtest():
    run_test()

def getMCs():
    print(getModelCollections())

def getMCData():
    mcId = '4ac2fece-d7e8-4027-8d30-c78575b97811'

    result = loadModelResult(mcId)

    print(result)

