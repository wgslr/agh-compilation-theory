

class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    # TODO remove - use printTreee
    def __repr__(self):
        return "{} {} {}".format(self.left, self.op, self.right)


class Assignment(BinExpr):
    pass

class Comparison(BinExpr):
    pass

class ArithemticOperation(BinExpr):
    pass

# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        pass
      
