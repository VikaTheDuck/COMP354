import abc

class _Exception():
    def __init__(self, message = 'Base Exception'):
        self.message = message
    def execute(self):
        return self.__str__()
    def __str__(self):
        return f'Exception : {self.message}'

class Expression(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute():
        pass
    def __str__(self) -> str:
        print(self.__class__.__name__)
        return f'( {self.x} {"+" if self.__class__.__name__ in ["Add", "CompositeAddition"] else "-"} {self.y} )'

class Assignment(Expression):
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
    
    def execute(self):
        if type(self.value) is float:
            return self.__str__()
        else:
            return f'Assigned {self.key} to {self.value.execute()}'

    def __str__(self) -> str:
        return f'Assigned {self.key} to {self.value}'

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
        output = ''
        length = len(self._children)
       
        for i, child in enumerate(self._children):
            if i == length-1:
                output += child.__str__() 
                break
            else:
                output += child.__str__() + " + "
        return output

class CompositeSubtraction(Expression):
    def __init__(self):
        self._children = []

    def execute(self):
        result = self._children[0].execute()
        for child in self._children[1:]:
            result -= child.execute()
        return result

    def addOperation(self, component):
        self._children.append(component)

    def removeOperation(self, component):
        self._children.remove(component) 
        
    def __str__(self) -> str:
        output = ''
        length = len(self._children)
       
        for i, child in enumerate(self._children):
            if i == length-1:
                output += child.__str__() 
                break
            else:
                output += child.__str__() + " - "
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

def expression_test():
    comp1 = CompositeAddition()
    comp1.addOperation(Add(3,4))

    comp2 = CompositeAddition()
    comp2.addOperation(Add(3,4))
    comp2.addOperation(Add(3,2))

    comp3 = CompositeAddition()
    comp3.addOperation(Add(3,4))
    comp3.addOperation(Subtract(3,2))

    comp4 = CompositeSubtraction()
    comp4.addOperation(Subtract(3,4))

    comp5 = CompositeSubtraction()
    comp5.addOperation(Add(3,4))
    comp5.addOperation(Add(3,2))

    comp6 = CompositeSubtraction()
    comp6.addOperation(Add(3,4))
    comp6.addOperation(Subtract(3,2))


    tests = [
        {'input': Add(3,4), 'expected': 7},
        {'input': Add(3, Add(4, 5)), 'expected': 12},
        {'input': Add(3, Subtract(5,9)), 'expected': -1},
        {'input': Subtract(5,2), 'expected': 3},
        {'input': Subtract(5, Add(6,7)), 'expected': -8},
        {'input': Subtract(5, Subtract(10, 2)), 'expected': -3},
        {'input': comp1, 'expected': 7},
        {'input': comp2, 'expected': 12},
        {'input': comp3, 'expected': 8},
        {'input': comp4, 'expected': -1},
        {'input': comp5, 'expected': 2},
        {'input': comp6, 'expected': 6},
        {'input': IfStatement(5,6, '>', '5+5', '4-1'), 'expected': 3},
        {'input': IfStatement(6,5, '>', '5+5', '4-1'), 'expected': 10},
        {'input': IfStatement(6,5, '<', '5+5', '4-1'), 'expected': 3},
        {'input': IfStatement(5,6, '>=', '5+5', '4-1'), 'expected': 3},
        {'input': IfStatement(6,5, '>=', '5+5', '4-1'), 'expected': 10},
        {'input': IfStatement(6,5, '<=', '5+5', '4-1'), 'expected': 3},
        {'input': IfStatement(5,5, '<=', '5+5', '4-1'), 'expected': 10},
        {'input': IfStatement(5,5, '>=', '5+5', '4-1'), 'expected': 10},
    ]
    
    for index, test in enumerate(tests):
        result = test.get('input').execute()
        try:
            assert result == test.get('expected')
            print(f'PASSED Test#{index+1} : {test.get("input")} = {test.get("expected")}')
        except AssertionError:
            print(f"""
                  =====================
                        TEST FAIL
                  Test: {test.get('input')} = {test.get('expected')}
                  Expected = {test.get('expected')}, Result = {result}
                  
                  Full:
                    type(result) = {type(result)}
                    {result}
                  =====================
                  """)
            raise AssertionError
    print('Tests passed.')
    print(u'='*20)

if __name__ == '__main__':
    expression_test()

