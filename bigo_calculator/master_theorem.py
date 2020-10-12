import sympy
n = sympy.Symbol('n', positive=True, even=True)

def master_theorem(main_TC, rest_TC):
    if sympy.oo in main_TC:
        #print(sympy.oo)
        return sympy.oo

    final_TC = []
    for m_list, r_list in zip(main_TC, rest_TC):

        #rest_TC
        r_tc = PowOfN_Transform(r_list)
        #r_var_list = set()
        #for symbol in r_list.free_symbols:
        #    r_var_list.update([(symbol, sympy.oo)])
        #    #r_var_list.update([(symbol, n)])
        #r_tc = sympy.O(r_list.subs(r_var_list), *{(n, sympy.oo)}).args[0]
        #r_tc = sympy.O(r_list, *r_var_list).args[0]

        #main_TC
        SUB_coeff, DIV_coeff = 0, 0 
        for coeff in m_list.free_symbols:
            if coeff.name == 'SUB':
                SUB_coeff = m_list.expand().coeff(coeff)
            if coeff.name == 'DIV':
                DIV_coeff = m_list.expand().coeff(coeff)

        #print('Main: ', SUB_coeff, DIV_coeff, 'Rest: ', r_tc)
        #print(MT_SUB(SUB_coeff, r_tc))
        if SUB_coeff:
            final_TC.append(MT_SUB(SUB_coeff, r_tc))
        elif DIV_coeff:
            final_TC.append(MT_DIV(DIV_coeff, r_tc))
        else:
            final_TC.append(r_tc)
    #print(max_of_final_TC(final_TC))
    return max_of_final_TC(final_TC)


def PowOfN_Transform(tc):
    var_list = set()
    for symbol in tc.free_symbols:
        var_list.update([(symbol, n)])

    result = sympy.O(tc.subs(var_list), *{(n, sympy.oo)}).args[0]
    if type(result) == sympy.exp:
        return 2**n
    else:
        return result

def MT_SUB(coeff, r_tc):
    if coeff == sympy.numbers.One:
        return r_tc*n
        #T(n) = 1*T(n-1) + f(n)
        #5 situation:1, 1/n, logn, n, nlogn, n**

    else:
        #T(n) = coeff*T(n-1) + f(n)
        return (coeff)**n

def MT_DIV(coeff, r_tc):
    bigger_tc = sympy.O(n**(sympy.log(coeff, 2)) + r_tc, (n, sympy.oo)).args[0]
    return bigger_tc*sympy.log(n)

def max_of_final_TC(final_TC):
    result = 0
    for tc in final_TC:
        result += tc

    return PowOfN_Transform(result)
