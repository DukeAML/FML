import numpy as np
from models.indicators import Indicators


class TestIndicators:

    def test_sma(self):
        prices = np.arange(10)
        expected = np.array([0, 0, 0, 0, 0, 2, 3, 4, 5, 6])
        assert (Indicators.sma(period=5, prices=prices) == expected).all()

    def test_ema(self, period):
        prices = np.arange(10)

        print(Indicators.ema(prices, period))

    def test_sma(self,period):
        prices = np.arange(10)

        print(Indicators.sma(prices, period))
    def test_macd(self):
        prices = np.arange(100)

        print(Indicators.macd(prices, 18, 9))
