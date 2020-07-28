from MachineLearningAlgorithm.LogisticRegression.ML.LogisticRegression import *
from sklearn.preprocessing import StandardScaler

def LogisticRegressionTraining(x, y) :

    model = LogisticRegression()

    ssler = StandardScaler()

    ssler.fit(x)

    x = ssler.transform(x)

    print(x)

    print(y)

    model.fit(x, y)

    print(model.score(x, y))

    return model, ssler

