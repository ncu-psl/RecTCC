from bigo_calculator.workload_analysis import workload_analysis
from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from bigo_ast import bigo_ast
import sympy
from symbol_table.table_manager import table_manager
from symbol_table.vn_table_manager import vn_table_manager

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
        self.backward_table_manager = table_manager()
        self.backward_vn_table_manager = vn_table_manager()

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

    def visit_CompilationUnitNode(self, compilation_unit_node: bigo_ast.CompilationUnitNode):
        self.backward_table_manager.push_table('compilation')
        self.backward_vn_table_manager.push_table('compilation')
        tc = 0
        for child in compilation_unit_node.children:
            self.visit(child)
            if (type(child) != bigo_ast.FuncDeclNode): 
                tc += child.time_complexity
        if tc == 0:
            tc = sympy.Rational(1)
        compilation_unit_node.time_complexity = tc
        self.backward_table_manager.pop_table()
        self.backward_vn_table_manager.pop_table()
    
    def visit_FuncDeclNode(self, func_decl_node: bigo_ast.FuncDeclNode):
        if func_decl_node.determine_recursion():
            func_decl_node.time_complexity = [sympy.Symbol(func_decl_node.name, integer=True, positive=True)]
        else:
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

    def visit_ConstantNode(self, const_node: bigo_ast.ConstantNode):
        return sympy.Rational(const_node.value)

    def visit_AssignNode(self, assign_node: bigo_ast.AssignNode):
        target = assign_node.target
        value = assign_node.value
        self.visit(target)

        value_tc = [sympy.Rational(1)]
        self.backward_table_manager.add_symbol(assign_node)
        self.backward_vn_table_manager.add_symbol(assign_node)
        #print(self.backward_vn_table_manager.table_list[-1].vn_table)
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

        if type(left) == sympy.Symbol:
            self.backward_table_manager.current_table.can_replace_varables.append(left.name)
        elif type(right) == sympy.Symbol:
            self.backward_table_manager.current_table.can_replace_varables.append(right.name)

        node.time_complexity = self.add_time(node.left.time_complexity, node.right.time_complexity)

        '''
        if op == '+':
            return operator.add(left, right)
        elif op == '-':
            return operator.sub(left, right)
        elif op == '*':
            return operator.mul(left, right)
        elif op == '/':
            return operator.truediv(left, right)
        elif op == '**':
            return left ** right
        elif op == '<<':
            return left * 2 ** right
        elif op == '>>':
            return left / (2 ** right)
        elif op == '//':
            return left // right
        elif op == '>>':
            return left / (2 ** right)
        elif op == '%':
            return left % right
        elif op == '>>':
            return left / (2 ** right)
        elif op == '|':
            return left | right
        elif op == '&':
            return left & right
        elif op == '>>':
            return left / (2 ** right)
        elif op == '@':
            return left @ right
        '''


    def visit_IfNode(self, if_node: bigo_ast.IfNode):
        self.visit(if_node.condition)
        cond_tc = if_node.condition.time_complexity
        self.backward_table_manager.push_table(scope_type = 'if')
        self.backward_vn_table_manager.push_table(scope_type = 'if')

        true_tc = [sympy.Rational(1)]
        for child in if_node.true_stmt:
            self.visit(child)
            true_tc = self.add_time(true_tc, child.time_complexity)
        print(1, self.backward_vn_table_manager.table_list[-1].vn_table)

        if len(if_node.false_stmt) != 0:
            self.backward_table_manager.push_table(scope_type = 'else')
            self.backward_vn_table_manager.push_table(scope_type = 'else')
        false_tc = [sympy.Rational(1)]
        for child in if_node.false_stmt:
            self.visit(child)
            false_tc = self.add_time(false_tc, child.time_complexity)
        print(2, self.backward_vn_table_manager.table_list[-1].vn_table)
        if len(if_node.false_stmt) != 0:
            self.backward_table_manager.pop_table()
        #    self.backward_vn_table_manager.pop_table()
        #print(3, self.backward_vn_table_manager.table_list[-1].vn_table)
        self.backward_table_manager.pop_table()
        #self.backward_vn_table_manager.pop_table()
        #print(4, self.backward_vn_table_manager.table_list[-1].vn_table)

        true_false_tc = []
        for t_tc in true_tc:
            true_false_tc.append(t_tc)
        for f_tc in false_tc:
            true_false_tc.append(f_tc)

        if_node.time_complexity = self.add_time(cond_tc, true_false_tc)
        self.backward_vn_table_manager.combine_if_else()
        print(3, self.backward_vn_table_manager.table_list[-1].vn_table)
        self.backward_vn_table_manager.update_symbol_to_parent_table()
        print(4, self.backward_vn_table_manager.table_list[-1].vn_table)


        pass

    def visit_ForeachNode(self, foreach_node: bigo_ast.ForeachNode):
        self.backward_table_manager.push_table()
        self.backward_vn_table_manager.push_table()

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

        self.backward_table_manager.pop_table()
        self.backward_vn_table_manager.pop_table()
        foreach_node.time_complexity = tc
        pass

    def visit_WhileNode(self, while_node: bigo_ast.WhileNode):
        self.backward_table_manager.push_table()

        cond = while_node.cond

      
        c_left = self.visit(cond.left)
        c_right = self.visit(cond.right)

        tc = 0
        for child in while_node.children:
            self.visit(child)
            tc += child.time_complexity
        if tc == 0:
            tc = 1

        step = 0
        if type(cond.right) == VariableNode:
            right_rate = self.backward_table_manager.get_symbol_rate(cond.right.name)
        if type(cond.left) == VariableNode:
            left_rate = self.backward_table_manager.get_symbol_rate(cond.left.name)


        if cond.op in ['<','<=']:
            a_n = c_right
            a_1 = c_left
            if '*' == left_rate or '/' == right_rate:
                q = 2
                step = sympy.log(a_n, q) + 1

            elif '+' == left_rate or '-' == right_rate:
                d = 1
                step = (a_n) / d + 1



        elif cond.op in ['>', '>=']:
            a_n = c_left
            a_1 = c_right
            if '/' == left_rate or '*' == right_rate:
                q = 2
                step = sympy.log(a_n / a_1, q) + 1
            elif '-' == left_rate or '+' == right_rate:
                d = 1
                step = (a_n - a_1) / d + 1
        
        else:
            raise NotImplementedError('can not handle loop update, op=', cond.op)
        if step.expand().is_negative:
            raise NotImplementedError('this loop can not analyze.\n', )
        self.backward_table_manager.pop_table()
        while_node.time_complexity = step * tc

        pass
