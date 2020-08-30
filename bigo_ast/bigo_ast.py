import json
import sympy

class BasicNode(object):

    def __init__(self):
        self.time_complexity = [sympy.Rational(1)]
        #self.time_complexity = '1'
        self.__children = []
        self.parent = None
        self.__type = self.__class__.__name__

    def __iter__(self):
        for child in self.__children:
            yield child

    @property
    def children(self) -> []:
        return self.__children

    @children.setter
    def children(self, children):
        self.__children = children

    def add_children(self, children):
        if not children:
            return

        if type(children) is list:
            self.__children.extend(children)
        else:
            self.__children.append(children)

    def add_parent_to_children(self):
        for child in self.__children:
            child.parent = self
            child.add_parent_to_children()
        pass

    def to_dict(self):
        d = {
#             '_type': self.__type,
             'time_complexity': self.time_complexity,
#             'col': self.col,
#             'line_number': self.line_number,
             'parent': None}

        children_list = []
        for child in self.__children:
            children_list.append(child.to_dict())

        d.update({'children': children_list})
        
        return d

###############################################################
###############################################################


###############################################################
###############################################################

class CompilationUnitNode(BasicNode):

    def __init__(self):
        super().__init__()

        pass


class ClassNode(BasicNode):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.inher = []
        self.vir_inher = []
    pass

class FuncDeclNode(BasicNode):
    def __init__(self):
        super().__init__()

        self.recursive = False
        self.name = ''
        self.parameter = []

        pass

    def determine_recursion(self):
        que = [self]

        while que:
            node = que.pop(0) 
            if isinstance(node, FuncCallNode):
                if node.name == self.name:
                    self.recursive = True
                    #break
            for child in node:
                que.append(child)

        return self.recursive

    def to_dict(self):
        d = super().to_dict()
        d.update({'recursive': self.recursive})
        d.update({'name': self.name})
        d.update({'parameter': self.parameter})

        return d


class FuncCallNode(BasicNode):
    def __init__(self):
        super().__init__()

        self.name = ''
        self.parameter = []
        
        pass

    def to_dict(self):
        d = super().to_dict()
        d.update({'name': self.name})
        d.update({'parameter': self.parameter})

        return d

class VariableNode(BasicNode):

    def __init__(self):
        super().__init__()

        self.name = ''
        self.value = ''

        pass

    def to_dict(self):
        d = super().to_dict()
        d.update({'value': self.name})

        return d
        
class ArrayNode(BasicNode):
    
    def __init__(self):
        super().__init__()

class ArrayNode(BasicNode):

    def __init__(self):
        super().__init__()

        self.array = []

        pass
    def to_dict(self):
        d = super().to_dict()
        d.update({'array': self.array})

        return d

class ConstantNode(BasicNode):

    def __init__(self):
        super().__init__()

        self.value = 0

        pass

    def to_dict(self):
        d = super().to_dict()
        d.update({'value': self.value})

        return d
    
    
class AssignNode(BasicNode):

    def __init__(self):
        super().__init__()
        self.__target = BasicNode()
        self.__value = BasicNode()

        pass

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, target):
        self.__target = target
        self.add_children(self.target)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.add_children(self.value)

    def to_dict(self):
        d = super().to_dict()
        d.update({'target': self.target.to_dict()})
        d.update({'value': self.value.to_dict()})

        return d


class Operator(BasicNode):

    def __init__(self):
        super().__init__()

        self.op = ''
        self.left = BasicNode()
        self.right = BasicNode()
        self.expression = ''

        pass

    def to_dict(self):
        d = super().to_dict()
        d.update({'left': self.left.to_dict()})
        d.update({'right': self.right.to_dict()})

        return d


class IfNode(BasicNode):
    
    def __init__(self):
        super().__init__()

        self.condition = BasicNode()
        self.true_stmt = []
        self.false_stmt = []

        pass

    def __iter__(self):
        for child in self.condition:
            yield child
        for child in self.true_stmt:
            yield child
        for child in self.false_stmt:
            yield child

    def to_dict(self):
        d = super().to_dict()
        d.update({'condition': self.condition.to_dict()})
        d.update({'true': self.true_stmt})
        d.update({'false': self.false_stmt})

        return d

class ForNode(BasicNode):
    def __init__(self):
        super().__init__()

        self.variable = None
        self.init = []
        self.term = []
        self.update = []

        pass

    def to_dict(self):
        d = super().to_dict()
        d.update({'variable': self.variable})

        init_list = []
        for child in self.init:
            init_list.append(child.to_dict())

        d.update({'init': init_list})

        term_list = []
        for child in self.init:
            term_list.append(child.to_dict())
        d.update({'terminal': term_list})

        update_list = []
        for child in self.init:
            update_list.append(child.to_dict())
        d.update({'update': update_list})

        return d

class ForeachNode(BasicNode):
    def __init__(self):
        super().__init__()

        self.variable = BasicNode()
        self.target = []
        self.iter = []
        pass

    def to_dict(self):
        d = super().to_dict()
        
        target_list = []
        for child in self.target:
            target_list.append(child.to_dict())

        d.update({'target': target_list})

        iter_list = []
        for child in self.iter:
            iter_list.append(child.to_dict())
        d.update({'iter': iter_list})

        d.update({'variable': self.variable})
        return d

class WhileNode(BasicNode):
    def __init__(self):
        super().__init__()

        self.cond = []

        pass

    def to_dict(self):
        d = super().to_dict()
        
        cond_list = []
        for clild in self.cond:
            cond_list.append(child.to_dict())
        d.update({'cond': cond_list})

        return d

