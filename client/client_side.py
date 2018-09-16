import urllib.parse
import urllib.request
import psutil
import json
import sys
import requests

def get_id(server_url):
    get_request = "{}/{}/{}".format(server_url, 'api','id')
    content = urllib.request.urlopen(get_request).read()
    id = content.decode("utf-8")
    #extract id and status code
    return id

def get_chunk(server_url, id):
    '''
    Returns int start, int stop, list<list<int>> equation
    Each variable x1, x2, x3, etc will be represented by 1, 2, 3, etc
    A negative int represents the complement
    e.g. -1 represents (NOT x1)
    '''
    parameters = urllib.parse.urlencode({"id": id})
    get_request = "{}/{}/{}?{}".format(server_url, 'api', 'data', parameters)
    content = urllib.request.urlopen(get_request).read()
    json_result = content.decode("utf-8")

    try:
        response_table = json.loads(json_result)
        error_message = "COULD NOT FIND \'{}\' IN CHUNK RESPONSE. FAILING NOW"
        try:
            start = response_table["start"]

        except KeyError:
            print(error_message.format("start"))
            sys.exit()

        try:
            stop = response_table["stop"]
        except KeyError:
            print(error_message.format("stop"))
            sys.exit()

        try:
            equation = response_table["equation"]

        except KeyError:
            print(error_message.format("equations"))
            sys.exit()

        return start, stop, equation


    except json.JSONDecodeError:
        print("COULDN'T DESERIALIZE CHUNK. FAILING NOW")
        sys.exit()


def send_result(server_url, result, solution, id):
    parameters = urllib.parse.urlencode({"id": id})
    post_request = "{}/{}/{}?{}".format(server_url, 'api', 'data', parameters)
    requests.post(post_request, json = {'result': result, 'solution': solution})

def monitor_extra_usage():
    #return True if CPU usage is greater than MAX, else false
    MAX = 30
    p = psutil.cpu_percent(interval=1)
    return p > MAX


def solve_chunk(equation, start, stop, num_variables):
    while (not monitor_extra_usage()):
        curr = start
        while curr < stop:
            success, solution = try_permutation(equation, curr, num_variables)
            if success:
                return success, solution
            curr += 1

        return False, None



def try_permutation(equation, curr, num_variables):
    variables = []
    for i in range(num_variables):
        literal = curr % 2
        if literal == 0:
            literal = -1
        variables.append((i+1)*literal)
        curr = curr // 2

    for clause in equation:
        l0 = clause[0]
        l1 = clause[1]
        l2 = clause[2]
        ass0 = variables[abs(l0)-1]
        ass1 = variables[abs(l1)-1]
        ass2 = variables[abs(l2)-1]
        if l0 != ass0 or l1 != ass1 or l2 != ass2:
            return False, None

    return True, variables


def main():
    server_url = "https://sadx-miner.herokuapp.com"
    # server_url = "http://127.0.0.1:5000"
    id = get_id(server_url)
    start, stop, equation = get_chunk(server_url, id)
    #assume we get None when there are no more chunks to process
    while len(equation) != 0:
        result, solution = solve_chunk(equation, start, stop, 16)
        send_result(server_url, result, solution, id)
        start, stop, equation = get_chunk(server_url, id)

        #for now just terminate when we don't have a chunk to process
        #later we can wait and check for a new one

if __name__ == "__main__":
    main()
