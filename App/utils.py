import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt



def dropColumns(dataSet:DataFrame, columns:list)  -> DataFrame:

    dataSet.drop(labels = columns)
