# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 23:50:34 2020

@author: Giyn
"""

import numpy as np
import matplotlib.pyplot as plt
from ML.model_selection import train_test_split
from ML.LogisticRegression import LogisticRegression
from sklearn import datasets


iris = datasets.load_iris() # 引入鸢尾花数据集

X = iris.data
y = iris.target

X = X[y<2, :2] # 只取前两个特征
y = y[y<2] # 二分类

X_train, X_test, y_train, y_test = train_test_split(X, y, seed=412) # 数据集分割
log_reg = LogisticRegression() # 实例化逻辑回归模型
log_reg.fit(X_train, y_train) # 训练模型

def decision_boundary(x):
    """
    逻辑回归模型的决策边界
    Parameters
    ----------
    x : ndarray
        决策边界的横坐标散点数组
    Returns
    -------
    float
        决策边界的纵坐标
    """
    return (-log_reg.coef_[0] * x - log_reg.intercept_) / log_reg.coef_[1]

x_plot = np.linspace(4, 7.5, num=1000) # 在指定的间隔内返回均匀间隔的数字
y_plot = decision_boundary(x_plot)

# 结果可视化
plt.rcParams['axes.facecolor'] = 'ivory' # 添加背景色
plt.title("iris-Dataset") # 添加标题
plt.xlabel('SepalLength') # 添加横坐标标签
plt.ylabel('SepalWidth') # 添加纵坐标标签
plt.scatter(X[y==0,0], X[y==0,1], color='g') # 0分类的散点图
plt.scatter(X[y==1,0], X[y==1,1], color='b') # 1分类的散点图
plt.plot(x_plot, y_plot, color='red')
plt.savefig("./Pictures/result.png")