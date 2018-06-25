'''
Copy.py
A small script to copy a given number of files from one folder to another

Author: Karsten Ladner
Date: 5/29/2018
'''
import os
import sys

if __name__ == '__main__':
    # dest: destination directory
    # src: source directory
    # size: how many files to copy

    src = sys.argv[1]
    dest = sys.argv[2]
    size = int(sys.argv[3])

    os.chdir(src)
    ls = os.listdir(os.getcwd())
    for fil in ls[:size]:
        old = os.path.join(os.getcwd(), fil)
        new = os.path.join("../", dest, fil)
        os.rename(old, new)
    os.chdir(os.path.join("../", dest))
    os.popen("cp -r . {0}".format(os.path.join("../", src)))
