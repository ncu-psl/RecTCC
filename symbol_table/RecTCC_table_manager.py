import copy
from bigo_ast.bigo_ast import FuncDeclNode, ForNode, FuncCallNode, CompilationUnitNode, IfNode, VariableNode, \
    AssignNode, ConstantNode, Operator, BasicNode, WhileNode, ArrayNode, SubscriptNode
class RecTCC_table_manager(object):
    def __init__(self):
        self.table_list = []
        self.__current_scope_number = 0

    @property
    def current_scope_number(self):
        return self.__current_scope_number

    def push_table(self, scope_type:str = 'other'):
        if self.current_scope_number == 0:
            table = vn_table(self.__current_scope_number, scope_type)
        else:
            if scope_type == 'else':
                table = copy.deepcopy(self.table_list[-2])
            else:
                table = copy.deepcopy(self.table_list[-1])
        table.scope_type = scope_type
        self.table_list.append(table)
        self.__current_scope_number += 1

    #def pop_table(self):
    #    if self.__current_scope_number != 0:
    #        #self.update_symbol_to_parent_table(self.table_list[-1].scope_type)
    #        self.table_list.pop()
    #        self.__current_scope_number -= 1
    #        if self.__current_scope_number != 0:
    #            self.current_table = self.table_list[-1]
    #    else:
    #        print('table list is empty')

    def add_symbol(self, node : AssignNode):
        symbol_name, value = self.find_changed_symbol(node)
        sym = Symbol(symbol_name, value)
        self.table_list[-1].update_assign_node(sym)

    def add_parameter(self, parameter : list):
        for p in parameter:
            sym = Symbol(p, p)
            self.table_list[-1].update_assign_node(sym)

    def add_recursive_call(self, node : FuncCallNode):
        for args in node.parameter:
            for i, arg in enumerate(self.table_list[-1].vn_table[args]):
                if '/' in arg or '*' in arg:
                    self.table_list[-1].vn_table['/'][i] += 1
                elif '-' in arg or '+' in arg:
                    self.table_list[-1].vn_table['-'][i] += 1

    def find_changed_symbol(self, node : BasicNode):
        if type(node) == AssignNode:
            if type(node.target) == VariableNode:
                value = self.find_changed_symbol(node.value)
                return node.target.name, value
            else:
                return
                #raise NotImplementedError('type(node.target) != VariableNode\n')

        if type(node) == VariableNode:
            return '(' + str(node.name) + ')'

        if type(node) == ConstantNode:
            return '(' + str(node.value) + ')'

        if type(node) == Operator:
            return '(' + self.find_changed_symbol(node.left) + node.op + self.find_changed_symbol(node.right) + ')'

        if type(node) == FuncCallNode:
            args = ''
            for p in node.parameter:
                args += p + ','
            return '(' + str(node.name) + '[' + args +  '])'

        if type(node) == SubscriptNode:
            return '(' + node.value.name + '[' + self.find_changed_symbol(node.slice[0]) + ']' + ')'

    def combine_if_else(self):
        vn_table_else = self.table_list.pop()
        vn_table_if = self.table_list.pop()
        for key, value in vn_table_else.vn_table.items():
            if key not in vn_table_if.vn_table:
                vn_table_if.vn_table[key] = ['']
            vn_table_if.vn_table[key].extend(value)
        self.table_list.append(vn_table_if)
        self.__current_scope_number -= 1

    def update_symbol_to_parent_table(self):
        vn_table_new = self.table_list.pop()
        vn_table_old = self.table_list.pop()
        self.table_list.append(vn_table_new)
        self.__current_scope_number -= 1


class vn_table(object):
    def __init__(self, scope_number, scope_type:str = 'other'):
        self.vn_table = {'-':[0], '/':[0]}
        self.num = scope_number
        self.scope_type = scope_type

    def update_assign_node(self, symbol):
        if symbol.name in self.vn_table:
            replaced = []
            for value in self.vn_table[symbol.name]:
                replaced.append(symbol.value.replace(symbol.name, value))
            self.vn_table.update({symbol.name: replaced})
        else:
            replaced = [symbol.value] * len(self.vn_table['-'])
            for key, value in self.vn_table.items():
                if key in symbol.value and key not in ['-', '/']:
                    for index, v in enumerate(value) :
                        replaced[index] = replaced[index].replace(key, v)
            if replaced:
                self.vn_table.update({symbol.name: replaced})
            else:
                self.vn_table.update({symbol.name: [symbol.value]})

    def get_symbol_value(self,symbol_name:str, default = None):
        try:
            return self.vn_table[symbo_name]
        except:
            return default

class Symbol():
    def __init__(self, name:str = '', value:str = ''):
        self.name = name
        self.value = value