from flask import Flask, request
import uuid

app = Flask(__name__)


userInfo = {}


@app.route('/api/data', methods=['GET', 'POST'])
def collection():
    if request.method == 'GET':
        pass  # Handle GET all Request
    elif request.method == 'POST':
        data = request.form
        pass  # Handle POST request


@app.route('/api/id', methods=['GET'])
def identification():
    if request.method == 'GET':
        userId = uuid.uuid4()
        userInfo[userId] = None
        return str(userId)


if __name__ == '__main__':
    app.debug = True
    app.run()
