import sympy
from collections import Counter

def recursion_time_complexity_calculator(funcParameter, funcCall):
    if len(funcParameter) == 1:
        argment = sympy.Symbol(funcParameter[0])
        time_complexity_list = []
        while funcCall:
            call_list_in_one_road = funcCall.pop(0)
            if call_list_in_one_road:
                time_complexity_list.append(master_theorem_one_arg(argment, call_list_in_one_road, sympy.Symbol('M')))
        print("time_complexity_list: ", time_complexity_list)
        return max_bigO(argment, time_complexity_list)

    elif len(funcParameter) > 1:
        return("Can't handle multi-arguments.")

    else:
        return("No argument.")

def master_theorem_one_arg(arg, call_list, bigo_not_recursion):
    argment = arg
    time_complexity = sympy.Rational(1)
    
    for call_arg in call_list:
        #if T(n) -> T(n/m) => time_complexity += log(n, m)
        if sympy.limit(argment - sympy.sympify(call_arg), argment, sympy.oo) == sympy.oo:
            time_complexity += log(argment, m)
        #if T(n) -> T(n-1) => time_complexity += n
        else:
            time_complexity += argment

    return bigo_not_recursion * time_complexity

def max_bigO(arg, bigO_list):
    time = sympy.Rational(1)
    if bigO_list:
        for bigO in bigO_list:
            time += bigO
    return sympy.O(time, (arg, sympy.oo))
