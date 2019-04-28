#!/usr/bin/python

from collections import defaultdict

allowed_operations = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "")))
allowed_operations["+="]["int"]["int"] = "int"


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

    def visit_Vector(self, node):
        # print("Visit Vector")
        for e in node.elements:
            self.visit(e)
        return "vector", ""

    def visit_Reference(self, node):
        # print("Visit Reference")
        return "ref", node.name

    def visit_FunctionCall(self, node):
        # print("Visit FunctionCall")
        pass

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
        v = self.variables[node.name]
        if v:
            return v.type, node.name
        else:
            return None, node.name

    def visit_If(self, node):
        # print("Visit if")
        pass

    def visit_BinExpr(self, node):
        # print("Visit BinExpr")

        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op

    def visit_ArithmeticOperation(self, node):
        # print("Visit ArithmeticOperation")
        self.visit_BinExpr(node)

    def visit_Assignment(self, node):
        # print("visit_Assignment")
        type1, name1 = self.visit(node.left)
        type2, name2 = self.visit(node.right)
        op = node.op
        if op == "=":
            self.variables[name1] = self.Variable(type2, "")
        else:
            newtype = allowed_operations[op][type1][type2]
            if newtype:
                self.variables[name1] = self.Variable(newtype, "")
            else:
                TypeChecker.print_error(node, "cannot assign {} to {}".format(type2, type1))

    def visit_IntNum(self, node):
        # print("visit_IntNum")
        return "int", ""

    def visit_FloatNum(self, node):
        # print("visit_FloatNum")
        return "float", ""

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
        def __init__(self, type, value):
            self.type = type
            self.value = value

