from flask import Flask, request, jsonify
from queue import PriorityQueue
import uuid
import time
import random

app = Flask(__name__)

random.seed()
# userInfo is a dict with keys of their id and value
userInfo = {}
# computeStack is a "stack" with dicts of start and stop values to be sent to users
computeStack = []
# dummy values
for x in range(0, 1000000 * 20, 1000000):
    equation = []
    for i in range(0, 20):
        equation.append([])
        for j in range(0, 3):
            multiplier = -1
            if random.randint(0, 1) == 1:
                multiplier = 1
            equation[i].append(random.randint(1, 10) * multiplier)
    computeStack.append({'start': x, 'stop': x + 1000000, 'equation': equation})
computeStack = [{'start': 4000000, 'stop': 5000000, 'equation': [[]]}]
# clientTimeline is a priority queue to show the soonest client tasks first, priority is unix timestamp and value is
# their userId
clientTimeline = PriorityQueue()
# seconds allowed for the user to do the computation. Now it's a constant, but one day it may be dynamic
COMP_TIME_LIMIT = 15


@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'GET':
        userId = request.args.get('id')
        if userId is None:
            return jsonify([]), 401
        if userInfo[userId] is None:
            return jsonify([]), 200
        # get their compute load and document it
        computeDatum = computeStack.pop()
        userInfo[userId] = computeDatum
        # add their load to the priority queue
        clientTimeline.put(time.time() + COMP_TIME_LIMIT, userId)
        # send the value
        return jsonify(computeDatum)
    elif request.method == 'POST':
        data = request.form
        pass  # Handle POST request


@app.route('/api/id', methods=['GET'])
def api_id():
    if request.method == 'GET':
        userId = uuid.uuid4()
        userInfo[userId] = None
        return str(userId)


if __name__ == '__main__':
    app.debug = True
    app.run()
