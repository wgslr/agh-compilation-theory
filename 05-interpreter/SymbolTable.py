#!/usr/bin/env python2


class Variable(object):
    def __init__(self, type, size=[], name=""):
        self.type = type
        self.size = size
        self.name = name

    def __str__(self):
        return '(Variable {}: {}, {})'.format(self.name, self.type, self.size)

    def __repr__(self):
        return str(self)


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        pass

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        pass

    def get(self, name): # get variable symbol or fundef from <name> entry
        pass

    def getParentScope(self):
        pass

    def pushScope(self, name):
        pass

    def popScope(self):
        pass
