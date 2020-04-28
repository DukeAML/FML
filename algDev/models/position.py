from algDev.models.trade import Trade
from algDev.models.finance import Finance
import datetime

class Position:
    def __init__(self, eq, init_date,days = 500, verbose=False):
        self.ticker = eq.ticker
        self.eq = eq
        self.init_date = init_date
        self.trades = []

    def get_trades_dictionary(self):
        ts = []
        for t in self.trades:
            if t.sold:
                sell_date = t.date_sold
            else:
                sell_date = None
            ts.append({'datePurchased': t.date_purchased, 'numShares': t.num_shares,'sold': t.sold, 'dateSold': sell_date})

        return ts
        
    def get_values(self, date):
        day_diff = (date - self.init_date).days
        vals = []
        dates = []
        
        for i in range(day_diff):
            i_day = datetime.timedelta(days=i)
            dates.append(self.init_date + i_day)
            vals.append(self.value(self.init_date + i_day))

        return dates, vals

    ##CHANGE TO ACCOMODATE SHORTING
    def purchase(self, prediction, allocation, today,verbose=False):
        if verbose:
            print("Checking purchase:",prediction)
            print("Allocation:", allocation)

        if prediction == 0 or allocation <=0:
            return 0
            
        #if prediction > 0:
        #    if verbose:
        #        print("Making purchase: ", allocation)
        #    left_over = self.trade_value(allocation, today, verbose)
        left_over = self.trade_value(allocation, today, verbose)
        #    return allocation - left_over
        return allocation - left_over
        #return 0
        
    def trade_shares(self, num_shares, date,verbose=False):
        self.trades.append(Trade(date, num_shares))

    def trade_value(self, amt, date,verbose=False):
        day_open = self.eq.get_price(date, 'o')
        
        num_shares = int(amt/day_open)
        if num_shares == 0:
            return amt
        total_purchased = num_shares * day_open
        left_over = amt - total_purchased
        if verbose:
            print("Buying ", num_shares, " at ", day_open)
        self.trade_shares(num_shares, date)
        return left_over

    def buy_shares(self, num_shares,verbose=False):
        return self.trade_shares(num_shares)

    def sell_shares(self, num_shares,verbose=False):
        return self.trade_shares(-1 * num_shares)

    def value(self, date,verbose=False):
        return self.eq.get_price(date, 'c', verbose) * self.get_shares(date)

    def is_short(self,verbose=False):
        return self.size < 0

    def has_position(self,verbose=False):
        return self.size is not 0

    def get_shares(self, date, verbose=False):
        total = 0
        
        for trade in self.trades:
            if trade.date_sold > date and trade.date_purchased <= date:
                total += trade.num_shares
                
        return total

    ##Note: lower_limit should be a negative float
    def handle_closings(self, params, today, close_type='threshold', verbose=False):
        cash = 0
        exp = params['period']
        upper_limit = params['upper_threshold']
        lower_limit = params['lower_threshold']
        
        if close_type == 'threshold':
            if verbose:
                print("Checking position for closings")
            for i,trade in enumerate(self.trades):
                if self.check_closed(trade, verbose):
                    continue
                pur_date = trade.purchase_date()
                days_since_pur = today - pur_date
                if days_since_pur > datetime.timedelta(days=exp):
                    # if verbose:
                    if verbose:
                        print("Bought at: ", self.eq.get_price(pur_date, 'o'))
                        print("Sold at: ", self.eq.get_price(today, 'c'))
                    cash += trade.num_shares * self.eq.get_price(today, 'c', verbose)
                    self.trades[i] = trade.sell(today, verbose)
                    continue
                upper_limit_price = self.eq.get_price(pur_date, 'o', verbose) * (1 + upper_limit)
            
                if self.eq.get_price(today, 'h', verbose) >= upper_limit_price:
                    if(verbose):
                        print("Bought at: ", self.eq.get_price(pur_date, 'o', verbose))
                        print("Sold at: ", self.eq.get_price(today, 'h', verbose))
                    cash += trade.num_shares * upper_limit_price
                    self.trades[i] = trade.sell(today, verbose)

                lower_limit_price = self.eq.get_price(pur_date, 'o', verbose) * (1+ lower_limit)

                if self.eq.get_price(today, 'l', verbose) <= lower_limit_price:
                    if verbose:
                        print("Bought at: ", self.eq.get_price(pur_date, 'o', verbose))
                        print("Sold at: ", self.eq.get_price(today, 'l', verbose))

                    cash += trade.num_shares * lower_limit_price
                    self.trades[i] = trade.sell(today, verbose)
        else:
            for i,trade in enumerate(self.trades):
                if self.check_closed(trade, verbose):
                    continue
                if verbose:
                    print("Bought at: ", self.eq.get_price(pur_date, 'o'))
                    print("Sold at: ", self.eq.get_price(today, 'c'))
                    
                cash += trade.num_shares * self.eq.get_price(today, 'c', verbose)
                self.trades[i] = trade.sell(today, verbose)

        if verbose:
            print("Trades:",self.trades)
        return cash

    def check_closed(self, trade,verbose=False):
        return trade.sold
