from MachineLearningAlgorithm.LogisticRegression.ML.LogisticRegression import *
from MachineLearningAlgorithm.LinearRegression.ML.LinearRegression import *
from MachineLearningAlgorithm.SupportVectorMachine.SupportVectorMachine import *
from MachineLearningAlgorithm.ClassificationAndRegressionTree.CART import *
from MachineLearningAlgorithm.Bayes.NaiveBayes import *
from MachineLearningAlgorithm.KNN.KNN import *
from sklearn.preprocessing import StandardScaler
from MachineLearningAlgorithm.Bayes.TextAnalyzer import *

def LogisticRegressionTraining(x, y) :

    model = LogisticRegression()

    ssler = StandardScaler()

    ssler.fit(x)

    x = ssler.transform(x)

    model.fit(x, y)

    print(model.score(x, y))

    return model, ssler

def LinearRegressionTraining(x, y) :

    model = LinearRegression()

    ssler = StandardScaler()

    ssler.fit(x)

    x = ssler.transform(x)

    x = x.reshape(len(x))

    model.fit(x, y)

    print(model.score(x, y))

    return model, ssler

def SVMTraining(x, y) :

    model = SVM()

    ssler = StandardScaler()

    ssler.fit(x)

    x = ssler.transform(x)

    model.fit(x, y)

    print((model.predict(x) == y).sum() / len(y))

    return model, ssler

def CART_REGTraining(x, y) :

    model = DecisionTree_CART(tree_type='reg')

    ssler = StandardScaler()

    ssler.fit(x)

    x = ssler.transform(x)

    model.fit(x, y)

    print((model.predict(x) == y).sum() / len(y))

    return model, ssler

def KNNTraining(x, y) :

    ssler = StandardScaler()

    ssler.fit(x)

    x = ssler.transform(x)

    model = KNN(x, y)

    print(model.fit(x, y))

    return model, ssler

def NBayesTraining(x, y, textColumns) :

    model = NaiveBayesClassifier()

    ssler = TextAnalyzer()

    ssler.fit(x, textColumns)

    x = ssler.transform(x, textColumns)

    model.fit(x, y)

    print((model.predict(x) == y).sum() / len(y))

    return model, ssler

