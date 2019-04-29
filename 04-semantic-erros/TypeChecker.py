#!/usr/bin/python

from collections import defaultdict
from copy import copy
import AST

allowed_operations = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "")))

allowed_operations["+"]["int"]["int"] = "int"
allowed_operations["+"]["float"]["int"] = "float"
allowed_operations["+"]["int"]["float"] = "float"
allowed_operations["+"]["vector"]["vector"] = "vector"
allowed_operations["+"]["matrix"]["matrix"] = "matrix"

allowed_operations["-"]["int"]["int"] = "int"
allowed_operations["-"]["float"]["int"] = "float"
allowed_operations["-"]["int"]["float"] = "float"
allowed_operations["-"]["vector"]["vector"] = "vector"
allowed_operations["-"]["matrix"]["matrix"] = "matrix"

allowed_operations["*"]["int"]["int"] = "int"
allowed_operations["*"]["float"]["int"] = "float"
allowed_operations["*"]["int"]["float"] = "float"
allowed_operations["*"]["vector"]["vector"] = "vector"
allowed_operations["*"]["matrix"]["matrix"] = "matrix"
allowed_operations["*"]["vector"]["int"] = "vector"
allowed_operations["*"]["int"]["vector"] = "vector"
allowed_operations["*"]["matrix"]["int"] = "matrix"
allowed_operations["*"]["int"]["matrix"] = "matrix"
allowed_operations["*"]["vector"]["float"] = "vector"
allowed_operations["*"]["float"]["vector"] = "vector"
allowed_operations["*"]["matrix"]["float"] = "matrix"
allowed_operations["*"]["float"]["matrix"] = "matrix"

allowed_operations["/"]["int"]["int"] = "float"
allowed_operations["/"]["float"]["int"] = "float"
allowed_operations["/"]["int"]["float"] = "float"
allowed_operations["/"]["vector"]["int"] = "vector"
allowed_operations["/"]["int"]["vector"] = "vector"
allowed_operations["/"]["matrix"]["int"] = "matrix"
allowed_operations["/"]["int"]["matrix"] = "matrix"
allowed_operations["/"]["vector"]["int"] = "vector"
allowed_operations["/"]["matrix"]["int"] = "matrix"
allowed_operations["/"]["vector"]["float"] = "vector"
allowed_operations["/"]["matrix"]["float"] = "matrix"

allowed_operations[".+"]["matrix"]["int"] = "matrix"
allowed_operations[".+"]["matrix"]["float"] = "matrix"
allowed_operations[".+"]["vector"]["int"] = "vector"
allowed_operations[".+"]["vector"]["float"] = "vector"

allowed_operations[".-"]["matrix"]["int"] = "matrix"
allowed_operations[".-"]["matrix"]["float"] = "matrix"
allowed_operations[".-"]["vector"]["int"] = "vector"
allowed_operations[".-"]["vector"]["float"] = "vector"

allowed_operations[".*"]["matrix"]["int"] = "matrix"
allowed_operations[".*"]["matrix"]["float"] = "matrix"
allowed_operations[".*"]["vector"]["int"] = "vector"
allowed_operations[".*"]["vector"]["float"] = "vector"

allowed_operations["./"]["matrix"]["int"] = "matrix"
allowed_operations["./"]["matrix"]["float"] = "matrix"
allowed_operations["./"]["vector"]["int"] = "vector"
allowed_operations["./"]["vector"]["float"] = "vector"

op_to_string = {
    '+': 'ADD',
    '-': 'SUB',
    '*': 'MUL',
    '/': 'DIV',
}


class NodeVisitor(object):
    loop = 0
    variables = defaultdict(lambda: None)

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)


