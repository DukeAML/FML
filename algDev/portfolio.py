from allocate import selectAssets

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
        


