import ast
from ast_transformer.python.transform_visitor import PyTransformVisitor
from bigo_calculator.bigo_calculator import BigOCalculator
from bigo_calculator.recursion_calculator_copy import RecursionChecker
from masterT import master_theorem

from bigo_calculator.scope_separater import ScopeSeparater


class PyASTGenerator(object):
    def __init__(self):
        pass

    def generate(self, filename: str):
        with open(filename, 'r') as file:
            source_code = file.read()

        return ast.parse(source_code)



def main():
    origin_ast = PyASTGenerator().generate('./examples/FiboTest.py')
    bigo_ast = PyTransformVisitor().transform(origin_ast)
    RCV = RecursionChecker(bigo_ast)
    RCV.check()
    for l in RCV.scope_list_final:
        print(l)
    #RCV.find_MaxRecursionTimes_in_one_scope()
    #print(RCV.scope_list_final)
    #print(RCV.recursion_time)
    #recursion_list = RCV.biggest_single_scope
    #print(recursion_list)
    #master_theorem(recursion_list)

    #SSV = ScopeSeparater(bigo_ast)
    #SSV.check()

    
    

if __name__ == '__main__' :
    main()

