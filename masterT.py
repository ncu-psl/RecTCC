import sympy
from collections import Counter

#d = {('fibo', ('n',)): [['(n - 1)'], ['(n - 2)']], ('fibo_dp', ('n',)): [['(n - 1)']]}

def master_theorem(d):
    n = sympy.Symbol('n', positive = True)
    change_rate = []
    time_complexity = {}

    for function, call in d.items():
        function_name = function[0]
        time_complexity.update({function_name: sympy(0)})
        function_arg = sympy.Symbol(function[1][0])

        for arg in call:
            call_arg = sympy.sympify(arg[0])
            change_rate.append(sympy.limit(call_arg / function_arg, function, sympy.oo))





#   for k, v in d.items():
#       c = []
#       original_arg = sympy.Symbol(k[1][0])
#       for value in v:
#           funcCall_arg = sympy.sympify(value[0])
#           c.append(sympy.limit(funcCall_arg / original_arg, original_arg, sympy.oo))
#       for b, a in Counter(c).items():
#           print("a, b = ", a, b)
#           if b > 1:
#               print("Time complexity is: ", sympy.Symbol('n') ** (sympy.log(a, b)) * sympy.log(sympy.Symbol('n')))
#           elif b == 1:
#               if a == 1:
#                   print("Time complexity is: ", sympy.log(sympy.Symbol('n')))
#               else:
#                   print("Time complexity is: ", a ** sympy.Symbol('n'))
