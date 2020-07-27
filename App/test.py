from utils import *
import numpy as np
from pandas import *
import matplotlib.pyplot as plt

if __name__ == '__main__' :

    data = read_csv('test.csv')

    data = DataFrame2Array(data)

    print(data)

    data = Array2DataFrame(data)

    print(data)