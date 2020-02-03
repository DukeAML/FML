import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from algDev.models.indicators import Indicators


class REIT(Indicators):

    def __init__(self, data_file):
        super().__init__(data_file)
