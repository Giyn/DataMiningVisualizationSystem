import numpy as np
import pandas as pd

class NaiveBayesClassifier(object) :

    def __init__(self) :

        self.ratio = None

        self.labels= None



    def fit(self, x, y) :

        self.ratio, self.labels = NaiveBayesClassifier.caculate(x, y, 1.0)

    def predict(self, data) :

        res = []

        for x in data :

            temp = [0, -0x3f3f3f3f]

            for label in self.labels :

                pos = self.ratio[label] * x

                neg = (1 - self.ratio[label]) * (1 - x)

                score = np.log(pos + neg).sum()

                score += np.log(self.labels[label])

                if(score > temp[1]) : temp = [label, score]

            res.append(temp[0])

        return np.array(res)

    @staticmethod
    def caculate(features, labels, lam) : 

        label_uni = set(labels.tolist())

        feat_res = {}

        label_res = {}

        for label in label_uni :

            data = features[labels == label]

            count_p = (data.sum(axis = 0) + lam) / (data.shape[0] + 2 * lam)

            count_n = (data.shape[0] - data.sum(axis = 0) + lam) / (data.shape[0] + 2 * lam)

            feat_res[label] = count_p

            label_res[label] = len(data) / len(labels)

        return feat_res, label_res

            


