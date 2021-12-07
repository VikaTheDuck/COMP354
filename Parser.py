import Expression as E
from Expression import _Exception, Assignment, Expression
        
''' Parser class implementation '''
class Parser:
    def __init__(self):
        # Fundemental key : value pairs to form the base syntax
        self.keywords = {
            'plus' : '+',
            'minus' : '-',
            
            # Conditional functions
            'if' : 'if',
            'then' : 'then',
            'else' : 'else',
            'is' : 'is',
            'greater' : 'greater',
            'less' : 'less',
            'than' : 'than',
            'or' : 'or',
            'equal' : 'equal',
            'to' : 'to',
            
            # Loop functions
            'for' : 'for',
            'times' : 'times',
            
            # Assignment functions
            'let' : 'let'
        }
        
        # User generated key : value pair to allow for variable assignment/storage
        self.user_keywords = {}
    
    def generate_if(self, if_arr):
        '''
            Helper function to generate if statement expressions
            
            @param:
                if_arr -> list
                    the if_arr param is a section of the full user input array focusing solely on the if statement
                    ie. the user input: 
                        ->'if 5 is greater than 2 then 5 plus 2 else 0' and 
                        ->'10 plus 2 plus if 5 is greater than 2 then 5 plus 2 else 0' 
                        form the same if_arr
                    
                        if_arr = ['if', 5.0, 'is', 'greater', 'than', 2.0, 'then', 5.0, '+', 2.0, 'else', 0.0]
            
            @return -> IfStatement(args)
                the returned IfStatement object is the object representation of the input string list with the condition, 
                then statement and else statement fully integrated
        '''
        # if_arr = [x,..opp..,y,then,..true..,else,..false..]
        
        # Converting a string condition to a ascii character
        condition = []
        for index, word in enumerate(if_arr[2:]):
            if type(word) is float and index != 0:
                if_arr = if_arr[1:2] + if_arr[index+2:] # + 2 to offset the loop starting index
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
        else:
            return _Exception("Invalid syntax: a valid comparison operation is required in an if statement conditional")
        
        # Reparsing the then and else conditions for execution within the returned IfStatement()
        then_condition = if_arr[if_arr.index('then')+1:if_arr.index('else')]
        then_condition = ''.join([str(x) for x in then_condition])
        
        else_condition = if_arr[if_arr.index('else')+1:]
        else_condition = ''.join([str(x) for x in else_condition])
        
        return E.IfStatement(if_arr[0], if_arr[1], condition, then_condition, else_condition)
    
    def check_assignment(self, user_input_arr):
        if 'let' not in user_input_arr:
            return False
        if 'equal' not in user_input_arr:
            return _Exception("Syntax error: 'equal' is a required keyword for assignment.")
        if 'to' not in user_input_arr:
            return _Exception("Syntax error: 'to' is a required keyword for assignment.")        
        
        # Checking for reserved keyword reassignment
        if user_input_arr[1] in self.keywords:
            return _Exception(f"Invalid variable name: {user_input_arr[1]} is a reserved keyword.")

        key, value = None, None
        # Error checking if the proposed variable name is not a string
        try:
            float(user_input_arr[1])
            return _Exception(f"Invalid variable name: {user_input_arr[1]} must be of type string.")
        except ValueError:
            key = user_input_arr[1]
        
        if len(user_input_arr[user_input_arr.index('to') + 1:]) < 2 : # single assingment ie. x = 5
            try:
                value = float(user_input_arr[4])
            except ValueError:
                return _Exception(f"Invalid value: {user_input_arr[4]} must be of type float or expression.")
            self.add_keyword(key, value)
            return Assignment(key, value)
        else: # expression assignment ie. x = 5 + 2
            value_expr = self.parse_new(' '.join(user_input_arr[user_input_arr.index('to') +1:]))
            self.add_keyword(key, value_expr.execute())
            return Assignment(key, value_expr)
    
    def parse_new(self, user_input):
        '''
            TODO: 
            
            Parser
            
            @param:
                user_input -> string

        '''
        n = 1
        if_expression = None
        for_composite = None
        
        '''
            0: start operation,
            -1: end operation,
            1: middle left operation,
            2: middle right operation
        '''
        if_opperation = {
            0: None,
            -1: None,
            1: None,
            2: None,
        }
        
        assignment = self.check_assignment(user_input.split(' '))
        if assignment or type(assignment) is _Exception:
            return assignment
        
        # Cleaning ie. checking for invalid syntax use and replacing variables to their respective values
        cleaned_input_arr = [self.clean(param) for param in user_input.split(' ')]
        
        # Checking for any thrown exceptions in the cleaning process
        for input_word in cleaned_input_arr:
            if type(input_word) is _Exception:
                return input_word
        
        # Looping pipeline
        if 'for' in cleaned_input_arr:
            if 'times' not in cleaned_input_arr:
                return _Exception("Invalid syntax: times is a required keyword in looping.")
            
            # Removal of the for portion of the user input
            for_arr = cleaned_input_arr[cleaned_input_arr.index('for'):cleaned_input_arr.index('times')+1]
            
            # Error checking to ensure the loop is placed last in the syntax
            if len(cleaned_input_arr[cleaned_input_arr.index('times')+1:]) > 0:
                return _Exception("Invalid syntax: expression present after looping end.")

            # Continue in loop expression splitting
            base_input = cleaned_input_arr = cleaned_input_arr[0:cleaned_input_arr.index('for')]
            n = for_arr[1]
            
            # Error checking to ensure a float n is provided in the syntax
            if type(n) is not float:
                return _Exception("Invalid syntax: for requires a float parameter. ie. 'for 5 times'.")
            
            # Creation of a composite addition parent to house the expression operations [n] times
            for_composite = E.CompositeAddition()
        else:
            # Error checking if for is not present in the input string but times is #
            if 'times' in cleaned_input_arr:
                return _Exception("Invalid syntax: times is a reserved keyword for looping.")

        # If statement conditional pipeline
        if 'if' in cleaned_input_arr:  
            # TODO: missing syntax error checking
            if 'then' not in cleaned_input_arr or 'else' not in cleaned_input_arr:
                return _Exception("Invalid syntax: both 'then' and 'else' are required keywords for use in an if conditional statement.")
            if_arr = cleaned_input_arr[cleaned_input_arr.index('if'):cleaned_input_arr.index('else') + 2]
            cleaned_input_arr = cleaned_input_arr[0:cleaned_input_arr.index('if')] + cleaned_input_arr[cleaned_input_arr.index('else') + 2:]

            if len(cleaned_input_arr) > 0:
                if type(cleaned_input_arr[0]) is not float:
                    if_opperation.update({0 : cleaned_input_arr[0]})
                    cleaned_input_arr = cleaned_input_arr[1:]
                if type(cleaned_input_arr[-1]) is not float:
                    if_opperation.update({-1: cleaned_input_arr[-1]})
                    cleaned_input_arr = cleaned_input_arr[:-1]
                    
                for i in range(len(cleaned_input_arr)-1):
                    if type(cleaned_input_arr[i]) == type(cleaned_input_arr[i+1]):
                        if_opperation.update({1: cleaned_input_arr[i], 2: cleaned_input_arr[i+1]})
                        cleaned_input_arr = cleaned_input_arr[:i] + cleaned_input_arr[i+1:]
                        break

            if_expression = self.generate_if(if_arr)
            if type(if_expression) is _Exception:
                return if_expression
        else:
            # Error checking if 'if' is not present in the input string but other if keywords are
            for param in ['then','else','is','greater','less','than','or','equal','to']:
                if param in cleaned_input_arr:
                    return _Exception(f'{param} is a reserved keyword to be used in if conditions')
        
        if len(cleaned_input_arr) > 0:
            for _ in range(int(n)):
                x,opp,y = cleaned_input_arr[-3:]
                cleaned_input_arr = cleaned_input_arr[:-3]
                
                if opp == '+':
                    expression = E.Add(x,y)
                elif opp == '-':
                    expression = E.Subtract(x,y)
                for i in range(len(cleaned_input_arr)-1, -1, -2):
                    if(len(cleaned_input_arr) == 1):
                        return _Exception(f"Invalid syntax: missing expression pair for '{cleaned_input_arr[0]}'")
                    x,opp = cleaned_input_arr[i-1:i+1] 
                    if opp == '+':
                        expression = E.Add(x,expression)
                    elif opp == '-':
                        expression = E.Subtract(x,expression)
                if n > 1:
                    for_composite.addOperation(expression)
                    cleaned_input_arr = base_input
        else:
            ''' No regular expression found check for if statement only expression '''
            
        
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
            elif not if_opperation.get(0) and not if_opperation.get(-1) and not if_opperation.get(1) and not if_opperation.get(2):
                if for_composite:
                    ''' if() for n times '''
                    for _ in range(int(n)):
                        for_composite.addOperation(if_expression)
                    return for_composite
                else:
                    ''' if() '''
                    return if_expression
            else:
                ''' float (+-) if() (+-) float '''
                # TODO: implement middle if statement logic?
                print(u'8=8'*20)
                print(u'8=8'*20)
                print(u'8=8'*20)
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
                return _Exception(f"{param} is not a valid keyword")
            return self.keywords.get(param) or self.user_keywords.get(param)
    
