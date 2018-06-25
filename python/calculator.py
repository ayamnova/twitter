"""
Calculator.py
A small calculator program

Author: Karsten Ladner
Date: 5/25/2018
"""


import re


def calculate(arg1, arg2, operator):
    '''
    Perform the calculation on num1 and num2 given the operator and return the
    result

    arg1: (string) the first argument
    arg2: (string) the second argument
    operator: (char) the operation to apply
    '''

    num1 = float(arg1)
    num2 = float(arg2)

    if operator == '+':
        return add(num1, num2)
    elif operator == '-':
        return subtract(num1, num2)
    elif operator == '*':
        return multiplty(num1, num2)
    elif operator == '/':
        return divide(num1, num2)


def add(arg1, arg2):
    return arg1 + arg2


def subtract(arg1, arg2):
    return arg1 - arg2


def multiplty(arg1, arg2):
    return arg1 * arg2


def divide(arg1, arg2):
    return arg1 / arg2


def parse(inp):
    pattern = '''
    (\d*)
    (\+)
    (\d*)
    '''
    test = "10+100" 
    print(test)
    #res = re.search(pattern, test, re.VERBOSE).groups()
    #res = re.search(r'(\d\d*)([+|-|\*|/])(\d\d*)', test, re.VERBOSE).groups()
    res = re.search(r'(\d*)(\+)(\d*)', test, re.VERBOSE)
    if res.groups() is not None:
        calculate(res.groups()[0], res.groups()[2], res.groups()[1])




if __name__ == '__main__':
    parse("momma")
    num1 = 10.05
    num2 = 5.05

    print("Adding {0} and {1}: {2}".format( \
        num1, num2, calculate(num1, num2, '+')))
    print("Subtracting {0} from {1}: {2}".format( \
        num1, num2, calculate(num1, num2, '-')))
    print("Multiplying {0} and {1}: {2}".format( \
        num1, num2, calculate(num1, num2, '*')))
    print("Dividing {0} with {1}: {2}".format( \
        num1, num2, calculate(num1, num2, '/')))
