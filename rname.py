import os
import os.path

d = os.getcwd()


def rename(d):
    for e in os.listdir(d):
        test = os.path.join(d, e)
        if os.path.isfile(test):
            n = os.path.basename(test).split('~')
            os.rename(test, os.path.join(d, n[0]))
        elif os.path.isdir(test):
            rename(test)


if __name__ == '__main__':
    rename(d)
