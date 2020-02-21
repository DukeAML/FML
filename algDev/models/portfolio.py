import numpy as np
import random
from algDev.models.equity import Equity
from algDev.models.position import Position

## Dummy function for testing purposes


def model_output(position):

    ## Game changing algorithm.
    signal = 1 if random.random() > .5 else 0
    alloc = random.random() / 10

    return signal, alloc

class Portfolio:

    def __init__(self, value, eqs, init_date):
        self.positions = []
        self.free_cash = value
        self.init_positions(eqs)

    def init_positions(self, eqs):

        for eq in eqs:
            e = Equity(eq)
            position = Position(e)
            self.positions.append(position)
    
    def getPosition(self, ticker):

        for p in self.positions:
            
            if p.ticker in ticker:
                return p

    def realloc(self, date, strategy_lookback, strategy_threshold):
        
        predictions, allocations = np.zeros((len(self.positions),)), np.zeros((len(self.positions),))
    
        self.update_closings(strategy_lookback, strategy_threshold, date)

        for i,position in enumerate(positions):
            ### RUN MODEL FOR PARTICULAR EQUITY
            predictions[i], allocations[i] = model_output(position)## MODEL WOULD GO HERE
        
        ## After that loop, predictions will be 1/0 corresponding to buy/do nothing
        ## allocations will be a decimal indicating how much of our portfolio we should give to that
        
        ## for first try, we will just ignore allocation, but this should turn allcations into dollar amounts
        self.calculate_allocations()
        
        for i, pos in enumerate(positions):
            self.free_cash -= pos.purchase(predictions[i], allocations[i], date)

        return self.update()

    def calculate_allocations(self):
        total = 0
        for i, alloc in enumerate(self.allocations):
            total += alloc
        
        ## Allocate one tenth of free cash
        self.allocations = self.allocations/(total * 10)

        self.allocations = self.allocations * self.free_cash

    def update_closings(self, strategy_lookback, strategy_threshold, date):

        for i, pos in enumerate(positions):
        
            self.free_cash += pos.handle_closings(strategy_threshold, strategy_lookback, date)
       
    def update(self):
        return 0
        

