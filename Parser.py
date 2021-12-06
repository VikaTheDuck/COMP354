import Expression as E

''' Temp Expression for Parser creation (use if you want) '''
class Expression():
    def __init__(self, expression_arr):
        '''
            Expression constructor
        '''
        if len(expression_arr) >= 3: # regular branch
            self.gen_branch(expression_arr)
        else: # leaf (ie. only number)
            self.gen_leaf(expression_arr)
    
    def gen_branch(self, expression_arr):
        '''
            Generates full branches
        '''
        self.left = expression_arr[0]
        self.opp = expression_arr[1]
        self.right = Expression(expression_arr[2:])
    
    def gen_leaf(self, expression_arr):
        '''
            Generates leaf branches (ie. no opperation or right side)
        '''
        self.left = expression_arr[0]
        self.right = self.opp = None      
        
    def evaluate(self):
        '''
            using python's built in eval() method the expression tree is first recombined and the evaluated result is returned
        '''
        return eval(self.recombine())
    
    def recombine(self):
        '''
            recombine before using eval() ensures all operations are done in the correct order according to pemdas
        '''
        if self.opp is None and self.right is None:
            return str(self.left)
        return str(self.left) + self.opp + str(self.right.recombine())
    
    def __str__(self):
        '''
            allows for easily printing an expression to view its contents
            
            @use:
                e = 
                print()
        '''
        return f'( {self.left} {self.opp} {self.right} )'
        
