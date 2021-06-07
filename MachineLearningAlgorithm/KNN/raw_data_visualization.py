import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import andrews_curves
from pandas.plotting import parallel_coordinates
from pandas.plotting import radviz

data = pd.read_csv('tree.csv')

# get the row index
index = data.index.values

# get the value of data
value = data.values

# get the col index
keys = data.keys().values

y_train = value[:, -1]
X_train = value[:, :-1]

y_test = value[:2, -1]
X_test = value[:2, :-1]

X = X_train[:, :2]  # 只取前两个特征
y = y_train  # 二分类

# 原始数据可视化（散点图）
plt.rcParams['axes.facecolor'] = 'ivory'  # 添加背景色
plt.title("tree-Dataset")  # 添加标题
plt.xlabel('leaf length')  # 添加横坐标标签
plt.ylabel('leaf width')  # 添加纵坐标标签
plt.scatter(X[y == 'poplar', 0], X[y == 'poplar', 1], color='lime')
plt.scatter(X[y == 'pear', 0], X[y == 'pear', 1], color='b')
plt.scatter(X[y == 'ginkgo', 0], X[y == 'ginkgo', 1], color='r')
plt.savefig("./Pictures/raw_scatter.png")  # 保存原始数据分布图

# 原始数据可视化（平行坐标）
data = pd.read_csv("tree.csv")
plt.figure('多维度-parallel_coordinates')
plt.title('parallel_coordinates')
parallel_coordinates(data, 'Class', color=['b', 'g', 'r'])
plt.savefig("./Pictures/raw_parallel_coordinates.png")  # 保存原始数据分布图

# 原始数据可视化（RadViz雷达图）
plt.figure('多维度-radviz')
plt.title('radviz')
radviz(data, 'Class', color=['red', 'm', 'g'])
plt.savefig("./Pictures/raw_radviz.png")  # 保存原始数据分布图

# 原始数据可视化（andrews_curves）
plt.figure('多维度-andrews_curves')
plt.title('andrews_curves')
andrews_curves(data, 'Class', color=['y', 'r', 'c'])
plt.savefig("./Pictures/raw_andrews_curves.png")  # 保存原始数据分布图

plt.figure('热力图-heatmap')
corr = data.corr()
sns.heatmap(corr, annot=True)
plt.savefig("./Pictures/raw_heatmap.png")
