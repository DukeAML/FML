from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum

import datetime
import queue

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        error_queue=queue.Queue()
        self._my_errors = error_queue

    def error(self, id, errorCode, errorString):
        ## Overriden method
        errormsg = "IB error id %d errorcode %d string %s" % (id, errorCode, errorString)
        self._my_errors.put(errormsg)
    
    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick price. Ticker ID:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, end = ' ')

    def tickSize(self, reqId, tickType, size):
        print("Tick size. Ticker ID:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)

    def historicalTicks(self, reqId: int, ticks, done: bool):
        for tick in ticks:
            print("HistoricalTick. ReqId:", reqId, tick)
    
    def historicalTicksBidAsk(self, reqId: int, ticks, done: bool):
        for tick in ticks:
            print("HistoricalTickBidAsk. ReqId:", reqId, tick)
    
    def historicalTicksLast(self, reqId: int, ticks, done: bool):
        for tick in ticks:
            print("HistoricalTickLast. ReqId:", reqId, tick)

    # ! [historicaldata]
    def historicalData(self, reqId:int, bar):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)
    # ! [historicaldata]
   
    

def main():
    app = TestApp()

    app.connect('127.0.0.1', 7497, 0)

    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"

    # historic_data = app.get_IB_historical_data(contract)    
    # print(historic_data)

    queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
    app.reqHistoricalData(0, contract, queryTime,
                               "1 M", "1 day", "MIDPOINT", 1, 1, False, [])

    app.run()




if __name__ == '__main__':
    main()