''' Parser class implementation '''
class Parser:
    def __init__(self):
        # Fundemental key : value pairs to form the base syntax
        self.keywords = {
            'plus' : '+',
            'minus' : '-',
            
            
            'if' : 'if',
            'then' : 'then',
            'else' : 'else',
            'is' : 'is',
            'greater' : 'greater',
            'than' : 'than',
            'or' : 'or',
            'equal' : 'equal',
            'to' : 'to',
            
            # loop functions
            'for' : 'for',
            'times' : 'times',
        }
        
        # User generated key : value pair to allow for variable assignment/storage
        self.user_keywords = {}
        
    def parse(self, user_input):
        '''
            main functional method for parser. allows for the splitting of a user input string through the gui into composite expressions
            
            @param:
                user_input -> string
                    the full string equation input from the gui to be converted into expressions and calculated
        '''
        cleaned_input_arr = [self.clean(param) for param in user_input.split(' ')]
        for input_word in cleaned_input_arr:
            if type(input_word) is Exception:
                return input_word
        
        self.output = Expression(cleaned_input_arr)
        return self.output.evaluate()
    
    def generate_if(self, if_arr):
        # if_arr = [x,..opp..,y,then,..true..,else,..false..]
        condition = []
        for index, word in enumerate(if_arr[2:]):
            if type(word) is float and index != 0:
                if_arr = if_arr[1:2] + if_arr[index+2:] # + 2 to offset the loop starting
                break
            condition.append(word)
        condition = ' '.join(condition)
        
        if condition == 'is greater than':
            condition = '>'
        elif condition == 'is greater than or equal to':
            condition = '>='
        elif condition == 'is less than':
            condition = '<'
        elif condition == 'is less than or equal to':
            condition = '<='
        
        print("hello")
        print(condition)
        print(if_arr)
        # for word in if_arr[3:]:
            
        then_condition = if_arr[if_arr.index('then')+1:if_arr.index('else')]
        then_condition = ''.join([str(x) for x in then_condition])
        
        else_condition = if_arr[if_arr.index('else')+1:]
        else_condition = ''.join([str(x) for x in else_condition])
        return E.IfStatement(if_arr[0], if_arr[1], condition, then_condition, else_condition)
    
    def parse_new(self, user_input):
        n = 1
        if_expression = None
        
        # 0: start operation, -1: end operation, 1: middle operation left, 2: middle operation right
        if_opperation = {
            0: None,
            -1: None,
            1: None,
            2: None,
        }
        cleaned_input_arr = [self.clean(param) for param in user_input.split(' ')]
        for input_word in cleaned_input_arr:
            if type(input_word) is Exception:
                return input_word
        if 'if' in cleaned_input_arr:  
            # TODO: missing syntax error checking
            
            
            if_arr = cleaned_input_arr[cleaned_input_arr.index('if'):cleaned_input_arr.index('else') + 2]
            cleaned_input_arr = cleaned_input_arr[0:cleaned_input_arr.index('if')] + cleaned_input_arr[cleaned_input_arr.index('else') + 2:]
            print(u"="*20)
            print(f'base = {cleaned_input_arr}')
            if type(cleaned_input_arr[0]) is not float:
                if_opperation.update({0 : cleaned_input_arr[0]})
                cleaned_input_arr = cleaned_input_arr[1:]
                print(f'0: {cleaned_input_arr}')
            if type(cleaned_input_arr[-1]) is not float:
                if_opperation.update({-1: cleaned_input_arr[-1]})
                cleaned_input_arr = cleaned_input_arr[:-1]
                print(f'-1: {cleaned_input_arr}')
            
            print(u"="*20)
                
            for i in range(len(cleaned_input_arr)-1):
                if type(cleaned_input_arr[i]) == type(cleaned_input_arr[i+1]):
                    print("MIDDLE DUPLICATE")
                    if_opperation.update({1: cleaned_input_arr[i], 2: cleaned_input_arr[i+1]})
                    cleaned_input_arr = cleaned_input_arr[:i] + cleaned_input_arr[i+1:]
                    break
                
            print(if_opperation)   
            print(f"if arr = {if_arr}")
            print(f"after if cleaned_input_arr = {cleaned_input_arr}")
            if_expression = self.generate_if(if_arr)
        if 'for' in cleaned_input_arr:
            if 'times' not in cleaned_input_arr:
                return Exception("Invalid syntax: times is a required keyword")
            for_arr = cleaned_input_arr[cleaned_input_arr.index('for'):cleaned_input_arr.index('times')+1]
            base_input = cleaned_input_arr = cleaned_input_arr[0:cleaned_input_arr.index('for')] + cleaned_input_arr[cleaned_input_arr.index('times') + 2:]
            print(f"for_arr = {for_arr}")
            n = for_arr[1]
            if type(n) is not float:
                return Exception("Invalid syntax: for requires a float parameter")
            for_composite = E.CompositeAddition()


        for _ in range(int(n)):
            x,opp,y = cleaned_input_arr[-3:]
            cleaned_input_arr = cleaned_input_arr[:-3]
            print(f'''
                x = {x}
                opp = {opp}
                y = {y}
                ''')
            if opp == '+':
                expression = E.Add(x,y)
            elif opp == '-':
                expression = E.Subtract(x,y)
            for i in range(len(cleaned_input_arr)-1, -1, -2):
                print(cleaned_input_arr[i-1:i+1])
                x,opp = cleaned_input_arr[i-1:i+1] 
                if opp == '+':
                    expression = E.Add(x,expression)
                elif opp == '-':
                    expression = E.Subtract(x,expression)
            print(expression)   
            if n > 1:
                for_composite.addOperation(expression)
                cleaned_input_arr = base_input
                
        if if_expression:
            '''
                if_operation = {
                    0: start operation,
                    -1: end operation,
                    1: middle left operation,
                    2: middle right operation
                }
            '''
            if if_opperation.get(0) and not if_opperation.get(1) and not if_opperation.get(2):
                if if_opperation.get(0) == '+':
                    '''if() + float'''
                    return E.Add(if_expression, expression)
                else:   
                    '''if() - float'''
                    return E.Subtract(if_expression, expression)
            elif if_opperation.get(-1) and not if_opperation.get(1) and not if_opperation.get(2):
                if if_opperation.get(-1) == '+':
                    '''float + if()'''
                    return E.Add(expression, if_expression)
                else:
                    '''float - if()'''
                    return E.Subtract(expression, if_expression)
            else:
                print(u'8=8'*20)
                print(u'8=8'*20)
                print(u'8=8'*20)
            
            # if if_opperation == '+':
            #     outputComposite = E.CompositeAddition()
            # else:
            #     outputComposite = E.CompositeSubtraction()
            # outputComposite.addOperation(expression)
            # outputComposite.addOperation(if_expression)
            # return outputComposite
        return expression if n == 1 else for_composite
            
    def add_keyword(self, new_user_keyword, value):
        ''' 
            sets/updates the current user keyword dictionary with a user defined key : value pair 
            
            @param:
                new_user_keyword -> string
                    the name of the variable to be stored (ie. x in the assignment equation x = 5.0)
                value -> float
                    the new value to link with the input variable keyword name (ie. 5.0 in the assignment equation x = 5.0)
        '''
        self.user_keywords.update({ new_user_keyword : value })
    
    def clean(self, param):
        '''
            cleaning helper function to test if a string input can be converted to a float (ie. is a number)
                if the input is of type string
                    a syntax test occurs that returns an exception with the raised exception message
                    the confirmed string keyword is used to obtain its value from the stored keyword/user_keyword dictionaries and returned
                else
                    the param is converted to a float and returned
            
            @param:
                param -> string
                    the desired string word to clean and check if it is a valid command
            @use:
                in list comprehension whilst splitting the original string input into words using a space delimitier
                ie.
                    cleaned_output = [clean(word) for word in user_input.split(" ")]
        '''
        try:
            return float(param)
        except ValueError:
            if type(param) == str and not (self.keywords.get(param) or self.user_keywords.get(param)):
                return Exception(f"{param} is not a valid keyword")
            return self.keywords.get(param) or self.user_keywords.get(param)
    
    
