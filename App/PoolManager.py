from numpy import *
from pandas import *
import matplotlib.pyplot as plt


MAXN = 20

modelPool = []

dataPool = []

def pushModel(model) :

    if(len(modelPool) >= MAXN) :
        for i in range(0, 10) :
            modelPool.pop(0)

    key = str(hash(model))

    modelPool.append([key, model])

    return key


def pushDataSet(dataSet, discrete, key):

    if(pullDataSet(key) is not None) : return False

    if (len(dataPool) >= MAXN):
        for i in range(0, 10):
            dataPool.pop(0)

    dataPool.append([key, dataSet, discrete])

    print("dataPool : " + str(len(dataPool)))

    return True

def pullModel(hashKey:str):

    for i in modelPool :

        if(i[0] == hashKey) : return i[1]

    return None

def pullDataSet(hashKey:str) :

    for i in dataPool :

        if(i[0] == hashKey) : return i[1]

    return None