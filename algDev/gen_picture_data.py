import numpy as np
from math import *
from build_features import gen_features
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def gen_pics(data):
    X = []
    look_back = data.shape[1]
    for i in range(len(data) - look_back - 1):
        a = data[i:(i + look_back), :]
        px_a = get_pixels(a)
        X.append(px_a)
    X = np.array(X)

    return X

def get_pixels(a):
    max = np.max(a)
    min = np.min(a)

    a = ((a - min)/(max - min)) * 255

    return a

def gen_data(eq)
    eq_path = r'./algDev/data/equities/%s.csv' % eq

    features = np.array(gen_features(eq_path, 500))

    ## Generate data that is square.

    pics = gen_pics(features)

    plt.imsave('first_25_days.png', np.array(pics[0]), cmap=cm.gray)