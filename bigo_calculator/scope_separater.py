from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from bigo_ast import bigo_ast

class ScopeSeparater(BigOAstVisitor):

    def __init__(self, root: bigo_ast.CompilationUnitNode):
        '''
        List all path separated by if/else
        '''
        self.root = root
        self.func_decl_name_list = []
        self.func_decl_parameter_list = []
        self.scope_list = []
        self.scope_list_final = []

    def check(self):
        super().visit(self.root)

        pass

    def add_road(self, old, new):
        result = []
        for new_road in new:
            for old_road in old:
                old_road_copy = old_road.copy()
                old_road_copy.extend(new_road)
                result.append(old_road_copy)
    
        return result
    
    def visit_FuncDeclNode(self, func_decl_node: bigo_ast.FuncDeclNode):
        self.func_decl_name_list.append(func_decl_node.name)
        self.func_decl_parameter_list.append(func_decl_node.parameter)
        self.scope_list.append([[]])
        for child in func_decl_node.children:
            self.visit(child)
        #print(self.scope_list)
        self.scope_list_final.append(self.scope_list.pop())

    def visit_FuncCallNode(self, func_call: bigo_ast.FuncCallNode):
        if self.scope_list and func_call.name == self.func_decl_name_list[-1]:
            current_scope_list = self.scope_list.pop()
            #print(func_call.name, current_scope_list)
            #current_scope_list = self.add_road(current_scope_list, [[func_call.name + func_call.parameter.replace("\n", "")]])
            current_scope_list = self.add_road(current_scope_list, [[func_call.parameter.replace("\n", "")]])
            self.scope_list.append(current_scope_list)

    #def visit_Operator(self, node: bigo_ast.Operator):
    #    self.visit(node.left)
    #    self.visit(node.right)
        
    def visit_IfNode(self, if_node: bigo_ast.IfNode):
        if self.scope_list:

            if_true = [[]]
            self.scope_list.append(if_true)
            for child in if_node.true_stmt:
                self.visit(child)

            if_false = [[]]
            self.scope_list.append(if_false)
            for child in if_node.false_stmt:
                self.visit(child)

            if_false = self.scope_list.pop()
            if_true = self.scope_list.pop()
            current_scope_list = self.scope_list.pop()

            true_and_false = []
            if if_true:
                for t_stmt in if_true:
                    true_and_false.append(t_stmt)
            if if_false:
                for f_stmt in if_false:
                    true_and_false.append(f_stmt)
            current_scope_list = self.add_road(current_scope_list, true_and_false)
            self.scope_list.append(current_scope_list)
