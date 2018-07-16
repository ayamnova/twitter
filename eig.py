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
                if top[0] != 0:
                    mult = float(num1) / top[0]
                else:
                    mult = float(num1)

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
    rows = loadall(jn(PROC, inp))
    with open(jn(PROC, temp), 'wb') as fout:
        try:
            top = rows.__next__()
            # print("Top: {0}".format(top))
        except StopIteration:
            print("Stopped")
            return(0)
        for row in rows:
            # print("Row: {0}".format(row))
            num1 = row[0]
            if top[0] != 0:
                mult = num1 / top[0]
            else:
                mult = num1
            subt = [mult * c for c in top]
            row = [r - t for r, t in zip(row, subt)]

            pickle.dump(row[1:], fout)

        print(top[0])
        with open(jn(PROC, eig), 'a') as eout:
            eout.write("\t{0}".format(top[0]))
            eout.close()
    return(1)


if __name__ == '__main__':
    start = time.time()
    first_run(sys.argv[1], "tempmat.tmp", "eig.txt")
    os.rename(jn(PROC, "tempmat.tmp"), jn(PROC, "tempmat"))
    count = 0
    while run("tempmat", "tempmat.tmp", "eig.txt") != 0:
        os.rename(jn(PROC, "tempmat.tmp"), jn(PROC, "tempmat"))
        if count % 1000 == 0 and count != 0:
            print("Finished 1000 rows taking {0}".format(start - time.time()))
        count += 1
    print("Finished!")
