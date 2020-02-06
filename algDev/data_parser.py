import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from models.equity import equity 
from models.indicators import *
 
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

vslr_file = r'./data/equities/energy/VSLR.csv'
vslr = equity(vslr_file)
trix_vec = trix_indicator(vslr.closes)
plt.plot(trix_vec[54:])
plt.show()
