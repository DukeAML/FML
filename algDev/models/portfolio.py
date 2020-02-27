import numpy as np
import random
import os
import datetime
import pandas as pd
from models.equity import Equity
from models.position import Position

## Dummy function for testing purposes


def model_output(position, verbose=False):

    ## Game changing algorithm.
    signal = 1 if random.random() > .5 else 0
    alloc = random.random() / 10

    return signal, alloc

class Portfolio:

    def __init__(self, value, eqs, init_date, verbose=False):
        self.positions = []
        self.free_cash = {init_date: value}
        self.init_positions(eqs, verbose)

    def init_positions(self, eqs, verbose=False):
        here = os.path.abspath(os.path.dirname(__file__))
        data_directory = os.path.join(here, '..\\data')
        eq_directory = os.path.join(data_directory, 'equities')
        for eq in eqs:
            eq_file = os.path.join(eq_directory, eq + '.xlsx')
            e = Equity(eq_file)
            position = Position(e, verbose)
            self.positions.append(position)
    
    def getPosition(self, ticker, verbose=False):

        for p in self.positions:
            
            if p.ticker in ticker:
                return p

    def realloc(self, date, strategy_lookback, strategy_threshold, verbose=False):
        
        self.free_cash[date] = self.free_cash[list(self.free_cash.keys())[len(self.free_cash.keys())-1]]
        
        predictions, allocations = np.zeros((len(self.positions),)), np.zeros((len(self.positions),))
    
        self.update_closings(strategy_lookback, strategy_threshold, date, verbose)

        for i,position in enumerate(self.positions):
            ### RUN MODEL FOR PARTICULAR EQUITY
            predictions[i], allocations[i] = model_output(position, verbose)## MODEL WOULD GO HERE
            
        
        ## After that loop, predictions will be 1/0 corresponding to buy/do nothing
        ## allocations will be a decimal indicating how much of our portfolio we should give to that
        
        ## for first try, we will just ignore allocation, but this should turn allcations into dollar amounts
        allocations = self.calculate_allocations(allocations, date, verbose)
        
        for i, pos in enumerate(self.positions):
            self.free_cash[date] -= pos.purchase(predictions[i], allocations[i], date, verbose)
        if verbose is True:
            print("Current Free Cash: ", self.free_cash[date])
            print("Current Positions Value: ", self.getValue(date) - self.free_cash[date])
        return self.update(verbose)

    def update(self, verbose=False):
        return 0

    def calculate_allocations(self, allocations, date, verbose=False):
        total = 0
        for i, alloc in enumerate(allocations):
            total += alloc
        
        ## Allocate one tenth of free cash
        allocations = allocations/(total * 10)

        allocations = allocations * self.free_cash[date]

        return allocations

    def update_closings(self, strategy_lookback, strategy_threshold, date, verbose=False):

        for i, pos in enumerate(self.positions):
        
            self.free_cash[date] += pos.handle_closings(strategy_threshold, strategy_lookback, date, verbose)
        
    def date_ob(self, date, verbose=False):

        pos = self.positions[0]

        most_recent_date = pos.eq.dates[0]
        
        return date > most_recent_date

    def getValue(self, date, verbose=False):

        value = self.free_cash[date]
        
        for pos in self.positions:
            if verbose:
                print("Pos:", pos.ticker)
                print("Trades:", pos.trades)
            pos_value = pos.value(date, verbose)
            if verbose:
                print(pos_value)
            value+=pos_value

        return value
        

