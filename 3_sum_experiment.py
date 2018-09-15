from random import randint
from random import sample

def make_three_sum(clauses = 1000, variables = 32):
    equation = []
    for i in range(clauses):
        X0 = randint(1, variables) * sample(set([1,-1]), 1)[0]
        X1 = randint(1, variables) * sample(set([1,-1]), 1)[0]
        while (X1 == X0):
            X1 = randint(1, variables) * sample(set([1,-1]),1)[0]
        X2 = randint(1, variables) * sample(set([1,-1]), 1)[0]
        while (X2 == X1 or X2 == X0):
            X2 = randint(1, variables) * sample(set([1,-1]), 1)[0]
        equation.append([X0, X1, X2])
    return equation

def solveable_three_sum(clauses = 1000, variables = 32):
    equation = []
    literal_map = {}
    for i in range(clauses):
        current_var = []
        X0 = assign_variable(literal_map,current_var,variables)
        current_var.append(X0)
        X1 = assign_variable(literal_map,current_var,variables)
        current_var.append(X1)
        X2 = assign_variable(literal_map,current_var,variables)

        equation.append([X0, X1, X2])

    return equation

def assign_variable(literal_map,current_var,variable_num):

    variable = randint(1,variable_num)

    if abs(variable) in literal_map:
        variable = literal_map[abs(variable)]
    else:
        variable = variable * sample(set([1,-1]),1)[0]
        literal_map[abs(variable)] = variable

    while variable in current_var:
        variable = randint(1,variable_num)

        if abs(variable) in literal_map:
            variable = literal_map[abs(variable)]
        else:
            variable = variable * sample(set([1,-1]),1)[0]
            literal_map[abs(variable)] = variable

    return variable



def get_chunks(chunk_size,total_size):
    chunks = []
    cur = 0
    while (cur <= total_size):
        chunks.append((cur,cur+chunk_size))
        cur += chunk_size
    return chunks 


def master():
    clauses = 10
    variables = 24
    chunks = get_chunks(2**10,2**24)
#    equation = make_three_sum(clauses)
    equation = solveable_three_sum(clauses,variables)
    for chunk in chunks:
        if client(equation,chunk[0],chunk[1],variables):
            print("YAY")
            return

    print("BOO")
    return


def client(equation, start, stop,num_variables):
    #tests three sum from (start,stop]

    curr = start
    while curr < stop:
        if try_permutation(equation, curr,num_variables):
            return True
        curr += 1

    return False

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

if __name__ == "__main__":
    master()
