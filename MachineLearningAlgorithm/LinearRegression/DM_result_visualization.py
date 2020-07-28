# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 23:50:34 2020

@author: Giyn
"""

import matplotlib.pyplot as plt
import pandas as pd
from ML.model_selection import train_test_split
from ML.LinearRegression import LinearRegression


data = pd.read_csv("housing.csv") # 读取数据
x_1 = data.values[:,[0]].flatten() # 特征1
x_2 = data.values[:,[1]].flatten() # 特征2
y = data.values[:,[2]].flatten() # 输出变量
x_1 = x_1[y < 50.0] # 剔除超过50的点（因为有可能有超过50的，但是在图中只显示50）
x_2 = x_2[y < 50.0]
y = y[y < 50.0]

# 分割数据集
x_1_train, x_1_test, y_train, y_test = train_test_split(x_1, y, seed=412)
x_2_train, x_2_test, y_train, y_test = train_test_split(x_2, y, seed=412)

# 实例化线性回归模型
reg_1 = LinearRegression()
reg_2 = LinearRegression()
# 线性回归模型训练
reg_1.fit(x_1_train, y_train)
reg_2.fit(x_2_train, y_train)

# 特征1
plt.rcParams['axes.facecolor'] = 'ivory' # 添加背景颜色
plt.title('housing') # 添加标题
plt.xlabel('RM') # 添加横坐标标签
plt.ylabel('MEDV') # 添加纵坐标标签
plt.scatter(x_1_train, y_train, color='r') # 画散点图
plt.plot(x_1_train, reg_1.predict(x_1_train), color='b') # 回归直线
plt.savefig("./Pictures/result_1.png") # 保存图片
plt.cla() # 清除图片

# 特征2
plt.rcParams['axes.facecolor'] = 'lavender' # 添加背景颜色
plt.title('housing') # 添加标题
plt.xlabel('LSTAT') # 添加横坐标标签
plt.ylabel('MEDV') # 添加纵坐标标签
plt.scatter(x_2_train, y_train, color='deeppink') # 画散点图
plt.plot(x_2_train, reg_2.predict(x_2_train), color='navy') # 回归直线
plt.savefig("./Pictures/result_2.png") # 保存图片