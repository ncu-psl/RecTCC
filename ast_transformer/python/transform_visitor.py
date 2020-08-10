import ast
import astunparse
from bigo_ast.bigo_ast import CompilationUnitNode, FuncDeclNode, FuncCallNode, Operator, BasicNode, IfNode


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
                print("Find a FunctionDef: ", child.name)
                #self.cu.add_children(self.visit(child))
            else:
                print("Not a FunctionDef. Do nothing.")

            self.cu.add_children(self.visit(child))
        self.cu.add_parent_to_children()

    def visit_FunctionDef(self, ast_func_def: ast.FunctionDef):
        print("Enter a FunctionDef: %s" %(ast_func_def.name))
        func_decl_node = FuncDeclNode()
        func_decl_node.name = ast_func_def.name

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

        print("FunctionDef args: %s" %(func_decl_node.parameter))

        for child in ast_func_def.body:
            self.parent = func_decl_node
            func_decl_node.add_children(self.visit(child))

        return func_decl_node

    def visit_Call(self, ast_call: ast.Call):
        func_call_node = FuncCallNode()
        if hasattr(ast_call.func, 'id'):
            func_call_node.name = ast_call.func.id
            #print('Call function(args): %s' %(ast_call.func.id))
            #print('Call args: %s' %(ast_call.args))
        else:
            func_call_node.name = ast_call.func.attr
            #print('Call function: %s' %(ast_call.func.attr))

        func_call_node.parameter = astunparse.unparse(ast_call.args)
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
        #print("Do Operation: %s" %(operator_node.expression))
        operator_node.add_children(operator_node.left)
        operator_node.add_children(operator_node.right)

        return operator_node

    def visit_If(self, ast_if: ast.If):
        if_node = IfNode()
        if_node.condition = self.visit(ast_if.test)

        if type(ast_if.body) is not list:
            ast_if.body = [ast_if.body]

        self.parent = if_node.true_stmt
        for child in ast_if.body or []:
            child_node = self.visit(child)
            if child_node:
                if type(child_node) is list:
                    if_node.true_stmt.extend(child_node)
                else:
                    if_node.true_stmt.append(child_node)

        if ast_if.orelse:
            if type(ast_if.orelse) is not list:
                ast_if.orelse = [ast_if.orelse]

            self.parent = if_node.false_stmt
            for child in ast_if.orelse or []:
                child_node = self.visit(child)
                if child_node:
                    if type(child_node) is list:
                        if_node.false_stmt.extend(child_node)
                    else:
                        if_node.false_stmt.append(child_node)

        return if_node


    def generic_visit(self, node):
        children = []
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        child = self.visit(item)
                        if type(child) is list:
                            children.extend(child)
                        else:
                            children.append(child)
            elif isinstance(value, ast.AST):
                child = self.visit(value)
                if type(child) is list:
                    children.extend(child)
                else:
                    children.append(child)
        return children

    #@staticmethod
    #def set_coordinate(node: BasicNode, coord):
    #    if coord:
    #        pass
