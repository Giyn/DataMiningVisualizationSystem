import re
import numpy as np

class TextAnalyzer(object) :


    def __init__(self) :

        self.phrase_position = {}

    def fit(self, x, textColumns) :

        for i in range(0, len(x)):

            text = x.loc[i][textColumns]

            text = re.findall('([A-Za-z]+)', text)

            for word in text:

                if (word not in self.phrase_position): self.phrase_position[word] = len(self.phrase_position)


    def transform(self, x, textColumns) :

        res = np.zeros(shape = (len(x), len(self.phrase_position)))

        for i in range(0, len(x)) :

            text = x.loc[i][textColumns]

            text = re.findall('([A-Za-z]+)', text)

            for word in text:

                if(word in self.phrase_position): res[i][self.phrase_position[word]] = 1

        return res
