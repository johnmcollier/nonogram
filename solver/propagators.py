'''
This file will contain different constraint propagators to be used within
bt_search.

propagator == a function with the following template
    propagator(csp, newly_instantiated_variable=None)
        ==> returns (True/False, [(Variable, Value), (Variable, Value) ...])

Consider implementing propagators for forward cehcking or GAC as a course project!        

'''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    pruned_vals = []
    if not newVar:
        return True, pruned_vals
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 1:
            unassigned_vars = c.get_unasgn_vars()
            unassigned_var = unassigned_vars[0]

            for val in unassigned_var.cur_domain():
                has_support = c.has_support(unassigned_var, val)
                if(not has_support):
                    pruned_vals.append((unassigned_var, val))

        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, pruned_vals

def prop_GAC(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    pruned_vals = []
    if not newVar:
        return True, pruned_vals

    gac_que = []
    for c in csp.get_cons_with_var(newVar):
        gac_que.append(c)

    # GAC enforce
    while(len(gac_que) != 0):
        c = gac_que.pop(0)
        for v in c.get_scope():
            for d in v.cur_domain():
                has_support = c.has_support(v, d)
                if(not has_support):
                    v.prune_value(d)
                    pruned_vals.append((v, d))

                    if(len(v.cur_domain()) == 0):
                        return False, pruned_vals
                    else:
                        for c_prime in csp.get_cons_with_var(v):
                            if c_prime not in gac_que:
                                gac_que.append(c_prime)

    # Check each CSP is satisfied
    for c in csp.get_cons_with_var(newVar):
        # Check constraint is satisfied
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, pruned_vals
    return True, pruned_vals
