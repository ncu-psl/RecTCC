import ast
import astunparse

class argumentModifier(ast.NodeTransformer):

    def visit_BinOp(self, ast_bin_op):
        if type(ast_bin_op.op) == ast.FloorDiv:
            ast_bin_op.op = ast.Div()
        elif type(ast_bin_op) == ast.Mod:
            ast_bin_op.op = ast.Div()
        #elif type(ast_bin_op.op) == ast.LShift:
        #    operator_node.op = '<<'
        #elif type(ast_bin_op.op) == ast.RShift:
        #    operator_node.op = '>>'
        #elif type(ast_bin_op.op) == ast.BitOr:
        #    operator_node.op = '|'
        #elif type(ast_bin_op.op) == ast.BitAnd:
        #    operator_node.op = '&'
        #elif type(ast_bin_op.op) == ast.MatMult:
        #    operator_node.op = '@'
        else:
            pass
        self.visit(ast_bin_op.left)
        self.visit(ast_bin_op.right)
        return ast_bin_op

