from flask import Flask, request, jsonify
from queue import PriorityQueue
import uuid
import time
import random

app = Flask(__name__)

random.seed()
# chunkOfUser is a dict with keys of user's id and the chunk they're currently working on
chunkOfUser = {}
# computeStack is a "stack" with dicts of start and stop values to be sent to users
computeStack = [{'start': 4000000, 'stop': 5000000, 'equation': [[]]}]
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
# clientTimeline is a priority queue to show the soonest client tasks first, priority is unix timestamp and value is
# their userId
clientTimeline = PriorityQueue()
# seconds allowed for the user to do the computation. Now it's a constant, but one day it may be dynamic
COMP_TIME_LIMIT = 15
solution = {'solution': None}


@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'GET':
        userId = request.args.get('id')
        # if they didn't specify a user id, they're unauthorized
        if userId is None or userId is '':
            print(1)
            return jsonify({}), 401
        # if their userId was never put into the system, they're also unauthorized
        if userId not in chunkOfUser:
            print(chunkOfUser)
            print(2)
            return jsonify({}), 401
        # they're in our system and already working on a compute part, so don't assign them a new one
        if chunkOfUser[userId] is not None:
            print(3)
            return jsonify({'start': None, 'stop': None, 'equation': None}), 200
        # get their compute load and document it
        computeDatum = computeStack.pop()
        chunkOfUser[userId] = computeDatum
        # add their load to the priority queue
        clientTimeline.put(time.time() + COMP_TIME_LIMIT, userId)
        # send the value
        return jsonify(computeDatum)
    elif request.method == 'POST':
        data = request.form
        print('data')
        print(data)
        userId = request.args.get('id')
        # if they didn't specify a user id, they're unauthorized
        if userId is None or userId is '' or 'result' not in data:
            return jsonify({}), 401
        chunkOfUser[userId] = None
        if data.result and 'solution' in data:
            solution = data.solution
#             TODO determine a procedure to do when solution is found...


@app.route('/api/id', methods=['GET'])
def api_id():
    if request.method == 'GET':
        userId = str(uuid.uuid4())
        chunkOfUser[userId] = None
        print(chunkOfUser)
        return userId


if __name__ == '__main__':
    app.debug = True
    app.run()