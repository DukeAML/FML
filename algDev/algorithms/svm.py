from sklearn import svm
from preprocessing.data_generator import split_data
#this is the file for running all versions of svm-model based voting algorithms

#20-50 svm models 
#features: combo (small bucket) of indicator, maybe only one 
#binary category is either: postive, negative, or window

class SVM:

    def __init__(self, C=1, gamma='auto'):
        self.model = svm.SVC(C=C, gamma=gamma)
        self.metrics = {}

    def train(self, X, y, splits, verbose=False):
        
        X_train, y_train, X_test, y_test = split_data(X, y, splits)
        
        self.model.fit(X_train, y_train)

        acc = self.model.score(X_test, y_test)
        
        self.metrics['acc'] = acc
