import json
from io import StringIO

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from pandas import *

app = Flask(__name__)

CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api-DataFrame', methods=['POST', 'GET'])
def dataFrame() :

    if request.method == 'POST':

        data = json.loads(str(request.data, 'utf-8'))

        text = StringIO(data['dataSet'])

        sep = ','

        if('sep' in data) : sep = data['sep']

        df = read_csv(text, sep = sep)

        res = [['id']]

        for i in range(0, len(df)) :

            res.append([i])

        for i in df.columns :

            res[0].append(i)

            for j in range(1, len(df) + 1):

                res[j].append(str(df[i][j - 1]))

        print(df.columns)

        return str(res)

    return ""


@app.route('/api-submit', methods=['POST', 'GET'])
def submit() :

    if request.method == 'POST':

        dataSet = None

        dropColumns = []

        discreteColumns = []

        print("header:\n" + str(request.headers))

        print("json:\n" + str(request.json))

        print("data:\n" + str(request.data))

        form = request.form.to_dict()

        if('dataSet' in form) : dataSet = request.form['dataSet']

        if('dropColumns' in form) : dropColumns = request.form['dropColumns']

        if('discreteColumns' in form) : discreteColumns = request.form['discreteColumns']

        print("dataSet:\n" + str(dataSet))

        print("dropColumns:\n" + str(dropColumns))

        print("discreteColumns:\n" + str(discreteColumns))

        return "Submit successfully!"

    return '<h1>请使用POST方法访问</h1>'

@app.before_request
def before_request():
    ip = request.remote_addr

    url = request.url

    print("地址[" + str(ip) + "] 试图访问：" + str(url))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug = True)