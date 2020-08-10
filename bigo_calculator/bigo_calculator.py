from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from bigo_ast import bigo_ast

class BigOCalculator(BigOAstVisitor):

    def __init__(self, root: bigo_ast.CompilationUnitNode):
        self.root = root
        self.function_list = []
        #self.backward_table_manager = table_manager()
        self.current_class = None
        for func in root.children:
            if type(func) == bigo_ast.FuncDeclNode:
                self.function_list.append(func)

        pass

    def calc(self):
        super().visit(self.root)

        pass

    def visit_FuncDeclNode(self, func_decl_node: bigo_ast.FuncDeclNode):
        if func_decl_node.determine_recursion():
            print('FunctionDef: %s is a recursive function' %(func_decl_node.name))
        else:
            print('FunctionDef: %s is not a recursive function' %(func_decl_node.name))

        pass

    #def visit_FuncCallNode(self, func_call: bigo_ast.FuncCallNode):
    #    target = func_call.name

    #def visit_Operator(self, node: bigo_ast.Operator):
    #    op = node.op
    #    left = self.visit(node.left)
    #    right = self.visit(node.right)

    #    if op == '+':
    #        return operator.add(left, right)
    #    elif op == '-':
    #        return operator.sub(left, right)
    #    elif op == '*':
    #        return operator.mul(left, right)
    #    elif op == '/':
    #        return operator.truediv(left, right)
    #    elif op == '**':
    #        return left ** right
    #    elif op == '<<':
    #        return left * 2 ** right
    #    elif op == '>>':
    #        return left / (2 ** right)
    #    elif op == '//':
    #        return left // right
    #    elif op == '>>':
    #        return left / (2 ** right)
    #    elif op == '%':
    #        return left % right
    #    elif op == '>>':
    #        return left / (2 ** right)
    #    elif op == '|':
    #        return left | right
    #    elif op == '&':
    #        return left & right
    #    elif op == '>>':
    #        return left / (2 ** right)
    #    elif op == '@':
    #        return left @ right

    #    
    #    pass

    def visit_IfNode(self, if_node: bigo_ast.IfNode):
        self.visit(if_node.condition)

        for child in if_node.true_stmt:
            self.visit(child)

        for child in if_node.false_stmt:
            self.visit(child)

        pass
