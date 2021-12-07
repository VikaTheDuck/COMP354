# Algo-lator
Final Project Submission for Introduction to Software Engineering (COMP 354) Fall 2021

Algo-lator is a calculator built to help teach young children who can read and write how to develop simple algorithms. Using Algo-lator's specially designed syntax even young children can begin to construct their own algorithms and execute them in real time. Algo-lator displays the execution result along with comprehensive error messages should an error occur to help the user understand and fix their errors. `Start writing your own algorithms with Algo-lator now by simply following the setup instructions below!`

# Usage
### Running the full application with GUI
```bash
> python TextEditor.py 
```

### Running tests
```bash
> python Parser.py
> python Expression.py
```

### Try some sample inputs:
* 10 plus 5
* 10 minus 5
* 5 plus 2 for 5 times
* let x equal to 5
* if x is greater than 2 then x else 0
* x plus 5
* 10 plus 2 minus if 5 is greater than 2 then 5 plus 2 else 0

### Modifying tests
 
To modify or add any test cases simply add a dictionary entry in the form:
<br>
`{'input' : '[input string]', 'expected' : [expected result]}`
<br> into the respective test array within the .py file

##### *Note: Assignment and Exception handling tests must contain only base Assignment() and _Exception() objects respectively
##### ie. 'expected' : Assignment() and 'expected' : _Exception()


# Syntax Table
<Table>
    <thead>
        <th>Operation</th>
        <th>Input</th>
        <th>Parsed Output</th>
    </thead>
    <tbody>
        <tr>
            <td>
                Addition
            </td>
            <td>
                5 plus 7
            </td>
            <td>
                5 + 7
            </td>
        </tr>
        <tr>
            <td>
                Subtraction
            </td>
            <td>
                5 minus 7
            </td>
            <td>
                5 - 7
            </td>
        </tr>
        <tr>
            <td>
                Assignment
            </td>
            <td>
                let x equal to 5
            </td>
            <td>
                x = 5
            </td>
        </tr>
        <tr>
            <td>
                Conditional
            </td>
            <td>
                if 5 is greater than 2 then 
            </td>
            <td>
                5 + 7
            </td>
        </tr>
        <tr>
            <td>
                Loops
            </td>
            <td>
                Add 1 to x for 5 times
            </td>
            <td>
                (1 + x) for 5 times
            </td>
        </tr>
    </tbody>
</Table>

# Troubleshooting
```bash
# replace 'python' with one of the following while running a file
1) > python3 <filename>
2) > py <filename>
```
### Missing package tk or tkinter
Try one of the following solutions
```bash
1) > pip install PySimpleGUI
2) > pip install python-tk
3) package installation
# Linux
> sudo apt-get install python3-tk
# Mac
> brew install tcl-tk
# Windows
# Ensure tcl/tk option is selected during python installation
```

# Team Members
Efe Harmankaya <br>
Ian Mullett <br>
Donovan Upsdell <br>
Sarah Joyal <br>
Victoria Solodovnikova <br>
Ibrahim Tawakol <br>

