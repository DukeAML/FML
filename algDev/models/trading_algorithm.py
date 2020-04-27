from algDev.models.equity import Equity
from algDev.algorithms.model_collection import ModelCollection
from algDev.algorithms.voter import Voter
from algDev.preprocessing import data_generator, feature_generation
import datetime
import time
from algDev.models.confusion_matrix import ConfusionMatrix
from algDev.db.wrapper import createTradingAlgorithm
import csv

class TradingAlgorithm:
    """ This is the main class. You would make a TradingAlgorithm 
    object to actually generate your predictions on and pass them into
    an AssetAllocationAlgorithm.
    
    Returns:
        TradingAlgorithm -- Object to be used to retrain and predict data points
    """
    
    def __init__(self, tickers, features, type = 'svm', data_lookback_period = 10, label_lower_threshold = -0.15, label_upper_threshold = 0.025, label_period = 10, data_splits = [0.8, 0.2], cnn_split=0, verbose=False, voting_type = 'maj_rule', models = None, model_params = None, test_mode=False):
        """Initialize the TradingAlgorithm Object
        
        Arguments:
            tickers {string array} -- tickers of the securities to include
            features {string array} -- indicators to include with parameters attached with underscores, more in README
        
        Keyword Arguments:
            type {str} -- [what type of algorithm the models will be] (default: {'svm'})
            data_lookback_period {int} -- [how long the input data should look back] (default: {10})
            label_threshold {float} -- [the amount the equity is expected to increase in order to be successful] (default: {0.015})
            label_period {int} -- [the length of time before the equity is exited] (default: {10})
            data_splits {list} -- [train,validation,test splits. can just be train,test] (default: {[0.8, 0.2]})
            cnn_split {int} -- [how many cnns we want (if necessary)] (default: {0})
        """
        super().__init__()
        self.algorithm_types = [
        'cnn',
        'svm'
        ]
        assert type in self.algorithm_types
        self.type = type
        self.test_mode=test_mode
        self.features = features
        self.tickers = tickers
        self.eqs = [Equity(t) for t in tickers]
        self.params = {'length': data_lookback_period, 'lower_threshold': label_lower_threshold, 'upper_threshold':label_upper_threshold, 'period': label_period, 'cnn_split': cnn_split, 'data_splits': data_splits}
        self.voter = Voter(voting_type)
        if models is None:
            self.models = [ModelCollection(t, type, features, self.params, model_params = model_params) for t in tickers]
            
            if verbose:
                print("Initializing Models")
            self.initialize_models(verbose)
        else:
            self.models = models

    def initialize_models(self, verbose=False):
        """Trains the model collections
        """
        for model in self.models:
            model.train_models(verbose)

    def plot_models_rocs(self, tickers = [], verbose=False):
        for model in self.models:
            if len(tickers) == 0 or model.eq.ticker in tickers:
                model.plot_rocs(verbose)
            
    def plot_model_cm(self, ticker, verbose=False):
        for model in self.models:
            if model.ticker==ticker:
                cm = model.get_conf_matricies(verbose)

        return cm
    
    def generate_conf_matricies(self, start_date, end_date, verbose=False):
        next_day = datetime.timedelta(days = 1)
        date = start_date
        cms = []
        for eq in self.eqs:
            cm = ConfusionMatrix()
            cms.append(cm)
        while date <= end_date:
            predictions = self.predict(date, self.test_mode, verbose)
            truths = self.get_labels(date)
            for i,eq in enumerate(self.eqs):
                pred = predictions[i][0]
                truth = truths[i]
                cms[i].add_value(truth,pred)
            date += next_day
        for cm in cms:
            cm.print_matrix()

    def get_labels(self, date):
        index = self.eqs[0].get_index_from_date(date)

        index = index + self.params['length']
        preds = []

        for eq in self.eqs:
            preds.append(feature_generation.get_label(eq, self.params['period'],self.params['upper_threshold'], self.type, index))
        
        return preds


    def predict(self, date, test_mode=False, verbose=False):
        """ Generate a prediction for each equity for this algorithm
        
        Arguments:
            date {datetime} -- date to make the prediction on
        
        Returns:
            dictionary -- key - ticker, value - tuple of prediction (0 or 1) and model accuracy
        """
        
        predictions = []
        for i, eq in enumerate(self.eqs):
            pred = self.voter.predict(self.models[i], date, test_mode,verbose)
            # print("Prediction for ", eq.ticker, " - ", pred)
            predictions.append(pred)
        
        return predictions
 
    def getPeriod(self):
        return self.params['period']

    def getUpperThreshold(self):
        return self.params['upper_threshold']

    def getLowerThreshold(self):
        return self.params['lower_threshold']

    def update(self, date):
        # Retrain the model overtime
        return 0

    def grid_search(self, tickers = [], verbose = False):
        for model in self.models:
            if len(tickers) == 0 or model.eq.ticker in tickers:
                model.grid_search_coll(verbose)
            
    def save(self):
        id = createTradingAlgorithm(self)
        return id

