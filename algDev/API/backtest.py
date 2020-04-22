from algDev.API.models import loadTradingAlgorithm
from algDev.models.backtest import Backtest
from algDev.models.trading_algorithm import TradingAlgorithm

from algDev.models.asset_strategy import AssetStrategy, AssetAllocation
import datetime

def run_backtest(start_date, end_date, pf_value, tradingAlgorithmId, target_return=0.0, closing_strategy='threshold'):
    
    trading_algorithm = loadTradingAlgorithm(tradingAlgorithmId)
    aa = AssetAllocation(trading_algorithm.params['upper_threshold'], trading_algorithm.params['lower_threshold'], target_return=target_return)
    asset_strategy = AssetStrategy(aa, close_type=closing_strategy)
    
    b = Backtest(trading_algorithm, asset_strategy, start_date, end_date, pf_value, False)
    return_vals = b.simulate(False)

    ## Return vals format:
    '''
    return_val = {'return':rtn, 'snp_rtn':snp_rtn, 'net_rtn':net_rtn, 'average_free_cash':avg_free_cash, 'beta': beta, 'vol':vol, 'treynor':treynor, 'sharpe':sharpe, 'dates':dates, 'pf_vals':pf_vals, 'initial_val':initial_val, 'snp_vals':snp_vals, 'positions':self.portfolio.positions}
    
    return - float
    snp_rtn - float
    net_rtn - float
    average_free_cash - float
    beta - float
    vol - float
    treynor - float
    sharpe - flaot
    dates - datetime[]
    pf_vals - float[]
    initial_vals - float[]
    snp_vals - float[]
    positions - Position[]
    '''
    return return_vals