import numpy as np
from models.finance import Finance

class AssetAllocation:

    def __init__(self, upper_threshold, lower_threshold):
        super.__init__()
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold

    def get_exp_ret(self, positions, predictions):
        expected_returns = []
        for position in positions:
            expected_returns.append(self.exp_ret(predictions[position.eq.ticker]))

        return expected_returns

    def exp_ret(self, prediction, confidence, verbose):
        threshold = 0
        if prediction == 1:
            threshold = self.upper_threshold
        elif prediction == -1:
            threshold = self.lower_threshold
        
        ##ISSUE HERE IS THAT EXPECTED RETURN IS CAPPED AT THRESHOLD (condiser multiplying is by 2)
        return confidence * threshold
    
    ##UPDATE THIS
    def calculate_allocations(self, date, positions, predictions, verbose=False):
        
        expected_returns = self.get_exp_ret(positions, predictions)

        cov_arr = self.get_cov_arr(positions, date)
        unit_vector = np.ones(len(expected_returns))
        inv_cov_arr = np.linalg.inv(cov_arr)

        A = np.dot(np.dot(np.transpose(unit_vector), inv_cov_arr), unit_vector)
        B = np.dot(np.dot(np.transpose(unit_vector),inv_cov_arr), expected_returns)
        C = np.dot(np.dot(np.transpose(expected_returns), inv_cov_arr), expected_returns)
        delta = np.dot(A,C) - np.dot(B,B)

        ##USE THE ABOVE FORMULAS TO CALCULATE THE EFFICIENT FRONTIER

        w_g = np.divide(np.dot(np.linalg.inv(cov_arr),unit_vector),A) #Weightings minimum risk portfolio
        w_d = np.divide(np.dot(np.linalg.inv(cov_arr),expected_returns),B) #Weightings tangency portfolio for r = 0% 
        if verbose:
            print("w_d:", w_d)

        total = 0
        for i, alloc in enumerate(w_d):
            total += alloc
        
        ## Allocate one tenth of free cash
        allocations = w_d/(total * 10)

        return allocations

    def get_DC_arr(self, positions, today, start = 'O', stop = 'C'):
        DC_arr = []
        for position in positions:
            DC_arr.append(Finance.update_dailyChanges(position, today, start, stop))

    def get_cov_arr(self, date, positions):
        DC_arr = self.get_DC_arr(positions, date)
        cov_arr = np.cov(DC_arr)
        #for i in range(0, len(self.positions)):
        #    eq1 = self.positions[i].eq
        #    for j in range(0, len(self.positions)):
        #        eq2 = self.positions[j].eq
        #        self.cov_arr[i, j] = Finance.covariance(eq1, eq2, init_date, days, start, stop)
        return cov_arr