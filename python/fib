"""
Fibonacci.py
A program to cacluate the value of the fibonacci number that is the given
distance away

Author: Karsten Ladner
Date: 5/24/2018
"""


def fibonacci(n):
    '''
    Calculate the fibonacci the nth fibonacci number

    n: the nth term of the sequence
    '''

    if n == 1:
        # base case
        return(0)
    elif n == 2:
        # second base case
        return(1)
    else:
        return(fibonacci(n - 2) + fibonacci(n - 1))


if __name__ == '__main__':
    n = input("How many terms in the series do you want to calculate: ")
    print("The {0}th term in the sequence is {1}".format(n, fibonacci(int(n))))
