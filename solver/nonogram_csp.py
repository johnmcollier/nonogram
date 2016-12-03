#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the nonogram models.  

'''
Construct and return nonogram CSP models.
'''

from cspbase import *
import itertools

def nonogram_csp_model(nonogram_rows, nonogram_columns):
    '''Return a CSP object representing a nonogram CSP problem along 
       with an array of variables for the problem. That is return

       nonogram_csp, variable_array

       where nonogram_csp is a csp representing the nonogram game and
       variable_array is an n by n matrix representing each cell in the
       game.
       
       The input rows and columns specify which cells in each row or column
       that need to be coloured in.
       
       This routine returns a model which consists of a variable for
       each cell of the board, with domain equal to {0,1}, with 0 being
       not coloured and 1 being coloured.
    '''

    n = len(nonogram_rows)
    m = len(nonogram_columns)

    # Create CSP object
    nonogram_csp = CSP("Model_david")

    # Create variable array
    # variable_array[i][j] corresponds to the row i column j cell
    variable_array = []
    for i in range(0, n):
        variable_array.append([])
        for j in range(0, m):
            name = 'V' + str(i+1) + "," + str(j+1)
            variable_array[i].append(Variable(name, [0, 1]))
            nonogram_csp.add_var(variable_array[i][j])

    # Create constraints
    # Row constraints
    for i in range(0, n): # row index
        name = 'Row ' + str(i)
        constraint = Constraint(name, [variable_array[i][j] for j in range(0, m)])
        valid_tuples = []
        get_valid_nary_tuples(m, nonogram_rows[i], valid_tuples)
        constraint.add_satisfying_tuples(valid_tuples)
        nonogram_csp.add_constraint(constraint)
    
    # Column constraints
    for i in range(0, m): # column index
        name = 'Column ' + str(i)
        constraint = Constraint(name, [variable_array[j][i] for j in range(0, n)])
        valid_tuples = []
        get_valid_nary_tuples(n, nonogram_columns[i], valid_tuples)
        constraint.add_satisfying_tuples(valid_tuples)
        nonogram_csp.add_constraint(constraint)

    return nonogram_csp, variable_array


def get_valid_nary_tuples(_span, _constraint, valid_tuples, current_tuple=[]):
    span = _span
    constraint = list(_constraint)
    #print(_span)
    #print(current_tuple)

    if(span == 0):
        if(len(constraint) == 0):
            valid_tuples.append(current_tuple)
        return

    # Either pop a constraint, or assign a 0
    # Assign 0
    temp = list(current_tuple)
    temp.append(0)
    get_valid_nary_tuples(span-1, constraint, valid_tuples, temp)

    # Pop constraint
    if(len(constraint) != 0):
        temp = list(current_tuple)
        top_constraint = constraint.pop(0)
        if (top_constraint > span):
            # con't fit constraint
            return
        for i in range(top_constraint):
            # "Color in" the specified number
            temp.append(1)
        span -= top_constraint

        if(span > 0):
            # If there is space left, there must be a gap
            temp.append(0)
            span -= 1

        get_valid_nary_tuples(span, constraint, valid_tuples, temp)
##############################

