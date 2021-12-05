import abc

class Expression(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute():
        pass

class CompositeAddition(Expression):
    def __init__(self):
        self._children = set()

    def execute(self):
        result = 0
        for child in self._children:
            result += child.execute()
        return result

    def addOperation(self, component):
        self._children.add(component)

    def removeOperation(self, component):
        self._children.discard(component) 

class CompositeSubtraction(Expression):
    def __init__(self):
        self._children = set()

    def execute(self):
        result = 0
        for child in self._children:
            result -= child.execute()
        return result

    def addOperation(self, component):
        self._children.add(component)

    def removeOperation(self, component):
        self._children.discard(component) 

class Add(Expression):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def execute(self):
        if isinstance(self.x,Expression):
            self.x = self.x.execute()
        if isinstance(self.y,Expression):
            self.y = self.y.execute()
        return self.x + self.y

class Subtract(Expression):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def execute(self):
        if isinstance(self.x,Expression):
            self.x = self.x.execute()
        if isinstance(self.y,Expression):
            self.y = self.y.execute()
        return self.x - self.y

class IfStatement(Expression):
    def __init__(self, x, y, operator, thenOperation) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.operator = operator
        self.thenOperation = thenOperation
    
    def execute(self):
        if eval(f'{self.x} {self.operator} + {self.y}'):
            return eval(self.thenOperation)
        return

def main():
    expr = CompositeAddition()
    # x = Add(3,1)
    # y = Add(1,4)
    # z = Subtract(5,3)
    # i = IfStatement(5, 4, '>', '2+2')
    # expr.addOperation(x)
    # expr.addOperation(y)
    # expr.addOperation(z)
    # expr.addOperation(i)
    x = Add(3, Add(1, Subtract(5,2)))
    expr.addOperation(x)
    print(x.execute())

if __name__ == "__main__":
    main()