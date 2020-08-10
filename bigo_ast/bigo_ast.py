import json

class BasicNode(object):

    def __init__(self):
        #self.time_complexity = sumpy.Rational(1)
        self.time_complexity = '1'
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
                    print("Find a recursive pattern!! %s%s" %(node.name, node.parameter))
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