class TypeChecker(NodeVisitor):

    def visit_Instructions(self, node):
        # print("Visit Instructions")
        for n in node.nodes:
            self.visit(n)

    def visit_FlowKeyword(self, node):
        # print("Visit Flowkeyword")
        if self.loop == 0:
            TypeChecker.print_error(node, "flow keyword {} outside loop".format(node.keyword))

    def visit_Print(self, node):
        # print("Visit Print")
        pass

    def visit_Return(self, node):
        # print("Visit Return")
        pass

    def visit_String(self, node):
        # print("Visit String")
        pass

    def visit_Matrix(self, node):
        size1 = len(node.elements)
        sizes = map(lambda x: len(x.elements), node.elements)
        size2 = min(sizes)
        if all(map(lambda x: x == size2, sizes)):
            return self.Variable("matrix", [size1, size2])
        else:
            TypeChecker.print_error(node, "vectors with different sizes int matrix initialization")
            return None

    def visit_Vector(self, node):
        # print("Visit Vector")
        return self.Variable("vector", [len(node.elements)])

    def visit_Reference(self, node):
        # print("Visit Reference")
        v = self.variables[node.name.name]
        if not v:
            TypeChecker.print_error(node, "undefined variable {}".format(node.name.name))
            return None
        if len(node.coords) > len(v.size):
            TypeChecker.print_error(node, "to many dimensions in vector reference")
            return None
        error = False
        for coord, size in zip(node.coords, v.size):
            if isinstance(coord, AST.IntNum) and coord.value >= size:
                TypeChecker.print_error(node, "reference {} is over vector size {}".format(coord.value, size))
                error = True
        if error:
            return None
        if len(v.size) - len(node.coords) == 0:
            return TypeChecker.Variable("float")
        else:
            return TypeChecker.Variable("vector", [v.size[-1]])

    def visit_FunctionCall(self, node):
        # print("Visit FunctionCall")
        return TypeChecker.Variable("matrix", node.arguments)

    def visit_While(self, node):
        # print("Visit While")
        self.loop += 1
        self.visit(node.body)
        self.loop -= 1

    def visit_For(self, node):
        # print("Visit For")
        self.loop += 1
        self.visit(node.body)
        self.loop -= 1

    def visit_Range(self, node):
        # print("Visit Range")
        pass

    def visit_Variable(self, node):
        # print("Visit Variable")
        return self.variables[node.name]

    def visit_If(self, node):
        # print("Visit if")
        pass

    def visit_BinExpr(self, node):
        # print("Visit BinExpr")

        var1 = self.visit(node.left)
        var2 = self.visit(node.right)
        if not var1:
            TypeChecker.print_error(node, "undefined variable {}".format(node.left.name))
            return None
        if not var2:
            TypeChecker.print_error(node, "undefined variable {}".format(node.right.name))
            return None
        op = node.op
        newtype = allowed_operations[op[0]][var1.type][var2.type]
        if newtype:
            new_var = copy(var1)
            new_var.type = newtype
            return new_var
        else:
            TypeChecker.print_error(node, "cannot {} {} and {}".format(op_to_string[op], var1.type, var2.type))
            return None

    def visit_ArithmeticOperation(self, node):
        # print("Visit ArithmeticOperation")
        return self.visit_BinExpr(node)

    def visit_Assignment(self, node):
        # print("visit_Assignment")
        var1 = self.visit(node.left)
        var2 = self.visit(node.right)
        if not var2:
            return None
        name = node.left.name
        op = node.op
        if op == "=":
            self.variables[name] = self.Variable(var2.type, var2.size, name)
        else:
            if not var1:
                TypeChecker.print_error(node, "undefined variable {}".format(name))
                return None
            newtype = allowed_operations[op[0]][var1.type][var2.type]
            if newtype:
                self.variables[name] = self.Variable(newtype, var2.size, name)
            else:
                TypeChecker.print_error(node, "cannot assign {} to {}".format(var2.type, var1.type))

    def visit_IntNum(self, node):
        # print("visit_IntNum")
        return self.Variable("int")

    def visit_FloatNum(self, node):
        # print("visit_FloatNum")
        return self.Variable("float")

    def visit_UnaryExpr(self, node):
        # print("visit_UnaryExpr")
        pass

    def visit_Comparison(self, node):
        # print("visit_Comparison")
        pass

    def visit_Error(self, node):
        # print("visit_Error")
        pass

    @staticmethod
    def print_error(node, error):
        print("Error: {}".format(error))

    class Variable(object):
        def __init__(self, type, size=[], name=""):
            self.type = type
            self.size = size
            self.name = name

        def __str__(self):
            return 'Variable {}: {}, {}'.format(self.name, self.type, self.size)
