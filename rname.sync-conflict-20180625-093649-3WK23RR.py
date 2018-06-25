import os
import os.path

d = os.getcwd()

def rename(d):
    for e in os.listdir(d):
        test = os.path.join(d, e)
        if os.path.isfile(
