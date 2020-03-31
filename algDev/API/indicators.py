from preprocessing.feature_generation import get_feature
from models.equity import Equity

def get_indicator_value(ticker, feature):
    """
    ticker: 'AAPL'
    feature: 'macd_9_18

    indicators - params:
    sma - period 
    ema - per
    return: ndarray - floats -- one for each day going back n days
    """

    eq = Equity(ticker)

    ind = get_feature(eq, feature)

    return ind[0].values