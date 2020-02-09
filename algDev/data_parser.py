import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from models.equity import Equity
from models.indicators import *

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

from algDev.utils import datapath

vslr_file = datapath('equities', 'VSLR.csv')
vslr = Equity(vslr_file)
trix_vec = trix_indicator(vslr.closes)
plt.plot(trix_vec[54:])
plt.show()
