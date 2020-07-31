import numpy as np
import matplotlib.pyplot as plt

class clf_assessment:
    def __init__(self, y_test, y_predict=None, y_predict_rate=None):
        """
        分类评估（没有预测概率无法话PR和ROC)
        :param y_predict: 预测结果
        :param y_predict_rate: 模型得出的概率
        :param y_test: 真实数据
        """
        self.TP, self.FP, self.TN, self.FN = 0,0,0,0
        self.y_predict = y_predict
        self.y_test = y_test
        self.y_predict_rate = y_predict_rate
        if y_predict_rate is None:
            self.predict()
        self.confuse_matrix()

    def predict(self, threshold=0.5):
        # 根据阈值判断正类还是负类
        a = np.empty(shape=np.array(self.y_predict_rate).shape)
        for i in range(len(self.y_predict_rate)):
            if self.y_predict_rate[i] >= threshold: a[i] = 1
            else: a[i] = 0
        self.y_predict = a

    def confuse_matrix(self):
        # 计算混淆矩阵
        TP, FP, TN, FN = 0,0,0,0
        for i in range(len(self.y_predict)):
            if self.y_predict[i] == self.y_test[i]:
                if self.y_predict[i] == 1: TP += 1
                else: TN += 1
            elif self.y_predict[i] == 1 and self.y_test[i] == 0:
                FP += 1
            elif self.y_predict[i] == 0 and self.y_test[i] == 1:
                FN += 1
        self.TP, self.FP, self.TN, self.FN = TP, FP, TN, FN

    def print_matrix(self, filename, view=False):
        """简单绘制混淆矩阵
        :param view: False为文字版，True为可视化图片
        :return:
        """
        if view is False:
            print("           预测结果    ")
            print("真实     正例      反例")
            print("正例     %3d      %3d" % (self.TP, self.FN))
            print("反例     %3d      %3d" % (self.FP, self.TN))
            return
        else:
            data = np.array([[self.TP, self.FP],[self.FN, self.TN]])
            plt.matshow(data, cmap=plt.cm.Greens)
            plt.colorbar()
            for y in range(len(data)):
                for x in range(len(data)):
                    plt.annotate(s=data[x,y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
            plt.ylabel("True label")
            plt.xlabel("Predicted label")
            plt.savefig(filename)
            plt.show()

    def TPR(self):
        try:
           return self.TP / (self.TP + self.FN)
        except :
            return 0.

    def FPR(self):
        try:
            return self.FP / (self.FP + self.TN)
        except :
            return 0.

    def accuracy(self):
        return (self.TP + self.TN) / (self.TP + self.FP + self.TN + self.FN)

    def precision(self):
        try:
            return self.TP / (self.TP + self.FP)
        except:
            return 0.

    def recall(self):
        try:
            return self.TP / (self.TP + self.FN)
        except:
            return 0.

    def F1_score(self):
        p = self.precision()
        r = self.recall()
        try:
            return (2 * p * r) / (p + r)
        except:
            return 0.

    def paint_PR(self, filename):
        """画PR曲线
        :param filename: 保存图片路径
        :return:
        """
        thresholds = np.arange(np.min(self.y_predict_rate), np.max(self.y_predict_rate), 0.1)
        precisions = []
        recalls = []
        for i in thresholds:
            self.predict(i)
            self.confuse_matrix()
            precisions.append(self.precision())
            recalls.append(self.recall())
        plt.plot(recalls, precisions)
        plt.savefig(filename)
        plt.show()

    def paint_ROC(self, filename):
        """画ROC曲线
        :param filename: 保存图片路径
        :return:
        """
        thresholds = np.arange(np.min(self.y_predict_rate), np.max(self.y_predict_rate), 0.1)
        fprs = []
        tprs = []
        for i in thresholds:
            self.predict(i)
            self.confuse_matrix()
            fprs.append(self.FPR())
            tprs.append(self.TPR())
        plt.plot(fprs, tprs)
        plt.savefig(filename)
        plt.show()

    def count_AUC(self):
        # 计算AUC
        N = 0
        P = 0
        neg_prob = []
        pos_prob = []
        for i in range(len(self.y_test)):
            if (self.y_test[i] == 1):
                P += 1
                pos_prob.append(self.y_predict_rate[i])
            else:
                N += 1
                neg_prob.append(self.y_predict_rate[i])
            number = 0
            for pos in pos_prob:
                for neg in neg_prob:
                    if pos > neg:
                        number += 1
                    elif pos == neg:
                        number += 0.5
        print("AUC值为：", number/(N*P))