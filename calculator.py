import ast
from ast_transformer.python.transform_visitor import PyTransformVisitor

class PyASTGenerator(object):
    def __init__(self):
        pass

    def generate(self, filename: str):
        with open(filename, 'r') as file:
            source_code = file.read()

        return ast.parse(source_code)



def main():
    origin_ast = PyASTGenerator().generate('./examples/FiboTest.py')
    FunctionDef_Visitor = PyTransformVisitor()
    FunctionDef_Visitor.transform(origin_ast)
    

if __name__ == '__main__' :
    main()

