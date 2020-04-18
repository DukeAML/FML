from models.backtest import Backtest
import datetime
import pickle

def run_test():

    pf_value = 1000000
    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime(2020, 1, 15)

    b = Backtest(["SNP"], start_date, end_date, pf_value, False)

    after_value, positions = b.simulate({'lookback_period': 5, 'strategy_threshold': .025}, False)

    rtn = ((after_value - pf_value) / pf_value) * 100

    print(b.portfolio.positions[0].trades)

    with open('data.pickle', 'wb') as f:
        pickle.dump(b.portfolio.positions, f)
    
    with open('data.pickle', 'rb') as f:
        poss = pickle.load(f)

    print(poss[0].trades)
    print(str(rtn) + "%")
    
    b.plot_value(pf_value, start_date, end_date)
