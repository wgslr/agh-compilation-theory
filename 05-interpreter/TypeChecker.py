#!/usr/bin/env python2

from collections import defaultdict
from copy import copy
import AST
from SymbolTable import Variable, SymbolTable

allowed_operations = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "")))

allowed_operations["+"]["int"]["int"] = "int"
allowed_operations["+"]["float"]["int"] = "float"
allowed_operations["+"]["int"]["float"] = "float"
allowed_operations["+"]["vector"]["vector"] = "vector"
allowed_operations["+"]["matrix"]["matrix"] = "matrix"
allowed_operations["+"]["string"]["string"] = "string"

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
    symbols = SymbolTable()

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)


class TypeChecker(NodeVisitor):
    error_occured = False

    def visit_Block(self, node):
        # print("visit_Instructions")
        self.symbols = self.symbols.createChild()
        self.visit(node.content)
        self.symbols = self.symbols.getParentScope()

    def visit_Instructions(self, node):
        # print("visit_Instructions")
        for n in node.nodes:
            self.visit(n)

    def visit_FlowKeyword(self, node):
        # print("visit_Flowkeyword")
        if self.loop == 0:
            self.print_error(node, "flow keyword {} outside loop".format(node.keyword))

    def visit_Print(self, node):
        # print("visit_Print")
        pass

    def visit_Return(self, node):
        # print("visit_Return")
        pass

    def visit_String(self, node):
        return Variable("string")

    def visit_Matrix(self, node):
        size1 = len(node.elements)
        sizes = map(lambda x: len(x.elements), node.elements)
        size2 = min(sizes)
        if all(x == size2 for x in sizes):
            return Variable("matrix", [size1, size2])
        else:
            self.print_error(node, "vectors with different sizes in matrix initialization")
            return None

    def visit_Vector(self, node):
        # print("visit_Vector")
        return Variable("vector", [len(node.elements)])

    def visit_Reference(self, node):
        # print("visit_Reference")
        v = self.symbols.get(node.container.name)
        if not v:
            self.print_error(node, "undefined variable {}".format(node.container.name))
            return None
        if len(node.coords) > len(v.size):
            self.print_error(node, "to many dimensions in vector reference")
            return None
        error = False
        for coord, size in zip(node.coords, v.size):
            if isinstance(coord, AST.IntNum) and coord.value >= size:
                self.print_error(node, "reference {} is over vector size {}".format(coord.value, size))
                error = True
        if error:
            return None
        if len(v.size) - len(node.coords) == 0:
            return Variable("float")
        else:
            return Variable("vector", [v.size[-1]])

    def visit_FunctionCall(self, node):
        print("visit_FunctionCall")
        arguments = node.arguments
        if len(arguments) == 1:
            arguments = [arguments[0], arguments[0]]
        return Variable("matrix", [x.value for x in arguments])

    def visit_While(self, node):
        # print("visit_While")
        self.loop += 1
        self.visit(node.body)
        self.loop -= 1

    def visit_For(self, node):
        # print("visit_For")
        self.loop += 1
        self.symbols = self.symbols.createChild()

        iterator_var = Variable('int', [], node.iterator.name)
        self.symbols.put(iterator_var.name, iterator_var)
        self.visit(node.body)

        self.symbols = self.symbols.getParentScope()
        self.loop -= 1

    def visit_Range(self, node):
        # print("visit_Range")
        pass

    def visit_Variable(self, node):
        # print("visit_Variable")
        return self.symbols.get(node.name)

    def visit_If(self, node):
        # print("visit_if")
        pass

    def visit_BinExpr(self, node):
        # print("visit_BinExpr")

        var1 = self.visit(node.left)
        var2 = self.visit(node.right)
        if not var1:
            self.print_error(node, "undefined variable {}".format(node.left.name))
            return None
        if not var2:
            self.print_error(node, "undefined variable {}".format(node.right.name))
            return None
        op = node.op
        newtype = allowed_operations[op[0]][var1.type][var2.type]
        if newtype:
            new_var = copy(var1)
            new_var.type = newtype
            return new_var
        else:
            self.print_error(node, "cannot {} {} and {}".format(op_to_string[op], var1.type, var2.type))
            return None

    def visit_ArithmeticOperation(self, node):
        # print("visit_ArithmeticOperation")
        return self.visit_BinExpr(node)

    def visit_Assignment(self, node):
        # print("visit_Assignment")
        var1 = self.visit(node.left)
        var2 = self.visit(node.right)
        if not var2:
            return None
        if isinstance(node.left, AST.Variable):
            name = node.left.name
        else:
            name = node.left.container.name
        op = node.op
        if op == "=":
            symbol = Variable(var2.type, var2.size, name)
            self.symbols.put(name, symbol)
        else:
            if not var1:
                self.print_error(node, "undefined variable {}".format(name))
                return None
            newtype = allowed_operations[op[0]][var1.type][var2.type]
            if newtype:
                symbol = Variable(newtype, var2.size, name)
                self.symbols.put(name, symbol)
            else:
                self.print_error(node, "cannot assign {} to {}".format(var2.type, var1.type))

    def visit_IntNum(self, node):
        # print("visit_IntNum")
        return Variable("int")

    def visit_FloatNum(self, node):
        # print("visit_FloatNum")
        return Variable("float")

    def visit_UnaryExpr(self, node):
        # print("visit_UnaryExpr")
        pass

    def visit_Comparison(self, node):
        # print("visit_Comparison")
        pass

    def visit_Error(self, node):
        # print("visit_Error")
        pass

    def print_error(self, node, error):
        self.error_occured = True
        print("Error in line {}: {}".format(node.lineno, error))

