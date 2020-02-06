import numpy as np
from algDev.models.indicators import Indicators


class TestIndicators:

    def test_sma(self):
        prices = np.arange(10)
        expected = np.array([0, 0, 0, 0, 0, 2, 3, 4, 5, 6])
        assert (Indicators.sma(period=5, prices=prices) == expected).all()
