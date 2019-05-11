
import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys
import operator

binop_to_operator = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.div
}

sys.setrecursionlimit(10000)


# TODO make TypeChecker throw error when using undefined variable
# in rhs context

class Interpreter(object):

    def __init__(self):
        self.memories = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Block)
    def visit(self, node):
        return node.content.accept(self)

    @when(AST.FlowKeyword)
    def visit(self, node):
        if node.keyword == "BREAK":
            raise BreakException()
        elif node.keyword == "CONTINUE":
            raise ContinueException()

    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException(node.value)

    @when(AST.Instructions)
    def visit(self, node):
        for n in node.nodes:
            n.accept(self)

    @when(AST.ArithmeticOperation)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        op_fun = binop_to_operator[node.op]
        return op_fun(r1, r2)

    @when(AST.Assignment)
    def visit(self, node):
        print("inteprete assignemnt: {} {} {}".format(node.left, node.op, node.right))
        # TODO make it work for matrices on lhs

        var = node.left

        if node.op == "=":
            value = node.right.accept(self)
            # TODO danger - 'name' can be Reference.name
            self.memories.insert(var.name, value)
        else:
            rhs = node.right.accept(self)
            op_fun = binop_to_operator[node.op[0]]
            value = op_fun(var.accept(self), rhs) 
            self.memories.insert(var.name, value)

    @when(AST.Print)
    def visit(self, node):
        print "PRINT: " + ", ".join((str(arg.accept(self)) for arg in node.arguments))

    @when(AST.Variable)
    def visit(self, node):
        return self.memories.get(node.name)

    @when(AST.Reference)
    def visit(self, node):
        vector = self.memories.get(node.name.name)
        for coord in node.coords[:-1]:
            vector = vector[coord.accept(self)]
        return IndexReference(vector, node.coords[-1].accept(self))

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.Vector)
    def visit(self, node):
        return [e.accept(self) for e in node.elements]

    @when(AST.Matrix)
    def visit(self, node):
        return [e.accept(self) for e in node.elements]

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    # simplistic while loop interpretation
    @when(AST.While)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r

    @when(IndexReference)
    def visit(self, node):
        return node.get()
