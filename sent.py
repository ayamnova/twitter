'''
Sentimentality
A module to compute the sentimentality of tweets

Author: Karsten Ladner
Date: 6/25/2018
'''

import sys
from tweets import get_tweets, get_sentiment

PATH = "./crisis/crisis/2018/"

if __name__ == '__main__':
    out = sys.argv[2]
    dirs = sys.argv[1].split(',')

    with open(out, 'w') as fout:
        for d in dirs:
            tweets = get_tweets([d], key='text', prefix=PATH)
            sent, total, mn, mx, neg, neut, pos = get_sentiment(tweets[0])
            fout.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\n".format(
                d, sent, mn, mx, neg, neut, pos, total, tweets[1]))
    fout.close()

