'''
Count
A script to count the english and non-english tweets from flume files

Author: Karsten Ladner
Date: 7/12/2018
'''

import sys
from os.path import join as jn
from tweets import get_tweets
from constants import PROC, OUT, PATH


if __name__ == '__main__':
    out = jn(OUT, sys.argv[2])
    dirs = sys.argv[1].split(',')

    with open(out, 'a') as fout:
        for d in dirs:
            tweets = get_tweets([d], prefix=PATH)
            print("{0},{1},{2}".format(d, len(tweets[0]), tweets[1]))
            fout.write("{0},{1},{2}".format(d, len(tweets[0]), tweets[1]))
    fout.close()
