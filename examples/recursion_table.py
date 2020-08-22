from bigo_ast.bigo_ast import BasicNode, FuncDeclNode, FuncCallNode, Operator, IfNode

class RecusionCall_table(object):

    def __init__(self):
        self.table = {}


class RecusionCall():

    def __init__(self, function_name:str = '', function_arg:list = []):
        self.name = function_name
        self.arg = function_arg
        
