import re
import jieba
import jieba.analyse
from random import *
from wordcloud import *
import matplotlib.pyplot as plt
from io import BytesIO
from base64 import *

def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    r = randint(0, 100)
    g = randint(100, 255)
    b = randint(100, 255)
    return "rgb({0}, {1}, {2})".format(r, g, b)

def wordcloudSpawn(dicts) :

    cloud = WordCloud(

        background_color='white',
        max_words=1000,

        max_font_size=100,

        prefer_horizontal=0.8,

        color_func = random_color_func
    )
    cloud.generate_from_frequencies(frequencies=dicts)

    save_file = BytesIO()

    plt.axis('off')

    plt.imshow(cloud)

    plt.savefig(save_file, format='png')

    b64 = b64encode(save_file.getvalue()).decode('utf8')

    return str(b64)

def stopwordslist(path):

    """
        生成停用词（stop_word)字典
    """

    stopwords = [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]

    return stopwords

import  os
print(os.getcwd())

stopword = stopwordslist('MachineLearningAlgorithm/Bayes/stop_words.txt')

def text_format(text):

    """
        分词函数
    """

    res = []

    temp = []


    TFIDF = jieba.analyse.extract_tags(text, topK = 100, withWeight = True)

    alphabet = re.findall('([A-Za-z]+)', text)

    text = re.compile('[^\u4e00-\u9fa5]').split(text)

    text = re.compile('\W+|\d+|[a-z]+|[A-Z]+').split(' '.join(text))



    """
        jieba进行语素划分
    """

    for word in text:
        temp.extend(jieba.cut(word))

    temp.extend(alphabet)

    """
        去除停用词(stop-word)
    """

    for word in temp:
        if(word not in stopword): res.append(word)

    return res

def createDict(dataSet, thres = 2):

    temp = {}

    res = {}

    count = 0

    """
        语素统计
    """

    for i in range(0, len(dataSet)):

        text = dataSet[i]

        text, tfidf = text_format(text)

        for word in text:

            if (word not in temp):

                temp[word] = 1

            else:

                temp[word] += 1


    """
        过滤阈值以下的语素
    """

    for i in temp:

        if (temp[i] <= thres): continue

        res[i] = temp[i]

        count += res[i]

    return (res, count)