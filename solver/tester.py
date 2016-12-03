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

NUM_TESTS = 41
PROBLEM = -1
DRAW = False

def main():
    global NUM_TESTS
    global PROBLEM

    parse_args()

    total_time = 0
    total_correct = 0
    if (PROBLEM == -1):
        for test_id in range(NUM_TESTS):
            print("--- Running Test " +str(test_id)+ " ---")
            succ, time_taken = run_test(test_id, nonogram_csp.nonogram_csp_model, orderings.val_lcv, orderings.ord_dh)
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
        succ, time_taken = run_test(test_id, nonogram_csp.nonogram_csp_model, orderings.val_lcv, orderings.ord_dh)
        total_time += time_taken
        
        succ_str = "Failed"
        if(succ):
            total_correct += 1
            succ_str = "Passed"
        print("Test " + str(test_id) + " " + succ_str + " after " + str(time_taken) + " seconds")


def run_test(test_id, model, value_ordering, variable_ordering):
    global DRAW

    row, col = getProblem(test_id)

    start = time.time()
    succ = False
    
    csp, var_array = model(row, col)
    solver = BT(csp)
    succ = solver.bt_search(prop_BT, variable_ordering, value_ordering)

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

    for row in range(0,num_row):
        draw_row([variable_array[row][i] for i in range(0, num_col)])

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
    global PROBLEM
    global DRAW

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--problem_num', type=int, help='problem number to solve')
    parser.add_argument('--draw', dest='draw', action='store_true', help='draw solution')
    parser.set_defaults(draw=False)

    args = parser.parse_args()
    if args.problem_num is not None:
        PROBLEM = args.problem_num
    DRAW = args.draw
        
if __name__=="__main__":
    main()