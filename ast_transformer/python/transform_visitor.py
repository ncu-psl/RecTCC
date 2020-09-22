import ast
import astunparse
from ast_transformer.python.print_ast_visitor import print_ast_visitor
from bigo_ast.bigo_ast import CompilationUnitNode, FuncDeclNode, FuncCallNode, Operator, BasicNode, IfNode, ClassNode, VariableNode, ConstantNode, ArrayNode, AssignNode, ForeachNode, WhileNode, SubscriptNode


class PyTransformVisitor(ast.NodeVisitor):
    def __init__(self):
        self.parent = None
        self.cu = None
    pass

    def transform(self, root):
        self.visit(root)
        return self.cu

    def visit_Module(self, ast_module: ast.Module):
        self.cu = CompilationUnitNode()
        for child in ast_module.body:
            self.parent = self.cu
            self.cu.add_children(self.visit(child))
        #self.cu.add_parent_to_children()
        pass

    def visit_ClassDef(self, ast_class_def : ast.ClassDef):
        class_def_node = ClassNode()
        class_def_node.name = ast_class_def.name
        for parent in ast_class_def.bases:
            class_def_node.inher.append(parent)
        
        for child in ast_class_def.body:
            self.parent = class_def_node
            class_def_node.add_children(self.visit(child))
        
    def visit_FunctionDef(self, ast_func_def: ast.FunctionDef):
        func_decl_node = FuncDeclNode()
        func_decl_node.name = ast_func_def.name

        if ast_func_def.args.args:
            args_list = ast_func_def.args.args
            for arg in args_list:
                func_decl_node.parameter.append(arg.arg)
                #print("args: ", arg.arg)
        if ast_func_def.args.kwonlyargs:
            kwonlyargs_list = ast_func_def.args.kwonlyargs
            for kwonlyarg in kwonlyargs_list:
                func_decl_node.parameter.append(kwonlyarg.arg)
                #print("kwonlyargs: ", kwonlyarg.arg)
        if ast_func_def.args.vararg:
            func_decl_node.parameter.append(ast_func_def.args.vararg.arg)
            #print("vararg: ", ast_func_def.args.vararg.arg)
        if ast_func_def.args.kwarg:
            func_decl_node.parameter.append(ast_func_def.args.kwarg.arg)
            #print("kwarg: ", ast_func_def.args.kwarg.arg)

        for child in ast_func_def.body:
            self.parent = func_decl_node
            func_decl_node.add_children(self.visit(child))

        return func_decl_node

    def visit_Call(self, ast_call: ast.Call):
        func_call_node = FuncCallNode()
        if hasattr(ast_call.func, 'id'):
            func_call_node.name = ast_call.func.id
        else:
            func_call_node.name = ast_call.func.attr

        args_list = []
        for arg in ast_call.args:
            args_list.append(astunparse.unparse(arg).replace("\n", ""))
        func_call_node.parameter = args_list

        #func_call_node.parameter = astunparse.unparse(ast_call.args)
        return func_call_node

    def visit_Name(self, ast_name: ast.Name):
        variable_node = VariableNode()
        variable_node.name = ast_name.id

        return variable_node

    def visit_List(self, ast_list: ast.List):
        array_node = ArrayNode()
        for elt in ast_list.elts:
            array_node.array.append(self.visit(elt))
        return array_node

    def visit_Tuple(self, ast_tuple: ast.Tuple):
        array_node = ArrayNode()
        for elt in ast_tuple.elts:
            array_node.array.append(self.visit(elt))
        return array_node

    def visit_Num(self, ast_num: ast.Num):
        constant_node = ConstantNode()
        if type(ast_num.n) == int:
            constant_node.value = ast_num.n
        # else:
        #     raise NotImplementedError('Constant type not support: ', type(ast_num.n))

        return constant_node

    def visit_Assign(self, ast_assign: ast.Assign):
        # create Big-O AST assign node
        assign_node = AssignNode()
        assign_node.target = self.visit(ast_assign.targets[0])
        assign_node.value = self.visit(ast_assign.value)

        return assign_node

    def visit_AnnAssign(self, ast_ann_assign: ast.AnnAssign):
        # create Big-O AST assign node
        assign_node = AssignNode()
        assign_node.target = self.visit(ast_ann_assign.targets[0])
        assign_node.value = self.visit(ast_ann_assign.value)

        return assign_node

    def visit_AugAssign(self, ast_aug_assign: ast.AugAssign):
        # need to do some trick of +=, -=, *=, /=
        if type(ast_aug_assign.op) == ast.Add:
            new_op = ast.BinOp(ast_aug_assign.target, ast.Add(), ast_aug_assign.value)
        elif type(ast_aug_assign.op) == ast.Sub:
            new_op = ast.BinOp(ast_aug_assign.target, ast.Sub(), ast_aug_assign.value)
        elif type(ast_aug_assign.op) == ast.Mult:
            new_op = ast.BinOp(ast_aug_assign.target, ast.Mult(), ast_aug_assign.value)
        elif type(ast_aug_assign.op) == ast.Div:
            new_op = ast.BinOp(ast_aug_assign.target, ast.Div(), ast_aug_assign.value)
        else:
            raise Exception("does not support operator: ", ast_aug_assign.op)
        ast_assign = ast.Assign(ast_aug_assign.target, new_op)

        # create Big-O AST assign node
        assign_node = AssignNode()
        assign_node.target = self.visit(ast_assign.targets)
        assign_node.value = self.visit(ast_assign.value)

        return assign_node
    def visit_BoolOp(self, ast_bool_op: ast.BoolOp):
        if type(ast_bool_op.op) == ast.And:
            op = '&&'
        elif type(ast_bool_op.op) == ast.Or:
            op = '||'
        else:
            raise Exception("does not support operator: ", ast_bool_op.op)

        operator_node = Operator()
        operator_node.op = op
        for i, node in enumerate(ast_bool_op.values):
            if i == (len(ast_bool_op.values)-1) and i > 1:
                right = self.visit(node)
                deep_operator_node.right = right

            elif i == 0:
                left = self.visit(node)
                operator_node.left = left

            else: #right
                left = self.visit(node)
                deep_operator_node = Operator()
                deep_operator_node.op = op
                deep_operator_node.left = left
                operator_node.right = deep_operator_node

        operator_node.add_children(operator_node.left)
        operator_node.add_children(operator_node.right)
        return operator_node

    def visit_BinOp(self, ast_bin_op: ast.BinOp):
        operator_node = Operator()

        if type(ast_bin_op.op) == ast.Add:
            operator_node.op = '+'
        elif type(ast_bin_op.op) == ast.Sub:
            operator_node.op = '-'
        elif type(ast_bin_op.op) == ast.Mult:
            operator_node.op = '*'
        elif type(ast_bin_op.op) == ast.Div:
            operator_node.op = '/'
        elif type(ast_bin_op.op) == ast.FloorDiv:
            operator_node.op = '//'
        elif type(ast_bin_op.op) == ast.Mod:
            operator_node.op = '%'
        elif type(ast_bin_op.op) == ast.Pow:
            operator_node.op = '**'
        elif type(ast_bin_op.op) == ast.LShift:
            operator_node.op = '<<'
        elif type(ast_bin_op.op) == ast.RShift:
            operator_node.op = '>>'
        elif type(ast_bin_op.op) == ast.BitOr:
            operator_node.op = '|'
        elif type(ast_bin_op.op) == ast.BitAnd:
            operator_node.op = '&'
        elif type(ast_bin_op.op) == ast.MatMult:
            operator_node.op = '@'
        else:
            raise Exception("does not support operator: ", ast_bin_op.op)

        operator_node.left = self.visit(ast_bin_op.left)
        operator_node.right = self.visit(ast_bin_op.right)

        operator_node.expression = astunparse.unparse(ast_bin_op)
        #print("Do Operation: %s" %(operator_node.expression))
        operator_node.add_children(operator_node.left)
        operator_node.add_children(operator_node.right)

        return operator_node

    def visit_Compare(self, ast_compare: ast.Compare):
        operator_node = Operator()
        left = self.visit(ast_compare.left)
        right = self.visit(ast_compare.comparators[0])
        op = self.transform_op(ast_compare.ops[0])
        operator_node.left = left
        operator_node.right = right
        operator_node.op = op
        return operator_node

    def transform_op(self, compare_op):
        if isinstance(compare_op, ast.Eq):
            return '=='
        if isinstance(compare_op, ast.NotEq):
            return '!='
        if isinstance(compare_op, ast.Lt):
            return '<'
        if isinstance(compare_op, ast.LtE):
            return '<='
        if isinstance(compare_op, ast.Gt):
            return '>'
        if isinstance(compare_op, ast.GtE):
            return '>='
        if isinstance(compare_op, ast.Is):
            return '=='
        if isinstance(compare_op, ast.IsNot):
            return '!='
        if isinstance(compare_op, ast.In):
            return '=='
        if isinstance(compare_op, ast.NotIn):
            return '!='
        else:
            raise Exception("can't support this compare op : ", type(compare_op)) 


    def visit_If(self, ast_if: ast.If):
        if_node = IfNode()
        if_node.condition = self.visit(ast_if.test)

        if type(ast_if.body) is not list:
            ast_if.body = [ast_if.body]

        self.parent = if_node.true_stmt
        for child in ast_if.body or []:
            child_node = self.visit(child)
            if child_node:
                if type(child_node) is list:
                    if_node.true_stmt.extend(child_node)
                else:
                    if_node.true_stmt.append(child_node)

        if ast_if.orelse:
            if type(ast_if.orelse) is not list:
                ast_if.orelse = [ast_if.orelse]

            self.parent = if_node.false_stmt
            for child in ast_if.orelse or []:
                child_node = self.visit(child)
                if child_node:
                    if type(child_node) is list:
                        if_node.false_stmt.extend(child_node)
                    else:
                        if_node.false_stmt.append(child_node)

        return if_node

    def for_iter(self, ast_iter):
        if type(ast_iter) == ast.Call:
            variable_node = VariableNode()
            variable_node.name = print_ast_visitor().print_node(ast_iter)
            return variable_node
            
        elif type(ast_iter) == ast.Attribute:
            variable_node = VariableNode()
            variable_node.name = print_ast_visitor().print_node(ast_iter)
            return variable_node

        else:
            if type(ast_iter) == ast.Name:
                terminal = self.visit(ast_iter)
                return terminal
        raise Exception("can't support this iter type : ", type(ast_iter)) 

    def visit_For(self, ast_for):
        foreach_node = ForeachNode()

        foreach_node.variable = self.for_iter(ast_for.iter)

        target = self.visit(ast_for.target)
        if type(target) is list:
            foreach_node.target.extend(target)
        else:
            foreach_node.target.append(target)

        iter = self.visit(ast_for.iter)
        if type(iter) is list:
            foreach_node.iter.extend(iter)
        else:
            foreach_node.iter.append(iter)

        for child in ast_for.body:
            child_node = self.visit(child)
            foreach_node.add_children(child_node)

        return foreach_node

    def visit_While(self, ast_while):
        while_node = WhileNode()        
        while_node.cond = self.visit(ast_while.test)
               
        for child in ast_while.body:
            child_node = self.visit(child)
            while_node.add_children(child_node)
            
        return while_node

    def visit_Subscript(self, ast_subscript: ast.Subscript):
        subscript_node = SubscriptNode()
        subscript_node.value = self.visit(ast_subscript.value)
        subscript_node.slice = self.visit(ast_subscript.slice)

        return subscript_node

    def generic_visit(self, node):
        children = []
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        child = self.visit(item)
                        if type(child) is list:
                            children.extend(child)
                        else:
                            children.append(child)
            elif isinstance(value, ast.AST):
                child = self.visit(value)
                if type(child) is list:
                    children.extend(child)
                else:
                    children.append(child)
        return children

    #@staticmethod
    #def set_coordinate(node: BasicNode, coord):
    #    if coord:
    #        pass
