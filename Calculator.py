
import Parser as P
from Expression import _Exception
class Calculator():
    
    def __init__(self):
        
        self.parser = P.Parser()
    
    def getInput(self, str):
        
        try:
            expr = self.parser.parse_new(str)
            return expr.execute()
        
        except Exception as e:
            return _Exception("Syntax Error: invalid structure")
        
