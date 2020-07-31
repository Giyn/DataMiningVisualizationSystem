# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:04:40 2020

@author: 许继元
"""

import numpy as np
from .metrics import r2_score # 一个点表示当前目录


class LinearRegression(object):
    """使用向量化实现线性回归"""
    def __init__(self):
        """在过程中计算出来的变量统一命令,后缀加上_"""
        self.a_ = None  # 表示线性的斜率
        self.b_ = None  # 表示线


    def fit(self, X_train, y_train):
        """
        训练模型
        :param X_train:
        :return:
        """
        assert X_train.ndim == 1 and y_train.ndim == 1, 'X和Y必须为1维'
        assert len(X_train) == len(y_train), 'X和Y的训练个数不相同'
        x_mean = np.mean(X_train)
        y_mean = np.mean(y_train)
        self.a_ = (X_train - x_mean).dot(y_train - y_mean) / (X_train - x_mean).dot(X_train - x_mean)
        self.b_ = y_mean - self.a_ * x_mean


    def _predict(self, x):
        """
        预测单个X的结果 线性方程y = a*x + b
        :param x:
        :return:
        """
        return self.a_ * x + self.b_


    def predict(self, X_test):
        """
        预测X，X是一维的数据
        :param X_test:
        :return:
        """
        assert X_test.ndim == 1, 'X_test必须是一维数组'
        assert self.a_ is not None and self.b_ is not None , '在predict之前请先fit'

        y_pridect = [self._predict(x) for x in X_test]
        return np.array(y_pridect)
    
    
    def score(self, x_test, y_test):
        """给定单个待预测数据x_single, 返回x_single的预测结果值"""
        y_predict = self.predict(x_test)
        return r2_score(y_test, y_predict)


    def __repr__(self):
        return 'LinearRegression(a=%s, b=%s)' %(self.a_, self.b_)