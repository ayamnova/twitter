"""
Area
A program to calculate the area of a triangle given three sides

Author: Karsten Ladner
Date: 5/24/2018

"""

import math


def area(a, b, c):
    '''
    Calculate the area of a triangle given the three sides
    a: (int) length of one side
    b: (int) length of one side
    c: (int) length of one side
    '''

    s = (float(a) + float(b) + float(c)) / 2.0

    return(math.sqrt(s * (s - a) * (s - b) * (s - c)))


if __name__ == '__main__':
    print("Area of a triangle with sides: 3, 4, 5 \n(Should be 6)")
    print(area(3, 4, 5))
