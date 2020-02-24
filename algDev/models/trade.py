import datetime

class Trade:

    def __init__(self, date, num_shares, verbose=False):
        self.date_purchased = date
        if verbose:
            print(num_shares)
        self.num_shares = num_shares
        self.sold = False
        self.date_sold = datetime.datetime(2100,1,1)

    def purchase_date(self, verbose=False):
        return self.date_purchased

    def sell(self, sell_date, verbose=False):
        self.sold = True
        self.date_sold = sell_date
        return self

    def __repr__(self):
        return "[Date Purchased: %s, %s shares, Date Sold: %s]" % ("" + str(self.date_purchased.day) + "/" + str(self.date_purchased.month) + "/" + str(self.date_purchased.year), self.num_shares, str(self.date_sold.day) + "/" + str(self.date_sold.month) + "/" + str(self.date_sold.year))

    def __str__(self):
        return "[Date Purchased: %s, %s shares, Date Sold: %s]" % ("" + str(self.date_purchased.day) + "/" + str(self.date_purchased.month) + "/" + str(self.date_purchased.year), self.num_shares, str(self.date_sold.day) + "/" + str(self.date_sold.month) + "/" + str(self.date_sold.year))