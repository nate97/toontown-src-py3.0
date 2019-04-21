Python Style Guidelines
=======================
For Python programming, we use a slightly modified version of the standard [PEP-8 Style Guide for Python Code](http://legacy.python.org/dev/peps/pep-0008 "PEP-8 Style Guide for Python Code"). Read below for our modifications.
- - -
## Code lay-out ##
### Indentation ###
The closing brace/bracket/parenthesis on multi-line constructs may either be directly at the end, as in:

    my_list = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20]
    result = some_function_that_takes_arguments(
        'a', 'b', 'c', 'd', 'e', 'f')
        
or it may be by itself on the next line:

    my_list = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20
    ]
    result = some_function_that_takes_arguments(
        'a', 'b', 'c', 'd', 'e', 'f'
    )

### Tabs or Spaces? ###
**_Always_** use spaces.

### Maximum Line Length ###
**Docstrings and comments** should be restricted to _80 characters_. Anything else should be limited to _100 characters_.

## Naming Conventions ##
### Variables ###
Intentionally **unused** variables should be named "**_**". This will make common IDEs and editors ignore it.

## Strings ##
### Quotations ###
Use single quotations _(')_ unless there is one inside the string, in which case use double quotations _(")_.

Remember to also put parentheses parentheses around strings to future proof the code for Python3. ('example_string')
