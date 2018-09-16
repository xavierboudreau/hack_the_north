from flask import Flask, request, jsonify
from queue import PriorityQueue
import uuid
import time
import random
from random import randint
from random import sample
import json
from twilio.rest import Client
import pdb
import os
import threading

lock = threading.Lock()
account_sid = "AC43d647b37856105ac82e47f42c9f439b"
auth_token = os.environ["TWILIO"]
app = Flask(__name__)
random.seed()
# chunkOfUser is a dict with keys of user's id and the chunk they're currently working on
chunkOfUser = {}
# computeStack is a "stack" with dicts of start and stop values to be sent to users
# computeStack = [{'start': 4000000, 'stop': 5000000, 'equation': [[]]}]
# # dummy values
# for x in range(0, 1000000 * 20, 1000000):
#     equation = []
#     for i in range(0, 20):
#         equation.append([])
#         for j in range(0, 3):
#             multiplier = -1
#             if random.randint(0, 1) == 1:
#                 multiplier = 1
#             equation[i].append(random.randint(1, 10) * multiplier)
#     computeStack.append({'start': x, 'stop': x + 1000000, 'equation': equation})

# clientTimeline is a priority queue to show the soonest client tasks first, priority is unix timestamp and value is
# their userId
clientTimeline = PriorityQueue()
# seconds allowed for the user to do the computation. Now it's a constant, but one day it may be dynamic
COMP_TIME_LIMIT = 15
solution = {'solution': None}
clauses = 10
variables = 18
startTime = time.time()
# dictionary that maps user id to another dictionary
# this second one maps each time interval (every 10 seconds since startTime)
# to the number of chunks done. so whenever adding a chunk, check to see which interval you're in and add accordingly
# i.e. {"910590151" : {"10": 5, "20": 3, "30", 0, "40": 8}
userGraphData = {}
# How often (in seconds) we want to plot the data
interval = 10


def round_up(num, divisor):
    return num + (divisor - num % divisor)


def add_to_data(userId, increment):
    if userId not in userGraphData:
        userGraphData[userId] = [("0",0)]
    pastChunksByTime = userGraphData[userId]
    currentTimeInterval = time.time() - startTime
    total = float(pastChunksByTime[len(pastChunksByTime)-1][0]) + currentTimeInterval
    new_count = pastChunksByTime[len(pastChunksByTime)-1][1] + increment
    pastChunksByTime.append((str(total),new_count))
    # else:
    #     total = pastTotal + increment
    #     pastChunksByTime[currentTimeInterval] = total

def check_timeouts():
    while len(clientTimeline.queue) > 0:
        head = clientTimeline.queue[0]
        if head[0] > time.time():
            curr = clientTimeline.get()
            lock.acquire()
            timed_out_chunk = chunkOfUser[curr[1]]
            lock.release()
            # TODO
            # Keep track of which ids timeout and refuse their next chunk report
            # i.e. don't accept their solution if they report True
            lock.acquire()
            chunkOfUser[curr[1]] = None
            lock.release()
            computeStack.append(timed_out_chunk)
        else:
            break

            # check timeouts every 30 seconds


# call_freq = 30.0
# t = threading.Timer(call_freq, check_timeouts)
# t.daemon = True  # finish when main finishes
# t.start()


def make_three_sum(clauses=1000, variables=32):
    equation = []
    for i in range(clauses):
        X0 = randint(1, variables) * sample(set([1, -1]), 1)[0]
        X1 = randint(1, variables) * sample(set([1, -1]), 1)[0]
        while (X1 == X0):
            X1 = randint(1, variables) * sample(set([1, -1]), 1)[0]
        X2 = randint(1, variables) * sample(set([1, -1]), 1)[0]
        while (X2 == X1 or X2 == X0):
            X2 = randint(1, variables) * sample(set([1, -1]), 1)[0]
        equation.append([X0, X1, X2])
    return equation


def solveable_three_sum(clauses=1000, variables=32):
    equation = []
    literal_map = {}
    for i in range(clauses):
        current_var = []
        X0 = assign_variable(literal_map, current_var, variables)
        current_var.append(X0)
        X1 = assign_variable(literal_map, current_var, variables)
        current_var.append(X1)
        X2 = assign_variable(literal_map, current_var, variables)

        equation.append([X0, X1, X2])

    return equation


def assign_variable(literal_map, current_var, variable_num):
    variable = randint(1, variable_num)

    if abs(variable) in literal_map:
        variable = literal_map[abs(variable)]
    else:
        variable = variable * sample(set([1, -1]), 1)[0]
        literal_map[abs(variable)] = variable

    while variable in current_var:
        variable = randint(1, variable_num)

        if abs(variable) in literal_map:
            variable = literal_map[abs(variable)]
        else:
            variable = variable * sample(set([1, -1]), 1)[0]
            literal_map[abs(variable)] = variable

    return variable


