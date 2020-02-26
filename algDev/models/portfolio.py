import numpy as np
import random
## Dummy function for testing purposes


def model_output(position):

    ## Game changing algorithm.
    signal = 1 if random.random() > .5 else 0
    alloc = random.random() / 10

    return signal, alloc

class Portfolio:

    def __init__(self, value, eqs):
        self.positions = []
        self.value = value
        

    def realloc(self, date):
        
        predictions, allocations = np.zeros((len(self.positions),)), np.zeros((len(self.positions),))
    
        for i,position in enumerate(positions):
            ### RUN MODEL FOR PARTICULAR EQUITY
            predictions[i], allocations[i] = model_output(position)## MODEL WOULD GO HERE

        ## After that loop, predictions will be 1/0 corresponding to buy/do nothing
        ## allocations will be a decimal indicating how much of our portfolio we should give to that
        
        ## for first try, we will just ignore allocation

        for i, position in enumerate(positions):
        
            curr_alloc = position.value / self.value

            amt = diff * self.value

            position.trade_value(amt, date)
            


