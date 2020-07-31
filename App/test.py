from App.utils import *
import numpy as np
from pandas import *
import matplotlib.pyplot as plt
from MachineLearningAlgorithm.Bayes.NaiveBayes import *
from MachineLearningAlgorithm.Bayes.TextAnalyzer import *
from MachineLearningAlgorithm.Bayes.WordStatistic import *

if __name__ == '__main__' :

    bayes = NaiveBayesClassifier()

    data = read_csv("../MachineLearningAlgorithm/Bayes/spam_ham_dataset.csv")

    x, y = DataFrame2NPArray(data, "label")

    ssler = TextAnalyzer()

    ssler.fit(data, "text")

    x = ssler.transform(data, "text")

    bayes.fit(x, y)

    bayes.visualize(ssler)