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
#this is the file for running all versions of svm-model based voting algorithms

#20-50 svm models 
#features: combo (small bucket) of indicator, maybe only one 
#binary category is either: postive, negative, or window

class SVM:
    """Class representing the SVM models
    
    Returns:
        SVM -- SVM with model and data
    """
    def __init__(self, X=None, y=None, C=1, gamma="auto", title='default',model = None, metrics = {}, ):
        """Initialize SVM
        
        Arguments:
            X {ndarray} -- input data
            y {ndarray} -- labels
        
        Keyword Arguments:
            C {int} -- error penalty (default: {1})
            gamma {str} -- kernal parameter (default: {'auto'})
            title {str} -- name of model (default: {'default'})
        """
        if model:
            self.model = model
        else:
            self.model = svm.SVC(C=C, gamma=gamma, probability=True)
        self.data = {'features':X, 'labels':y}
        self.title = title
        
        self.metrics = metrics

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
    
    


    def generate_hyperparam_viz(self, verbose = False):

        # https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
        # see link for details 

        #for Below hyper param visualization 

        # Utility function to move the midpoint of a colormap to be around
        # the values of interest.
        
        class MidpointNormalize(Normalize):

            def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
                self.midpoint = midpoint
                Normalize.__init__(self, vmin, vmax, clip)

            def __call__(self, value, clip=None):
                x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
                return np.ma.masked_array(np.interp(value, x, y))
            
        #DATA
        X = self.data['features']
        y = self.data['labels']

        #grid search for values of C, gamma
        C_range = np.logspace(-2, 10, 13)
        gamma_range = np.logspace(-9, 3, 13)
        param_grid = dict(gamma=gamma_range, C=C_range)
        cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
        grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
        grid.fit(X, y)

        if verbose == True:
            print("The best parameters are %s with a score of %0.2f"
                % (grid.best_params_, grid.best_score_))

        # Now we need to fit a classifier for all parameters in the 2d version
        # (we use a smaller set of parameters here because it takes a while to train)

        C_2d_range = [1e-2, 1, 1e2]
        gamma_2d_range = [1e-1, 1, 1e1]

        if verbose == True:
            print("C_2d_range = [1e-2, 1, 1e2]")
            print("gamma_2d_range = [1e-1, 1, 1e1]")

        classifiers = []
        for C in C_2d_range:
            for gamma in gamma_2d_range:
                clf = SVC(C=C, gamma=gamma)
                clf.fit(X, y)
                classifiers.append((C, gamma, clf))
        
        #visualize impact of gamma, C
        plt.figure(figsize=(8, 6))
        xx, yy = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
        for (k, (C, gamma, clf)) in enumerate(classifiers):
            # evaluate decision function in a grid
            Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
            Z = Z.reshape(xx.shape)

            # visualize decision function for these parameters
            plt.subplot(len(C_2d_range), len(gamma_2d_range), k + 1)
            plt.title("gamma=10^%d, C=10^%d" % (np.log10(gamma), np.log10(C)),
                    size='medium')

            # visualize parameter's effect on decision function
            plt.pcolormesh(xx, yy, -Z, cmap=plt.cm.RdBu)
            plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdBu_r,
                        edgecolors='k')
            plt.xticks(())
            plt.yticks(())
            plt.axis('tight')

        scores = grid.cv_results_['mean_test_score'].reshape(len(C_range),  
                                                            len(gamma_range))
        # Draw heatmap of the validation accuracy as a function of gamma and C
        #
        # The score are encoded as colors with the hot colormap which varies from dark
        # red to bright yellow. As the most interesting scores are all located in the
        # 0.92 to 0.97 range we use a custom normalizer to set the mid-point to 0.92 so
        # as to make it easier to visualize the small variations of score values in the
        # interesting range while not brutally collapsing all the low score values to
        # the same color.

        plt.figure(figsize=(8, 6))
        plt.subplots_adjust(left=.2, right=0.95, bottom=0.15, top=0.95)
        plt.imshow(scores, interpolation='nearest', cmap=plt.cm.hot,
                norm=MidpointNormalize(vmin=0.2, midpoint=0.92))
        plt.xlabel('gamma')
        plt.ylabel('C')
        plt.colorbar()
        plt.xticks(np.arange(len(gamma_range)), gamma_range, rotation=45)
        plt.yticks(np.arange(len(C_range)), C_range)
        plt.title('Validation accuracy')
        plt.show()
