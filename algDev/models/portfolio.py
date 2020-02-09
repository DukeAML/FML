import numpy as np

class Portfolio:

    def __init__(self, value):
        self.positions = []
        self.value = value

    def realloc(self, date)

        predictions = np.zeros((len(self.positions), 10))

        for i,position in enumerate(positions):
            ### RUN MODEL FOR PARTICULAR EQUITY
            predictions[i, :] = ## MODEL WOULD GO HERE

        recommended_allocation = selectAssets(predictions)

        for i, position in enumerate(positions):

            curr_alloc = position.value / self.value

            diff = recommended_allocation[i] - curr_alloc

            amt = diff * self.value

            position.trade_value(amt, date)
                
    def selectAssets(o, short=False):

        evs = []

        for pred in o:
            evs.append(expected_value(pred))

        total = 0
        for i in range(len(evs)):
            if evs[i] < 0:
                evs[i] = 0
            total = total + evs[i]

        evs = evs/total

        return evs

    def expected_value(x):

        ev = 0
        bounds = [-0.9, -0.4, -0.085, -.045, -0.01, 0.01, 0.035, 0.065,
                  0.095, 0.13]

        for i in range(len(bounds)):
            ev = ev + (bounds[i] * x[i])

        return ev

