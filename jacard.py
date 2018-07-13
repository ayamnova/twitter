'''
Jaccard Module
A script to calculate the Jaccard index for two days

Author: Karsten Ladner
Date: 7/13/2018
'''

import sys
from os import listdir as ls
from os.path import join as jn
from os.path import isfile
from tweets import load_values_from_file as load


def jaccard(a, b):
    '''A method to calculate the Jaccard index for the two sets, a and b
    a: a set
    b: a set

    Returns an int
    '''

    return(len(a & b) / len(a | b))


if __name__ == '__main__':
    path = sys.argv[1]
    a = None
    b = None
    f1 = None
    f2 = None
    # create the list of user files using a magical list comprehension
    files = [jn(path, f) for f in ls(path) if isfile(jn(path, f)) and "users-" in f]
    # sort the files so that it is in ascending order
    for f in sorted(files):
        # b is the file that comes out of the queue
        b = load(f)
        # clean up the filename
        f2 = f.strip(path + "users-").strip(".dat")
        # this is really just for the first pass through the loop
        if a is not None:
            j = jaccard(set(a['data']), set(b['data']))
            print("{0} - {1}: {2}".format(f1, f2, j))
        # make a point at b
        a = b
        f1 = f2
