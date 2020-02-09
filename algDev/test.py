from algDev.models.equity import Equity

from algDev.utils import datapath

vslr_file = datapath('commodities', 'OIL.csv')
vslr = Equity(vslr_file)
