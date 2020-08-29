from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from bigo_ast import bigo_ast
import sympy

class TimeSeparater(BigOAstVisitor):

    def __init__(self, root: bigo_ast.CompilationUnitNode):
        '''
        List all path separated by if/else
        '''
        self.root = root
        self.function_list = []
        self.tc_list = []
        self.tc_list_final = []
        for func in root.children:
            if type(func) == bigo_ast.FuncDeclNode:
                self.function_list.append(func)

        pass

    def check(self):
        super().visit(self.root)

        pass

    def add_time(self, old, new):
        result = []
        for new_time in new:
            for old_time in old:
                result.append(old_road_copy)
    
        return result
    
    def visit_FuncDeclNode(self, func_decl_node: bigo_ast.FuncDeclNode):
        if func_decl_node.determine_recursion():
            func_decl_node.time_complexity = sympy.Symbol(func_decl_node.name, integer=True, positive=True)
        else:
            tc = 0
            for child in func_decl_node.children:
                self.visit(child)
                tc += child.time_complexity
            if tc == 0:
                tc = 1
            func_decl_node.time_complexity = tc

        pass
       # for child in func_decl_node.children:
       #     self.visit(child)
       #     tc = self.add_time(tc, child.time_complexity)
       # func_decl_node.time_complexity = tc
       # self.tc_list_final.append(self.tc_list.pop())

    def visit_FuncCallNode(self, func_call: bigo_ast.FuncCallNode):
        target = func_call.name
        for func in self.function_list:
            if target == func.name:
                func_call.time_complexity = sympy.Symbol(func.name, integer=True, positive=True)
                break

        pass

    def visit_VariableNode(self, variable_node: bigo_ast.VariableNode):
        return sympy.Symbol(variable_node.name, integer=True, positive=True)

    def visit_ConstantNode(self, const_node: bigo_ast.ConstantNode):
        return sympy.Rational(const_node.value)

    def visit_AssignNode(self, assign_node: bigo_ast.AssignNode):
        target = assign_node.target
        value = assign_node.value
        self.visit(target)

        value_tc = 0
        if type(value) is not list:
            self.visit(value)
            value_tc = value.time_complexity
        else:
            for child in value:
                self.visit(child)
                value_tc += child.time_complexity

        assign_node.time_complexity = value_tc

        pass

    def visit_Operator(self, node: bigo_ast.Operator):
        op = node.op
        left = self.visit(node.left)
        right = self.visit(node.right)

        node.time_complexity = node.left.time_complexity + node.right.time_complexity

        if op == '+':
            return operator.add(left, right)
        elif op == '-':
            return operator.sub(left, right)
        elif op == '*':
            return operator.mul(left, right)
        elif op == '/':
            return operator.truediv(left, right)
        elif op == '<<':
            return left * 2 ** right
        elif op == '>>':
            return left / (2 ** right)
        
    #def visit_IfNode(self, if_node: bigo_ast.IfNode):
    #    if self.scope_list:

    #        if_true = [[]]
    #        self.scope_list.append(if_true)
    #        for child in if_node.true_stmt:
    #            self.visit(child)

    #        if_false = [[]]
    #        self.scope_list.append(if_false)
    #        for child in if_node.false_stmt:
    #            self.visit(child)

    #        if_false = self.scope_list.pop()
    #        if_true = self.scope_list.pop()
    #        current_scope_list = self.scope_list.pop()

    #        true_and_false = []
    #        if if_true:
    #            for t_stmt in if_true:
    #                true_and_false.append(t_stmt)
    #        if if_false:
    #            for f_stmt in if_false:
    #                true_and_false.append(f_stmt)
    #        current_scope_list = self.add_road(current_scope_list, true_and_false)
    #        self.scope_list.append(current_scope_list)

    def visit_IfNode(self, if_node: bigo_ast.IfNode):
        self.visit(if_node.condition)
        cond_tc = if_node.condition.time_complexity

        true_tc = 0
        for child in if_node.true_stmt:
            self.visit(child)
            true_tc += child.time_complexity

        if true_tc == 0:
            true_tc = 1

        false_tc = 0
        for child in if_node.false_stmt:
            self.visit(child)
            false_tc += child.time_complexity

        if false_tc == 0:
            false_tc = 1

        if_node.time_complexity = cond_tc + sympy.Max(true_tc, false_tc)

        pass

