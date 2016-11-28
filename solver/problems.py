
def getProblem(problem_num):
    if(problem_num == 0):
        return getProblem0
    if(problem_num == 1):
        return getProblem1

def getProblem0():
    row = [[1], [3], [1]]
    col = [[1], [3], [1]]
    return row, col

def getProblem1():
    row = [[1,1], [3], [1,1]]
    col = [[3], [1], [3]]
    return row, col
