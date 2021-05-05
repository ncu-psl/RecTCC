import ast
import astunparse
from ast_transformer.python.ast_generator import PyASTGenerator
from bigo_ast.bigo_ast import CompilationUnitNode, FuncDeclNode, FuncCallNode, Operator, BasicNode, IfNode, ClassNode, VariableNode, ConstantNode, ArrayNode, AssignNode, ForeachNode, WhileNode, SubscriptNode

class ValueNumberingVisitor(ast.NodeVisitor):
    def __init__(self):
        self.func_decl_node = FuncDeclNode()
        self.visited_func_decl_node = []
        
    def add_VN(self, old, new):
        result = []
        for new_assign in new:
            for old_assign in old:
                result.append(new_assign + old_assign)
    
        return result
        
    def transform(self, root):
        for child in root.body:
            if isinstance(child, ast.FunctionDef):
                self.visit(child)
        print(self.visited_func_decl_node)
        return self.visited_func_decl_node
        
    def visit_FunctionDef(self, ast_func_def: ast.FunctionDef):
        self.func_decl_node = FuncDeclNode()
        if ast_func_def.args.args:
            args_list = ast_func_def.args.args
            for arg in args_list:
                self.func_decl_node.parameter.append(arg.arg)
        if ast_func_def.args.kwonlyargs:
            kwonlyargs_list = ast_func_def.args.kwonlyargs
            for kwonlyarg in kwonlyargs_list:
                self.func_decl_node.parameter.append(kwonlyarg.arg)
        if ast_func_def.args.vararg:
            self.func_decl_node.parameter.append(ast_func_def.args.vararg.arg)
        if ast_func_def.args.kwarg:
            self.func_decl_node.parameter.append(ast_func_def.args.kwarg.arg)
            
        for child in ast_func_def.body:
            if isinstance(child, ast.Assign):
                self.func_decl_node.vn_table = self.add_VN(self.func_decl_node.vn_table, [[child]])
            else:
                self.visit(child)
        self.visited_func_decl_node.append(self.func_decl_node)
            
    def visit_If(self, ast_if: ast.If):
        
        true_assign = [[]]
        if type(ast_if.body) is not list:
            ast_if.body = [ast_if.body]  
        for child in ast_if.body or []:
            if isinstance(child, ast.Assign):
                true_assign = self.add_VN(true_assign, [[child]])
                
        false_assign = [[]]
        if ast_if.orelse:
            if type(ast_if.orelse) is not list:
                ast_if.orelse = [ast_if.orelse]
            for child in ast_if.orelse or []:
                false_assign = self.add_VN(false_assign, [[child]])
                
        true_false_assign = []
        for t_assign in true_assign:
            true_false_assign.append(t_assign)
        for f_assign in false_assign:
            true_false_assign.append(f_assign)
                
        self.func_decl_node.vn_table = self.add_VN(self.func_decl_node.vn_table, true_false_assign)
                
origin_ast = PyASTGenerator().generate('./examples/if_else.py')
node = ValueNumberingVisitor().transform(origin_ast)
print(node[0].vn_table)
