from algDev.preprocessing.feature_generation import *
from algDev.preprocessing import data_generator
import matplotlib.pyplot as plt
import numpy as np
from algDev.models.equity import Equity
from algDev.algorithms.cnn import CNN
from algDev.algorithms.svm import SVM
from algDev.API.indicators import get_indicator_value
from algDev.db.wrapper import *

def test_one():
    eq = Equity('AAPL')
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
