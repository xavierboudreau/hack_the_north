import psutil

def get_id():
	pass
	
def get_chunk():
	pass

def send_result():
	pass

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