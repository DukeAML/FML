class Trade:

    def __init__(self, date, num_shares):
        self.date = date
        self.num_shares = num_shares
        self.sold = False

    def purchase_date(self):
        return self.date

    def sell(self):
        self.sold = False