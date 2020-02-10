import numpy as np

def selectAssets(o, short=False):
    
    evs = []

    for pred in o:
        evs.append(expected_value(pred))

    total = 0
    for i in range(len(evs)):
        if evs[i] < 0:
            evs[i] = 0
        total = total + evs[i]
    
    evs = evs/total

    return evs
        
    

def expected_value(x):

    ev = 0
    bounds = [-0.9, -0.4, -0.085, -.045, -0.01, 0.01, 0.035, 0.065,
              0.095, 0.13]

    for i in range(len(bounds)):
        ev = ev + (bounds[i] * x[i])

    return ev