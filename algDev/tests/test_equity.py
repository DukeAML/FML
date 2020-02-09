import pytest
import os

from algDev.models.equity import Equity
from algDev.utils import datapath


@pytest.fixture
def commodity_filepath():
    return datapath('commodities', 'OIL.csv')


@pytest.fixture
def equity_filepath():
    return datapath('equities', 'PLUG.csv')


@pytest.fixture
def index_filepath():
    return datapath('indexes', 'SNP.csv')


@pytest.mark.usefixtures("commodity_filepath", "equity_filepath", "index_filepath")
class TestEquity:
    def test_csv_load_to_df(self, commodity_filepath, equity_filepath, index_filepath):
        Equity(commodity_filepath)
        Equity(equity_filepath)
        Equity(index_filepath)

    def test_asset_sma(self):
        pass
