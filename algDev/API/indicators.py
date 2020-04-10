from algDev.preprocessing.feature_generation import create_features
from algDev.models.equity import Equity


def get_indicator_value(ticker, feature):
    """
    ticker: 'AAPL'
    feature: 'macd_9_18

    indicators - params:
    sma - period 
    ema - per
    return: ndarray - floats -- one for each day going back n days
    """
    print("Calling indicators.py", feature)
    eq = Equity(ticker)

    inds = create_features(eq, [feature], normalize = False)

    return inds
