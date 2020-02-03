from models.equity import equity
from models.indicators import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

vslr_file = r'./data/equities/energy/VSLR.csv'
vslr = equity(vslr_file)

a = true_range(vslr, 10)
b = true_range(vslr, 20)

print(b[45])
plt.plot(a[40:], 'r-')
plt.plot(b[40:], 'b-')
plt.show()
