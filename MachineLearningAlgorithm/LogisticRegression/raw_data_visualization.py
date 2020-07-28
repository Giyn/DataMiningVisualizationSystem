# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 04:18:27 2020

@author: Giyn
"""

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import parallel_coordinates
from pandas.plotting import radviz
from pandas.plotting import andrews_curves
from sklearn import datasets


iris = datasets.load_iris() # 引入鸢尾花数据集

X = iris.data
y = iris.target

X = X[y<2, :2] # 只取前两个特征
y = y[y<2] # 二分类

# 原始数据可视化（散点图）
plt.rcParams['axes.facecolor'] = 'ivory' # 添加背景色
plt.title("iris-Dataset") # 添加标题
plt.xlabel('SepalLength') # 添加横坐标标签
plt.ylabel('SepalWidth') # 添加纵坐标标签
plt.scatter(X[y==0,0], X[y==0,1], color='g') # 0分类的散点图
plt.scatter(X[y==1,0], X[y==1,1], color='b') # 1分类的散点图
plt.savefig("./Pictures/raw_scatter.png") # 保存原始数据分布图

# 原始数据可视化（平行坐标）
data = pd.read_csv(r"iris.csv")
plt.figure('多维度-parallel_coordinates')
plt.title('parallel_coordinates')
parallel_coordinates(data, 'Class', color=['b', 'g'])
plt.savefig("./Pictures/raw_parallel_coordinates.png") # 保存原始数据分布图

# 原始数据可视化（RadViz雷达图）
plt.figure('多维度-radviz')
plt.title('radviz')
radviz(data, 'Class', color=['red', 'm'])
plt.savefig("./Pictures/raw_radviz.png") # 保存原始数据分布图

# 原始数据可视化（andrews_curves）
plt.figure('多维度-andrews_curves')
plt.title('andrews_curves')
andrews_curves(data, 'Class', color=['pink', 'gold'])
plt.savefig("./Pictures/raw_andrews_curves.png") # 保存原始数据分布图