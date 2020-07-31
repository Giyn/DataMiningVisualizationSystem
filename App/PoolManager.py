from numpy import *
from pandas import *
import matplotlib.pyplot as plt


MAXN = 20

modelPool = []

dataPool = []

def pushModel(model, ssler) :

    if(len(modelPool) >= MAXN) :
        for i in range(0, 10) :
            modelPool.pop(0)

    key = str(hash(model) + hash(ssler))

    modelPool.append([key, model, ssler])

    print("modelPool :{0}".format(len(modelPool), MAXN))

    return key


def pushDataSet(dataSet, discrete, textColumns, key):

    if(pullDataSet(key) is not None) : return False

    if (len(dataPool) >= MAXN):
        for i in range(0, 10):
            dataPool.pop(0)

    dataPool.append([key, dataSet, discrete, textColumns])

    print("dataPool :{0}".format(len(dataPool), MAXN))

    return True

def pullModel(hashKey:str):

    for i in modelPool :

        if(i[0] == hashKey) : return i[1], i[2]

    return None, None

def pullDataSet(hashKey:str) :

    for i in dataPool :

        if(i[0] == hashKey) : return i[1], i[2], i[3]

    return None