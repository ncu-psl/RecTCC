from ast import Module
import ast

class PyASTGenerator(object):
    def __init__(self):
        pass

    def generate(self, filename: str):
        with open(filename, 'r') as file:
            source_code = file.read()

        return ast.parse(source_code)

class PyTransformVisitor(ast.NodeVisitor):
    def __init__(self):
        self.parent = None
        self.cu = None
    pass

    def transform(self, root):
        self.visit(root)
        return self.cu

    def visit_Module(self, ast_module: ast.Module):
        #self.cu = CompilationUnitNode()
        for child in ast_module.body:
            if isinstance(child, ast.FunctionDef):
                print("Find a FunctionDef")
                self.visit(child)
            else:
                print("Pass")

    def visit_FunctionDef(self, ast_func_def: ast.FunctionDef):
        print("Function name is %s" %(ast_func_def.name))

        for child in ast_func_def.body:
            self.visit(child)

    def visit_Call(self, ast_call: ast.Call):
        if hasattr(ast_call.func, 'id'):
            print('Call function: %s' %(ast_call.func.id))
        else:
            print('Call function: %s' %(ast_call.func.attr))





def main():
    origin_ast = PyASTGenerator().generate('fibo_2pown.py')
    FunctionDef_Visitor = PyTransformVisitor()
    FunctionDef_Visitor.transform(origin_ast)
    
#    big0_ast = PyTransformVisitor().transform(origin_ast)

if __name__ == '__main__' :
    main()

