import ast
from ast_transformer.python.ast_generator import PyASTGenerator
from ast_transformer.python.transform_visitor import PyTransformVisitor
#from bigo_calculator.scope_separater import ScopeSeparater
from bigo_calculator.scope_separater_mainTC import TimeSeparater_main
#from masterT import recursion_time_complexity_calculator

from bigo_calculator.time_complexity_scope_separater import TimeSeparater
from bigo_calculator.bigo_simplify import BigOSimplify

from arg_analysis import arg_analysis

import astunparse

def main():
    #origin_ast = PyASTGenerator().generate('./examples/binarySearch_recursion.py')
    origin_ast = PyASTGenerator().generate('./examples/FiboTest.py')
    bigo_ast = PyTransformVisitor().transform(origin_ast)

    #Rest of time complexity formular
    TCV = TimeSeparater(bigo_ast)
    TCV.calc()
    time_ast = TCV.root
    rest_TC = []
    for function_name, function_path in zip(TCV.function_list, time_ast.children):
        print('Time complexity of %s: %s' %(function_name, function_path.time_complexity))
        rest_TC.append(function_path.time_complexity)

    #Main of time complexity formular
    CV = TimeSeparater_main(bigo_ast)
    CV.calc()
    main_TC = []
    for i in bigo_ast.children:
        print("funcName: %s%s, funcCall: %s" %(i.name, i.parameter, i.time_complexity))
        main_TC.append(i.time_complexity)

    #RCV = ScopeSeparater(bigo_ast)
    #RCV.check()
    #RCV_T = []
    #for funcName, funcParameter, funcCall in zip(RCV.func_decl_name_list, RCV.func_decl_parameter_list, RCV.scope_list_final):
    #    #recur_tc_function = arg_analysis(funcName, funcParameter, funcCall)
    #    #RCV_T.append(recur_tc_function)
    #    #print(recur_tc_function)
    #    #print("funcName: %s%s, funcCall: %s" %(funcName, funcParameter, funcCall))
    #    #print(recursion_time_complexity_calculator(funcParameter, funcCall))




    print('main_TC:', main_TC)
    print('rest_TC:', rest_TC)
    

if __name__ == '__main__' :
    main()

