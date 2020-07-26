import utils
import numpy as np
from pandas import *
import matplotlib.pyplot as plt

if __name__ == '__main__' :

    data = read_csv('test.csv')

    data = utils.dropColumns(data, columns = ['PassengerId'])

    data = utils.getDummies(data, columns = ['Survived'])

    print(data)