def parser_test():
    tests = [
        { 'input' : '2 plus 5 plus 2 minus 2', 'expected' : 7.0}
    ]
    
    for test in tests:
        print(f"Test: {test.get('input')} = {test.get('expected')}")
        assert Parser().parse(test.get('input')) == test.get('expected')
        
    print("Tests passed")

def new_parser_tests():
    tests = [
        # float (+-) if('>') 
        # 10 + 2 + (if 5 > 2 {5 + 2} else {0}) = 19
        {'input' : '10 plus 2 plus if 5 is greater than 2 then 5 plus 2 else 0', 'expected' : 19.0},
        # 10 + 2 - (if 5 > 2 {5 + 2} else {0}) = 5
        {'input' : '10 plus 2 minus if 5 is greater than 2 then 5 plus 2 else 0', 'expected' : 5.0},
        
        # if('>') (+-) float 
        # (if 5 > 2 {5 + 2} else {0}) + (5 + 2)
        {'input' : 'if 5 is greater than 2 then 5 plus 2 else 0 plus 5 plus 2', 'expected' : 14.0},
        # (if 5 > 2 {5 + 2} else {0}) - (5 + 2)
        {'input' : 'if 5 is greater than 2 then 5 plus 2 else 0 minus 5 plus 2', 'expected' : 0},
    ]
    
    for test in tests:
        print(f"Test: {test.get('input')} = {test.get('expected')}")
        assert Parser().parse_new(test.get('input')).execute() == test.get('expected')
    print('Tests passed.')
if __name__ == '__main__':
    # parser_test()
    # print(u'='*10)
    # parser = Parser()
    # output = parser.parse("2 plus 5 plus 2 minus 2")
    # print(output)
    
    parser = Parser()
    
    new_parser_tests()
    
    # Working
    
    # float (+-) if()
    # output = parser.parse_new("10 plus 2 plus if 5 is greater than 2 then 2 plus 5 else 0")
    # output = parser.parse_new("10 plus 2 minus if 5 is greater than 2 then 2 plus 5 else 0")
    
    # if() (+-) float
    # output = parser.parse_new("if 5 is greater than 2 then 2 plus 5 else 0 plus 5 plus 2")
    # output = parser.parse_new("if 5 is greater than 2 then 2 plus 5 else 0 minus 5 plus 2")
    
    # float (+-) if() (+-) float
    output = parser.parse_new("5 plus 2 if 5 is greater than 2 then 2 plus 5 else 0 plus 5 plus 2")
    
    
    # output = parser.parse_new("5 plus 2")
    # [5.0, '+', 2.0, '-', 1.0, '+', 7.0]
    # output = parser.parse_new("5 plus 2 minus 1")
    # output = parser.parse_new("5 plus 2 minus 1 plus 7")
    
    # 5 plus 2 for 5 times
    
    # output = parser.parse_new("5 plus 2 for 5 times")

    # output = parser.parse_new("5 plus 2 minus 10 for 5 times")
    print(output)
    if type(output) is not Exception:
        print(output.execute())
    
    