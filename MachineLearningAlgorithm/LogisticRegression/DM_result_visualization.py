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

X_1 = X[y<2, :2] # 只取前两个特征
X_2 = X[y<2, 2:4]
y = y[y<2] # 二分类


X_1_train, X_1_test, y_train, y_test = train_test_split(X_1, y, seed=412) # 数据集分割
log_reg_1 = LogisticRegression() # 逻辑回归模型实例化
log_reg_1.fit(X_1_train, y_train) # 训练模型

X_2_train, X_2_test, y_train, y_test = train_test_split(X_2, y, seed=412) # 数据集分割
log_reg_2 = LogisticRegression() # 逻辑回归模型实例化
log_reg_2.fit(X_2_train, y_train) # 训练模型


def decision_boundary_1(x):
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
    return (-log_reg_1.coef_[0] * x - log_reg_1.intercept_) / log_reg_1.coef_[1]

def decision_boundary_2(x):
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
    return (-log_reg_2.coef_[0] * x - log_reg_2.intercept_) / log_reg_2.coef_[1]

x1_plot = np.linspace(4, 7.5, num=1000) # 在指定的间隔内返回均匀间隔的数字
x2_plot = np.linspace(1, 5, num=1000)
x_1_plot = decision_boundary_1(x1_plot)
x_2_plot = decision_boundary_2(x2_plot)

# 结果可视化
plt.rcParams['axes.facecolor'] = 'ivory' # 添加背景色
plt.title("iris-Dataset") # 添加标题
plt.xlabel('SepalLength') # 添加横坐标标签
plt.ylabel('SepalWidth') # 添加纵坐标标签
plt.scatter(X_1[y==0,0], X_1[y==0,1], color='green') # 0分类的散点图
plt.scatter(X_1[y==1,0], X_1[y==1,1], color='blue') # 1分类的散点图
plt.plot(x1_plot, x_1_plot, color='red') # 绘制决策边界
plt.savefig("./Pictures/result_1.png") # 保存图片
plt.cla()

# 结果可视化
plt.rcParams['axes.facecolor'] = 'ivory' # 添加背景色
plt.title("iris-Dataset") # 添加标题
plt.xlabel('PetalLength') # 添加横坐标标签
plt.ylabel('PetalWidth') # 添加纵坐标标签
plt.scatter(X_2[y==0,0], X_2[y==0,1], color='purple') # 0分类的散点图
plt.scatter(X_2[y==1,0], X_2[y==1,1], color='r') # 1分类的散点图
plt.plot(x2_plot, x_2_plot, color='red') # 绘制决策边界
plt.savefig("./Pictures/result_2.png") # 保存图片
plt.cla()