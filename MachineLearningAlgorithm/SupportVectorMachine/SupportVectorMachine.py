import numpy as np
import cvxopt
# import matplotlib.pyplot as plt
# from sklearn.datasets import load_breast_cancer
# from sklearn.preprocessing import normalize
# from sklearn.model_selection import train_test_split


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
        self.kernel = kernel
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
        self.kernel = self.kernel(  # 初始化核函数
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
            self.intercept -= self.lagr_multipliers[i] * self.support_vectors_labels[i] *\
                              self.kernel(self.support_vectors[i], self.support_vectors[0])
        y[y == -1] = 0

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

    # def plot_picture(self, c,):


# def load_data():
#     data = np.array([
#         [0.1, 0.7],
#         [0.3, 0.6],
#         [0.4, 0.1],
#         [0.5, 0.4],
#         [0.8, 0.04],
#         [0.42, 0.6],
#         [0.9, 0.4],
#         [0.6, 0.5],
#         [0.7, 0.2],
#         [0.7, 0.67],
#         [0.27, 0.8],
#         [0.5, 0.72]
#     ])
#     target = [1] * 6 + [0] * 6
#     return data, np.array(target)


def plot_picture(data, target, dimension=(0, 1), C=1, gamma=None, kernel=rbf_kernel, power=4, coef=4):
    # 画图函数
    x_min, x_max = data[:, dimension[0]].min() - 0.02, data[:, dimension[0]].max() + 0.02
    y_min, y_max = data[:, dimension[1]].min() - 0.02, data[:, dimension[1]].max() + 0.02
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))
    clf = SVM(C=C, kernel=kernel, gamma=gamma, power=power, coef=coef)
    # clf = SVC(kernel='rbf', gamma=gamma, C=C)
    data = data[:, dimension[0]:dimension[1]+1]
    clf.fit(data, target)
    z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)
    plt.contourf(xx, yy, z, cmap=plt.cm.ocean, alpha=0.6)
    # plt.scatter(data[:6, 0], data[:6, 1], marker='o', color='r', s=100, lw=3)
    plt.scatter(data[target == 0][:, 0], data[target == 0][:, 1], marker='o', color='r', s=100, lw=3)
    # plt.scatter(data[6:, 0], data[6:, 1], marker='x', color='k', s=100, lw=3)
    plt.scatter(data[target == 1][:, 0], data[target == 1][:, 1], marker='x', color='k', s=100, lw=3)
    gamma = clf.gamma
    plt.title('SVM with $\gamma=$' + str(gamma))
    plt.show()

# if __name__ == '__main__':
#     data, target = load_data()
#     plot_picture(data, target, (0, 1), 6, 5, rbf_kernel)



if __name__ == '__main__':
    # iris = load_iris()
    # X = iris.data
    # y = iris.target
    # X = normalize(X[y != 0], norm='l2')
    # # X = X[y != 0]
    # y = y[y != 0]
    # y[y == 1] = 0
    # y[y == 2] = 1
    # clf = SVM(kernel=polynomial_kernel, power=4, coef=1)
    # plot_picture(X, y, (2,3), C=1, kernel=polynomial_kernel, power=3, coef=1)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    # clf = SVM(kernel=polynomial_kernel, power=4, coef=1)
    # clf.fit(X_train, y_train)
    # y_predict = clf.predict(X_test)
    # print(np.sum(y_predict == y_test) / len(y_test))

    digit = load_breast_cancer()
    X = normalize(digit.data, norm='l2')
    y = digit.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    clf = SVM(kernel=polynomial_kernel, power=4, coef=3)
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)
    print(np.sum(y_predict == y_test) / len(y_test))