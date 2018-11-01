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
import config


def get_tweets(dirs, key=None):
    '''Get all the tweets from a list of directories

    A function to get all the tweets from a list of directories

    Args:
        directory (list): a list of directories

    Return:
        (tuple) the first component is a the list of tweets and the second
        component is the number filtered tweets (int)
    '''

    ls = list()  # the list of tweets to return
    num_filtered = 0  # the number of filtered tweets
    files = list()  # the list of flume files

    # Find all the flume files
    files = get_flume_files(dirs)

    # process files
    temp = Parallel(n_jobs=-1)(delayed(
        process_flume_file)(f,key=key) for f in files)
    for x in temp:
        ls += x[0]
        num_filtered += x[1]

    print("Files processed")  # Log

    return (ls, num_filtered)


def get_flume_files(dirs):
    '''Find all the flume files from a list of directories

    Args:
        dirs (list): a list of directories containing flume files

    Return:
        list of strings that are paths to files
    '''

    files = list()  # the list of files

    # find all the flume files and add them to a list of files
    for d in dirs:
        print("Walking Directory: {0}".format(d))  # Log
        for dirp, dirn, fils in os.walk(d):
            print(dirp)  # Log
            print("Number of files: {0}".format(len(fils)))  # Log
            files.extend([os.path.join(dirp, f) for f in fils])

    print("Found all files in {0}".format(dirs))  # Log
    print("Number of files: {0}".format(len(files)))  # Log

    return(files)


def is_valid(tweet):
    '''Determine whether tweet is valid

    Args:
        tweet (tweet): tweet to test whether it needs to be filtered

    Return:
        bool:

    '''

    if tweet["lang"] in config.LANG:
        return(True)
    else:
        return(False)


def process_flume_file(fin):
    '''Return a list of tweets from a flume file

    Args:
        fin (string): file to read from

    Return:
        tuple: first component is a list of tweets, the second component is the
            number of tweets filtered
    '''


    ls = list()  # the list to return
    num_filtered = 0  # the number of filtered tweets

    # If there's an error wrap this in a try block
    with open(fin, 'r') as f:
        # Read each line as a new tweet
        for line in f:
                # Get the tweet from the json
                tweet = json.loads(line)
                if is_valid(tweet):
                    # Append good tweets to the return list
                    ls.append(tweet)
                else:
                    # Count the number of filtered tweets
                    num_filtered += 1
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
    '''Get the values for a particular field from a list of tweets

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
