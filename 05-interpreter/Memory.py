
import AST
import Interpreter

class Memory:

    def __init__(self):  # memory name
        self.variables = dict()

    def __str__(self):
        return repr(self.variables)

    def __repr__(self):
        return str(self)

    def has_key(self, node):  # variable name
        if isinstance(node, AST.Variable):
            return self.variables.get(node.name)
        elif isinstance(node, Interpreter.ConcreteReference):
            print(node.container)
            return self.variables.get(node.container.name)
        else:
            raise TypeError("{} is not a memory reference".format(node.__class__))

    def get(self, node):         # gets from memory current value of variable <name>

        if isinstance(node, AST.Variable):
            print("getting variable")
            return self.variables.get(node.name)
        elif isinstance(node, Interpreter.ConcreteReference):
            print("getting reference")
            value = self.get(node.container)
            for coord in node.coords:
                print("value = {}[{}]".format(value, coord))
                value = value[coord]
                if value is None:
                    break
            return value
        else:
            raise TypeError("{} is not a memory reference".format(node.__class__))

    def put(self, node, value):  # puts into memory current value of variable <name>
        if isinstance(node, AST.Variable):
            print("setting variable")
            self.variables[node.name] = value
        elif isinstance(node, Interpreter.ConcreteReference):
            print("setting reference")
            container = self.variables[node.container.name]
            for coord in node.coords[:-1]:
                container = container[coord]
            container[node.coords[-1]] = value
        else:
            raise TypeError("{} is not a memory reference".format(node.__class__))
        print("{} becomes {}".format(node.name, value))


class MemoryStack:

    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.stack = [Memory()]

    def __str__(self):
        s = "MEMORY [\n"
        for m in self.stack:
            s += str(m) + "\n"
        return s + "]"

    def __repr__(self):
        return str(self)

    def get(self, node):             # gets from memory stack current value of variable <name>
        for m in self.stack[::-1]:
            if m.has_key(node):
                return m.get(node)
        return None

    def insert(self, node, value):  # inserts into memory stack variable <name> with value <value>
        """
        Sets variable identified by <node> to value <value> in the current scope
        """
        self.stack[-1].put(node, value)

    def set(self, node, value):
        """
        Sets variable identified by <node> to value <value> in the scope where
        it was declared. Creates new local variable if undefined.
        """
        for m in stack[::-1]:
            if m.has_key(node):
                m.put(node, value)
                break
        else:
            self.insert(node, value)

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()


# class Reference(object):
#     def get(self):
#         raise NotImplementedError()
#     def set(self, value):
#         raise NotImplementedError()



# class IndexReference(object):
#     def __init__(self, vector, index):
#         self.vector = vector
#         self.index = index
    
#     def get(self):
#         return self.vector[self.index]
    
#     def set(self, value):
#         self.vector[self.index] = value

#     def __str__(self):
#         return str(self.get())