import sympy

n = sympy.Symbol("n")

def master_theorom(tc_list, tc_list_else):
    add_sub = tc_list[0]
    mul_div = tc_list[1]

    if add_sub > 0:
        #there is T(n) = T(n-1)
        if add_sub == 1:
            #4 situation:1, logn, n, nlogn, n**
            if tc_list_else == 1:
                return n
            elif type(tc_list_else) == sympy.log:
                return sympy.log(sympy.factorial(n))
            elif tc_list_else == n:
                return n*n
            elif type(tc_list_else) == sympy.Mul:
                if type(tc_list_else.args[0]) == sympy.Symbol:
                    return n*tc_list_else
                if type(tc_list_else.args[0]) == sympy.Pow:
                    if tc_list_else.args[0].args[1] > 1:
                        return n*tc_list_else
                    elif tc_list_else.args[0].args[1] == -1:
                        return sympy.log(n)**2
                    elif tc_list_else.args[0].args[1] < -1:
                        return sympy.log(n)
            elif type(tc_list_else) == sympy.Pow:
                if tc_list_else.args[1] <= -1:
                    return sympy.log(n)
                elif tc_list_else.args[1] > 1:
                    return n**(tc_list_else.args[1]+1)
            else:
                return 0
        else:
            #only 1 situation:
            return add_sub**n

    else:
        #there is T(n) = T(n/2)
        pass


print(master_theorom([1, 0], n**2*sympy.log(n)))
