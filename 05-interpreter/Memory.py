

class Memory:

    def __init__(self):  # memory name
        self.variables = dict()

    def __str__(self):
        return repr(self.variables)

    def __repr__(self):
        return str(self)

    def has_key(self, name):  # variable name
        return name in self.variables

    def get(self, name):         # gets from memory current value of variable <name>
        return self.variables.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.variables[name] = value


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

    def get(self, name):             # gets from memory stack current value of variable <name>
        for m in self.stack[::-1]:
            if m.has_key(name):
                return m.get(name)
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        # TODO what's the difference from insert?
        self.stack[-1].put(name, value)

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()
