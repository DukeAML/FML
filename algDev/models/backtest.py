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

    def __init__(self, trading_algorithm, asset_strategy, start_date, end_date, portfolio_value, verbose=False):
        super().__init__()
        
        self.today = start_date
        self.value = portfolio_value
        self.end_date = end_date
        self.start_date = start_date
        self.asset_strategy = asset_strategy
        self.trading_algorithm = trading_algorithm
        
        self.portfolio = Portfolio(self.value, self.today, self.trading_algorithm, self.asset_strategy, verbose)

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

        return self.get_relevant_information()

    def gen_positions(self, positions):

        poss = []
        for p in positions:
            poss.append({'ticker':p.ticker, 'values':p.get_values(self.today)[1], 'trades':p.get_trades_dictionary()})

        return poss

    def get_relevant_information(self):
        rtn = self.get_return()
        snp_rtn = self.get_snp_return()
        net_rtn = self.get_net_rtn()

        avg_free_cash = self.get_avg_free_cash()

        beta = self.get_beta()
        vol = self.get_vol()

        treynor = self.get_treynor()
        sharpe = self.get_sharpe()

        dates, pf_vals, initial_val, snp_vals = self.get_pf_values()
        stats = [{'name': 'return', 'value':rtn}, {'name':'snp_return', 'value':snp_rtn}, {'name':'net_return', 'value':net_rtn}, {'name':'average_free_cash', 'value':avg_free_cash}, {'name':'beta', 'value': beta}, {'name':'vol','value':vol}, {'name':'treynor', 'value':treynor}, {'name':'sharpe','value':sharpe}]
        positions = self.gen_positions(self.portfolio.positions)
        return_val = {'stats': stats, 'dates':dates, 'portfolioValues':pf_vals, 'initialValues':initial_val, 'snpVals':snp_vals, 'positions':positions, 'predictions':self.portfolio.predictions}

        return return_val

    def get_rtns(self):
        vals = self.get_pf_values()
        vals = vals[1]
        
        rtns = []
        for val in vals:
            rtns.append((val-vals[0])/vals[0])

        return rtns

    def get_pf_values(self):

        day_diff = (self.end_date - self.start_date).days
        vals = []
        initial_val = []
        dates = []
        snp = []
        
        sp = Equity('SNP')
        for i in range(day_diff):
            i_day = datetime.timedelta(days=i)
            dates.append(self.start_date + i_day)
            vals.append(self.portfolio.getValue(self.start_date + i_day))
            initial_val.append(self.value)
            snp.append(sp.get_price(self.start_date + i_day))

        return dates, vals, initial_val, snp

    def get_snp_return(self):
        snp = self.get_pf_values()[3]
        initial_snp = snp[0]
        end_snp = snp[len(snp)-1]

        return (end_snp - initial_snp)/initial_snp

    def get_avg_free_cash(self):
        free_cash = np.array(list(self.portfolio.free_cash.values()))
        
        return np.mean(free_cash)


    def get_net_rtn(self):
        rtn = self.get_return()
        snp_rtn = self.get_snp_return()

        return rtn-snp_rtn

    def get_vol(self):

        return np.std(self.get_rtns())

    def get_sharpe(self):
        vol = self.get_vol()
        rtn = self.get_return()
        if vol==0:
            return 10000
        return rtn/vol

    def get_beta(self):
        beta = 1.0
        rf = self.asset_strategy.asset_allocation.rf
        rtn = self.get_return()
        snp_rtn = self.get_snp_return()
        er = (rtn - rf)
        em = (snp_rtn - rf)
        if(em==0.0):
            return 1000.0
        beta = er/em
        return beta

    def get_treynor(self):
        beta = self.get_beta()
        rtn = self.get_return()
        if beta==0.0:
            return 1000
        return rtn/beta

    def get_return(self):
        vals = self.get_pf_values()[1]
        initial_value = vals[0]
        final_value = vals[len(vals)-1]

        return (final_value-initial_value)/initial_value
    
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
            
