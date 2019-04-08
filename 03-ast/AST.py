

class Node(object):
    pass


class Instructions(Node):
    def __init__(self, nodes):
        self.nodes = nodes


class FlowKeyword(Node):
    def __init__(self, keyword):
        self.keyword = keyword.upper()


class Print(Node):
    def __init__(self, arguments):
        self.arguments = arguments


class Return(Node):
    def __init__(self, value=None):
        """argument may be None for return statement
        without a return value"""
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Vector(Node):
    def __init__(self, elements):
        self.elements = elements


class Reference(Node):
    """A matrix cell reference"""

    def __init__(self, name, coords):
        self.name = name
        self.coords = coords


class FunctionCall(Node):
    def __init__(self, func_name, argument):
        self.name = func_name
        self.argument = argument


class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class For(Node):
    def __init__(self, iterator, start, end, body):
        self.iterator = iterator
        self.range = Range(start, end)
        self.body = body


class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Variable(Node):
    def __init__(self, name):
        self.name = name


class If(Node):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class ArithmeticOperation(BinExpr):
    pass

class Assignment(BinExpr):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class UnaryExpr(Node):
    def __init__(self, operation, operand):
        self.operation = operation
        self.operand = operand



class Comparison(BinExpr):
    pass


class Error(Node):
    def __init__(self):
        pass
