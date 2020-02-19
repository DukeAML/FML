class Position:
    def __init__(self, sym, shares, price):
        self.symbol = sym
        self.shares = shares
        self.price = price
        self.trades = {}

    def trade_shares(self, num_shares, date):
        self.trades[date] = num_shares
        self.shares = self.shares + num_shares

    def trade_value(self, amt, date):
        num_shares = int(amt/self.price)
        self.trades[date] = num_shares
        self.shares = self.shares + num_shares
        
    def buy_shares(self, num_shares):
        return self.trade(num_shares)

    def sell_shares(self, num_shares):
        return self.trade(-1 * num_shares)

    def value(self):
        return self.price * self.shares

    def is_short(self):
        return self.size < 0

    def has_position(self):
        return self.size is not 0

    