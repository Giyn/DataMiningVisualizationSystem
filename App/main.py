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

        # result_text = {"statusCode": 200, "message": "访问成功", "dataSet" : request.form['dataSet']}
        # response = make_response(jsonify(result_text))
        # response.headers['Access-Control-Allow-Origin'] = '*'
        # response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        # response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

        return request.form['dataSet']

    return '<h1>请使用POST方法访问</br>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)