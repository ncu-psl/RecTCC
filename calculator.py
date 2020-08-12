import ast
from ast_transformer.python.transform_visitor import PyTransformVisitor
from bigo_calculator.bigo_calculator import BigOCalculator
from bigo_calculator.recursion_calculator import RecursionChecker


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
    RCV.find_MaxRecursionTimes_in_one_scope()
    print(RCV.recursion_time)

    
    

if __name__ == '__main__' :
    main()