def get_chunks(chunk_size, total_size):
    chunks = []
    cur = 0
    while (cur <= total_size):
        chunks.append((cur, cur + chunk_size))
        cur += chunk_size
    return chunks


def get_chunks_formatted(chunk_size, total_size, equation, num_var):
    chunks = []
    cur = 0
    while (cur <= total_size):
        chunks.append({'start': cur, 'stop': cur + chunk_size, 'equation': equation, 'num_variables': num_var})
        cur += chunk_size
    return chunks


def try_permutation(equation, curr, num_variables):
    variables = []
    for i in range(num_variables):
        literal = curr % 2
        if literal == 0:
            literal = -1
        variables.append((i + 1) * literal)
        curr = curr // 2

    for clause in equation:
        l0 = clause[0]
        l1 = clause[1]
        l2 = clause[2]
        ass0 = variables[abs(l0) - 1]
        ass1 = variables[abs(l1) - 1]
        ass2 = variables[abs(l2) - 1]
        if l0 != ass0 or l1 != ass1 or l2 != ass2:
            return False

    return True


equation = solveable_three_sum(clauses, variables)
#    equation = make_three_sum(clauses)
chunks = get_chunks_formatted(2 ** 12, 2 ** variables, equation, variables)
computeStack = chunks


@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'GET':
        lock.acquire()
        userId = request.args.get('id')
        # if they didn't specify a user id, they're unauthorized
        if userId is None or userId not in chunkOfUser:
            return "invalid user id " + userId + " " + str(chunkOfUser), 401
        # they're in our system and already working on a compute part, so don't assign them a new one
        if chunkOfUser[userId] is not None:
            print(3)
            return jsonify({'start': None, 'stop': None, 'equation': None}), 200
        # if there are no more hashes left
        if len(computeStack) < 1:
            return jsonify({'start': -1, 'stop': -1, 'equation': []}), 200
        # get their compute load and document it
        computeDatum = computeStack.pop()
        chunkOfUser[userId] = computeDatum
        lock.release()
        # add their load to the priority queue
        clientTimeline.put(time.time() + COMP_TIME_LIMIT, userId)
        # send the value
        return jsonify(computeDatum)
    elif request.method == 'POST':
        # print(request.data)
        # data = request.get_json()
        data = json.loads(request.data)
        userId = request.args.get('id')
        # if they didn't specify a user id, they're unauthorized
        # print(data)
        if userId is None or userId is '' or 'result' not in data:
            chunkOfUser[userId] = None
            return jsonify({}), 401
        lock.acquire()
        chunkOfUser[userId] = None
        lock.release()
        print(data['result'])
        if 'result' in data and 'solution' in data:
            print("WE MADE IT")
            add_to_data(userId, 1)
            solution = data['solution']
            if 'result' in data and data['result'] == True:
                send_sms(solution)
            return jsonify({}), 200


@app.route('/api/id', methods=['GET'])
def api_id():
    if request.method == 'GET':
        userId = str(uuid.uuid4())
        lock.acquire()
        chunkOfUser[userId] = None
        lock.release()
        return userId


@app.route('/api/graphData', methods=['GET'])
def api_graph_data():
    if request.method == 'GET':
        return jsonify(userGraphData)
# dictionary that maps user id to another dictionary
# this second one maps each time interval (every 10 seconds since startTime)
# to the number of chunks done. so whenever adding a chunk, check to see which interval you're in and add accordingly
# i.e. {"910590151" : {"10": 5, "20": 3, "30", 0, "40": 8}
# example: {'7e8ebe47-b27c-4545-9935-bae6ce293e77': {'0': 0, 'total': 4, '110.0': 1, '120.0': 2, '130.0': 3, '140.0': 4}, '70c1130d-e887-40d5-98f1-e3aaae2d8dd2': {'0': 0, 'total': 1, '150.0': 1}}

@app.route('/api/reset', methods=['GET'])
def api_reset():
    if request.method == 'GET':
        global clientTimeline
        clientTimeline = PriorityQueue()
        global chunkOfUser
        chunkOfUser = {}
        global equation
        equation = []
        global chunks
        chunks = []
        global computeStack
        computeStack = []
        return jsonify({}), 200


def send_sms(msg):
    print("WOW WE MADE IT TO THE END")
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="+15166100458",
        from_="+15017649009",
        body="EUREKA! The solution is SUPER FOUND!"
    )


if __name__ == '__main__':
    app.debug = True
    app.run()
    # check timeouts every 30 seconds
    call_freq = 30.0
    t = threading.Timer(call_freq, check_timeouts)
    t.daemon = True  # finish when main finishes
    t.start()
    app.run()
