import urllib.parse
import urllib.request
import psutil

def get_id(server_url):
	get_request = "{}/{}".format(server_url, 'id')
	content = urllib.urlrequest.urlopen(get_request).read()
	#extract id and status code
	
def get_chunk(server_url):
	parameters = urllib.parse.urlencode({"id": id})
	parameters = parameters.encode("utf-8")
	get_request = "{}/{}?{}".format(server_url, 'data', parameters)
	content = urllib.urlrequest.urlopen(get_request).read()
	
	#extract chunk, we don't know what this looks like yet
	#we want to return None if there was no chunk provided
	return content

def send_result(server_url, result, solution):
	server_url = "{}/{}".format(server_url, "data")
	data = urllib.parse.urlencode({"id": id, "result": result, "solution": solution})
	data = data.encode("utf-8")
	request = urllib.request.Request(server_url, data)
	content = urllib.request.urlopen(request).read()
	
	#extract and return result code
	return content
	
def solve_chunk():
	pass

def main():
	id = get_id()
	chunk = get_chunk()
	#assume we get None when there are no more chunks to process
	while chunk != None:
		result, solution = solve_chunk(chunk)
		recieved = False
		while not received:
			code = send_result()
			#update received based on code
			received = ?
	
	#for now just terminate when we don't have a chunk to process
	#later we can wait and check for a new one
	
	

if __name__ == "__main__":
	main()