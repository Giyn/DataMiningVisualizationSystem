import sys,os

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #获取要导入模块的上上级目录

sys.path.insert(0,p)


import json
from io import StringIO

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from App.utils import *
from App.PoolManager import *
from MachineLearningAlgorithm.LogisticRegression.ML.LogisticRegression import *

app = Flask(__name__)

CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api-DataFrame', methods = ['POST', 'GET'])
def dataFrame() :

    if request.method == 'POST':

        data = json.loads(str(request.data, 'utf-8'))

        text = StringIO(data['dataSet'])

        if ('sep' in data) : sep = data['sep']

        df = read_csv(text, sep = sep)

        if("Unnamed: 0" in df.columns) : df = dropColumns(df, columns = ["Unnamed: 0"])

        print(df.columns)

        res = DataFrame2Array(df)

        return str(res)

    return '<h1>请使用POST方法访问</h1>'

@app.route('/api-pretreatment', methods = ['POST', 'GET'])
def pretreatment() :

    if request.method == 'POST':

        data = json.loads(str(request.data, 'utf-8'))

        dataSet = str(data['dataSet'])

        df = Array2DataFrame(dataSet)

        print(df)

        hashKey = str(pushDataSet(df, str(hash(dataSet))))

        if("Unnamed: 0" in df.columns) : df = dropColumns(df, columns = ["Unnamed: 0"])

        if('dropColumns' in data) : print(data['dropColumns'])

        if('discreteColumns' in data) : print(data['discreteColumns'])

        # print(pullDataSet(hashKey))

        return hashKey

    return '<h1>请使用POST方法访问</h1>'

@app.route('/api-fit', methods = ['POST', 'GET'])
def fit() :

    if request.method == 'POST':

        data = json.loads(str(request.data, 'utf-8'))

        dataSet = pullDataSet(str(data['hashKey']))

        print(dataSet)

        if(dataSet is None) : return '{"msg" : "数据已过期"}'

        if('models' in data) : print(data['models'])

        print(dataSet.columns)

        return str(DataFrame2Array(dataSet))

    return '<h1>请使用POST方法访问</h1>'



@app.route('/api-submit', methods=['POST', 'GET'])
def submit() :

    if request.method == 'POST':

        return '{"msg" : "该API已经停用"}', 403

    if request.method == 'GET':

        return '<h1>该页面已停用</h1>'

@app.before_request
def before_request():
    ip = request.remote_addr

    url = request.url

    print("地址[" + str(ip) + "] 试图访问：" + str(url))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug = True)