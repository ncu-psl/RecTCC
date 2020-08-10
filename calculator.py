import ast
from ast_transformer.python.transform_visitor import PyTransformVisitor
from bigo_calculator.bigo_calculator import BigOCalculator


class PyASTGenerator(object):
    def __init__(self):
        pass

    def generate(self, filename: str):
        with open(filename, 'r') as file:
            source_code = file.read()

        return ast.parse(source_code)



def main():
    origin_ast = PyASTGenerator().generate('./examples/FiboTest.py')
    origin_ast = PyASTGenerator().generate('./examples/fibo.py')
    bigo_ast = PyTransformVisitor().transform(origin_ast)
    print("===================================")
    BigOCalculator(bigo_ast).calc()
    
    

if __name__ == '__main__' :
    main()

