from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from bigo_ast import bigo_ast

class RecursionChecker(BigOAstVisitor):

    def __init__(self, root: bigo_ast.CompilationUnitNode):
        '''
        將funcDef裡出現過的funcCall記錄下來
        若有funcCall的名字與funcDef的名字相同，即為遞迴

        利用scope_list、scope_list_final來區分作用域
        將同樣作用域的funcCall放入同一個且同一階層的List
        若在同一階層的List中，有出現複數個funcCall
        則這些funcCall為同時出現，遞迴次數會增加
        '''
        self.root = root
        self.scope_list = []
        self.scope_list_final = []
        self.recursion_time = {}

        pass

    def find_MaxRecursionTimes_in_one_scope(self):
        '''
        找出funcDef中，同一作用域中遞迴被呼叫的最大次數
        如：在example/FiboTest.py中的兩種遞迴(fibo, fibo_dp)
        fibo最大次數是2次，fibo_dp最大僅為1次
        '''
        for function in self.scope_list_final:
            function_name = function.pop(0)
            max_number = self.find_max_number(function_name, function)
            #print(function_name, max_number)
            if max_number > 0:
                self.recursion_time.update({function_name: max_number})
            
    def find_max_number(self, name: str, scope: list):
        '''
        支援find_MaxRecursionTimes_in_one_scope
        即計算「同一階的遞迴funcCall出現幾次」
        '''
        max_number = 0
        if len(scope) == 0:
            return max_number

        for child in scope:
            if isinstance(child, list):
                list_number = self.find_max_number(name, child)
                if list_number > max_number:
                    max_number = list_number
            elif child == name:
                max_number += 1

        return max_number


    def check(self):
        super().visit(self.root)

        pass

    #def visit_CompilationUnitNode(self, compilation_unit_node: bigo_ast.CompilationUnitNode):
    #    for child in compilation_unit_node.children:
    #        self.visit(child)

    def visit_FuncDeclNode(self, func_decl_node: bigo_ast.FuncDeclNode):
        self.scope_list.append([func_decl_node.name])
        for child in func_decl_node.children:
            self.visit(child)
        self.scope_list_final.append(self.scope_list.pop())

    def visit_FuncCallNode(self, func_call: bigo_ast.FuncCallNode):
        if self.scope_list:
            current_scope_list = self.scope_list.pop()
            current_scope_list.append(func_call.name)
            self.scope_list.append(current_scope_list)



    #def visit_Operator(self, node: bigo_ast.Operator):
    #    self.visit(node.left)
    #    self.visit(node.right)
        
    def visit_IfNode(self, if_node: bigo_ast.IfNode):
        if self.scope_list:

            if_true = []
            self.scope_list.append(if_true)
            for child in if_node.true_stmt:
                self.visit(child)

            if_false = []
            self.scope_list.append(if_false)
            for child in if_node.false_stmt:
                self.visit(child)

            if_false = self.scope_list.pop()
            if_true = self.scope_list.pop()
            current_scope_list = self.scope_list.pop()

            true_and_false = []
            if if_true:
                true_and_false.append(if_true)
            if if_false:
                true_and_false.append(if_false)
            current_scope_list.append(true_and_false)

            self.scope_list.append(current_scope_list)
