import numpy as np
from pandas import DataFrame, get_dummies
import matplotlib.pyplot as plt

def dropColumns(dataSet:DataFrame, columns:list)  -> DataFrame:

    return dataSet.drop(labels = columns, axis = 1)

def getDummies(dataSet:DataFrame, columns:list)  -> DataFrame:

    return get_dummies(dataSet, columns = columns)