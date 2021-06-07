import base64
from base64 import *
from io import BytesIO

import cvxopt
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize


# 核函数选择
def linear_kernel(**kwargs):  # 线性核函数
    def f(x1, x2):
        return np.inner(x1, x2)

    return f


def rbf_kernel(gamma, **kwargs):  # 高斯核函数
    def f(x1, x2):
        dist = np.linalg.norm(x1 - x2) ** 2
        return np.exp(-gamma * dist)

    return f


def polynomial_kernel(power, coef, **kwargs):  # 多项式核函数
    def f(x1, x2):
        return (np.inner(x1, x2) + coef) ** power

    return f


class SVM:
    def __init__(self, C=1., kernel=rbf_kernel, power=4, gamma=None, coef=4):
        """
        :param C: 惩罚参数
        :param kernel: 核函数
        :param power: 多项式核函数最高次项
        :param gamma: 核函数参数
        :param coef: 多项式核函数参数
        """
        self.C = C
        self.kernel_spawner = kernel
        self.kernel = None
        self.power = power
        self.gamma = gamma
        self.coef = coef
        self.lagr_multipliers = None
        self.support_vectors = None
        self.support_vectors_labels = None
        self.intercept = None

    def fit(self, X, y):
        """
        :param X: 连续数据
        :param y: 二分类 传入只有1和0的
        :return:
        """
        y[y == 0] = -1
        m, n = np.shape(X)
        if not self.gamma:
            self.gamma = 1 / n  # 若为空，设默认值
        self.kernel = self.kernel_spawner(  # 初始化核函数
            power=self.power,
            gamma=self.gamma,
            coef=self.coef
        )
        kernel_matrix = np.zeros((m, m))  # 计算样本点之间结果，结果存在矩阵中
        for i in range(m):
            for j in range(m):
                kernel_matrix[i, j] = self.kernel(X[i], X[j])
        # 处理凸优化问题
        P = cvxopt.matrix(np.outer(y, y) * kernel_matrix, tc='d')
        q = cvxopt.matrix(np.ones(m) * -1)
        A = cvxopt.matrix(y, (1, m), tc='d')
        b = cvxopt.matrix(0, tc='d')

        if not self.C:
            G = cvxopt.matrix(np.identity(m) * -1)
            h = cvxopt.matrix(np.zeros(m))
        else:
            G_max = np.identity(m) * -1
            G_min = np.identity(m)
            G = cvxopt.matrix(np.vstack((G_max, G_min)))
            h_max = cvxopt.matrix(np.zeros(m))
            h_min = cvxopt.matrix(np.ones(m) * self.C)
            h = cvxopt.matrix(np.vstack((h_max, h_min)))
        # 使用cvxopt库解决凸优化问题
        minimization = cvxopt.solvers.qp(P, q, G, h, A, b)
        lagr_mult = np.ravel(minimization['x'])  # 拉格朗日乘子
        idx = lagr_mult > 1e-7  # 获取非0拉格朗日乘子的索引
        self.lagr_multipliers = lagr_mult[idx]  # 获取符合的拉格朗日乘子
        self.support_vectors = X[idx]  # 获取支持向量
        self.support_vectors_labels = y[idx]  # 获取对应标签
        self.intercept = self.support_vectors_labels[0]  # 计算wx+b中的b
        for i in range(len(self.lagr_multipliers)):
            self.intercept -= self.lagr_multipliers[i] * self.support_vectors_labels[i] * \
                              self.kernel(self.support_vectors[i], self.support_vectors[0])
        y[y == -1] = 0

    def visualize(self):
        res = []

        paths = ["MachineLearningAlgorithm/SupportVectorMachine/Pictures/dimension1.png",
                 "MachineLearningAlgorithm/SupportVectorMachine/Pictures/dimension2.png",
                 "MachineLearningAlgorithm/SupportVectorMachine/Pictures/dimension3.png",
                 "MachineLearningAlgorithm/SupportVectorMachine/Pictures/show.png"]

        for pa in paths:
            with open(pa, 'rb') as f:
                data = base64.b64encode(f.read())

            res.append(str(data))

        return res

    def predict(self, X_text):
        y_predict = []
        for sample in X_text:
            prediction = 0
            for i in range(len(self.lagr_multipliers)):
                prediction += self.lagr_multipliers[i] * self.support_vectors_labels[i] * \
                              self.kernel(self.support_vectors[i], sample)
            prediction += self.intercept
            y_predict.append(np.sign(prediction))  # 大于0返回1，小于0返回-1
        y_predict = np.array(y_predict, dtype=np.int8)
        y_predict[y_predict == -1] = 0
        return y_predict


def plot_picture(clf, data, target, dimension=(0, 1)):
    # 画图函数
    x_min, x_max = data[:, dimension[0]].min() - 0.02, data[:, dimension[0]].max() + 0.02
    y_min, y_max = data[:, dimension[1]].min() - 0.02, data[:, dimension[1]].max() + 0.02
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))

    data = data[:, dimension[0]:dimension[1] + 1]
    clf.fit(data, target)
    z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)
    plt.contourf(xx, yy, z, cmap=plt.cm.ocean, alpha=0.6)
    # plt.scatter(data[:6, 0], data[:6, 1], marker='o', color='r', s=100, lw=3)
    plt.scatter(data[target == 0][:, 0], data[target == 0][:, 1], marker='o', color='r', s=100,
                lw=3)
    # plt.scatter(data[6:, 0], data[6:, 1], marker='x', color='k', s=100, lw=3)
    plt.scatter(data[target == 1][:, 0], data[target == 1][:, 1], marker='x', color='k', s=100,
                lw=3)
    gamma = clf.gamma
    plt.title('SVM with $\gamma=$' + str(gamma))

    save_file = BytesIO()

    plt.savefig(save_file, format='png')

    b64 = b64encode(save_file.getvalue()).decode('utf8')

    return str(b64)
