# from tests import test_indicators
# from visualization import plot_indicators
# from preprocessing.feature_generation import *
# from preprocessing import data_generator
# import matplotlib.pyplot as plt
# import numpy as np
from models.equity import Equity
# from algorithms.cnn import CNN
# from algorithms.svm import SVM
from API.indicators import get_indicator_value
from db.wrapper import *
eq = Equity('AAPL')
print(eq.opens)
print(eq.dates)
print(getTickers())
# feature_set = ['macd_9_18', 'volumes', 'rainbow_1_5_9_13', 'oil', 'snp', 'reit','accumSwing']
# feature_set = ['closes']
# length = 10
# threshold = 0.015
# period = 10
# # fig, ax = plt.subplots()
# # ax = plot_features(eq, feature_set, ax, 255)
# # # ax = plot_labels(eq, 10, .015, ax, range=255)
# # plt.show()

# X,y = data_generator.gen_svm_data(eq, feature_set, length, threshold, period)

# svm = SVM(X, y)
# svm.train([0.8,0.2])
# cnn.train_model(X_train,y_train,X_test,y_test)

# print(get_indicator_value('AAPL', 'macd_9_18'))
