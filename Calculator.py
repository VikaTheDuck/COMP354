
import Parser as P

class Calculator():
    
    def __init__(self, parser):
        
        self.parser = P()
    
    def getInput(self, str):
        
        try:
            return float(P().parse_new(str))
        
        except Exception as e:
            return e
        
