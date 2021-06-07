# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 23:48:08 2020

@author: Giyn
"""

import pandas as pd

from ML.MultipleLinearRegression import MultipleLinearRegression
from ML.metrics import *
from ML.model_selection import train_test_split

data = pd.read_csv("housing.csv")

X = data.values[:, [0, 1, 2, 3]]
y = data.values[:, [4]]
X_train, X_test, y_train, y_test = train_test_split(X, y, seed=412)

reg = MultipleLinearRegression()
reg.fit_normal(X_train, y_train)

y_predict = reg.predict(X_test)
MSE = mean_squared_error(y_test, y_predict)
RMSE = root_mean_squared_error(y_test, y_predict)
MAE = mean_absolute_error(y_test, y_predict)
R_Square = r2_score(y_test, y_predict)
