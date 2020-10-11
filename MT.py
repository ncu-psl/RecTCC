import sympy
n = sympy.Symbol('n')

def master_theorem(main_TC, rest_TC):
    print("==================")
    print(main_TC, rest_TC)

    if sympy.oo in main_TC:
        print("OOOOOOOOOOOOOOOO")
        #return sympy.oo

    for m_list, r_list in zip(main_TC, rest_TC):

        #rest_TC
        r_var_list = set()
        for symbol in r_list.free_symbols:
            r_var_list.update([(symbol, sympy.oo)])
            #r_var_list.update([(symbol, n)])
        #r_tc = sympy.O(r_list.subs(r_var_list), *{(n, sympy.oo)}).args[0]
        r_tc = sympy.O(r_list, *r_var_list).args[0]


        #main_TC

        SUB_coeff, DIV_coeff = 0, 0 
        for coeff in m_list.free_symbols:
            if coeff.name == 'SUB':
                SUB_coeff = m_list.expand().coeff(coeff)
            if coeff.name == 'DIV':
                DIV_coeff = m_list.expand().coeff(coeff)

        print('Main: ', SUB_coeff, DIV_coeff, 'Rest: ', r_tc)



    pass
