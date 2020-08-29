import ast


class print_ast_visitor(ast.NodeVisitor):
    def __init__(self):
        self.parent = None
        self.name = ''
        pass

    def print_node(self, root):
        self.visit(root)
        return self.name

    def visit_Call(self, ast_call: ast.Call):
        self.name += '#'
        self.visit(ast_call.func)
        self.name += '('
        if ast_call.args:
            for arg in ast_call.args:
                self.visit(arg)
                self.name += ','
            self.name = self.name[:-1]
        self.name+=')'
    
    def visit_Name(self, ast_name: ast.Name):
        self.name += ast_name.id

    def visit_Attribute(self, ast_attribute: ast.Attribute):
        self.visit(ast_attribute.value)
        self.name += '.' + ast_attribute.attr
        
    def visit_Num(self, ast_num):
        self.name += str(ast_num.n)
    
    def visit_BinOp(self, ast_op):
        self.visit(ast_op.left)

        if type(ast_op.op) == ast.Add:
            op = '+'
        elif type(ast_op.op) == ast.Sub:
            op = '-'
        elif type(ast_op.op) == ast.Mult:
            op = '*'
        elif type(ast_op.op) == ast.Div:
            op = '/'
        elif type(ast_op.op) == ast.FloorDiv:
            op = '//'
        elif type(ast_op.op) == ast.Mod:
            op = '%'
        elif type(ast_op.op) == ast.Pow:
            op = '**'
        elif type(ast_op.op) == ast.LShift:
            op = '<<'
        elif type(ast_op.op) == ast.RShift:
            op = '>>'
        elif type(ast_op.op) == ast.BitOr:
            op = '|'
        elif type(ast_op.op) == ast.BitAnd:
            op = '&'
        elif type(ast_op.op) == ast.MatMult:
            op = '@'
        self.name += op
        self.visit(ast_op.right)
