import numpy as np
import math
from algDev.models.indicators import Indicators
from algDev.models.equity import Equity
from algDev.models.portfolio import Portfolio

### Simulate the success of a model or trading strategy
class Backtest():

    def __init__(self, eqs, start_date, portfolio_value):
        super().__init__()
        
        self.today = start_date
        self.value = portfolio_value
        self.eqs = eqs

        self.portfolio = Portfolio(value, eqs)

    def step(self, strategy_lookback, strategy_threshold):

        self.portfolio.realloc(self.today, strategy_lookback, strategy_threshold)

        self.today = self.today + 1

    def simulate(self, strategy):

        strategy_lookback = strategy.lookback_period
        strategy_threshold = strategy.strategy_threshold

        while not portfolio.date_ob(self.today):

            self.step(strategy_lookback, strategy_threshold)

        print(value)

    
