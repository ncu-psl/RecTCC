import ast
import astunparse

class RecursionCallCollector(ast.NodeVisitor):
    def __init__(self):
        self.func_decl_name = ''
        self.recursive_call = []

    def visit_FunctionDef(self, ast_func_def):
        self.func_decl_name = ast_func_def.name

        for child in ast_func_def.body:
            self.visit(child)

    def visit_Call(self, ast_call):
        func_call_name = ''
        if hasattr(ast_call.func, 'id'):
            func_call_name = ast_call.func.id
        else:
            func_call_name = ast_call.func.attr
        if func_call_name != self.func_decl_name:
            return
            
        args_list = []
        if func_call_name == self.func_decl_name:
            for arg in ast_call.args:
                args_list.append(astunparse.unparse(arg).replace("\n", ""))
        self.recursive_call.append(args_list)
