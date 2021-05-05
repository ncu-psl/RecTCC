import operator
from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from bigo_ast import bigo_ast
import sympy

class TimeSeparater_partial(BigOAstVisitor):

    def __init__(self, root: bigo_ast.CompilationUnitNode):
        '''
        List all path separated by if/else
        '''
        self.root = root
        self.tc_list:list

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
        tc = [sympy.Rational(1)]
        for child in func_decl_node.children:
            self.visit(child)
            tc = self.add_time(tc, child.time_complexity)
        func_decl_node.time_complexity = tc
        self.tc_list = tc

        pass

    def visit_FuncCallNode(self, func_call: bigo_ast.FuncCallNode):
        func_call.time_complexity = [sympy.Rational(1)]

        pass

    def visit_VariableNode(self, variable_node: bigo_ast.VariableNode):
        return [sympy.Rational(1)]
        

    def visit_ConstantNode(self, const_node: bigo_ast.ConstantNode):
        return [sympy.Rational(1)]

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

        pass

    def visit_IfNode(self, if_node: bigo_ast.IfNode):
        self.visit(if_node.condition)
        cond_tc = if_node.condition.time_complexity

        true_tc = [sympy.Rational(1)]
        for child in if_node.true_stmt:
            self.visit(child)
            true_tc = self.add_time(true_tc, child.time_complexity)

        if len(if_node.false_stmt) != 0:
            false_tc = [sympy.Rational(1)]
            for child in if_node.false_stmt:
                self.visit(child)
                false_tc = self.add_time(false_tc, child.time_complexity)

            true_false_tc = []
            for t_tc in true_tc:
                true_false_tc.append(t_tc)
            for f_tc in false_tc:
                true_false_tc.append(f_tc)
        else:
            true_false_tc = true_tc

        if_node.time_complexity = self.add_time(cond_tc, true_false_tc)

        pass

    def visit_ForeachNode(self, foreach_node: bigo_ast.ForeachNode):
        tc = [sympy.Rational(1)]
        for child in foreach_node.children:
            self.visit(child)
            tc = self.add_time(tc, child.time_complexity)

        tc = self.mul_time(tc, [sympy.Symbol('n')])
        for child in foreach_node.target:
            tc = self.add_time(tc, child.time_complexity)
        for child in foreach_node.iter:
            tc = self.add_time(tc, child.time_complexity)

        foreach_node.time_complexity = tc

        pass
    
    def visit_WhileNode(self, while_node: bigo_ast.WhileNode):
        tc = [sympy.Rational(1)]
        for child in while_node.children:
            self.visit(child)
            tc = self.add_time(tc, child.time_complexity)

        tc = self.mul_time(tc, [sympy.Symbol('n')])

        while_node.time_complexity = tc

        pass