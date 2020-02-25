from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.order import Order


import datetime
import queue

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        ## Overriden method
        print("Error.", reqId, errorCode, errorString)

    def historicalData(self, reqId, bar):
        print("HistoricalData. ReqId:", reqId, "date", bar.date, "open", bar.open, "high", bar.high, "low", bar.low, "close", bar.close)
   


def main():
    app = TestApp()

    app.connect('127.0.0.1', 7497, 0)

    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"

    app.reqHistoricalData(5, contract, "", "1 D", "1 min", "MIDPOINT", 0, 1, False, [])


    # historic_data = app.get_IB_historical_data(contract)    
    # print(historic_data)

    # otherContract = Contract()
    # otherContract.symbol = "EUR"
    # otherContract.secType = "CASH"
    # otherContract.exchange = "IDEALPRO"
    # otherContract.currency = "USD"

    # app.reqHistoricalData(1, otherContract, "", "1 D", "1 min", "MIDPOINT", 0, 1, False, [])

    app.run()




if __name__ == '__main__':
    main()

# OK SO - still just hanging, not really getting any new data - at this point, not sure what to do - re try to implement
# thing from the two videos to see if any of this is still working - start with the one that's open, move to the one after...
# In theory, they both should work, might lead you to something you're missing