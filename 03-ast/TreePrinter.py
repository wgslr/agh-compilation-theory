from __future__ import print_function
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " +
                        self.__class__.__name__)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for n in self.nodes:
            n.printTree(indent)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + 'FOR')
        self.iterator.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + 'WHILE')
        self.condition.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + 'IF')
        self.condition.printTree(indent + 1)
        print(TreePrinter.makeIndent(indent) + 'THEN')
        self.body.printTree(indent + 1)
        if self.else_body is not None:
            print(TreePrinter.makeIndent(indent) + 'ELSE')
            self.else_body.printTree(indent + 1)


    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + 'PRINT')
        for arg in self.arguments:
            arg.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + 'RETURN')
        if self.value is not None:
            self.value.printTree(indent + 1)


    @addToClass(AST.String)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + self.value)


    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + 'RANGE')
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + "VECTOR")
        for e in self.elements:
            e.printTree(indent + 1)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + self.name)

    @addToClass(AST.Reference)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + "REF")
        self.name.printTree(indent + 1)
        for c in self.coords:
            c.printTree(indent + 1)

    @addToClass(AST.FunctionCall)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + self.name)
        self.argument.printTree(indent + 1)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + str(self.value))

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
        # TODO fill in the body

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + self.operation)
        self.operand.printTree(indent + 1)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print(TreePrinter.makeIndent(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.ArithmeticOperation)
    def printTree(self, indent=0):
        AST.BinExpr.printTree(self, indent)

    @classmethod
    def makeIndent(_self, indent):
        return ''.join("|  " * indent)
