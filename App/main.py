import sys,os

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #获取要导入模块的上上级目录

sys.path.insert(0,p)


import json
from io import StringIO

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from App.utils import *
from App.PoolManager import *
from App.ModelManager import *

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

        discrete = []

        if('dropColumns' in data) :

            dataSet += str(data['dropColumns'])

            df = dropColumns(df, columns = data['dropColumns'])

        if('discreteColumns' in data) :

            dataSet += str(data['dropColumns'])

            discrete = data['discreteColumns']

        hashKey = str(hash(dataSet))

        pushDataSet(df, discrete, hashKey)

        if("Unnamed: 0" in df.columns) : df = dropColumns(df, columns = ["Unnamed: 0"])

        return hashKey

    return '<h1>请使用POST方法访问</h1>'



@app.route('/api-fit', methods = ['POST', 'GET'])
def fit() :

    if request.method == 'POST':

        data = json.loads(str(request.data, 'utf-8'))

        dataSet = pullDataSet(str(data['hashKey']))

        model = -1

        ssler = None

        target = ''

        if(dataSet is None) : return '{"msg" : "数据已过期"}'

        if('model' in data) : model = data['model']

        if(model <= 0 or model > 6) : return '{"msg" : "模型种类无效"}'

        if('target' in data and data['target'] in dataSet.columns): target = data['target']
        else : return '{"msg" : "标签无效"}'

        if(model == 1) :

            pass

        elif(model == 2) :

            pass

        elif(model == 3) :

            pass

        elif(model == 4) :

            pass

        elif(model == 5) :

            x, y = DataFrame2NPArray(dataSet, target)

            model, ssler = LogisticRegressionTraining(x, y)

        elif(model == 6) :

            pass

        key = pushModel(model, ssler)

        return str(key)

    return '<h1>请使用POST方法访问</h1>'

@app.route('/api-predict', methods=['POST', 'GET'])
def predict() :

    if request.method == 'POST':

        data = json.loads(str(request.data, 'utf-8'))

        dataSet = pullDataSet(str(data['hashKeyI']))

        model, ssler = pullModel(str(data['hashKeyII']))

        if (dataSet is None): return '{"msg" : "数据已过期"}'

        if (model is None): return '{"msg" : "模型已过期"}'

        dataSet = DataFrame2NPArray(dataSet)

        res = model.predict(ssler.fit(dataSet))

        return DataFrame2Array(DataFrame({'label' : res}))

    return '<h1>请使用POST方法访问</h1>'

@app.before_request
def before_request():
    ip = request.remote_addr

    url = request.url

    print("地址[" + str(ip) + "] 试图访问：" + str(url))

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000, debug = True)
