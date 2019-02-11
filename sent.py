'''
Sentimentality
A module to compute the sentimentality of tweets

Author: Karsten Ladner
Date: 6/25/2018
'''

import sys
from os.path import join as jn
from tweets import get_tweets
from joblib import Parallel, delayed
from afinn import Afinn
from config import PATH, OUT


def get_sentiment(tweets):
    '''Get the sentiment of a list of tweets
    
    A method to get the sentimentality of all the tweets in a directory

    tweets: a list of tweets

    Return: (total sentimentality, number of tweets, min, max)
    '''

    total = 0
    _min = 0
    _max = 0
    pos = 0
    neg = 0
    neut = 0

    temp = Parallel(n_jobs=-1)(delayed(
        process_sentiment)(t) for t in tweets)

    for x in temp:
        total += x[0]
        if x[1] < _min:
            _min = x[1]
        if x[2] > _max:
            _max = x[2]
        neg += x[3]
        neut += x[4]
        pos += x[5]

    print("Sentiment Processed")  # Log

    return(total, len(tweets), _min, _max, neg, neut, pos)


def process_sentiment(tweet):
    total = 0
    _min = 0
    _max = 0
    pos = 0
    neg = 0
    neut = 0

    afinn = Afinn(emoticons=True)
    sc = afinn.score(tweet['text'])

    total += sc

    if sc < _min:
        _min = sc
    if sc > _max:
        _max = sc
    if sc < 0:
        neg += 1
    elif sc > 0:
        pos += 1
    elif sc == 0:
        neut += 1

    return(total, _min, _max, neg, neut, pos)


if __name__ == '__main__':
    out = jn(OUT, sys.argv[2])
    dirs = sys.argv[1].split(',')

    with open(out, 'w') as fout:
        for d in dirs:
            tweets = get_tweets([d], key='text', prefix=PATH)
            sent, total, mn, mx, neg, neut, pos = get_sentiment(tweets[0])
            print("Sentiment Calculated")
            fout.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\n".format(
                d, sent, mn, mx, neg, neut, pos, total, tweets[1]))
    fout.close()