def new_parser_tests():
    parser = Parser()
    tests = [
        # if('>')
        {'input' : 'if 5 is greater than 2 then 5 plus 2 else 0', 'expected' : 7},
        {'input' : 'if 2 is greater than 5 then 5 plus 2 else 0', 'expected' : 0},
        {'input' : 'if 2 is greater than 5 then 5 plus 2 else 6', 'expected' : 6},
        
        
        # float (+-) if('>') 
        # TODO: fix logic to allow this test
        # {'input' : '10 plus if 5 is greater than 2 then 5 plus 2 else 0', 'expected' : 17},
        # 10 + 2 + (if 5 > 2 {5 + 2} else {0}) = 19
        {'input' : '10 plus 2 plus if 5 is greater than 2 then 5 plus 2 else 0', 'expected' : 19.0},
        # 10 + 2 - (if 5 > 2 {5 + 2} else {0}) = 5
        {'input' : '10 plus 2 minus if 5 is greater than 2 then 5 plus 2 else 0', 'expected' : 5.0},
        
        # if('>') (+-) float 
        # (if 5 > 2 {5 + 2} else {0}) + (5 + 2)
        {'input' : 'if 5 is greater than 2 then 5 plus 2 else 0 plus 5 plus 2', 'expected' : 14.0},
        # (if 5 > 2 {5 + 2} else {0}) - (5 + 2)
        {'input' : 'if 5 is greater than 2 then 5 plus 2 else 0 minus 5 plus 2', 'expected' : 0},
        
        
        # (+-)
        {'input' : '10 plus 5', 'expected' : 15},
        {'input' : '10 minus 5', 'expected' : 5},
        {'input' : '5 minus 10', 'expected' : -5},
        {'input' : '5 plus 10', 'expected' : 15},

        #  loops
        {'input' : '5 plus 2 for 5 times', 'expected' : 35},
        {'input' : '5 minus 2 for 5 times', 'expected' : 15},
        {'input' : 'if 5 is greater than 2 then 1 plus 0 else 0 for 5 times', 'expected' : 5},
        {'input' : 'if 5 is greater than 2 then 10 plus 5 else 0 for 5 times', 'expected' : 75},
        
        # exception handling    
        {'input' : '10 less 2', 'expected' : _Exception()},
        {'input' : 'plus 2 plus 5', 'expected' : _Exception()},
        {'input' : 'else 5 plus 2', 'expected' : _Exception()},
        {'input' : 'if 5 plus 2', 'expected' : _Exception()},
        {'input' : 'if else then 5 plus 2', 'expected' : _Exception()},
        {'input' : 'times 5 plus 2', 'expected' : _Exception()},
        
        # Assignment
        {'input' : 'let x equal to 1', 'expected' : Assignment()},
        {'input' : 'x plus 1', 'expected' : 2},
        {'input' : 'let x equal to 5 plus 2', 'expected' : Assignment()},
        {'input' : 'x plus 0', 'expected' : 7},
        {'input' : 'let x equal to 5', 'expected' : Assignment()},
        {'input' : 'x plus 1 for 5 times', 'expected' : 30},
        {'input' : 'x minus 1 for 5 times', 'expected' : 20},
        {'input' : 'let x equal to 1', 'expected' : Assignment()},
        {'input' : 'if x is less than 2 then 5 else 0', 'expected' : 5},
    ]
    
    for index, test in enumerate(tests):
        result = parser.parse_new(test.get('input'))
        try:
            if type(result) is _Exception or type(result) is Assignment:
                assert type(result) == type(test.get('expected'))
            else:
                assert result.execute() == test.get('expected')
            print(f'PASSED Test#{index+1} : {test.get("input")}')
        except AssertionError:
            print(f"""
                  =====================
                        TEST FAIL
                  Test: {test.get('input')} = {test.get('expected')}
                  Expected = {test.get('expected')}, Result = {result.execute()}
                  
                  Full:
                    type(result) = {type(result)}
                    {result}
                  =====================
                  """)
            raise AssertionError
    print('Tests passed.')
    print(u'='*20)

