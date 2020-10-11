from bigo_calculator.workload_analysis import workload_analysis
from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from bigo_ast import bigo_ast
import sympy

class TimeSeparater_main(BigOAstVisitor):

    def __init__(self, root: bigo_ast.CompilationUnitNode):
        '''
        List
        '''
        self.root = root
        self.function_list = []
        self.current_func = []
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











        self.current_func.append(func_decl_node)
        tc = [sympy.Rational(1)]
        for child in func_decl_node.children:
            self.visit(child)
            tc = self.add_time(tc, child.time_complexity)
        func_decl_node.time_complexity = tc


        pass

    def visit_FuncCallNode(self, func_call: bigo_ast.FuncCallNode):
        #if not recursive funcCall, skip.
        target = func_call.name
        if target != self.current_func[-1].name:
            return

        #print('funcDecl: %s, args: %s ; funcCall: %s, args: %s' %(self.function_list_current_scope[-1].name, self.function_list_current_scope[-1].parameter, func_call.name, func_call.parameter))
        #recursive funcCall, do arg_analysis
        #if can't analysis, return
        #if arg_analysis(funcName, funcParameter, funcCall) == 0:
        #    return
        #else:
        #    func_call.time_complexity = TC_formula_result

        tc = workload_analysis(self.current_func[-1], func_call)
        func_call.time_complexity = [tc]


    def visit_VariableNode(self, variable_node: bigo_ast.VariableNode):
        return [sympy.Symbol(variable_node.name, integer=True, positive=True)]

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
        self.visit(node.left)
        self.visit(node.right)

        node.time_complexity = self.add_time(node.left.time_complexity, node.right.time_complexity)



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
