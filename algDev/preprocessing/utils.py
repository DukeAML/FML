import math
import numpy as np
def log_returns(p_1, p_0):

    rtn = p_1/p_0

    lr = math.log(rtn)

    return lr

def norm(f):

    std = np.std(f)

    mean = np.mean(f)

    f = (f - mean) / std

    min = np.min(f)
    f = f - min
    max = np.max(f)
    f = f/max
    return f

def get_style(i):
    colors = ['r','b','k','g','m']
    styles = ['-', '--','.']

    if i >= len(colors) * len(styles):
        return 'k-'

    color = colors[i%len(colors)]
    style = styles[math.floor(i/len(colors))]

    return color+style