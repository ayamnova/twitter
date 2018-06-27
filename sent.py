'''
Sentimentality
A module to compute the sentimentality of tweets

Author: Karsten Ladner
Date: 6/25/2018
'''

import sys
import re
from os.path import join
from tweets import get_tweets, get_sentiment

PATTERN = r'(/\d{2}/\d{2})'
PATH = "./crisis/crisis/2018/"


def save_to_file(day, total, number, minimum, maximum, neg, pos, fout):
    fout.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format(
        day, total, number, minimum, maximum, neg, pos))


if __name__ == '__main__':
    out = sys.argv[2]
    dirs = sys.argv[1].split(',')
    dirs = [join(PATH, d) for d in dirs]

    with open(out, 'w') as fout:
        for d in dirs:
            tweets = get_tweets(d, unique=True)
            total, num, mn, mx, neg, pos = get_sentiment(tweets[0])
            date = re.search(PATTERN, d)
            if date is not None:
                d = date.groups()[0]
            print(d)
            save_to_file(d, total, num, mn, mx, neg, pos, fout)
    fout.close()
