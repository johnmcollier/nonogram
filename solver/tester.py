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

NUM_TESTS = 2
PROBLEM = -1

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

    print("\nFinal results: " + str(total_correct) + "/" + str(NUM_TESTS) + " solved in " + str(total_time) + " seconds")

def run_test(test_id, model, value_ordering, variable_ordering):
    row, col = getProblem(test_id)

    start = time.time()
    succ = False
    
    csp, var_array = model(row, col)
    solver = BT(csp)
    #solver.bt_search(prop_BT, variable_ordering, value_ordering)

    #if check_solution(var_array):
    #    succ = True

    time_taken = (time.time() - start)
    return succ, time_taken

def parse_args():
    global PROBLEM

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--problem_num', type=int, help='problem number to solve')

    args = parser.parse_args()
    if(args.problem_num):
        PROBLEM = args.problem_num

if __name__=="__main__":
    main()