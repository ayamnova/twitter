"""
Square Root
A program to calculate the square root of a number by guessing

Author: Karsten Ladner
Date: 5/24/2018
"""


import math


def sqrt(guesses, num):
    '''
    Calculate the square root of num by guessing with the number of guesses

    num: the number to calculate
    guesses: how many times to guess
    guess: the current number of guesses
    value: the calculated value of the sqrt
    '''

    value = num / 2.0

    guess = 0
    while guess < guesses:
        value = (value + num / value) / 2.0
        guess += 1
    return(value)


if __name__ == '__main__':
    num = int(input("What number would you like to calculate: "))
    guesses = int(input("How many guesses: "))
    val = sqrt(guesses, num)

    print("Guessed value: {0}\nPython's value: {1}".format(val, math.sqrt(num)))



