

class Node(object):
    pass


class Instructions(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class Print(Node):
    def __init__(self, arguments):
        self.arguments = arguments


class Return(Node):
    def __init__(self, value=None):
        """argument may be None for return statement
        without a return value"""
        self.value = value


class For(Node):
    def __init__(self, iterator, start, end, body):
        self.iterator = iterator
        self.range = Range(start, end)
        self.body = body

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class If(Node):
    def __init__(self, condition, body, else_body = None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class FunctionCall(Node):
    def __init__(self, func_name, argument):
        self.name = func_name
        self.argument = argument


class Vector(Node):
    def __init__(self, elements):
        self.elements = elements


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class Reference(Node):
    """A matrix cell reference"""

    def __init__(self, name, coords):
        self.name = name
        self.coords = coords


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


class ArithmeticOperation(BinExpr):
    pass


class Variable(Node):
    def __init__(self, name):
        self.name = name


class Error(Node):
    def __init__(self):
        pass
