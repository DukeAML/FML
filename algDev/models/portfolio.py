import numpy as np
import random
import os
import datetime
import pandas as pd
from algDev.models.equity import Equity
from algDev.models.position import Position

## Dummy function for testing purposes
def model_output(position, verbose=False):
    """
    Generate random buy/sell/hold signal
    1:Buy, 0:Hold, -1:Short
    Confidence Level: # between 0 and 1
    """
    signal = random.randint(0, 1) ##Placeholder, does not include shorting
    confidence = random.random() ##Placeholder

    return signal, confidence

class Portfolio:

    def __init__(self, value, init_date, trading_algorithm, asset_strategy, days = 500, start_price = 'O', stop_price = 'C', verbose=False):
        self.positions = []
        self.predictions = []
        day_before = init_date - datetime.timedelta(days=1)
        self.free_cash = {day_before: value}

        self.days = days
        self.start_price = start_price
        self.stop_price = stop_price

        self.trading_algorithm = trading_algorithm
        self.asset_strategy = asset_strategy        

        self.init_positions(init_date, days, verbose)
        self.init_preds()

    def init_positions(self, init_date, days = 500, verbose=False):
        for eq in self.trading_algorithm.eqs:
            position = Position(eq, init_date, days, verbose)
            self.positions.append(position)
    
    def init_preds(self):
        for eq in self.trading_algorithm.eqs:
            self.predictions.append({'ticker':eq.ticker, 'predictions':[]})
    
    def getPosition(self, ticker, verbose=False):

        for p in self.positions:
            
            if p.ticker in ticker:
                return p

    def add_predictions(self, predictions, date):

        for i, pos in enumerate(self.positions):
            self.predictions[i]['predictions'].append({'date': date, 'prediction': predictions[i][0], 'confidence': predictions[i][1]})

    def realloc(self, date, verbose=False):

        ##ASK LUKE ABOUT THIS LINE
        self.free_cash[date] = self.free_cash[list(self.free_cash.keys())[len(self.free_cash.keys())-1]]
        print("Free Cash: ", self.free_cash)
        # Dictionary of tickers and tuples of prediction and confidence
        predictions = self.trading_algorithm.predict(date)
        self.add_predictions(predictions, date)
        print("Predictions ", predictions)
        ## After that loop, predictions will be 1/0/-1 corresponding to buy/do nothing/short
        ##Confidence is the output of the model, from which we can calculate expected return
        ## allocations will be a decimal indicating how much of our available cash we should give to that
        
        ## for first try, we will just ignore allocation, but this should turn allcations into dollar amounts
        print("Allocation Breakdown ", self.asset_strategy.allocate(date, self.positions, predictions, verbose))
        allocations = self.asset_strategy.allocate(date, self.positions, predictions, verbose) * self.free_cash[date]
        print("Allocations in Total", allocations)
        for i, pos in enumerate(self.positions):
            self.free_cash[date] = self.free_cash[date] - pos.purchase(predictions[i][0], allocations[i], date, verbose)
        if verbose is True:
            print("Current Free Cash: ", self.free_cash[date])
            print("Current Positions Value: ", self.getValue(date) - self.free_cash[date])
        
        print("Todays Cash after making purchases", self.free_cash[date])
        self.trading_algorithm.update(date)

        self.update_closings(date, self.asset_strategy.closing_type, verbose)
        print("Todays Cash after making sales", self.free_cash[date])
        return self.update(verbose)

    def update(self, verbose=False):
        return 0

    def update_closings(self, date, closing_type, verbose=False):

        for i, pos in enumerate(self.positions):
        
            self.free_cash[date] += pos.handle_closings(self.trading_algorithm.params, date, closing_type, verbose)
        
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
        

