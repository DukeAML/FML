from algDev.models.asset_strategy import *
from algDev.algorithms.asset_allocation import *
from algDev.models.position import Position
from algDev.models.equity import Equity
import datetime

import random
import numpy as np
def run_test_one():
    tickers = ['AAPL', 'BRK.B', 'GOOG', 'C']
    positions = []
    predictions = {}
    for t in tickers:
        positions.append(Position(Equity(t), datetime.date(2010,3,3)))
        predictions[t] = (random.randint(0,1), random.random())
    print(predictions)
    aa = AssetAllocation(upper_threshold= 0.025 , lower_threshold=  -0.15)
    a = AssetStrategy(aa)

    p = a.allocate(datetime.date(2017,3,3), positions, predictions, True)

    print(p)

    
    