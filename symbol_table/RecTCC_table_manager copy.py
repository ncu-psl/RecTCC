from bigo_ast.bigo_ast import FuncDeclNode, ForNode, FuncCallNode, CompilationUnitNode, IfNode, VariableNode, \
    AssignNode, ConstantNode, Operator, BasicNode, WhileNode, ArrayNode
class RecTCC_table_manager(object):
    def __init__(self):
        self.table_list = []
        self.__current_scope_number = 0
        #self.current_table:vn_table

    @property
    def current_scope_number(self):
        return self.__current_scope_number

    def push_table(self, scope_type:str = 'other'):
        #if scope_type == 'else':
        #    self.table_list[-1].scope_type = 'other'
        table = vn_table(self.__current_scope_number, scope_type)
        if len(self.table_list) != 0:
            #previous_table = self.current_table
            previous_table = self.table_list[-1]
            if scope_type == 'eles':
                previous_table = self.table_list[-2]
            for key, value in previous_table.vn_table.items():
                table.vn_table[key] = value
        self.table_list.append(table)
        #self.current_table = table
        self.__current_scope_number += 1
        #print(scope_type, self.table_list[-1].vn_table)

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
        if '/' in node.parameter:
            self.table_list[-1]['/'] += 1
        elif '-' in node.parameter:
            self.table_list[-1]['-'] += 1
        else:
            pass

#    def print_current_table(self):
#        return self.current_table.vn_table

    def find_changed_symbol(self, node : BasicNode):
        if type(node) == AssignNode:
            if type(node.target) == VariableNode:
                value = self.find_changed_symbol(node.value)
                return node.target.name, value
            else:
                raise NotImplementedError('type(node.target) != VariableNode\n')

        if type(node) == VariableNode:
            return '(' + str(node.name) + ')'

        if type(node) == ConstantNode:
            return '(' + str(node.value) + ')'

        if type(node) == Operator:
            return '(' + self.find_changed_symbol(node.left) + node.op + self.find_changed_symbol(node.right) + ')'

    def combine_if_else(self):
        print('AAAAAAAAAAAA', self.table_list[0].vn_table)
        vn_table_else = self.table_list.pop()
        vn_table_if = self.table_list.pop()
        combined_table = vn_table(0, 'if')
        for key, value in vn_table_if.vn_table.items():
            combined_table.vn_table[key] = value
        for key, value in vn_table_else.vn_table.items():
            if key in combined_table.vn_table:
                combined_table.vn_table[key].extend(value)
            else:
                combined_table.vn_table[key] = vn_table_else.vn_table[key]
        #for key, value in vn_table_else.vn_table.items():
        #    if key in vn_table_if.vn_table:
        #        vn_table_if.vn_table[key].extend(value)
        #    else:
        #        vn_table_if.vn_table[key] = vn_table_else.vn_table[key]
        print('BBBBBBBBB', self.table_list[0].vn_table)
        self.table_list.append(vn_table_if)
        #self.current_table = self.table_list[-1]
        self.__current_scope_number -= 1

    def copy_table(self, target : object):
        table = vn_table(target.num, target.scope_type)
        for key, value in target.vn_table.items():
            table.vn_table[key] = value
        return table

    #def update_symbol_to_parent_table(self):
    #    vn_table_new = self.table_list.pop()
    #    vn_table_old = self.table_list.pop()
    #    updated_vn_table = vn_table(vn_table_old.num, vn_table_old.scope_type)

    #    for key_new, list_new in vn_table_new.vn_table.items():
    #        if key_new in vn_table_old.vn_table:
    #            updated = []
    #            for value_new in list_new:
    #                element = '(' + value_new + ')'
    #                for value_old in vn_table_old.vn_table[key_new]:
    #                    updated.append(element.replace(key_new, value_old))
    #            updated_vn_table.update(Symbol(key_new, updated))
    #        else:
    #            updated_vn_table.update(Symbol(key_new, list_new))
    #    self.table_list.append(updated_vn_table)
    #    self.current_table = self.table_list[-1]
    #    self.__current_scope_number -= 1
    def update_symbol_to_parent_table(self):
        vn_table_new = self.table_list.pop()
        vn_table_old = self.table_list.pop()
        self.table_list.append(vn_table_new)
        #self.current_table = self.table_list[-1]
        self.__current_scope_number -= 1





class vn_table(object):
    def __init__(self, scope_number, scope_type:str = 'other'):
        self.vn_table = {'-':[0], '/':[0]}
        #self.can_replace_varables = []
        self.num = scope_number
        self.scope_type = scope_type

    def update_assign_node(self, symbol):
        if isinstance(symbol.value, list):
            self.vn_table.update({symbol.name: symbol.value})
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