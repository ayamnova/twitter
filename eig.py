'''
Eig.py
A python script to get the eigenvalues from a huge symmetric matrix

Author: Karsten Ladner
Date: 7/16/2018
'''

import os
import sys
import time
from os.path import join as jn
import pickle

from constants import *


def first_run(raw, temp, eig):
    with open(jn(PROC, raw), 'r') as fin:
        with open(jn(PROC, temp), 'wb') as fout:
            top = [float(c) for c in fin.readline().split("\t") if c is not "\n"]
            for row in fin:
                # Calculate the scalar
                num1 = row[:row.index("\t")]
                mult = float(num1) / top[0]

                # Scale the top row by the factor just calculated
                subt = [mult * c for c in top]

                # Transform the row by the scaled top row
                row = [float(r) - t for r, t in zip(row.split("\t"), subt)]

                # print("Dumping {0}".format(row[1:]))
                pickle.dump(row[1:], fout)

            print(top[0])
            with open(PROC + eig, 'w') as eout:
                eout.write("\t{0}".format(top[0]))
                eout.close()
        fout.close()
    fin.close()


def loadall(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def run(inp, temp, eig):
    '''
    A method to calculate the eigenvalue for one row
    Reads from an input pickle file that has pickled a list of floats and will
    continue to run until there are no more rows to process from the pickled
    file

    inp (str): the input file
    temp (str): the temp file to save the modified rows to
    eig (str): the file where the eigenvalue should be saved
    '''
    # Load the pickle file as a generator
    rows = loadall(jn(PROC, inp))
    # Open the temp file for writing
    with open(jn(PROC, temp), 'wb') as fout:
        try:
            # Try to get the first row from the pickle
            top = rows.__next__()
            # print("Top: {0}".format(top))
        except StopIteration:
            # The pickle is empty. We're done
            print("Stopped")
            return(0)
        for row in rows:
            # Iterate through the rest of the rows and transform them before
            # saving them to the temp file

            # Figure out what the scalar value is
            num1 = row[0]
            mult = num1 / top[0]
            subt = [mult * c for c in top]
            row = [r - t for r, t in zip(row, subt)]

            pickle.dump(row[1:], fout)
            # print(row[1:10])

        print(top[0])
        with open(jn(PROC, eig), 'a') as eout:
            eout.write("\t{0}".format(top[0]))
            eout.close()
    return(1)


if __name__ == '__main__':
    start = time.time()
    # The first run has to be different to account for the different kinds
    # of input
    first_run('big', "tempmat.tmp", "eig.txt")
    # Make the temp file the one to read from
    os.rename(jn(PROC, "tempmat.tmp"), jn(PROC, "tempmat"))
    count = 0
    # Keep on running until run returns a 0
    while run("tempmat", "tempmat.tmp", "eig.txt") != 0:
        os.rename(jn(PROC, "tempmat.tmp"), jn(PROC, "tempmat"))
        if count % 1000 == 0 and count != 0:
            print("Finished 1000 rows taking {0}".format(start - time.time()))
        count += 1
    print("Finished!")
