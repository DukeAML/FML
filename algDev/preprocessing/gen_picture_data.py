import numpy as np
from math import *
from build_features import gen_features
from models.feature_builder import build_labels_string
import matplotlib.pyplot as plt
import matplotlib.cm as cm

## GENERATE IMAGES OF INDICATOR DATA -- VISUALIZE INPUT TO CNN ##


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

    a = ((a - min)/(max - min))

    return a

def gen_data(eq):

    features = np.array(gen_features(eq))
    labels = np.array(build_labels_string(eq))
    ## Generate data that is square.

    pics = gen_pics(features)

    return pics, labels
