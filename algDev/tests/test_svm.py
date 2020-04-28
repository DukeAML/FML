from algDev.algorithms.svm import SVM
from algDev.preprocessing import data_generator
from algDev.models.equity import Equity
from algDev.models.trading_algorithm import TradingAlgorithm
from algDev.algorithms.model_collection import ModelCollection

import datetime
import numpy as np
import pickle

def run():
    X = np.zeros((5,2))
    y = np.zeros((5,))

    y[3] = 1
    y[4] = 1

    X[0,:] = [-2,4]
    X[1,:] = [-1,1]
    X[2,:] = [0,0]
    X[3,:] = [1,1]
    X[4,:] = [2,4]

    svm = SVM(X=X, y=y, params= {'C': 1, 'gamma' :0.1})

    svm.train([1,0], verbose=True)

    print(svm.predict([[3,9]]))

def run_2():
    X = np.zeros((5,2))
    y = np.zeros((5,))

    y[3] = 1
    y[4] = 1

    X[0,:] = [-2,4]
    X[1,:] = [-1,1]
    X[2,:] = [0,0]
    X[3,:] = [1,1]
    X[4,:] = [2,4]

    svm = SVM(X=X, y=y, params= {'C': 1, 'gamma' :0.1})

    svm.train([1,0], verbose=True)

    modelData = pickle.dumps(svm.model)

    saved_data = pickle.loads(modelData)

    new_svm = SVM(model=saved_data)

    print(new_svm.predict([[3,3]]))

def run_3():
    params = {'length':10, 'upper_threshold': 0.035, 'lower_threshold': -0.15, 'period': 10}
    mc = ModelCollection('AAPL', 'svm', ['macd_9_18', 'closes', 'ema_9'], params)
    mc.train_models(True)
    mc.get_conf_matricies(True)
    # ta = TradingAlgorithm(['AAPL'], ['ema_9', 'macd_9_18'])

    # ta.generate_conf_matricies(datetime.datetime(2019, 1, 1), datetime.datetime(2020,1,1))

    # eq = Equity('AAPL')
    # X,y = data_generator.gen_svm_data(eq, ['ema_9'], 15, 0.025, 10)
    
    # svm = SVM(X,y)
    # svm.train([0.8,0.2])
    # svm.build_conf_matrix([0.8,0.2])
    
    # X_i = data_generator.get_subset(eq, ['ema_9'], 0, 15, 'svm')

    
    


    