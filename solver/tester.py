import sys
import time
from cspbase import *
from propagators import *
import itertools
import traceback
import orderings
import nonogram_csp
import argparse
from problems import *

NUM_TESTS = 42
PROBLEM = -1
DRAW = False

MODEL = nonogram_csp.nonogram_csp_model
PROPAGATOR = prop_GAC
VARIABLE_ORDERING = orderings.ord_mrv
VALUE_ORDERING = orderings.val_lcv

def main():
    global NUM_TESTS
    global PROBLEM

    parse_args()

    total_time = 0
    total_correct = 0
    if (PROBLEM == -1):
        for test_id in range(NUM_TESTS):
            print("--- Running Test " +str(test_id)+ " ---")
            succ, time_taken = run_test(test_id)
            total_time += time_taken
            
            succ_str = "Failed"
            if(succ):
                total_correct += 1
                succ_str = "Passed"
            print("Test " + str(test_id) + " " + succ_str + " after " + str(time_taken) + " seconds")
        print("\nFinal results: " + str(total_correct) + "/" + str(NUM_TESTS) + " solved in " + str(total_time) + " seconds")
    else:
        test_id = PROBLEM
        print("--- Running Test " +str(test_id)+ " ---")
        succ, time_taken = run_test(test_id)
        total_time += time_taken
        
        succ_str = "Failed"
        if(succ):
            total_correct += 1
            succ_str = "Passed"
        print("Test " + str(test_id) + " " + succ_str + " after " + str(time_taken) + " seconds")


def run_test(test_id):
    global MODEL
    global PROPAGATOR
    global VARIABLE_ORDERING
    global VALUE_ORDERING

    global DRAW

    row, col = getProblem(test_id)

    start = time.time()
    succ = False
    
    csp, var_array = MODEL(row, col)
    solver = BT(csp)
    succ = solver.bt_search(PROPAGATOR, VARIABLE_ORDERING, VALUE_ORDERING)

    time_taken = (time.time() - start)

    if (succ):
        succ = check_solution(var_array, row, col)

    if(DRAW):
        draw_solution(var_array)

    return succ, time_taken

def check_solution(variable_array, row, col):
    n = len(row)
    m = len(col)

    succ = True

    for row_num in range(0,n):
        my_row = get_row_constraint_from_var([variable_array[row_num][i] for i in range(0, m)])
        if(my_row != row[row_num]):
            succ = False
            break;
    for col_num in range(0,m):
        my_col = get_row_constraint_from_var([variable_array[i][col_num] for i in range(0, n)])
        if(my_col != col[col_num]):
            succ = False
            break;

    return succ

def get_row_constraint_from_var(variable_array):
    constraint = []
    num_vars = len(variable_array)

    consecutive = 0
    for i in range(0, num_vars):
        current = variable_array[i].get_assigned_value()
        if(current == 0):
            if(consecutive != 0):
                constraint.append(consecutive)
            consecutive = 0
        else:
            consecutive += 1

    if(consecutive != 0):
        constraint.append(consecutive)

    if(len(constraint) == 0):
        constraint.append(0)

    return constraint

def draw_solution(variable_array):
    num_row = len(variable_array)
    num_col = len(variable_array[0])

    print("")
    
    for row in range(0,num_row):
        draw_row([variable_array[row][i] for i in range(0, num_col)])
    
    print("")

def draw_row(row):
    num_vars = len(row)
    drawing = ""

    for i in range(0, num_vars):
        if(drawing != ""):
            drawing = drawing + " "

        current = row[i].get_assigned_value()
        if(current == 0):
            drawing = drawing + "□"
        else:
            drawing = drawing + "■"

    print(drawing)

def parse_args():
    global MODEL
    global PROPAGATOR
    global VARIABLE_ORDERING
    global VALUE_ORDERING
    global PROBLEM
    global DRAW

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--problem', type=int, help='problem number to solve')
    parser.add_argument('--draw', dest='draw', action='store_true', help='draw solution')
    parser.add_argument('--model', choices=['model1'], default='model1', help='select model')
    parser.add_argument('--propagator', choices=['bt', 'fc', 'gac'], default='gac', help='select propagator')
    parser.add_argument('--var_ordering', choices=['random', 'mrv', 'dh', 'custom'], default='mrv', help='select variable ordering heuristic')
    parser.add_argument('--val_ordering', choices=['arbitrary', 'lcv'], default='lcv', help='select value ordering heuristic')
    parser.set_defaults(draw=False)

    args = parser.parse_args()

    if args.problem is not None:
        PROBLEM = args.problem
    
    DRAW = args.draw

    model = args.model
    if(model == 'model1'):
        MODEL = nonogram_csp.nonogram_csp_model

    propagator = args.propagator
    if(propagator == 'bt'):
        PROPAGATOR = prop_BT
    elif(propagator == 'fc'):
        PROPAGATOR = prop_FC
    elif(propagator == 'gac'):
        PROPAGATOR = prop_GAC

    var_ordering = args.var_ordering
    if(var_ordering == 'random'):
        VARIABLE_ORDERING = orderings.ord_random
    elif(var_ordering == 'mrv'):
        VARIABLE_ORDERING = orderings.ord_mrv
    elif(var_ordering == 'dh'):
        VARIABLE_ORDERING = orderings.ord_dh
    elif(var_ordering == 'custom'):
        VARIABLE_ORDERING = orderings.ord_custom

    val_ordering = args.val_ordering
    if(val_ordering == 'arbitrary'):
        VALUE_ORDERING = orderings.val_arbitrary
    elif(val_ordering == 'lcv'):
        VALUE_ORDERING = orderings.val_lcv

    
        
if __name__=="__main__":
    main()