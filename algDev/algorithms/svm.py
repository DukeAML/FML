from sklearn import svm
from scipy import interp
from algDev.preprocessing.data_generator import split_data
from algDev.models.confusion_matrix import ConfusionMatrix
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import auc
from sklearn.metrics import plot_roc_curve
from sklearn.model_selection import StratifiedKFold

from matplotlib.colors import Normalize
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV


class SVM:
    """Class representing the SVM models
    
    Returns:
        SVM -- SVM with model and data
    """
    def __init__(self, X=None, y=None, params = None, title='default',model = None, metrics = {}, ):
        """Initialize SVM
        
        Arguments:
            X {ndarray} -- input data
            y {ndarray} -- labels
        
        Keyword Arguments:
            params {dict} -- dictionary of model parameters below, if None default values are used
                gamma {int/str} -- kernal parameter , str options: 'auto', 'scale', (default: {'auto'} = 1 / n_features)
                C {int} -- penalty factor (default)
            title {str} -- name of model (default: {'default'})
            model {svm object} -- option to use pretrained svm
            metrics {dictionary} -- set saved metrics for pretrained models
            
        """
        if not bool(params) == True:
            gamma = 'auto'
            C = 1
        else:
            gamma = params['gamma']
            C = params['C']

        if model:
            self.model = model
        else:
            self.model = svm.SVC(C=C, gamma=gamma, probability=True)
        
        self.data = {'features':X, 'labels':y}
        self.title = title
        
        self.metrics = metrics

    def build_conf_matrix(self, splits, X=None, y=None, verbose=False):
        ''' build confusion matrix for svm model
            prints the matrix, returns the command for writing cm to file 
        '''
        if not X or not y:
            X = self.data['features']
            y = self.data['labels']

        X_train, y_train, X_test, y_test = split_data(X, y, splits)

        ## Want to step through the X_test and match up with y_test manually

        cm = ConfusionMatrix()

        for i,X_i in enumerate(X_test):
            pred = self.predict(X_i.reshape(1, -1))
            true = int(y_test[i])
            pred = int(pred)
            cm.add_value(true, pred)

        matrix = cm.print_matrix()

        return matrix

    def voter_metrics(self, splits, X=None, y=None, verbose=False):
        ''' 
        '''
        if not X or not y:
            X = self.data['features']
            y = self.data['labels']

        X_train, y_train, X_test, y_test = split_data(X, y, splits)

        true_neg =0
        false_neg =0
        true_pos =0
        false_pos =0
        for i,X_i in enumerate(X_test):
            pred = self.predict(X_i.reshape(1, -1))
            true = int(y_test[i])
            pred = int(pred)

            if true == 0 and pred == 0:
                true_neg += 1
            elif true == 0 and pred == 1:
                false_pos += 1
            elif true == 1 and pred == 0:
                false_neg += 1
            elif true == 1 and pred == 1:
                true_pos += 1

        false_posR = false_pos/ (true_neg + false_pos)
        balance = (false_neg + true_pos)/(true_neg + false_pos)
        pop = false_neg + true_pos +true_neg + false_pos
        self.metrics['balance'] = balance
        self.metrics['False Positive Rate'] = false_posR
        self.metrics['pop'] = pop

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
        
        if verbose:
            print("Feature Shape for SVM ", self.title)
            print(X_train.shape)
            print("Label Shape for SVM ", self.title)
            print(y_train.shape)

        self.model.fit(X_train, y_train)
        if len(X_test) <= 0:
            return
        self.test(X_test, y_test, verbose)

    def test(self, X, y, verbose = False):
        """Run a test on a set of data
        
        Arguments:
            X {ndarray} -- input data
            y {ndarray} -- labels
        """
        acc = self.model.score(X, y)
        if verbose:
            print("Accuracy for SVM ", self.title, " - ", acc)
        self.metrics['acc'] = acc
        

    def plot_roc(self, verbose=False):
        """ Plot ROC Curve for model
        """
        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)
        cv = StratifiedKFold(n_splits=6)

        fig, ax = plt.subplots()
        for i, (train, test) in enumerate(cv.split(self.data['features'], self.data['labels'])):
            self.model.fit(self.data['features'][train], self.data['labels'][train])
            viz = plot_roc_curve(self.model, self.data['features'][test], self.data['labels'][test],
                                 name='ROC fold {}'.format(i),
                                 alpha=0.3, lw=1, ax=ax)
            interp_tpr = interp(mean_fpr, viz.fpr, viz.tpr)
            interp_tpr[0] = 0.0
            tprs.append(interp_tpr)
            aucs.append(viz.roc_auc)

        ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
                label='Chance', alpha=.8)

        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)
        ax.plot(mean_fpr, mean_tpr, color='b',
            label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
            lw=2, alpha=.8)

        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
        ax.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                        label=r'$\pm$ 1 std. dev.')

        ax.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],
               title="Receiver operating characteristic example")
        ax.legend(loc="lower right")
        plt.show()

    def predict(self, Xi):
        """make a prediction of a data point
        
        Arguments:
            Xi {ndarray} -- data point to predict output of
        
        Returns:
            float -- predicted class of input
        """
        
        pred = self.model.predict(Xi)
        # print("Prediction for model ", self.title, " - ", pred, ' accuracy: ', self.metrics['acc'])
        return pred[0]


    def grid_search_model(self, verbose = False):
        """ Perform grid search to find optimal gamma, C for model
        """
        #DATA
        X = self.data['features']
        y = self.data['labels']

        #grid search for values of C, gamma

        #ideally run below 
        # C_range = np.logspace(-2, 10, 13)
        # gamma_range = np.logspace(-9, 3, 13)

        #w/o gpu run within smaller space
        C_range = np.logspace(9, 10,4)
        gamma_range = np.logspace(0, 2, 2)
        param_grid = dict(gamma=gamma_range, C=C_range)
        cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
        grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
        grid.fit(X, y)

        if verbose == True:
            print("The best parameters are %s with a score of %0.2f"
                % (grid.best_params_, grid.best_score_))
        
        return (grid.best_params_, grid.best_score_)
    

