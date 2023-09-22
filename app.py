from flask import Flask
from flask import request,jsonify
from util.pyjudgeUtil import execute
from flask_cors import CORS


app = Flask("My Server")
CORS(app)

@app.route('/api/executeCode', methods=['POST'])
def executeCode():
    if request.method == 'POST':
        data = request.get_json()
        code = data['code'] if "code" in data else ""
        inp= data['input'] if "input" in data else ""
        out= data['output'] if "output" in data else ""
        result = execute(code,inp,out)
        return jsonify(result)