from tests import test_indicators
from visualization import plot_indicators
from preprocessing.feature_generation import *
from preprocessing import data_generator
import matplotlib.pyplot as plt
import numpy as np
from models.equity import Equity
from algorithms.cnn import CNN

eq = Equity('AAPL')
# feature_set = ['macd_9_18', 'volumes', 'rainbow_1_5_9_13', 'oil', 'snp', 'reit','accumSwing']
feature_set = ['closes', 'rainbow_11_15_29_43']
length = 10
threshold = 0.015
period = 10
# fig, ax = plt.subplots()
# ax = plot_features(eq, feature_set, ax, 255)
# # ax = plot_labels(eq, 10, .015, ax, range=255)
# plt.show()

X,y = data_generator.gen_cnn_data(eq, feature_set, length, threshold, period)

X_train,y_train,X_test,y_test = data_generator.split_data(X,y,[.8,.2])

cnn = CNN(X_train.shape)

cnn.train_model(X_train,y_train,X_test,y_test)