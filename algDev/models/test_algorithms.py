import numpy as np
import math
from algDev.models.indicators import Indicators
from algDev.models.equity import Equity
### Simulate the success of a model or trading strategy

def backtest(eqs, strategy, start_date='max'):

    strategy_lookback = strategy.lookback_period
    start_index = get_start_index(eqs, strategy_lookback, start_date)

    portfolio = 



def get_start_index(dates, strategy_lookback, start_date):
    ## Eventually should come up with a way to cut off the 
    ## Indicies that are irrelevant to us because the indicators can't
    ## Be calculated.
    if start_date == 'max':
        return strategy_lookback

    for i, date in enumerate(dates):
        if date in start_date:
            if i < strategy_lookback:
                return strategy_lookback
            else:
                return i
