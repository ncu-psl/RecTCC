from bigo_ast.bigo_ast import FuncCallNode, FuncDeclNode, IfNode, BasicNode




class table_manager(object):

    def __init__(self):
        self.table_list = []
        
    def push_table(self):
        table = road_table()
        self.table_list.append(table)

    def pop_table(self):
        if self.table_list:
            return table_list.pop()
        else:
            print('table list is empty')

    def add_recursioncall(self, node : BasicNode):
        current_table = self.table_list.pop()



class road_table(object):

    def __init__(self):
        self.table = []



class RecursionCall():

    def __init__(self, FuncCallNode):
        self.node = FuncCallNode
        self.name = FuncCallNode.name
        self.parameter = FuncCallNode.parameter
