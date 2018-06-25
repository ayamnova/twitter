"""
String.py
A program to reverse a string

Author: Karsten Ladner
Date: 5/24/2018
"""


def reverse(string):
    '''
    A function to reverse a string

    string: string to reverse
    '''
    string = string.strip()

    temp = list()
    for i in range(len(string)):
        temp.append(string[i])

    out = ""
    for i in range(len(temp)):
        out += temp.pop() 

    return out

if __name__ == '__main__':
    print(reverse("hello world"))
        
        
        
