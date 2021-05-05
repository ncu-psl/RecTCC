from bigo_ast import bigo_ast
from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from symbol_table.RecTCC_table_manager import RecTCC_table_manager

class TimeSeparater_main(BigOAstVisitor):
    def __init__(self, root: bigo_ast.CompilationUnitNode):
        self.root = root
        self.tc_list = []
        self.func_name = ''
        self.backward_vn_table_manager = RecTCC_table_manager()

        pass

    def calc(self):
        super().visit(self.root)

        pass

    def visit_CompilationUnitNode(self, compilation_unit_node: bigo_ast.CompilationUnitNode):
        self.backward_vn_table_manager.push_table('compilation')
        for child in compilation_unit_node.children:
            self.visit(child)

        pass

    def visit_FuncDeclNode(self, func_decl_node: bigo_ast.FuncDeclNode):
        self.backward_vn_table_manager.push_table('funcdecl')
        self.func_name = func_decl_node.name
        #for v in func_decl_node.parameter:
        #    self.backward_vn_table_manager.table_list[-1].vn_table[v] = [v]
        self.backward_vn_table_manager.add_parameter(func_decl_node.parameter)
        for child in func_decl_node.children:
            self.visit(child)
        self.tc_list.append(self.backward_vn_table_manager.table_list[-1].vn_table)

        pass

    def visit_AssignNode(self, assign_node: bigo_ast.AssignNode):
        if type(assign_node.target) != bigo_ast.SubscriptNode:
            self.backward_vn_table_manager.add_symbol(assign_node)
        self.visit(assign_node.value)

        pass

    def visit_FuncCallNode(self, func_call: bigo_ast.FuncCallNode):
        if func_call.name == self.func_name:
            self.backward_vn_table_manager.add_recursive_call(func_call)

        pass

    def visit_IfNode(self, if_node: bigo_ast.IfNode):
        self.backward_vn_table_manager.push_table(scope_type = 'if')
        for child in if_node.true_stmt:
            self.visit(child)
        if len(if_node.false_stmt) != 0:
            self.backward_vn_table_manager.push_table(scope_type = 'else')
            for child in if_node.false_stmt:
                self.visit(child)
            self.backward_vn_table_manager.combine_if_else()
        self.backward_vn_table_manager.update_symbol_to_parent_table()

        pass