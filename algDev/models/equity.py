import math
import numpy as np
import pandas as pd
import datetime
from algDev.db.wrapper import getData
from algDev.models.indicators import Indicators

class Equity: 
    """[Class that represents an asset by parsing the inputted data file.
        This class contains a few methods for extracting more information
        about prices and movement.]
    
    Fields:
        closes {float[]} - Closing prices of the equity
        opens {float[]}
        highs {float[]}
        lows {float[]}
        volumes {int[]}
        dates {String[]}
        
    Returns:
        {Equity}
    """
    def __init__(self, ticker, verbose=False):

        self.dates = []
        self.opens = []
        self.closes = []
        self.lows = []
        self.highs = []
        self.volumes = []
        self.ticker = ticker

        self.parse_data(verbose)

    def fill_open(self, day):
        has_open = day[1] is not None
        if has_open:
            return day
        has_low = day[3] is not None
        has_high = day[2] is not None
        has_close = day[4] is not None
        if has_low and has_high:
            day[1] = day[3] + (day[2] - day[3])/2
            return day
        elif has_low:
            day[1] = day[3]
        elif has_high:
            day[1] = day[2]
        elif has_close:
            day[1] = day[4]
        
        return day

    def fill_close(self, day):
        has_close = day[4] is not None
        if has_close:
            return day
        has_low = day[3] is not None
        has_high = day[2] is not None
        has_open = day[1] is not None
        if has_low and has_high:
            day[4] = day[3] + (day[2] - day[3])/2
            return day
        elif has_low:
            day[4] = day[3]
        elif has_high:
            day[4] = day[2]
        elif has_close:
            day[4] = day[4]
        
        return day

    def fill_high(self,day):
        has_high = day[2] is not None
        if has_high:
            return day
        has_low = day[3] is not None
        has_open = day[1] is not None
        has_close = day[4] is not None
        if has_low:
            day[2] = day[3]
        elif has_open:
            day[2] = day[1]
        elif has_close:
            day[2] = day[4]
        
        return day
    def fill_low(self,day):
        
        has_low = day[3] is not None
        if has_low:
            return day
        has_high= day[2] is not None
        has_open = day[1] is not None
        has_close = day[4] is not None
        if has_close:
            day[3] = day[4]
        elif has_open:
            day[3] = day[1]
        elif has_high:
            day[3] = day[2]
        
        return day

    def fill_vol(self,day):
        if day[5] is None:
            day[5] = 0
        return day
    def val_row(self, day):
        day = self.fill_open(day)
        day = self.fill_close(day)
        day = self.fill_high(day)
        day = self.fill_low(day)
        day = self.fill_vol(day)
        return day[0], day[1], day[2], day[3], day[4], day[5]

    def update_data(self, verbose=False):
        self.dates = []
        self.opens = []
        self.closes = []
        self.lows = []
        self.highs = []
        self.volumes = []

        self.parse_data()
    def parse_data(self, verbose=False):
        """[Parses the incoming data into the appropriate fields. 
        There have been reported issues with the parsing on certain
        file types.]
        
        Arguments:
            data_file {String} -- [Path to the data file that contains 
            the equity information]
        """

        # eq_path = r'./algDev/data/equities/%s.xlsx' % ticker
        # self.data = pd.read_excel(eq_path)
        
        # dataFile_len = len(eq_path)
        # i = dataFile_len - 5
        # while True:
            
        #     if eq_path[i] == r'/' or  eq_path[i] == '\\':
        #         break
        #     i=i-1
        
        # self.ticker = eq_path[i+1:dataFile_len-5]
        
        # volumeCol = self.ticker + ' US Equity - Volume'
        
        incoming_data = getData(self.ticker)
        
        for day in incoming_data:
            day_arr = []
            day_arr.append(day[1]); day_arr.append(day[2]); day_arr.append(day[3]); day_arr.append(day[4]); day_arr.append(day[5]); day_arr.append(day[6])
            date, open, high, low, close, volume = self.val_row(day_arr)
            if not open:
                open = self.opens[len(self.opens)-1]
                close = self.closes[len(self.closes)-1]
                high = self.highs[len(self.highs)-1]
                low = self.highs[len(self.lows)-1]
                volume = self.volumes[len(self.volumes)-1]
            self.dates.append(datetime.datetime(date.year, date.month, date.day))
            self.opens.append(float(open))
            self.highs.append(float(high))
            self.lows.append(float(low))
            self.closes.append(float(close))
            self.volumes.append(int(volume))
        self.dates = np.array(self.dates)
        self.opens = np.array(self.opens)
        self.highs = np.array(self.highs)
        self.lows = np.array(self.lows)       
        self.closes = np.array(self.closes)
        self.volumes = np.array(self.volumes)
    
    def get_price(self, date, type='c', verbose=False):
        if verbose:
            print(date)
        i = self.get_index_from_date(date)
        
        if type=='o':
            if verbose:
                print("Getting Open", self.opens[i])
            return self.opens[i]

        elif type=='h':
            if verbose:
                print("Getting High", self.highs[i])
            return self.highs[i]

        elif type == 'l':
            if verbose:
                print("Getting Low", self.lows[i])
                
            return self.lows[i]

        else:
            if verbose:
                print("Getting Close", self.closes[i])
            return self.closes[i]

    def get_index_from_date(self, date, verbose=False):

        if date == 'max':
            return len(self.closes) - 1

        
        for i, d in enumerate(self.dates):
            diff = d - date
            if diff <= datetime.timedelta(0):
                return i

    def ohlc(self, verbose=False):
        """The average of the open low high close
        
        Returns:
            [float[]] -- [A vector of the averages]
        """
        
        avg = (self.opens + self.highs + self.lows + self.closes) / 4

        return avg

    def typical_prices(self, verbose=False):
        """The 'Typical Prices' of the equity, or the average of the high,low, and close
        
        Returns:
            [float[]] -- [Vector of the averages]
        """
        tps = (self.highs + self.lows + self.closes) / 3

        return tps

    def balance_of_power(self, verbose=False):
        """The balance of the power is a metric for
         determining the variability in the opens/closes versus
         highs/lows
        
        Returns:
            [float[]] -- [Vector of the index]
        """

        bop = (self.closes - self.opens) / (self.highs - self.lows)

        return bop

    def bollinger_bands(self, period=20, stds=2, verbose=False):
        """[The Bolinger Bands is essentially a confidence interval of 
        stds Deviations where the price should be based on the last 
        period periods of prices]
        
        Keyword Arguments:
            period {int} -- [The period over which to look over the 
            prices] (default: {20})
            stds {int} -- [The number of standard deviations the bands 
            should take up] (default: {2})
        
        Returns:
            [float[], float[]] -- [Upper Bolinger Band, Lower Bolinger Band vectors respectively]
        """
        tp = self.typical_prices()
        ma = Indicators.sma(prices=tp, period=period)
        std = Indicators.calc_std(prices=tp, period=period)

        bolu = np.array([ma[i] + stds * std[i] for i in range(len(ma))])
        bold = np.array([ma[i] + stds * std[i] for i in range(len(ma))])

        return bolu, bold

    def accumulative_swing_index(self, verbose=False):
        """[ASI is a way of looking at the prices of the equity
        in order to get information regarding momentum and market
        conditions]
        
        Returns:
            [float[]] -- [ASI values in a vector]
        """
        asi = np.zeros((len(self.closes),))
        for i in range(len(self.closes)):
            if i + 1>= len(self.closes):
                break
            curr_close = self.closes[i]
            prev_close = self.closes[i + 1]
            curr_open = self.opens[i]
            prev_open = self.opens[i + 1]
            curr_high = self.highs[i]
            prev_high = self.highs[i + 1]
            curr_low = self.lows[i]
            prev_low = self.lows[i + 1]
            k = np.max([(prev_high - curr_close), (prev_low - curr_close)])
            t = curr_high - curr_low
            kt = k / t

            num = (prev_close - curr_close + (0.5 * (prev_close - prev_open)) + (0.25 * (curr_close - curr_open)))

            r = Indicators.get_r(curr_high, curr_low, prev_close, prev_open)

            body = num / r

            asi[i] = 50 * body * kt
        return asi[:-1]

    def gop_range_index(self, period=10, verbose=False):
        """The GOP looks at the largest swing in prices over the
        last period periods.
        
        Keyword Arguments:
            period {int} -- [Period over which to calculate GOP] 
            (default: {10})
        
        Returns:
            [float[]] -- [A vector of the GOP values]
        """
        gop = np.zeros((len(self.closes),))

        for i in range(len(self.closes)):
            if i + period >= len(self.closes):
                continue
            highest = np.max(self.highs[i:i+period])
            lowest = np.min(self.lows[i:i + period])
            price_range = highest - lowest
            gop[i] = math.log(price_range) / math.log(period)

        return gop

    def pivot_points(self, verbose=False):
        """[Pivot poits are the centers of recent price movement]
        
        Returns:
            [float[],float[],float[],float[],float[]] -- [The pivot
            points, restiance one band, resistance 2 band, support 1
            band and support 2 band respectively as vectors.]
        """
        closes = self.closes
        highs = self.highs
        lows = self.lows

        pivots = np.zeros((len(closes),))
        r1s = np.zeros((len(closes),))
        r2s = np.zeros((len(closes),))
        s1s = np.zeros((len(closes),))
        s2s = np.zeros((len(closes),))

        for i in range(len(closes)):
            pivot, r1, r2, s1, s2 = Indicators.calc_pivot_points(highs[i], lows[i], closes[i])
            pivots[i] = pivot
            r1s[i] = r1
            r2s[i] = r2
            s1s[i] = s1
            s2s[i] = s2

        return pivots, r1s, r2s, s1s, s2s

    def pivot_indicator(self, verbose=False):
        """[Gets the spread between closing prices and the pivot points
        for a given day]
        
        Returns:
            [float[]] -- [Vector of the differences]
        """
        pivots, *_ = self.pivot_points()

        ind = np.zeros((len(pivots),))
        for i in range(len(pivots)):
            ind[i] = self.closes[i] - pivots[i]

        return ind

    def conv_date(self, date, verbose=False):
        ts = pd.Timestamp(date)

        return ts.to_pydatetime()   
