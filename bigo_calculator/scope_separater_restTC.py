import operator
from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from bigo_ast import bigo_ast
import sympy

class TimeSeparater_rest(BigOAstVisitor):

    def __init__(self, root: bigo_ast.CompilationUnitNode):
        '''
        List all path separated by if/else
        '''
        self.root = root
        self.function_list = []
        self.function_list_current_scope = []
        self.tc_list = []
        self.tc_list_final = []
        for func in root.children:
            if type(func) == bigo_ast.FuncDeclNode:
                self.function_list.append(func.name)

        pass

    def calc(self):
        super().visit(self.root)

        pass

    def add_time(self, old, new):
        result = []
        for new_time in new:
            for old_time in old:
                result.append(new_time + old_time)
    
        return result

    def mul_time(self, old, new):
        result = []
        for new_time in new:
            for old_time in old:
                result.append(new_time * old_time)
    
        return result
    
    def visit_FuncDeclNode(self, func_decl_node: bigo_ast.FuncDeclNode):
        #if func_decl_node.determine_recursion():
        #    func_decl_node.time_complexity = sympy.Symbol(func_decl_node.name, integer=True, positive=True)
        #else:
        #    tc = 0
        #    for child in func_decl_node.children:
        #        self.visit(child)
        #        tc += child.time_complexity
        #    if tc == 0:
        #        tc = 1
        #    func_decl_node.time_complexity = tc
        self.function_list_current_scope.append(func_decl_node.name)
        tc = [sympy.Rational(1)]
        for child in func_decl_node.children:
            self.visit(child)
            tc = self.add_time(tc, child.time_complexity)
        func_decl_node.time_complexity = tc
        #print("time_complexity: ", func_decl_node.time_complexity)

        pass

    def visit_FuncCallNode(self, func_call: bigo_ast.FuncCallNode):
        #if recursive funcCall, skip.
        target = func_call.name
        if target == self.function_list_current_scope[-1]:
            return

        #if target not in self.function_list:
        #    func_call.time_complexity = self.add_time(func_call.time_complexity, [sympy.Symbol(target, integer=True, positive=True)])

        for func in self.function_list:
            if target == func:
                func_call.time_complexity = [sympy.Symbol(func, integer=True, positive=True)]
                break

        pass

    def visit_VariableNode(self, variable_node: bigo_ast.VariableNode):
        return [sympy.Symbol(variable_node.name, integer=True, positive=True)]

    def visit_ConstantNode(self, const_node: bigo_ast.ConstantNode):
        return [sympy.Rational(const_node.value)]

    def visit_AssignNode(self, assign_node: bigo_ast.AssignNode):
        target = assign_node.target
        value = assign_node.value
        self.visit(target)

        value_tc = [sympy.Rational(1)]
        if type(value) is not list:
            self.visit(value)
            value_tc = value.time_complexity
        else:
            for child in value:
                self.visit(child)
                value_tc = self.add_time(value_tc, child.time_complexity)

        assign_node.time_complexity = value_tc

        pass

    def visit_Operator(self, node: bigo_ast.Operator):
        op = node.op
        left = self.visit(node.left)
        right = self.visit(node.right)

        node.time_complexity = self.add_time(node.left.time_complexity, node.right.time_complexity)

    #    if op == '+':
    #        return operator.add(left, right)
    #    elif op == '-':
    #        return operator.sub(left, right)
    #    elif op == '*':
    #        return operator.mul(left, right)
    #    elif op == '/':
    #        return operator.truediv(left, right)
    #    elif op == '<<':
    #        return left * 2 ** right
    #    elif op == '>>':
    #        return left / (2 ** right)
        
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

        true_tc = [sympy.Rational(1)]
        for child in if_node.true_stmt:
            self.visit(child)
            true_tc = self.add_time(true_tc, child.time_complexity)

        false_tc = [sympy.Rational(1)]
        for child in if_node.false_stmt:
            self.visit(child)
            false_tc = self.add_time(false_tc, child.time_complexity)

        true_false_tc = []
        for t_tc in true_tc:
            true_false_tc.append(t_tc)
        for f_tc in false_tc:
            true_false_tc.append(f_tc)

        if_node.time_complexity = self.add_time(cond_tc, true_false_tc)

        pass

    def visit_ForeachNode(self, foreach_node: bigo_ast.ForeachNode):

        #target = self.visit(foreach_node.target)
        #iter = self.visit(foreach_node.iter)

        tc = [sympy.Rational(1)]
        for child in foreach_node.children:
            self.visit(child)
            tc = self.add_time(tc, child.time_complexity)

        step = self.visit(foreach_node.variable)
        tc = self.mul_time(tc, step)
        for child in foreach_node.target:
            tc = self.add_time(tc, child.time_complexity)
        for child in foreach_node.iter:
            tc = self.add_time(tc, child.time_complexity)

        foreach_node.time_complexity = tc
        pass
