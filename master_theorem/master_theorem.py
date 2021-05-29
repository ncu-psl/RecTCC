from ast import NameConstant
from re import T
import sympy
n = sympy.Symbol('n', positive=True, even=True)

def master_theorem(main, partial):
    tc = []
    for (s, d, p) in zip(main[0]['-'], main[0]['/'], partial):
        p_tc = sympy.degree(p, n)
        #'/'
        if d != 0:
            l = sympy.log(d,2)
            if l > p_tc:
                tc.append(n**l)
            elif l == p_tc:
                tc.append((n**p_tc)*sympy.log(n))
            else:
                tc.append(n**p_tc)
        #no '-', '/'
        elif s == 0:
            tc.append(n**p_tc)
        #no '/', 1'-'
        elif s == 1:
            tc.append(n*(n**p_tc))
        #no '/', 2'-'
        else:
            tc.append(2**n)
    #print(tc)

    max_tc = 1
    for t in tc:
        if sympy.limit(t/max_tc, n, sympy.oo) > 1:
            max_tc = t
    print(max_tc)