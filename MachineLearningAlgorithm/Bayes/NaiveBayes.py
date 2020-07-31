import numpy as np
import pandas as pd
from MachineLearningAlgorithm.Bayes.WordStatistic import *

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

    def visualize(self, ssler) :

        dicts = ssler.phrase_position

        res = []

        totall = np.zeros(shape = (len(dicts)))

        for i in self.ratio :

            totall += self.ratio[i]

        for i in self.ratio :

            temp = self.ratio[i] / totall

            top = np.argsort(-temp)[0:len(temp) // 10]

            word = {}

            for j in top:

                key = list(dicts.keys())[list(dicts.values()).index(j)]

                word[key] = self.ratio[i][dicts[key]]

            res.append(wordcloudSpawn(word))

        return res

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




