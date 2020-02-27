from models.trade import Trade
import datetime

def test_trade():
    trades = [Trade(datetime.datetime(2016,1,1), 10), Trade(datetime.datetime(2016,3,1), 15), Trade(datetime.datetime(2016,5,1), 5)]

    trades[2] = trades[2].sell()

    print(trades)

test_trade()
