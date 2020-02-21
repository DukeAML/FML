from algDev.models.trade import Trade
import datetime

class Position:
    def __init__(self, eq):
        self.ticker = eq.ticker
        self.eq = eq
        self.trades = []

    def purchase(self, prediction, allocation, today):
        if prediction > 0:
            self.trade_value(allocation, today)
            return allocation
        return 0
        
    def trade_shares(self, num_shares, date):
        self.trades.append(Trade(date, num_shares))

    def trade_value(self, amt, date):
        num_shares = int(amt/self.opens)
        self.trade_shares(num_shares, date)
        
    def buy_shares(self, num_shares):
        return self.trade_shares(num_shares)

    def sell_shares(self, num_shares):
        return self.trade_shares(-1 * num_shares)

    def value(self):
        return self.price * self.shares

    def is_short(self):
        return self.size < 0

    def has_position(self):
        return self.size is not 0

    def get_shares(self):
        total = 0
        for trade in self.trades:
            total += trade.num_shares

        return total

    def handle_closings(self, limit, exp, today):
        cash = 0
        for trade in self.trades:
            if self.check_closed(trade):
                continue
            pur_date = trade.purchase_date()
            days_since_pur = today - pur_date
            if days_since_pur > exp:
                cash += trade.num_shares * eq.get_price(today, 'c')
                trade.sell()
            limit_price = eq.get_price(pur_date, 'o') * (1 + limit)
            if eq.get_price(today, 'h') >= limit_price:
                cash += trade.num_shares * limit_price
                trade.sell()

        return cash

    def check_closed(self, trade):
        return trade.sold