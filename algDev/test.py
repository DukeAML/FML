from models.equity import Equity
from models.feature_builder import *

ticker = 'AAPL'
eq_path = r'./algDev/data/equities/%s.xlsx' % ticker
eq = Equity(eq_path)

print(build_labels(eq))
