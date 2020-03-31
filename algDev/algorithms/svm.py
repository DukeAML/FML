from sklearn import svm
from preprocessing.data_generator import split_data
#this is the file for running all versions of svm-model based voting algorithms

#20-50 svm models 
#features: combo (small bucket) of indicator, maybe only one 
#binary category is either: postive, negative, or window

class SVM:
    """Class representing the SVM models
    
    Returns:
        SVM -- SVM with model and data
    """
    def __init__(self, X, y, C=1, gamma='auto', title='default'):
        """Initialize SVM
        
        Arguments:
            X {ndarray} -- input data
            y {ndarray} -- labels
        
        Keyword Arguments:
            C {int} -- error penalty (default: {1})
            gamma {str} -- kernal parameter (default: {'auto'})
            title {str} -- name of model (default: {'default'})
        """
        self.model = svm.SVC(C=C, gamma=gamma)
        self.data = {'features':X, 'labels':y}
        self.title = title
        self.metrics = {}

    def train(self, splits, X=None, y=None, verbose=False):
        """train the svm
        
        Arguments:
            splits {float array} -- test train splits
        
        Keyword Arguments:
            X {ndarray} -- input data (default: {None})
            y {ndarray} -- labels (default: {None})
            verbose {bool} -- Print output (default: {False})
        """
        if not X or not y:
            X = self.data['features']
            y = self.data['labels']
        
        X_train, y_train, X_test, y_test = split_data(X, y, splits)
        print(X_train.shape)
        print(y_train.shape)
        self.model.fit(X_train, y_train)

        self.test(X_test, y_test)

    def test(self, X, y):
        """Run a test on a set of data
        
        Arguments:
            X {ndarray} -- input data
            y {ndarray} -- labels
        """
        acc = self.model.score(X, y)
        
        self.metrics['acc'] = acc

    def predict(self, Xi):
        """make a prediction of a data point
        
        Arguments:
            Xi {ndarray} -- data point to predict output of
        
        Returns:
            float -- predicted class of input
        """
        pred = self.model.predict(Xi)
        
        return pred
