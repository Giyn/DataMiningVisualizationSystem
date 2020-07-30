import numpy as np
import copy

def train_test_split(X, y, test_ratio, seed=None): # 留出法
    """
    :param X: 特征集
    :param y: 结果集
    :param test_ratio: 测试集占比
    :param seed: 随机种子
    :return:
    """
    if seed: np.random.seed(seed)
    a = len(X)
    shuffled_indexes = np.random.permutation(a) #打乱索引
    shuffled_train = shuffled_indexes[:int(a*(1-test_ratio))] #分配索引
    shuffled_test = shuffled_indexes[int(a*(1-test_ratio)):a]
    # 根据索引找元素
    X_train = np.array([X[i] for i in shuffled_train])
    X_test = np.array([X[i] for i in shuffled_test])
    y_train = np.array([y[i] for i in shuffled_train])
    y_test = np.array([y[i] for i in shuffled_test])
    return X_train, X_test, y_train, y_test

def cross_validation(algorihm, X, y, n): #交叉验证法
    """
    :param algorihm: 传入算法的类
    :param X: 特征集
    :param y: 结果集
    :param n: 划分个数
    :return:
    """
    def accuracy_score(y_true, y_predict): # 计算准确率
        return np.sum(y_true == y_predict) / len(y_true)
    all = np.random.permutation(len(X)) #打乱索引
    size = len(X) // n
    # 根据n把数据分成n部分
    s = []
    for i in range(0, len(X), size):
        a = all[i:i+size]
        s.append(a)
    result = np.empty((n,)) # 记录准确率

    # 遍历s，交叉验证过程
    for i in range(n):
        b = copy.deepcopy(s)
        verify = b.pop(i) # 弹出一个元素做验证集
        train = np.hstack(b) # 其他元素合并做训练集
        # 根据索引找元素
        verify_real_X = np.array([X[j] for j in verify])
        verify_real_y = np.array([y[j] for j in verify])
        train_real_X = np.array([X[j] for j in train])
        train_real_y = np.array([y[j] for j in train])
        # 代入验证类
        algorihm.fit(train_real_X, train_real_y)
        verify_predict = algorihm.predict(verify_real_X) #计算预测值
        result[i] = accuracy_score(verify_real_y, verify_predict) # 计算准确率
    return np.mean(result) # 准确率求均值返回

def bootstraping(X, y): #自助法
    """
    :param X: 特征集
    :param y: 结果集
    :return:
    """
    a = len(X)
    test_index = np.empty((a,), dtype=int) # 索引容器
    for i in range(a): # 根据数据集长度随机抽取a次
        test_index[i] = np.random.randint(a)
    # 根据索引找元素
    X_train = np.array([X[i] for i in test_index])
    y_train = np.array([y[i] for i in test_index])
    X_test = []
    y_test = []
    # 没抽到的做测试集
    for i in range(a):
        if i not in test_index:
            X_test.append(X[i])
            y_test.append(y[i])
    return X_train, np.array(X_test), y_train, np.array(y_test)