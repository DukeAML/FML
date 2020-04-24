from sklearn import svm
from algDev.algorithms.svm import SVM
from algDev.models.equity import Equity
import math

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
        'accuracy', 'Penrose'
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
            predictions[model.title] = (model_predictions[i], model.metrics['acc'], model.metrics['balance'], model.metrics['False Positive Rate'])
        
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
            total_votes =0
            votes_toPass= 0
            votes_toReject =0
            for title, metrics in predictions.items():
                pred = metrics[0]
                acc = metrics[1] 
                balance = metrics[2] 
                FPR = metrics[3] 

                if pred ==0 :
                    vote_to = 'reject'
                else:
                    vote_to = 'Pass'

                multiplier = (acc)* math.sqrt(balance*FPR)
                votes = int(multiplier)
                print("votes")
                print(votes)
        

                if vote_to == 'reject':
                    votes_toReject += votes
                elif vote_to == 'Pass':
                    votes_toPass += votes
                total_votes += votes

                if verbose:
                    print(title + ' casts %d votes to %s ' %(votes,vote_to))
            
            ratio = votes_toPass/total_votes
            if ratio > .5:
                prediction = 1
            else:
                prediction = 0

        else:
            prediction = 'you have not selected a valid voting method'
        
        if verbose:
            print("Voting Output ", prediction, " for model with accuracy ", model_collection.accuracy)
        
        return (prediction, model_collection.accuracy)
