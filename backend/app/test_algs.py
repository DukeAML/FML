import sys
# gives backend app access to modules in algDev by adding directory to pythonpath
sys.path.insert(1, '../')

from algDev import run

run.test_three()