if __name__ == '__main__':
    new_parser_tests()

    parser = Parser()
    # Testing Exceptions
    # output = parser.parse_new("10 less 2")
    # output = parser.parse_new("plus 2 plus 5")
    # output = parser.parse_new("else 5 plus 2")
    # output = parser.parse_new("if 5 plus 2")
    # output = parser.parse_new("if else then 5 plus 2")
    # output = parser.parse_new("times 5 plus 2")
    
    # Assignment
    # output = parser.parse_new("let x equal to 1")
    # output = parser.parse_new("let x equal to 1")    
    # output = parser.parse_new("let x equal to 5 plus 2")
    
    # print(output)
    # print(output.execute())
    # print(parser.user_keywords)
    
    # output = parser.parse_new("x plus 1 for 5 times")
    # output = parser.parse_new("x plus 1")
    # print(output)
    # print(output.execute())
    
    
    
    # Working
    
    # float (+-) if()
    # output = parser.parse_new("10 plus 2 plus if 5 is greater than 2 then 2 plus 5 else 0")
    # output = parser.parse_new("10 plus 2 minus if 5 is greater than 2 then 2 plus 5 else 0")
    
    # if() (+-) float
    # output = parser.parse_new("if 5 is greater than 2 then 2 plus 5 else 0 plus 5 plus 2")
    # output = parser.parse_new("if 5 is greater than 2 then 2 plus 5 else 0 minus 5 plus 2")
    
    # float (+-) if() (+-) float
    # output = parser.parse_new("5 plus 2 if 5 is greater than 2 then 2 plus 5 else 0 plus 5 plus 2")
    
    
    # output = parser.parse_new("5 plus 2")
    # [5.0, '+', 2.0, '-', 1.0, '+', 7.0]
    # output = parser.parse_new("5 plus 2 minus 1")
    # output = parser.parse_new("5 plus 2 minus 1 plus 7")
    
    # 5 plus 2 for 5 times
    
    # output = parser.parse_new("5 plus 2 for 5 times")

    # output = parser.parse_new("if 5 is greater than 2 then 1 plus 0 else 0 for 5 times")
    # print(output)
    # if type(output) is not Exception:
    #     print(output.execute())

    