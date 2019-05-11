
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


class Interpreter(object):

    def __init__(self):
        self.memories = MemoryStack()


    @on('node')
    def visit(self, node):
        print("interpret DEFAULT")
        pass

    @when(AST.Block)
    def visit(self, node):
        return node.content.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        print("interpret Instructions")
        for n in node.nodes:
            n.accept(self)

    @when(AST.BinExpr)
    def visit(self, node):
        print("interpret AST.BinExpr")
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        op_fun = binop_to_operator[node.op]
        return op_fun(r1, r2)

    @when(AST.Assignment)
    def visit(self, node):
        print("interpret AST.Assignment")
        value = node.right.accept(self)
        # TODO make it work for matrices on lhs
        var = node.left
        print("{} = {}".format(var, value))
        self.memories.insert(var.name, value)
        print(self.memories)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    # simplistic while loop interpretation
    @when(AST.While)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r
