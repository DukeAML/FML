import numpy as np
import math
import time
import matplotlib.pyplot as plt
from algDev.models.equity import Equity
from algDev.models.portfolio import Portfolio
import datetime
import os
### Simulate the success of a model or trading strategy
class Backtest():

    def __init__(self, eqs, trading_algorithm, asset_strategy, start_date, end_date, portfolio_value, verbose=False):
        super().__init__()
        
        self.today = start_date
        self.value = portfolio_value
        self.end_date = end_date
        self.eqs = eqs

        self.asset_strategy = asset_strategy
        self.trading_algorithm = trading_algorithm

        self.portfolio = Portfolio(self.value, self.eqs, self.today, self.trading_algorithm, self.asset_strategy, verbose)

    def step(self, verbose=False):
        start = time.perf_counter()
        self.portfolio.realloc(self.today, verbose)
        end = time.perf_counter()
        if verbose:
            print("", self.today, (end-start))
        self.today = self.today + datetime.timedelta(days=1)

    def simulate(self, verbose=False):
        
        while not self.portfolio.date_ob(self.today) and self.end_date >= self.today:
            
            self.step(verbose)
            
        final_day = self.today - datetime.timedelta(days=1)
        if verbose is True:

            print(self.portfolio.getValue(final_day, True))

        return self.portfolio.getValue(final_day), self.portfolio.positions

    def plot_value(self, initial_value, start_date, end_date):

        day_diff = (end_date - start_date).days
        vals = []
        initial_val = []
        dates = []
        snp = []
        here = os.path.abspath(os.path.dirname(__file__))
        data_directory = os.path.join(here, '..\\data')
        snp_directory = os.path.join(data_directory, 'indexes\\SNP.xlsx')
        sp = Equity(snp_directory)
        for i in range(day_diff):
            i_day = datetime.timedelta(days=i)
            dates.append(start_date + i_day)
            vals.append(self.portfolio.getValue(start_date + i_day))
            initial_val.append(initial_value)
            snp.append(sp.get_price(start_date + i_day))

        import numpy as np

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('Day')
        ax1.set_ylabel('Portfolio', color=color)
        ax1.plot(dates, vals, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.plot(dates, initial_val, 'b-')
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('SNP', color=color)  # we already handled the x-label with ax1
        ax2.plot(dates, snp, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()

        return
            
