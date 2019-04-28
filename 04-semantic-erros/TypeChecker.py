#!/usr/bin/python


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)


class TypeChecker(NodeVisitor):
    pass

    def visit_BinExpr(self, node):
        print("Visit BinExpr")

        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op

    def visit_Instructions(self, node):
        print("Visit Instructions")
        for n in node.nodes:
            self.visit(n)


    def visit_FlowKeyword(self, node):
        print("Visit Flowkeyword")


    def visit_Print(self, node):
        print("Visit Print")


    def visit_Return(self, node):
        print("Visit Return")


    def visit_String(self, node):
        print("Visit String")


    def visit_Vector(self, node):
        print("Visit Vector")


    def visit_Reference(self, node):
        print("Visit Reference")


    def visit_FunctionCall(self, node):
        print("Visit FunctionCall")


    def visit_While(self, node):
        print("Visit While")


    def visit_For(self, node):
        print("Visit For")


    def visit_Range(self, node):
        print("Visit Range")


    def visit_Variable(self, node):
        print("Visit Variable")


    def visit_If(self, node):
        print("Visit if")


    def visit_ArithmeticOperation(self, node):
        print("Visit ArithmeticOperation")


    def visit_Assignment(self, node):
        print("visit_Assignment")


    def visit_IntNum(self, node):
        print("visit_IntNum")


    def visit_FloatNum(self, node):
        print("visit_FloatNum")


    def visit_UnaryExpr(self, node):
        print("visit_UnaryExpr")


    def visit_Comparison(self, node):
        print("visit_Comparison")


    def visit_Error(self, node):
        print("visit_Error")


