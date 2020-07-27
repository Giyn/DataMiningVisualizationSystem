import numpy as np
from pandas import DataFrame, get_dummies, cut
import matplotlib.pyplot as plt

def dropColumns(dataSet:DataFrame, columns:list)  -> DataFrame:

    return dataSet.drop(labels = columns, axis = 1)

def getDummies(dataSet:DataFrame, columns:list)  -> DataFrame:

    return get_dummies(dataSet, columns = columns)

def cutColumns(dataSet:DataFrame, columns:list, silce:list) :

    for c, s in zip(columns, silce) :

        dataSet[c] = cut(dataSet[c], silce)

    return dataSet