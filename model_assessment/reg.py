import numpy as np


class reg_assessment:
    def __init__(self, y_predict, y_test):
        """
        回归评估
        :param y_predict: 预测值
        :param y_test: 真实值
        """
        self.y_predict = y_predict
        self.y_test = y_test
        self.MAE = None
        self.MSE = None
        self.R_square = None
        self.RMSE = None
        self.MAPE = None

    def get_MSE(self):
        if self.MSE is not None: return self.MSE
        self.MSE = np.sum((self.y_predict - self.y_test) ** 2) / len(self.y_predict)
        return self.MSE

    def get_MAE(self):
        if self.MAE is not None: return self.MAE
        self.MAE = np.sum(np.abs(self.y_predict - self.y_test)) / len(self.y_predict)
        return self.MAE

    def get_RMSE(self):
        if self.RMSE is not None: return self.RMSE
        if self.MSE is None: self.get_MSE()
        self.RMSE = np.sqrt(self.MSE)
        return self.RMSE

    def get_R2(self):
        if self.R_square is not None: return self.R_square
        if self.MSE is None: self.get_MSE()
        self.R_square = 1 - (self.MSE / np.sum((self.y_test - np.mean(self.y_test)) ** 2))
        return self.R_square

    def get_MAPE(self):
        if self.MAPE is not None: return self.MAPE
        self.MAPE = np.sum(np.abs((self.y_predict - self.y_test) / self.y_test)) / len(self.y_predict)
        return self.MAPE

    def assessment(self):
        print("均方误差（MSE）：", self.get_MSE())
        print("平均绝对误差（MAE）：", self.get_MAE())
        print("均方根误差（RMSE）：", self.get_RMSE())
        print("平均绝对百分比误差（MAPE）：", self.get_MAPE())
        print("R平方：", self.get_R2())
