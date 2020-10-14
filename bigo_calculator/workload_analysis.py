import collections
import sympy

'''
Analysis work loading of recursive call, and return as TC.

First, analysis arguments to find which arguments affect workload.

'''

def workload_analysis(func_decl_node, func_call):
    affective_arg_index = arg_analysis(func_decl_node, func_call)

    if affective_arg_index:
        if len(affective_arg_index) == 1:
            #Only one arg affect workload: T(n) = T(n-1)
            workload_diff = workload_arg1(func_decl_node, func_call, affective_arg_index)

            return workloadDiff_to_TC(workload_diff)

        elif len(affective_arg_index) == 2:
            #Two args affect workload: T(a, b) = T(a+1, b-1)
            workload_diff = workload_arg2(func_decl_node, func_call, affective_arg_index)

            return workloadDiff_to_TC(workload_diff)

        else:
            #More than 3 args affect workloead.
            #Can't handle. return O(oo)
            return sympy.oo

    else:
        #No arg change
        return sympy.oo




def arg_analysis(func_decl_node, func_call):
    decl_parameter = func_decl_node.parameter
    call_parameter_all = func_decl_node.recursive_call_arg

    affective_arg_index = []
    for call_parameter in call_parameter_all:
        for index, args in enumerate(zip(decl_parameter, call_parameter)):
            if args[0] != args[1]:
                affective_arg_index.append(index)
    affective_arg_index = list(set(affective_arg_index))

    return affective_arg_index

def workload_arg1(func_decl_node, func_call, affective_arg_index):
    head = affective_arg_index[0]
    workload_origin = func_decl_node.parameter[head]
    workload_new = func_call.parameter[head]

    #if isinstance(ast.parse(workload_new, mode='eval').body, ast.Subscript):
    #    subscript = ast.parse(workload_new, mode='eval').body
    #    if subscript.slice.lower:
    #        lower = astunparse.unparse(subscript.slice.lower).replace("\n", "")
    #    else:
    #        lower = 0
    #    if subscript.slice.upper:
    #        upper = astunparse.unparse(subscript.slice.upper).replace("\n", "")
    #    else:
    #        upper = 1
    #    workload_diff = '(' + str(upper) + ') - (' + str(lower) + ')'
    #    print(workload_diff)
    #    workload_diff = sympy.sympify(workload_diff)

    workload_diff = '(' + workload_origin + ') - (' + workload_new + ')'
    #print(workload_diff)
    workload_diff = sympy.sympify(workload_diff)

    return workload_diff


def workload_arg2(func_decl_node, func_call, affective_arg_index):
    head = affective_arg_index[0]
    tail = affective_arg_index[1]
    workload_origin = func_decl_node.parameter[tail] + ' - ' + func_decl_node.parameter[head]
    workload_new = func_call.parameter[tail] + ' - ' + func_call.parameter[head]

    workload_diff = '(' + workload_origin + ') - (' + workload_new + ')'
    workload_diff = sympy.sympify(workload_diff)

    return workload_diff

def workloadDiff_to_TC(workload_diff):
    if workload_diff == 0:
        return sympy.oo
    else:
        if workload_diff.free_symbols:
            #There is at least one symbol in workload_diff. Not constant diff.
            return sympy.Symbol('DIV', integer=True, positive=True)
        else:
            #There is only constant diff in workload_diff.
            return sympy.Symbol('SUB', integer=True, positive=True)
