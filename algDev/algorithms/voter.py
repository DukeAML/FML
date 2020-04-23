from sklearn import svm
from algDev.algorithms.svm import SVM
from algDev.models.equity import Equity

class Voter:
    """Voting algorithm class
    
    Returns:
        Voter -- Object for running votes
    """
    
    def __init__(self, voting_type):
        """initialize voter
        
        Arguments:
            voting_type {string} -- the voting mechanism to use (see docs)
        """
        super().__init__()
        self.valid_voting_types = [
        'accuracy'
        ]
        assert voting_type in self.valid_voting_types
        self.voting_type = voting_type
        
    def predict(self, model_collection, date, verbose=False):
        """make a prediction of the data for a given model_collection
        
        Arguments:
            model_collection {ModelCollection} -- Object to predict with
            date {datetime} -- set of data to make predict of
        
        Returns:
            (int, float) -- predicted class and models accuracy in tuple
        """
        if verbose:
            print(date)
        #get predictions, metrics
        model_predictions = model_collection.predict(date, verbose)
        model_collection.get_voter_metrics()
        
        if verbose:
            print("Model Predictions: ", model_predictions)
        
        predictions = {}
        for i,model in enumerate(model_collection.models):
            predictions[model.title] = (model_predictions[i], model.metrics['acc'],model.metrics['balance'],model.metrics['False Positive Rate'])
        
        if verbose:
            print("Updated Predictions in Voter", predictions)
        
        
        if self.voting_type == "accuracy":

            sum_voting = 0
            for pred in predictions.items():
                pred = pred[1]
                sum_voting += pred[0]*pred[1]
                sum_voting += pred[0]*pred[1]
            sum_voting = sum_voting/len(predictions)
            if sum_voting > 0.4:
                prediction = 1
            else:
                prediction = 0

        elif self.voting_type == 'Penrose':

            ####

        else:
            prediction = 'you have not selected a valid voting method'
        
        if verbose:
            print("Voting Output ", prediction, " for model with accuracy ", model_collection.accuracy)
        
        return (prediction, model_collection.accuracy)
