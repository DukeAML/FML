import numpy as np
import textwrap


class ConfusionMatrix():

    def __init__(self):
        self.true_positives = 0
        self.false_positives = 0
        self.true_negatives = 0
        self.false_negatives = 0


    def add_value(self, true, predicted):
        if true == 0 and predicted == 0:
            self.true_negatives += 1
        elif true == 0 and predicted == 1:
            self.false_positives += 1
        elif true == 1 and predicted == 0:
            self.false_negatives += 1
        elif true == 1 and predicted == 1:
            self.true_positives += 1

    def print_matrix(self):
        print("---------------------------------------")
        print("| Actual\Pred |  1   |   0   |  Total |")
        print("|-------------|------|-------|--------|")
        print("|     1       |  " + str(self.true_positives) +"  |  "+ str(self.false_negatives)+"  |  "+ str(self.true_positives+self.false_negatives) +"  |")
        print("|-------------|------|-------|--------|")
        print("|     0       |  " + str(self.false_positives) +"  |  "+ str(self.true_negatives)+"  |  "+ str(self.true_negatives+self.false_positives) +"  |")
        print("|-------------|------|-------|--------|")
        print("|   Total     |  " + str(self.true_positives + self.false_positives) +"  |  "+ str(self.false_negatives + self.true_negatives)+"  |  "+ str(self.true_positives+self.false_negatives + self.true_negatives+self.false_positives) +"  |")
        print("|-------------|------|-------|--------|")

        #return this long string for file writing purposes
        s = "---------------------------------------" + "| Actual\Pred |  1   |   0   | Total  |" + "|-------------|------|-------|--------|" + "|     1       | "+ str(self.true_positives) +" |  " + str(self.false_negatives)+"   |  "+ str(self.true_positives+self.false_negatives) + "   |" + "|-------------|------|-------|--------|" + "|     0       |  " + str(self.false_positives) +" |   "+ str(self.true_negatives)+"  |   "+ str(self.true_negatives+self.false_positives) +"   |" + "|-------------|------|-------|--------|" + "|   Total     |  " + str(self.true_positives + self.false_positives) +"  |  "+ str(self.false_negatives + self.true_negatives)+"  |  "+ str(self.true_positives+self.false_negatives + self.true_negatives+self.false_positives) +"  |" + "|-------------|------|-------|--------|"
        
        return textwrap.wrap(s, width=39)