import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
"""
@function:the gaussian function
@parameter: dis - the independent variable distance
@return: weight - the dependent variable weight
"""


def gaussian(dist, sigma=10.0):
    """ Input a distance and return it`s weight"""
    weight = np.exp(-dist ** 2 / (2 * sigma ** 2))
    return weight


"""
@function:realize the knn
@parameter:
@return:X_train - the train data
        X_test - the test data
        y_train - the train target
        y_test - the test target
@return:score - the right score

"""
class knn:
    def __init__(self,X_train,y_train):
        self.X_train = X_train
        self.y_train =y_train



    def fit(self,X_test, y_test):
        k = 11  # 超参数取11

        predict_true = 0  # the num of right predicted
        max = X_test.shape[0]  # the max num of iteration

        for i in range(max):
            x_p = X_test[i]
            y_p = y_test[i]

            distances = [np.sqrt(np.sum((x_p - x) ** 2)) for x in self.X_train]
            # calculate the distance between point in x_p and point in x
            d = np.sort(distances)
            # sort the distances
            nearest = np.argsort(distances)
            # the index of sorted data
            # print(nearest)

            topk_y = [self.y_train[j] for j in nearest[:k]]
            # select k nearest num

            classCount = {}
            for i in range(0, k):
                voteLabel = topk_y[i]
                weight = gaussian(distances[nearest[i]])
                # print(index, dist[index],weight)
                ## 这里不再是加一，而是权重*1
                classCount[voteLabel] = classCount.get(voteLabel, 0) + weight * 1

            maxCount = 0

            for key, value in classCount.items():
                if value > maxCount:
                    maxCount = value
                    classes = key
            # select the type of max num
            if (classes == y_p): predict_true += 1

            precision = float(predict_true / max)

        return precision

    """
    @function:predict the data
    @parameter:
    @return:X_train - the train data
            X_p - the data need to be predicted
            y_train - the train target

    @return:score - the right score

    """

    def predict(self, X_p):
        k = 11  # 超参数取11

        predict_true = 0  # the num of right predicted
        max = X_p.shape[0] # the max num of iteration
        y_p = []
        for i in range(max):
            x_p = X_p[i]

            distances = [np.sqrt(np.sum((x_p - x) ** 2)) for x in self.X_train]
            # calculate the distance between point in x_p and point in x
            d = np.sort(distances)
            # sort the distances
            nearest = np.argsort(distances)
            # the index of sorted data
            # print(nearest)

            topk_y = [self.y_train[j] for j in nearest[:k]]
            # select k nearest num

            for i in range(k):
                if topk_y[i] == 'pear':
                    color = 'b'
                elif topk_y[i] == 'poplar':
                    color = 'y'
                else:
                    color = 'g'
                plt.scatter(self.X_train[nearest[i], 0], self.X_train[nearest[i], 1], color=color)
            classCount = {}
            for i in range(0, k):
                voteLabel = topk_y[i]
                weight = gaussian(distances[nearest[i]])
                # print(index, dist[index],weight)
                ## 这里不再是加一，而是权重*1
                classCount[voteLabel] = classCount.get(voteLabel, 0) + weight * 1

            maxCount = 0

            for key, value in classCount.items():
                if value > maxCount:
                    maxCount = value
                    classes = key
            # select the type of max num
            y_p.append(classes)
            if topk_y[i] == 'pear':
                color = 'b'
            elif topk_y[i] == 'poplar':
                color = 'y'
            else:
                color = 'g'
            plt.scatter(x_p[0], x_p[1], color=color, s=100, edgecolors='r')
        plt.savefig("./Pictures/result.png")  # 保存原始数据分布图

        return y_p
