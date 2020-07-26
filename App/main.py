from flask import Flask, request, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

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

        if('dataSet' not in form) : return "feature \"dataSet\" not found"

        dataSet = request.form['dataSet']

        if('dropColumns' in form) : dropColumns = request.form['dropColumns']

        if('discreteColumns' in form) : discreteColumns = request.form['discreteColumns']

        print(dataSet)

        print(dropColumns)

        print(discreteColumns)

        return "Submit successfully!"

    return '<h1>请使用POST方法访问</h1>'

@app.before_request
def before_request():
    ip = request.remote_addr

    url = request.url

    print("地址[" + str(ip) + "] 试图访问：" + str(url))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)