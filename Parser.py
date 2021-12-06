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
            
            # TODO: change solution path based on assignment
            'let' : '=',
            
            # TODO: check with use cases to finalize
            'more' : '>',
            'less' : '<'
        }
        
        # User generated key : value pair to allow for variable assignment/storage
        self.user_keywords = {}
        
    def parse_2(self, user_input):
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
        assert Parser().parse_2(test.get('input')) == test.get('expected')
        
    print("Tests passed")

if __name__ == '__main__':
    parser_test()
    print(u'='*10)
    parser = Parser()
    output = parser.parse_2("2 plus 5 plus 2 minus 2")
    print(output)
    
    