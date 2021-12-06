import abc

class Expression(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute():
        pass
    def __str__(self) -> str:
        return f'( {self.x} {self.__class__.__name__} {self.y} )'

class CompositeAddition(Expression):
    def __init__(self):
        self._children = []

    def execute(self):
        result = 0
        for child in self._children:
            result += child.execute()
        return result

    def addOperation(self, component):
        self._children.append(component)

    def removeOperation(self, component):
        self._children.remove(component) 
        
    def __str__(self) -> str:
        print("in comp str")
        output = ''
        for child in self._children:
            output += child.__str__() + " ADD "
        return output

class CompositeSubtraction(Expression):
    def __init__(self):
        self._children = []

    def execute(self):
        result = 0
        for child in self._children:
            result -= child.execute()
        return result

    def addOperation(self, component):
        self._children.append(component)

    def removeOperation(self, component):
        self._children.remove(component) 
        
    def __str__(self) -> str:
        print("in comp str")
        output = ''
        for child in self._children:
            output += child.__str__() + " MINUS "
        return output

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
    def __init__(self, x, y, operator, thenOperation, elseOperation=0) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.operator = operator
        self.thenOperation = thenOperation
        self.elseOperation = elseOperation
    
    def execute(self):
        if isinstance(self.x,Expression):
            self.x = self.x.execute()
        if isinstance(self.y,Expression):
            self.y = self.y.execute()
        if eval(f'{self.x} {self.operator} {self.y}'):
            return eval(self.thenOperation)
        else:
            return eval(self.elseOperation)
    
    def __str__(self) -> str:
        return f'( if {self.x} {self.operator} {self.y} then {self.thenOperation} else {self.elseOperation} )'

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
    x = Add(3, Add(1, Subtract(5, IfStatement(5,4, '>', '5+4'))))
    y = IfStatement(5,4, '>', '2+3')
    # y = IfStatement(5,4, '>', Add(1,4), Add(2,5))
    
    
    expr.addOperation(x)
    print(y.execute())
if __name__ == "__main__":
    main()