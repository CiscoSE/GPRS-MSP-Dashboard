from flask import Flask, request, jsonify
import Teamswebhookreceiver

app = Flask(__name__)

@app.route('/', methods=['POST'])
def entry():
    return Teamswebhookreceiver.runme(request=request)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
