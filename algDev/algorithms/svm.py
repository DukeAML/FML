from sklearn import svm
from scipy import interp
from algDev.preprocessing.data_generator import split_data
from algDev.models.confusion_matrix import ConfusionMatrix
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import auc
from sklearn.metrics import plot_roc_curve
from sklearn.model_selection import StratifiedKFold
#this is the file for running all versions of svm-model based voting algorithms

#20-50 svm models 
#features: combo (small bucket) of indicator, maybe only one 
#binary category is either: postive, negative, or window

class SVM:
    """Class representing the SVM models
    
    Returns:
        SVM -- SVM with model and data
    """
    def __init__(self, X, y, C=1, gamma="auto", title='default'):
        """Initialize SVM
        
        Arguments:
            X {ndarray} -- input data
            y {ndarray} -- labels
        
        Keyword Arguments:
            C {int} -- error penalty (default: {1})
            gamma {str} -- kernal parameter (default: {'auto'})
            title {str} -- name of model (default: {'default'})
        """
        self.model = svm.SVC(C=C, gamma=gamma, probability=True)
        self.data = {'features':X, 'labels':y}
        self.title = title
        self.metrics = {}

    def build_conf_matrix(self, splits, X=None, y=None, verbose=False):
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

        cm.print_matrix()

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
        
        return pred[0]
