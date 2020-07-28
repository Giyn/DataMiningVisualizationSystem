from MachineLearningAlgorithm.LogisticRegression.ML.LogisticRegression import *

def LogisticRegressionTraining(x, y) :

    model = LogisticRegression()

    print(x)

    print(y)

    model.fit(x, y)

    print(model.score(x, y))

    return model

