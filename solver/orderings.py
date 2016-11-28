#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random

'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    ord_type(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    ord_type returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''


def ord_random(csp):
    '''
    ord_random(csp):
    A var_ordering function that takes a CSP object csp and returns a Variable object var at random.  var must be an unassigned variable.
    '''
    var = random.choice(csp.get_all_unasgn_vars())
    return var


def val_arbitrary(csp,var):
    '''
    val_arbitrary(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a value in var's current domain arbitrarily.
    '''
    return var.cur_domain()


def ord_mrv(csp):
    '''
    ord_mrv(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var, 
    according to the Minimum Remaining Values (MRV) heuristic as covered in lecture.  
    MRV returns the variable with the most constrained current domain 
    (i.e., the variable with the fewest legal values).
    '''
#IMPLEMENT
    all_unassigned_vars = csp.get_all_unasgn_vars()
    min_domain_size = -1

    for var in all_unassigned_vars:
        current_domain_size = var.cur_domain_size()
        if (min_domain_size == -1 or current_domain_size < min_domain_size):
            ret = var
            min_domain_size = current_domain_size

    return ret

def ord_dh(csp):
    '''
    ord_dh(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to the Degree Heuristic (DH), as covered in lecture.
    Given the constraint graph for the CSP, where each variable is a node, 
    and there exists an edge from two variable nodes v1, v2 iff there exists
    at least one constraint that includes both v1 and v2,
    DH returns the variable whose node has highest degree.
    '''    
#IMPLEMENT
    all_unassigned_vars = csp.get_all_unasgn_vars()
    connection_matrix = []
    for i in range(0, len(all_unassigned_vars)):
        connection_matrix.append([0] * len(all_unassigned_vars))
    max_degree = -1

    for constraint in csp.get_all_cons():
        scope = constraint.get_scope()
        for i, var1 in enumerate(all_unassigned_vars):
            for j, var2 in enumerate(all_unassigned_vars):
                if(i < j):
                    in_scope = (var1 in scope) and (var2 in scope)
                    if(in_scope):
                        connection_matrix[i][j] = 1
                        connection_matrix[j][i] = 1
    degree_list = []
    for i in range(0, len(all_unassigned_vars)):
        degree_list.append(sum(connection_matrix[i]))
    ret = all_unassigned_vars[degree_list.index(max(degree_list))]

    return ret

def val_lcv(csp,var):
    '''
    val_lcv(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a list of Values [val1,val2,val3,...]
    from var's current domain, ordered from best to worst, evaluated according to the 
    Least Constraining Value (LCV) heuristic.
    (In other words, the list will go from least constraining value in the 0th index, 
    to most constraining value in the $j-1$th index, if the variable has $j$ current domain values.) 
    The best value, according to LCV, is the one that rules out the fewest domain values in other 
    variables that share at least one constraint with var.
    '''    
#IMPLEMENT
    value_constraint_pairs = []

    # Count number of values in the domain of other variables unavailable before assignment
    values_unavailable_before_assignment = 0
    for constraint in csp.get_all_cons():
        scope = constraint.get_scope()
        if (var in scope):
            for other_var in csp.get_all_unasgn_vars():
                if(other_var in scope):
                    if (other_var != var):
                        for other_value in other_var.cur_domain():
                            if (not constraint.has_support(other_var, other_value)):
                                values_unavailable_before_assignment += 1

    # Count the number of values unavailble after assignment of each 
    for value in var.cur_domain():
        # Assign Value
        var.assign(value)

        # Count number of values unavailable after assignment
        values_unavailable_after_assignment = 0
        for constraint in csp.get_all_cons():
            scope = constraint.get_scope()
            if (var in scope):
                for other_var in csp.get_all_unasgn_vars():
                    if(other_var in scope):
                        for other_value in other_var.cur_domain():
                            if (not constraint.has_support(other_var, other_value)):
                                values_unavailable_after_assignment += 1

        # Calculate the number of values eliminated when assigning this variable
        values_eliminated = values_unavailable_after_assignment - values_unavailable_before_assignment
        
        # Unassign value
        var.unassign()

        # Add to list
        if not value_constraint_pairs:
            value_constraint_pairs.append((value, values_eliminated))
        else:
            # Find insertion point
            assigned = False
            for i in range(0, len(value_constraint_pairs)):
                if (values_eliminated < value_constraint_pairs[i][1]):
                    # Current value eliminates less values
                    value_constraint_pairs.insert(i, (value, values_eliminated))
                    assigned = True
                    break
            if (not assigned):
                value_constraint_pairs.append((value, values_eliminated))

    # Return list
    ordered_list = []
    for i in range(0, len(value_constraint_pairs)):
        ordered_list.append(value_constraint_pairs[i][0])
    return ordered_list

def ord_custom(csp):
    '''
    ord_custom(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to a Heuristic of your design.  This can be a combination of the ordering heuristics 
    that you have defined above.
    '''    
#IMPLEMENT

    # DH heuristic
    # Re-implement instead of calling function to use connection_matrix
    all_unassigned_vars = csp.get_all_unasgn_vars()
    connection_matrix = []
    for i in range(0, len(all_unassigned_vars)):
        connection_matrix.append([0] * len(all_unassigned_vars))
    max_degree = -1

    for constraint in csp.get_all_cons():
        scope = constraint.get_scope()
        for i, var1 in enumerate(all_unassigned_vars):
            for j, var2 in enumerate(all_unassigned_vars):
                if(i < j):
                    in_scope = (var1 in scope) and (var2 in scope)
                    if(in_scope):
                        connection_matrix[i][j] = 1
                        connection_matrix[j][i] = 1
    degree_list = []
    for i in range(0, len(all_unassigned_vars)):
        degree_list.append(sum(connection_matrix[i]))

    # MRV heuristic
    rv_list = []
    for var in all_unassigned_vars:
        current_domain_size = var.cur_domain_size()
        rv_list.append(current_domain_size)

    # Use a heuristic to choose "best" variable given degree and remaining values
    # Divide dh by remaining values
    heuristic_list = []
    for i in range(0, len(all_unassigned_vars)):
        heuristic_list.append(degree_list[i] / rv_list[i])
    
    ret = all_unassigned_vars[heuristic_list.index(max(heuristic_list))]
    return ret

