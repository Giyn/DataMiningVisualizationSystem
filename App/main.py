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
from MachineLearningAlgorithm.Bayes.NaiveBayes import *
from model_assessment.divide_data import *

set_option('display.max_columns', None)

set_option('display.max_rows', None)

set_option('max_colwidth', 100)

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

        textColumn = None

        if('dropColumns' in data) :

            dataSet += str(data['dropColumns'])

            if(len(data['dropColumns']) != 1 or data['dropColumns'][0] != '' ) : df = dropColumns(df, columns = data['dropColumns'])

        df = df.dropna(axis = 0, how = 'any')

        df = df.reset_index(drop=True)

        if('discreteColumns' in data) :

            dataSet += str(data['discreteColumns'])

            discrete = data['discreteColumns']

            if(len(data['discreteColumns']) != 1 or data['discreteColumns'][0] != '' ) : df = getDummies(df, columns = discrete)

        if ('textColumn' in data):

            dataSet += str(data['textColumn'])

            if(data['textColumn'] != '' ) : textColumn = str(data['textColumn'])


        hashKey = str(hash(dataSet))

        print(df)

        pushDataSet(df, discrete, textColumn, hashKey)

        if("Unnamed: 0" in df.columns) : df = dropColumns(df, columns = ["Unnamed: 0"])

        return hashKey

    return '<h1>请使用POST方法访问</h1>'



@app.route('/api-fit', methods = ['POST', 'GET'])
def fit() :

    if request.method == 'POST':

        data = json.loads(str(request.data, 'utf-8'))

        dataSet, discrete, textColumn = pullDataSet(str(data['hashKey']))

        model = -1

        ssler = None

        target = ''

        if(dataSet is None) : return '{"status_code" : 403,"msg" : "数据已过期"}'

        if('model' in data) : model = data['model']

        if(model <= 0 or model > 6) : return '{"status_code" : 403,"msg" : "模型种类无效"}'

        if('target' in data and data['target'] in dataSet.columns): target = data['target']
        else : return '{"status_code" : 403,"msg" : "标签无效"}'

        if(model == 1) :

            y = np.array(dataSet[target])

            model, ssler = NBayesTraining(dataSet, y, textColumn)

        elif(model == 2) :

            x, y = DataFrame2NPArray(dataSet, target)

            model, ssler = KNNTraining(x, y)

        elif(model == 3) :

            x, y = DataFrame2NPArray(dataSet, target)

            model, ssler = SVMTraining(x, y)

        elif(model == 4) :

            x, y = DataFrame2NPArray(dataSet, target)

            x = x.reshape(len(x))

            model, ssler = LinearRegressionTraining(x, y)

        elif(model == 5) :

            x, y = DataFrame2NPArray(dataSet, target)

            model, ssler = LogisticRegressionTraining(x, y)

        elif(model == 6) :

            x, y = DataFrame2NPArray(dataSet, target)

            model, ssler = CART_REGTraining(x, y)

        if(not isinstance(model, NaiveBayesClassifier)) :

            x, y = DataFrame2NPArray(dataSet, target)

            x = ssler.transform(x)

        else :

            x = ssler.transform(dataSet, textColumn)

        cv_score = cross_validation(model, x, y, 10)

        key = pushModel(model, ssler)

        res = jsonify({

            "hashKey" : str(key),

            "cv_score" : cv_score,

            "status_code" : 200

        })

        print(str(res))

        return str(res)

    return '<h1>请使用POST方法访问</h1>'

@app.route('/api-predict', methods=['POST', 'GET'])
def predict() :

    if request.method == 'POST':

        data = json.loads(str(request.data, 'utf-8'))

        dataSet, discrete, textColumn = pullDataSet(str(data['hashKeyI']))

        model, ssler = pullModel(str(data['hashKeyII']))

        if (dataSet is None): return '{"msg" : "数据已过期"}'

        if (model is None): return '{"msg" : "模型已过期"}'

        if(not isinstance(model, NaiveBayesClassifier)) :

            dataSet = DataFrame2NPArray(dataSet)

            res = model.predict(ssler.transform(dataSet))

        else :

            res = model.predict(ssler.transform(dataSet, textColumn))

        return str(DataFrame2Array(DataFrame({'label' : res})))

    return '<h1>请使用POST方法访问</h1>'

@app.before_request
def before_request():
    ip = request.remote_addr

    url = request.url

    print("地址[" + str(ip) + "] 试图访问：" + str(url))

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000, debug = True)
