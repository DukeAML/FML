import pandas as pd
import math
import datetime
import numpy as np
import statistics as stat 
#from portfolio import Portfolio

class Finance:

    """
    Contains methods to calculate important statistical characeristics
    of securities and their relationships to each other to build efficient
    portfolios
    """

    def __init__(self):
        pass
    
    #Calculate the percent change between any two numbers
    #DONE
    @staticmethod
    def pChange(p1, p2):
        if p1 == 0 or p2 == 0:
            return 0
        return (p2-p1)/p1

    """
    Calculate the percent change each day between p1 and p2
    There are two cases:
    1) If start and stop are the same value, then it calculates the pChange from one day to the next of that value
    2) If start and stop are the same value, then it calculates the pChange of that value in that day

    There are 4 potential inputs for start and stop: 'O', 'C', 'H', 'L'
    days refers to how back you would like to go
    """
    #TESTING
    @staticmethod
    def dailyChanges(eq, today = datetime.datetime(2020,2,5), days = 500, start = 'O', stop = 'C'):
        

        today_index = eq.get_index_from_date(today)

        start = start.upper()
        stop = stop.upper()

        #Switch Case
        switcher = {'O':eq.opens, 'C':eq.closes, 'H':eq.highs, 'L':eq.lows}

        p1 = switcher.get(start, 0)
        p2 = switcher.get(stop, 0)

        #If IPO date happened < days days ago from today
        if today_index + days - 1 > len(p1):
            print("This should not be happening")
            days = len(p1) - today_index

        if(start == stop):
            daily_returns = np.zeros(days-1)
            i = today_index
            counter = 0
            for i in range(today_index, today_index + days -1):
                daily_returns[counter] = Finance.pChange(p1[i+1],p2[i])
                counter = counter + 1

        else:
            daily_returns = np.zeros(days)
            i = today_index
            counter = 0
            for i in range(today_index,today_index + days):
                daily_returns[counter] = Finance.pChange(p1[i],p2[i])
                counter = counter + 1
                
        return daily_returns

    #DONE
    @staticmethod
    def update_dailyChanges(position, today, start = 'O', stop = 'C', verbose = False):
        if verbose:
            print("Updating daily changes")

        np.delete(position.daily_changes, len(position.daily_changes)-1)
        
        np.insert(position.daily_changes, 0, Finance.dailyChanges(position.eq, today, 1, start, stop))

        return position.daily_changes

    #DONE
    @staticmethod
    def mean(eq, today = datetime.datetime(2020,2,5), days = 500, start = 'O', stop = 'C'):
        start = start.upper()
        stop = stop.upper()

        return stat.mean(Finance.dailyChanges(eq, today, days, start, stop))

    #DONE
    @staticmethod
    def variance(eq, today = datetime.datetime(2020,2,5), days = 500, start = 'O', stop = 'C'):
        start = start.upper()
        stop = stop.upper()

        return stat.pvariance(Finance.dailyChanges(eq, today, days, start, stop))

    #DONE
    @staticmethod
    def covariance(eq1, eq2, today = datetime.datetime(2020,2,5), days = 500, start = 'O', stop = 'C'):
        start = start.upper()
        stop = stop.upper()

        DCeq1 = Finance.dailyChanges(eq1, today, days, start, stop)
        DCeq2 = Finance.dailyChanges(eq2, today, days, start, stop)

        print("DCeq1:", DCeq1)
        print(len(DCeq1))
        print("DCeq2:", DCeq2)
        print(len(DCeq2))

        #If one security IPO in the last days days, then adjust so lists are same length
        if(len(DCeq1) != len(DCeq2)):
            if(len(DCeq1)>len(DCeq2)):
                DCeq1 = DCeq1[0:len(DCeq2)-1]
            else:
                DCeq2 = DCeq2[0:len(DCeq1)-1]
        
        return np.cov(DCeq1, DCeq2)[0,1]

    #DONE
    @staticmethod
    def stddev(eq, today = datetime.datetime(2020,2,5), days = 500, start = 'O', stop = 'C'):
        start = start.upper()
        stop = stop.upper()

        return math.sqrt(Finance.variance(eq, today, days, start, stop))
    
    #DONE
    @staticmethod
    def correlation(eq1, eq2, today = datetime.datetime(2020,2,5), days = 500, start = 'O', stop = 'C'):
        start = start.upper()
        stop = stop.upper()

        cov = Finance.covariance(eq1, eq2, today, days, start, stop)
        std1 = Finance.stddev(eq1, today, days, start, stop)
        std2 = Finance.stddev(eq2, today, days, start, stop)

        return cov/(std1*std2)
