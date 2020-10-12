import ast
from ast_transformer.python.ast_generator import PyASTGenerator
from ast_transformer.python.transform_visitor import PyTransformVisitor
from bigo_calculator.scope_separater_mainTC import TimeSeparater_main
from bigo_calculator.scope_separater_restTC import TimeSeparater_rest
from bigo_calculator.bigo_simplify import BigOSimplify
from bigo_ast.bigo_ast import FuncDeclNode

from MT import master_theorem

def main():
    #origin_ast = PyASTGenerator().generate('./examples/binarySearch_recursion.py')
    origin_ast = PyASTGenerator().generate('./examples/FiboTest.py')
    #origin_ast = PyASTGenerator().generate('./examples/normal_recursive.py')

    #Rest of time complexity formula
    bigo_ast = PyTransformVisitor().transform(origin_ast)
    restTCV = TimeSeparater_rest(bigo_ast)
    restTCV.calc()
    rest_TC = []
    for child in restTCV.root.children:
        if type(child) != FuncDeclNode:
            continue
        #print("funcName: %s%s, funcCall: %s" %(child.name, child.parameter, child.time_complexity))
        child.determine_recursion()
        rest_TC.append(child.time_complexity)

    #Main of time complexity formula
    bigo_ast = PyTransformVisitor().transform(origin_ast)
    mainTCV = TimeSeparater_main(bigo_ast)
    mainTCV.calc()
    main_TC = []
    for child in mainTCV.root.children:
        if type(child) != FuncDeclNode:
            continue
        #print("funcName: %s%s, funcCall: %s" %(child.name, child.parameter, child.time_complexity))
        child.determine_recursion()
        main_TC.append(child.time_complexity)


    #print('Function name:', mainTCV.function_list)
    #print('main_TC:', main_TC)
    #print('rest_TC:', rest_TC)
    
    #master_theorem(main_TC[-3], rest_TC[-3])
    for f_list, m_list, r_list in zip(mainTCV.function_list, main_TC, rest_TC):
        #master_theorem(m_list, r_list)
        print('TimeComplexity of %s: O(%s)' %(f_list, master_theorem(m_list, r_list)))
    


if __name__ == '__main__' :
    main()
