import ast
import astunparse
from bigo_ast.bigo_ast import CompilationUnitNode, FuncDecNode, FuncCallNode, Operator


class PyTransformVisitor(ast.NodeVisitor):
    def __init__(self):
        self.parent = None
        self.cu = None
    pass

    def transform(self, root):
        self.visit(root)
        return self.cu

    def visit_Module(self, ast_module: ast.Module):
        self.cu = CompilationUnitNode()
        for child in ast_module.body:
            self.parent = self.cu
            if isinstance(child, ast.FunctionDef):
                print("Find a FunctionDef")
                self.visit(child)
            else:
                print("Not a FunctionDef. Do nothing.")

    def visit_FunctionDef(self, ast_func_def: ast.FunctionDef):
        func_decl_node = FuncDecNode()
        func_decl_node.name = ast_func_def.name

        print("Function name is %s" %(func_decl_node.name))

        if ast_func_def.args.args:
            args_list = ast_func_def.args.args
            for arg in args_list:
                func_decl_node.parameter.append(arg.arg)
                #print("args: ", arg.arg)
        if ast_func_def.args.kwonlyargs:
            kwonlyargs_list = ast_func_def.args.kwonlyargs
            for kwonlyarg in kwonlyargs_list:
                func_decl_node.parameter.append(kwonlyarg.arg)
                #print("kwonlyargs: ", kwonlyarg.arg)
        if ast_func_def.args.vararg:
            func_decl_node.parameter.append(ast_func_def.args.vararg.arg)
            #print("vararg: ", ast_func_def.args.vararg.arg)
        if ast_func_def.args.kwarg:
            func_decl_node.parameter.append(ast_func_def.args.kwarg.arg)
            #print("kwarg: ", ast_func_def.args.kwarg.arg)

        print(func_decl_node.parameter)
        for child in ast_func_def.body:
            self.parent = func_decl_node
            func_decl_node.add_children(self.visit(child))


        return func_decl_node

    def visit_Call(self, ast_call: ast.Call):
        func_call_node = FuncCallNode()
        if hasattr(ast_call.func, 'id'):
            func_call_node.name = ast_call.func.id
            print('Call function: %s' %(ast_call.func.id))
            print('Call args: %s' %(ast_call.args))
        else:
            func_call_node.name = ast_call.func.attr
            print('Call function: %s' %(ast_call.func.attr))

        return func_call_node

    def visit_BinOp(self, ast_bin_op: ast.BinOp):
        operator_node = Operator()

        if type(ast_bin_op.op) == ast.Add:
            operator_node.op = '+'
        elif type(ast_bin_op.op) == ast.Sub:
            operator_node.op = '-'
        elif type(ast_bin_op.op) == ast.Mult:
            operator_node.op = '*'
        elif type(ast_bin_op.op) == ast.Div:
            operator_node.op = '/'
        elif type(ast_bin_op.op) == ast.FloorDiv:
            operator_node.op = '//'
        elif type(ast_bin_op.op) == ast.Mod:
            operator_node.op = '%'
        elif type(ast_bin_op.op) == ast.Pow:
            operator_node.op = '**'
        elif type(ast_bin_op.op) == ast.LShift:
            operator_node.op = '<<'
        elif type(ast_bin_op.op) == ast.RShift:
            operator_node.op = '>>'
        elif type(ast_bin_op.op) == ast.BitOr:
            operator_node.op = '|'
        elif type(ast_bin_op.op) == ast.BitAnd:
            operator_node.op = '&'
        elif type(ast_bin_op.op) == ast.MatMult:
            operator_node.op = '@'
        else:
            raise Exception("does not support operator: ", ast_bin_op.op)

        operator_node.left = self.visit(ast_bin_op.left)
        operator_node.right = self.visit(ast_bin_op.right)

        operator_node.expression = astunparse.unparse(ast_bin_op)
        print("Do Operation: %s" %(operator_node.expression))

        return operator_node
