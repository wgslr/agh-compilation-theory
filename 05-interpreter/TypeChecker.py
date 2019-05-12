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

allowed_operations[".+"]["matrix"]["matrix"] = "matrix"
allowed_operations[".+"]["vector"]["vector"] = "vector"

allowed_operations[".-"]["matrix"]["matrix"] = "matrix"
allowed_operations[".-"]["vector"]["vector"] = "vector"

allowed_operations[".*"]["matrix"]["matrix"] = "matrix"
allowed_operations[".*"]["vector"]["vector"] = "vector"

allowed_operations["./"]["matrix"]["matrix"] = "matrix"
allowed_operations["./"]["vector"]["vector"] = "vector"

# unary operations - encoded by repeating same type
allowed_operations["NEGATE"]["int"]["int"] = "int"
allowed_operations["NEGATE"]["float"]["float"] = "float"
allowed_operations["TRANSPOSE"]["matrix"]["matrix"] = "matrix"

op_to_string = {
    '=': 'ASSIGN',
    '+': 'ADD',
    '-': 'SUB',
    '*': 'MUL',
    '/': 'DIV',
    '.+': 'DOT-ADD',
    '.-': 'DOT-SUB',
    '.*': 'DOT-MUL',
    './': 'DOT-DIV',
    '+=': 'ADD-ASSIGN',
    '-=': 'SUB-ASSIGN',
    '*=': 'MUL-ASSIGN',
    '/=': 'DIV-ASSIGN',
}


class NodeVisitor(object):
    loop = 0
    symbols = SymbolTable()

    def visit(self, node, *args, **kwargs):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node, *args, **kwargs)


class TypeChecker(NodeVisitor):
    encountered_error = False

    def ensure_defined(self, node, variable):
        if variable.type == "undefined":
            self.print_error(node, "undefined variable")
            return False
        return True

    def visit_Block(self, node):
        # print("visit_Instructions")
        self.symbols = self.symbols.createChild()
        self.visit(node.content)
        self.symbols = self.symbols.getParentScope()

    def visit_Instructions(self, node):
        # print("visit_Instructions")
        map(self.visit, node.nodes)

    def visit_FlowKeyword(self, node):
        # print("visit_Flowkeyword")
        if self.loop == 0:
            self.print_error(node, "flow keyword {} must be used inside a loop".format(node.keyword))

    def visit_Print(self, node):
        # print("visit_Print")
        map(self.visit, node.arguments)

    def visit_Return(self, node):
        # print("visit_Return")
        if node.value is not None:
            self.visit(node.value)

    def visit_String(self, node):
        return Variable("string")

    def visit_Matrix(self, node):
        map(self.visit, node.elements)
        size1 = len(node.elements)
        sizes = map(lambda x: len(x.elements), node.elements)
        size2 = min(sizes)
        if all(x == size2 for x in sizes):
            return Variable("matrix", [size1, size2])
        else:
            self.print_error(node, "vectors with different sizes in matrix initialization")
            return None

    def visit_Vector(self, node):
        map(self.visit, node.elements)
        return Variable("vector", [len(node.elements)])

    def visit_Reference(self, node, *args, **kwargs):
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
        # print("visit_FunctionCall")
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

    def visit_Variable(self, node, allow_undefined = False):
        # print("visit_Variable")
        result = self.symbols.get(node.name)
        if result is None:
            if not allow_undefined:
                self.print_error(node, "undefined variable {}".format(node.name))
            result = Variable("undefined", [], node.name)
        return result

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
            # self.print_error(node, "undefined variable {}".format(node.right.name))
            return None
        op = node.op
        newtype = allowed_operations[op][var1.type][var2.type]
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

        op = node.op
        allow_undefined = op == "="

        var1 = self.visit(node.left, allow_undefined)
        var2 = self.visit(node.right)
        if not var2:
            print(node.lineno, node.right)
            # print(node.right.op)
            # self.print_error(node, "undefined variable {}".format(node.right.name))
            return None

        if var2.type == "undefined":
            self.print_error(node, "undefined variable {}".format(node.right.name))


        if isinstance(node.left, AST.Variable):
            name = node.left.name
        else:
            name = node.left.container.name

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
                op_str = op_to_string[op]
                self.print_error(node, "cannot {} {} to {}".format(op_str, var2.type, var1.type))

    def visit_IntNum(self, node):
        # print("visit_IntNum")
        return Variable("int")

    def visit_FloatNum(self, node):
        # print("visit_FloatNum")
        return Variable("float")

    def visit_UnaryExpr(self, node):
        # print("visit_UnaryExpr")
        operand = self.visit(node.operand)
        if operand.type == "undefined":
            self.print_error(node, "undefined variable {}".format(operand.name))
        newtype = allowed_operations[node.operation][operand.type][operand.type]
        if newtype:
            return Variable(newtype, operand.size[::-1])
        else:
            self.print_error(node, "cannot perform {} on {}".format(
                node.operation, operand.type))

    def visit_Comparison(self, node):
        # print("visit_Comparison")
        pass

    def visit_Error(self, node):
        # print("visit_Error")
        pass

    def print_error(self, node, error):
        self.encountered_error = True
        print("Error in line {}: {}".format(node.lineno, error))

