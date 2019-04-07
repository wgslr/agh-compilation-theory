

class Node(object):
    pass


class Instructions(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Print(Node):
    def __init__(self, arguments):
        if isinstance(arguments, list):
            self.arguments = arguments
        else:
            self.arguments = [arguments]


class Return(Node):
    def __init__(self, value=None):
        """argument may be None for return statement
        without a return value"""
        self.value = value


class FunctionCall(Node):
    def __init__(self, func_name, argument):
        self.name = func_name
        self.argument = argument


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class UnaryExpr(Node):
    def __init__(self, operation, operand):
        self.operation = operation
        self.operand = operand


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


class Variable(Node):
    def __init__(self, name):
        self.name = name


class Error(Node):
    def __init__(self):
        pass
