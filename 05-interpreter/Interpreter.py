
import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys
import operator
import copy


def transpose(matrix):
    dim1 = len(matrix[0])
    dim2 = len(matrix)
    new_matrix = [[0] * dim2 for _ in range(dim1)]

    for i in range(dim1):
        for j in range(dim2):
            new_matrix[i][j] = matrix[j][i]

    return new_matrix


def ones(dim1, dim2=None):
    if dim2 is None:
        dim2 = dim1
    return [[1] * dim2 for _ in range(dim1)]


def zeros(dim1, dim2=None):
    if dim2 is None:
        dim2 = dim1
    return [[0] * dim2 for _ in range(dim1)]


def eye(dim1, dim2=None):
    if dim2 is None:
        dim2 = dim1
    arr = [[0] * dim2 for _ in range(dim1)]
    for i in range(min(dim1, dim2)):
        arr[i][i] = 1
    return arr


def mul(var1, var2):
    if not (isinstance(var1, list) and isinstance(var2, list)):
        return var1 * var2
    # matrix multiplication
    dim1, dim2 = len(var1), len(var2[0])
    trans = transpose(var2)
    result = zeros(dim1, dim2)
    for i in range(dim1):
        for j in range(dim2):
            result[i][j] = sum(x * y for x, y in zip(var1[i], trans[j]))
    return result


binop_to_operator = {
    '+': operator.add,
    '-': operator.sub,
    '*': mul,
    '/': operator.div,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
    '!=': operator.ne,
    '==': operator.eq,
}

unop_to_operator = {
    'NEGATE': operator.neg,
    'TRANSPOSE': transpose
}

builtin = {
    'ones': ones,
    'zeros': zeros,
    'eye': eye
}


def elementwise(op):
    def fun(left, right):
        if isinstance(left, list):
            return [fun(l, r) for l, r in zip(left, right)]
        else:
            return binop_to_operator[op[1]](left, right)
    return fun


sys.setrecursionlimit(10000)


# TODO ensure all AST classes are covered


class Interpreter(object):
    memories = MemoryStack()

    # indicates that next variable reference should not be resolved
    # to its value
    lvalue = False

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Instructions)
    def visit(self, node):
        for n in node.nodes:
            n.accept(self)

    @when(AST.Block)
    def visit(self, node):
        self.memories.push()
        try:
            node.content.accept(self)
        finally:
            self.memories.pop()

    @when(AST.FlowKeyword)
    def visit(self, node):
        if node.keyword == "BREAK":
            raise BreakException()
        elif node.keyword == "CONTINUE":
            raise ContinueException()

    @when(AST.Print)
    def visit(self, node):
        print "PRINT: " + ", ".join(str(arg.accept(self))
                                     for arg in node.arguments)

    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException(node.value.accept(self))

    @when(AST.Vector)
    def visit(self, node):
        return [e.accept(self) for e in node.elements]

    @when(AST.Matrix)
    def visit(self, node):
        return [e.accept(self) for e in node.elements]

    @when(AST.Reference)
    def visit(self, node):
        lvalue = self.lvalue
        self.lvalue = False

        reference = ConcreteReference(
            node.lineno,
            node.container,
            [c.accept(self) for c in node.coords]
        )

        if lvalue:
            return reference
        else:
            return self.memories.get(reference)

    @when(AST.FunctionCall)
    def visit(self, node):
        arguments = [arg.accept(self) for arg in node.arguments]
        func = builtin[node.name]
        return func(*arguments)

    @when(AST.While)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.body.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break

    @when(AST.For)
    def visit(self, node):
        self.memories.push()
        try:
            self.lvalue = True
            iterator_ref = node.iterator.accept(self)
            self.lvalue = False

            start, end = node.range.accept(self)
            self.memories.insert(iterator_ref, start)

            while self.memories.get(iterator_ref) < end:
                try:
                    node.body.accept(self)
                except ContinueException:
                    pass
                except BreakException:
                    break
                iterator_val = self.memories.get(iterator_ref)
                self.memories.set(iterator_ref, iterator_val + 1)
        finally:
            self.memories.pop()

    @when(AST.Range)
    def visit(self, node):
        start = node.start.accept(self)
        end = node.end.accept(self)
        return start, end

    @when(AST.Variable)
    def visit(self, node):
        if self.lvalue:
            return node
        return self.memories.get(node)

    @when(AST.If)
    def visit(self, node):
        if node.condition.accept(self):
            node.body.accept(self)
        elif node.else_body is not None:
            node.else_body.accept(self)

    @when(AST.ArithmeticOperation)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        if node.op[0] == '.':
            op_fun = elementwise(node.op)
        else:
            op_fun = binop_to_operator[node.op]
        return op_fun(r1, r2)

    @when(AST.Assignment)
    def visit(self, node):
        self.lvalue = True
        target_ref = node.left.accept(self)
        self.lvalue = False

        if node.op == "=":
            value = node.right.accept(self)
            self.memories.insert(target_ref, value)
        else:
            op_fun = binop_to_operator[node.op[0]]

            rhs = node.right.accept(self)
            lhs_value = node.left.accept(self)
            value = op_fun(lhs_value, rhs)

            self.memories.set(target_ref, value)

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.Comparison)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        op_fun = binop_to_operator[node.op]
        return op_fun(r1, r2)

    @when(AST.UnaryExpr)
    def visit(self, node):
        op_fun = unop_to_operator[node.operation]
        operand = node.operand.accept(self)
        return op_fun(operand)


class ConcreteReference(AST.Reference):
    """Vector or matrix reference with its container
    and coordinates resolved to concerte values"""
    pass
