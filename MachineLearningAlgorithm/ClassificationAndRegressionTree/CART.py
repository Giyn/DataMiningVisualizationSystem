import numpy as np
# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# from sklearn.datasets import load_iris
# from sklearn.model_selection import train_test_split
# from TV_examine.model_assessment import reg


class TreeNode:
    def __init__(self, left_child=None, right_child=None,
                 col=-1, value=None, data=None, result=None):
        self.left_child = left_child
        self.right_child = right_child
        self.col = col
        self.value = value
        self.data = data
        self.result = result

class DecisionTree_CART:
    def __init__(self, max_depth=np.inf, min_impurity=1e-7, min_sample=2, tree_type='clf'):
        self.root = None
        self.max_depth = max_depth
        self.min_impurity = min_impurity
        self.min_sample = min_sample
        self.tree_type = tree_type

    def fit(self, X_train, y_train):
        def calculate_variance(X):
            """ Return the variance of the features in dataset X """
            mean = np.ones(np.shape(X)) * X.mean(0)
            n_samples = np.shape(X)[0]
            variance = (1 / n_samples) * np.diag((X - mean).T.dot(X - mean))
            return variance

        def count_info(left, right, data):
            if self.tree_type == 'clf':
                base_gain = gini(data)
                prop = left.shape[0] / data.shape[0]
                info_gain = base_gain - prop * gini(left) - (1 - prop) * gini(right)
                return info_gain
            else:
                var_tot = calculate_variance(data[:, -1:])
                var_1 = calculate_variance(left[:, -1:])
                var_2 = calculate_variance(right[:, -1:])
                frac_1 = len(left) / len(data)
                frac_2 = len(right) / len(data)
                # 计算均方差
                variance_reduction = var_tot - (frac_1 * var_1 + frac_2 * var_2)
                return sum(variance_reduction)

        def majority_vote(data):
            if self.tree_type == 'clf':
                a = np.unique(data[:, -1])
                max_feature = np.empty(2)
                for i in a:
                    b = np.sum(data[:, -1] == i)
                    if b > max_feature[0]:
                        max_feature[0] = b
                        max_feature[1] = i
                return max_feature[1]
            value = np.mean(data[:, -1:], axis=0)
            return value if len(value) > 1 else value[0]

        def gini(data):
            length = data.shape[0]
            if length == 0:
                return 1
            unique = np.unique(data[:, -1])
            res = 0.0
            for i in unique:
                res += (np.sum(data[:, -1] == i) / length)**2
            return 1-res

        def split_data(data, value, col):
            if isinstance(value, int) or isinstance(value, float):
                func = lambda sample: sample[col] >= value
            else:
                func = lambda sample: sample[col] == value
            X1 = np.array([sample for sample in data if func(sample)])
            X2 = np.array([sample for sample in data if not func(sample)])
            return X1, X2

        def create_tree(data, current_depth):
            m, n = data.shape
            best_gain = 0.0
            best_feature = None
            best_data = None
            if m >= self.min_sample and current_depth <= self.max_depth:
                for col in range(n-1):
                    data_col = data[:, col]
                    unique_col = np.unique(data_col)
                    for value in unique_col:
                        left, right = split_data(data, value, col)
                        if len(left) > 0 and len(right) > 0:
                            info_gain = count_info(left, right, data)
                            if info_gain > best_gain:
                                best_gain = info_gain
                                best_feature = (col, value)
                                best_data = (left, right)

            if best_gain > self.min_impurity:
                true_branch = create_tree(best_data[0], current_depth+1)
                false_branch = create_tree(best_data[1], current_depth+1)
                return TreeNode(true_branch, false_branch, col=best_feature[0], value=best_feature[1], data=data)

            else:
                return TreeNode(result=majority_vote(data))

        dataset = np.hstack((X_train, y_train.reshape(-1, 1)))
        self.root = create_tree(dataset, 0)
        return self.root

    def _predict(self, X_test):
        def find_label(tree):
            if tree.result is not None:
                return tree.result
            v = X_test[tree.col]
            if isinstance(v, int) or isinstance(v, float):
                if v >= tree.value:
                    branch = tree.left_child
                else:
                    branch = tree.right_child
            else:
                if v == tree.value:
                    branch = tree.left_child
                else:
                    branch = tree.right_child
            return find_label(branch)
        return find_label(self.root)

    def predict(self, X_test):
        m = X_test.shape[0]
        res = np.empty(m)
        for i in range(m):
            res[i] = self._predict(X_test[i])
        return res

def load_data(data, bin=None):
    le = LabelEncoder()
    dt = []
    for i in bin:
        data2 = data[:, i]
        res = le.fit_transform(data2).reshape(-1, 1)
        dt.append(res)
    dt = np.hstack(dt)
    return dt

def cut_data(data, bin=None):
    # 离散值连续化
    le = LabelEncoder()
    res = []
    a = range(data.shape[1]) if bin is None else bin
    for i in a:
        data1 = np.unique(np.sort(data[:, i]))
        divide = [data1[0]-1]
        for j in range(data1.shape[0]-1):
            divide.append((data1[j]+data1[j+1])/2)
        divide.append(data1[-1]+1)
        data2 = np.array(pd.cut(data[:, i], divide))
        data3 = le.fit_transform(data2).reshape(-1, 1)
        res.append(data3)
    return np.hstack(res)


if __name__ == '__main__':
    # X, y = load_data("/Users/huangzhuoxi/Documents/学术部/学术部作业/寒假作业/测试/12.csv")
    # cart = DecisionTree_CART()
    # cart.fit(X, y)
    # res = cart.predict(X)
    # print(res, "\n", y)

    # iris = load_iris()
    # X = iris.data
    # y = iris.target
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    # cart = DecisionTree_CART()
    # cart.fit(X_train, y_train)
    # print(np.sum(cart.predict(X_test) == y_test) / len(y_test))

    data = pd.read_csv("/Users/huangzhuoxi/Documents/工作室考核/qg/中期考核/数据集/forestfires/forestfires.csv")
    data1 = load_data(data.values, (2, 3))
    data2 = cut_data(data.values, range(4, 11))
    X = np.hstack((data.values[:, :2], data1, data2))
    y = data.values[:, -1]
    cart = DecisionTree_CART(tree_type='reg')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    cart.fit(X_train, y_train)
    pr = cart.predict(X_test)
    ass = reg.reg_assessment(pr, y_test)
    ass.assessment()
    pass