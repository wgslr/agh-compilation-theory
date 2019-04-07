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
