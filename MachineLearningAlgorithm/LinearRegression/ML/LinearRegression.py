# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:04:40 2020

@author: 许继元
"""
import base64
import numpy.linalg as lg
import numpy as np
from .metrics import r2_score # 一个点表示当前目录


class LinearRegression(object):
    """使用向量化实现线性回归"""

    def __init__(self):

        self.weights = None



    def predict(self, data):

        self.weights = np.random.randn(data.shape[1] + 1, 1)

        data_t = np.ones((data.shape[0], data.shape[1] + 1))

        data_t[0:data.shape[0], 0:data.shape[1]] = data

        return np.array([i.sum() for i in (data_t * self.weights.transpose())])

    def fit(self, data, label):
        data_t = np.ones((data.shape[0], data.shape[1] + 1))

        data_t[0:data.shape[0], 0:data.shape[1]] = data

        self.weights = lg.inv(data_t.transpose().dot(data_t)).dot(data_t.transpose()).dot(label.transpose())
    
    
    def score(self, x_test, y_test):
        """给定单个待预测数据x_single, 返回x_single的预测结果值"""
        y_predict = self.predict(x_test)
        return r2_score(y_test, y_predict)

    def visualize(self, ssler, x, y) :

        res = []

        paths = ["MachineLearningAlgorithm/LinearRegression/Pictures/raw_1.png",
                "MachineLearningAlgorithm/LinearRegression/Pictures/raw_2.png",
                "MachineLearningAlgorithm/LinearRegression/Pictures/raw_3.png",
                "MachineLearningAlgorithm/LinearRegression/Pictures/raw_4.png",
                "MachineLearningAlgorithm/LinearRegression/Pictures/result_1.png",
                "MachineLearningAlgorithm/LinearRegression/Pictures/result_2.png",
                "MachineLearningAlgorithm/LinearRegression/Pictures/result_3.png",
                "MachineLearningAlgorithm/LinearRegression/Pictures/result_4.png"]

        for pa in paths :

            with open(pa, 'rb') as f:
                data = base64.b64encode(f.read())

            res.append(str(data))

        return res

    def __repr__(self):
        return 'LinearRegression(a=%s, b=%s)' %(self.a_, self.b_)