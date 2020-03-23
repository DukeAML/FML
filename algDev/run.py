from tests import test_indicators
from visualization import plot_indicators
from preprocessing.feature_generation import *
from preprocessing import data_generator
import matplotlib.pyplot as plt
import numpy as np
from models.equity import Equity

eq = Equity('AAPL')
features = ['rainbow_1_3_15_7_19','closes']

fig, ax = plt.subplots()
ax = plot_features(eq, features, ax, 255)
# ax = plot_labels(eq, 10, .015, ax, range=255)
plt.show()

# data_generator.gen_cnn_data(eq, 10, .015, 10)
