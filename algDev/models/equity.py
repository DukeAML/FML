import pandas as pd
import numpy as np
from algDev.models.indicators import Indicators


class Equity(Indicators):

    def __init__(self, data_file):
        super().__init__(data_file)

        self.opens = self.data['Open'].values
        self.highs = self.data['High'].values
        self.lows = self.data['Low'].values
        self.volumes = self.data['Volume'].values

    def ohlc(self):
        return (self.opens + self.highs + self.lows + self.closes) / 4

    def typical_prices(self):
        return (self.highs + self.lows + self.closes) / 3
