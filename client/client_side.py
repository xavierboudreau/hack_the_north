import urllib.parse
import urllib.request
import psutil
import json
import sys

def get_id(server_url):
	get_request = "{}/{}/{}".format(server_url, 'api','id')
	content = urllib.request.urlopen(get_request).read()
	id = content.decode("utf-8")
	#extract id and status code
	return id

def get_chunk(server_url):
	'''
	Returns int start, int stop, list<list<int>> equation
	Each variable x1, x2, x3, etc will be represented by 1, 2, 3, etc
	A negative int represents the complement
	e.g. -1 represents (NOT x1)
	'''
	parameters = urllib.parse.urlencode({"id": id})
	parameters = parameters.encode("utf-8")
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
			sys.exit()
		except KeyError:
			print(error_message.format("equations"))
			sys.exit()

		return start, stop, equation


	except json.JSONDecodeError:
		print("COULDN'T DESERIALIZE CHUNK. FAILING NOW")
		sys.exit()


def send_result(server_url, result, solution):
	server_url = "{}/{}".format(server_url, "data")
	data = urllib.parse.urlencode({"id": id, "result": result, "solution": solution})
	data = data.encode("utf-8")
	request = urllib.request.Request(server_url, data)
	content = urllib.request.urlopen(request).read()

	#extract and return result code
	return content


def monitor_extra_usage():
	while(True):
		print(psutil.cpu_percent(interval=1))
		if (psutil.cpu_percent(interval=1) > 15):
			return true;


def solve_chunk(equation, start, stop,num_variables):
	while (monitor_extra_usage != true)
	    curr = start
	    while curr < stop:
	        if try_permutation(equation, curr, num_variables):
	            return True
	        curr += 1

	    return False
	exit()


def try_permutation(equation,curr,num_variables):
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
            return False

    return True


def main():
	server_url = "https://sadx-miner.herokuapp.com"
	id = get_id(server_url)
	chunk = get_chunk()
	#assume we get None when there are no more chunks to process
	while chunk != None:
		#TODO get equation, start, stop, num_variables from server response
		result, solution = solve_chunk(equation, start, stop, num_variables)
		recieved = False
		while not received:
			code = send_result()
			#update received based on code
			received = -99

	#for now just terminate when we don't have a chunk to process
	#later we can wait and check for a new one

if __name__ == "__main__":
	#main()
	server_url = "https://sadx-miner.herokuapp.com"
	get_id(server_url)