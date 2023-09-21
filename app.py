from flask import Flask
from flask import request,jsonify
from util.pyjudgeUtil import execute

app = Flask(__name__)

@app.route('/api/executeCode', methods=['POST'])
def executeCode():
    if request.method == 'POST':
        data = request.get_json()
        code = data['code']
        inp= data['input']
        out= data['output']
        result = execute(code,inp,out)
        return jsonify(result)
      