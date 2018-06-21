"""
greg.py
A program to calculate when Easter should fall in a given year

Author: Karsten Ladner
Date: 5/24/2018
"""


def epact( year ):
    '''
    Calculate the number of days between Jan. 1 of a given year and Easter
    
    year: (int) the year
    '''

    c = year / 100

    return((8 + (c/4)) - c + ((8 * c + 13) / 25) + 11 * (year % 19) % 30 )

if __name__ == '__main__':
    year = input("What year would you like to calculate (xxxx): ")
    year = int(year)
    print("There are {0} days between January 1st and Easter during {1}".format(epact(year), year))
