from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from bigo_ast import bigo_ast
from scope_table.table_manager import table_manager

class ScopeSeparater(BigOAstVisitor):

    def __init__(self, root: bigo_ast.CompilationUnitNode):
        self.root = root
        self.functionDef = {}
        self.table_manager = table_manager()
        
        pass

    def check(self):
        super().visit(self.root)

        pass

    def visit_FuncDeclNode(self, func_decl_node: bigo_ast.FuncDeclNode):
        self.table_manager.push_table()

        for child in func_decl_node.children:
            print(self.visit(child))

        FuncDeclTable = self.table_manager.pop_table()
        self.functionDef.update({func_decl_node.name: FuncDeclTable})

        pass

    def visit_FuncCallNode(self, func_call: bigo_ast.FuncCallNode):

        pass

    def visit_IfNode(self, if_node: bigo_ast.IfNode):

        t = []
        for child in if_node.true_stmt:
            #self.visit(child)
            t.append(self.visit(child))


        f = []
        for child in if_node.false_stmt:
            #self.visit(child)
            f.append(self.visit(child))

        #return if_node
        #return [t, f]
        pass
