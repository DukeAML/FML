import numpy as np
import math
import time
import matplotlib.pyplot as plt
from models.equity import Equity
from models.portfolio import Portfolio
import datetime
### Simulate the success of a model or trading strategy
class Backtest():

    def __init__(self, eqs, start_date, end_date, portfolio_value, verbose=False):
        super().__init__()
        
        self.today = start_date
        self.value = portfolio_value
        self.end_date = end_date
        self.eqs = eqs

        self.portfolio = Portfolio(self.value, self.eqs, self.today, verbose)

    def step(self, strategy_lookback, strategy_threshold, verbose=False):
        start = time.perf_counter()
        self.portfolio.realloc(self.today, strategy_lookback, strategy_threshold, verbose)
        end = time.perf_counter()
        if verbose:
            print("", self.today, (end-start))
        self.today = self.today + datetime.timedelta(days=1)

    def simulate(self, strategy, verbose=False):

        strategy_lookback = strategy['lookback_period']
        strategy_threshold = strategy['strategy_threshold']
        
        while not self.portfolio.date_ob(self.today) and self.end_date >= self.today:
            
            self.step(strategy_lookback, strategy_threshold, verbose)
            
        final_day = self.today - datetime.timedelta(days=1)
        if verbose is True:

            print(self.portfolio.getValue(final_day, True))

        return self.portfolio.getValue(final_day), self.portfolio.positions

    def plot_value(self, initial_value, start_date, end_date):

        day_diff = (end_date - start_date).days
        vals = []
        initial_val = []
        dates = []
        
        for i in range(day_diff):
            i_day = datetime.timedelta(days=i)
            dates.append(start_date + i_day)
            vals.append(self.portfolio.getValue(start_date + i_day))
            initial_val.append(initial_value)

        plt.plot(dates, vals, 'r-')

        plt.plot(dates, initial_val, 'b-')

        plt.show()

        return
            
