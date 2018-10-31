"""
Tweet Text
A module for consolidating tweets in many different files to one file that has
all the tweet text

Author: Karsten Ladner
Date: 5/29/2018
"""

import json
import os
import sys
import pickle
from joblib import Parallel, delayed
from config import PATH


def get_tweets(dirs, prefix=None, key=None):
    '''
    A function to get all the tweets from a list of directories

    directory: a directory with files that have tweets separated by lines

    Returns a the list of tweets and the number filtered
    '''

    files = list()  # the list of flume files
    ls = list()  # the list of tweets to return
    num_filtered = 0  # the number of filtered tweets

    # add the prefix to the directory arguments
    if prefix is not None:
        dirs = [os.path.join(prefix, d) for d in dirs]

    # find all the flume files and add them to a list of files
    for d in dirs:
        print("Walking Directory: {0}".format(d))  # Log
        for dirp, dirn, fils in os.walk(d):
            print(dirp)  # Log
            print("Number of files: {0}".format(len(fils)))  # Log
            files.extend([os.path.join(dirp, f) for f in fils])

    print("Found all files in {0}".format(dirs))  # Log
    print("Number of files: {0}".format(len(files)))  # Log

    # process files
    temp = Parallel(n_jobs=-1)(delayed(
        process_flume_file)(f,key=key) for f in files)
    for x in temp:
        ls += x[0]
        num_filtered += x[1]

    print("Files processed")  # Log

    return (ls, num_filtered)


def process_flume_file(fin, key=None):
    ls = list()
    num_filtered = 0
    try:
        with open(fin, 'r') as f:
            for line in f:
                    # Get the tweet from the json
                    # and append it to ls if it is in English
                    tweet = json.loads(line)
                    if tweet["lang"] == "en":
                        # only process tweets in English
                        if key is None:
                            ls.append(tweet)
                        elif key == 'text':
                            if tweet.get("extended_tweet") is None:
                                text = tweet["text"]
                            else:
                                text = tweet["extended_tweet"]["full_text"]
                            ls.append(text)
                        elif key == 'names':
                            if tweet.get('extended_tweet') is not None:
                                ls.append(tweet['retweeted_status']['user']['screen_name'])
                            ls.append(tweet['user']['screen_name'])
                    else:
                        # the tweet isn't English. Filter it!
                        num_filtered += 1
    except:
        pass
    return(ls, num_filtered)


def consolidate(directory, key, outfile=None):
    '''Consolidates the values of a specific field from a directory of tweets

    A wrapper function for get_tweets and get_values to consolidate all the
    values in all the tweets in a given directory.

    Args:
        directory: (list) a list of directories to search for tweets
        key: (list) a list of strings with each subsequent string matching a
            JSON field

    Returns:
        list of values from that given field
    '''

    # get all the tweets from directory
    tweets, filt_num = get_tweets(directory)
    # get all the values from the tweets
    values = get_values(tweets, key)

    return(values)


def get_values(tweets, key):
    '''
    A function to get the value for a particular field from a list of tweets

    Args:
        tweets: a list of tweets to parse
        field: field to get

    Returns:
        a list of the values from the fields

    Raises:
        KeyError
    '''

    ls = list()  # the list to return
    # access the value from each field and store it to return
    for tweet in tweets:
        # catch any errors
        try:
            ls.append(tweet[key[0]])
        # print a message if the key is not found
        except KeyError:
            print("Key (\"{0}\") was not found for tweet. ID: {1}".format(
                    key[0], tweet["id_str"]))

    if len(key) == 1:
        # base case
        # there's are no more layers to go down
        return ls
    else:
        # go down another layer
        return get_values(ls, key[1:])


def parse_key_argument(inp):
    '''Parse the key to display'''

    return inp.split(',')


def save_to_file(values, fout):
    f = open(fout, 'wb')
    try:
        pickle.dump(values, f)
    finally:
        f.close()


def load_values_from_file(fin):
    f = open(fin, 'rb')
    values = pickle.load(f, encoding="utf8")
    return(values)


if __name__ == '__main__':
    directory = sys.argv[2]
    directory = os.path.join(PATH, directory)
    if sys.argv[1] == "con":
        key = parse_key_argument(sys.argv[3])
        print(consolidate([directory], key))
    elif sys.argv[1] == "loc":
        get_locations(directory)
    elif sys.argv[1] == "save":
        dirs = sys.argv[3].split(',')
        tweets = get_tweets(dirs, key=sys.argv[2], prefix=PATH)
        v = {
                'data': tweets[0], 
                'num': len(tweets[0]),
                'num_filtered': tweets[1]
            }
        save_to_file(v, sys.argv[4])
    elif sys.argv[1] == "load":
        val = load_values_from_file(sys.argv[2])
        for v in val['data']:
            print(v)
    else:
        get_tweets(["./crisis/crisis/2018/05/31"])
        print("I didin't understand what method you are calling."
                + "Please enter 'con', 'loc' or 'sent'")
