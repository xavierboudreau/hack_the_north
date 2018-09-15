from random import randint

def make_three_sum(clauses = 10):
	equation = []
	#let 0 represent not, 1 represent regular variable
	for i in range(clauses):
		X0 = randint(0,1)
		X1 = randint(0,1)
		X2 = randint(0,1)
		equation.append((X0, X1, X2))
	return equation

def get_chunks(clauses, chunk_size):
	input_size = 2**(3*clauses)
	num_chunk_size_chunks = input_size//chunk_size
	partial_chunk = input_size%chunk_size
	return num_chunk_size_chunks, partial_chunk
	
def master():
	clauses = 10
	chunk_size = 10000000
	equation = make_three_sum(clauses)
	print(equation)
	num_chunks, partial_chunk_size = get_chunks(clauses, chunk_size)
	sum_ = partial_chunk_size + num_chunks*chunk_size
	
	result = False
	
	if (client(equation, 0, partial_chunk_size-1)):
		result = True
		return result
	curr = partial_chunk_size
	for i in range(num_chunks):
		if client(equation, curr, curr+chunk_size-1):
			result = True
			return result
	
	return result
	
def try_permutation(equation, bin_array):
	i = 0
	for clause in equation:
		T1 = bin_array[i] == clause[0]
		T2 = bin_array[i+1] == clause[1]
		T3 = bin_array[i+2] == clause[1]
		result = T1 or T2 or T3
		if not result:
			return False
		i += 3
	print(bin_array)
	return True

def to_binary(dec, num_terms):
	#won't work I need the clause length
	base = [int(x) for x in bin(dec)[2:]]
	zero_pad = [0 for i in range(num_terms-len(base))]
	result = zero_pad + base
	return result

def client(equation, start, stop):
	#tests three sum from start to stop (inclusive)
	success = False
	
	curr = start
	num_terms = len(equation)*3
	while curr <= stop:
		curr_binary = to_binary(curr, num_terms)
		if try_permutation(equation, curr_binary):
			success = True
			return success
		curr += 1
	
	return success
	
if __name__ == "__main__":
	m = master()
	print(m)
	