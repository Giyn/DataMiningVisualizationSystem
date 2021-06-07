# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 04:18:27 2020

@author: Giyn
"""

import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("housing.csv")  # 读取数据
x_1 = data.values[:, [0]].flatten()  # 特征1
x_2 = data.values[:, [1]].flatten()  # 特征2
x_3 = data.values[:, [2]].flatten()  # 特征3
x_4 = data.values[:, [3]].flatten()  # 特征4
y = data.values[:, [4]].flatten()  # 输出变量
x_1 = x_1[y < 50.0]  # 剔除超过50的点（因为有可能有超过50的，但是在图中只显示50）
x_2 = x_2[y < 50.0]
x_3 = x_3[y < 50.0]
x_4 = x_4[y < 50.0]
y = y[y < 50.0]

# 原始数据可视化（特征1）
plt.rcParams['axes.facecolor'] = 'ivory'  # 添加背景颜色
plt.title('housing')  # 添加标题
plt.xlabel('RM')  # 添加横坐标标签
plt.ylabel('MEDV')  # 添加纵坐标标签
plt.scatter(x_1, y, color='r')  # 画散点图
plt.savefig("./Pictures/raw_1.png")  # 保存图片
plt.cla()  # 清空图片

# 原始数据可视化（特征2）
plt.rcParams['axes.facecolor'] = 'lavender'  # 添加背景颜色
plt.title('housing')  # 添加标题
plt.xlabel('LSTAT')  # 添加横坐标标签
plt.ylabel('MEDV')  # 添加纵坐标标签
plt.scatter(x_2, y, color='deeppink')  # 画散点图
plt.savefig("./Pictures/raw_2.png")  # 保存图片
plt.cla()  # 清空图片

# 原始数据可视化（特征3）
plt.rcParams['axes.facecolor'] = 'aquamarine'  # 添加背景颜色
plt.title('housing')  # 添加标题
plt.xlabel('DIS')  # 添加横坐标标签
plt.ylabel('MEDV')  # 添加纵坐标标签
plt.scatter(x_3, y, color='deepskyblue')  # 画散点图
plt.savefig("./Pictures/raw_3.png")  # 保存图片
plt.cla()  # 清空图片

# 原始数据可视化（特征4）
plt.rcParams['axes.facecolor'] = 'lightsalmon'  # 添加背景颜色
plt.title('housing')  # 添加标题
plt.xlabel('AGE')  # 添加横坐标标签
plt.ylabel('MEDV')  # 添加纵坐标标签
plt.scatter(x_4, y, color='blueviolet')  # 画散点图
plt.savefig("./Pictures/raw_4.png")  # 保存图片
plt.cla()  # 清空图片
