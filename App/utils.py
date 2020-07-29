import numpy as np
from pandas import *
import re
import matplotlib.pyplot as plt

def dropColumns(dataSet:DataFrame, columns:list)  -> DataFrame:

    return dataSet.drop(labels = columns, axis = 1)

def getDummies(dataSet:DataFrame, columns:list)  -> DataFrame:

    return get_dummies(dataSet, columns = columns)

def cutColumns(dataSet:DataFrame, columns:list, silce:list) :

    for c, s in zip(columns, silce) :

        dataSet[c] = cut(dataSet[c], silce)

    return dataSet

def DataFrame2Array(df:DataFrame) :

    res = [['id']]

    for i in range(0, len(df)) :
        res.append([i])

    for i in df.columns :

        res[0].append(i)

        for j in range(1, len(df) + 1):
            res[j].append(str(df[i][j - 1]))

    return res

def Array2DataFrame(array:str) :

    array = eval(array)

    res = {}

    for i in range(1, len(array[0])) :

        res[array[0][i]] = []

        for j in range(1, len(array)) :

            if(array[j][i] == 'nan') :
                res[array[0][i]].append(np.nan)
            else :
                res[array[0][i]].append(array[j][i])

    res = DataFrame(res)

    return res

def DataFrame2NPArray(dataSet:DataFrame, target = None) :

    x = []

    y = []

    for i in range(0, len(dataSet)) :

        x.append([])

        for j in dataSet.columns :

            if(is_number(dataSet[j][i])) :

                if (target is None or j != target):
                    x[i].append(float(dataSet[j][i]))
                else:
                    y.append(float(dataSet[j][i]))

            else :

                if (target is None or j != target):
                    x[i].append(dataSet[j][i])
                else:
                    y.append(dataSet[j][i])

    if(target is None) :

        return np.array(x)

    return np.array(x), np.array(y)


def is_number(s) :
    try:
        float(s)

        return True

    except ValueError :
        pass

    return False