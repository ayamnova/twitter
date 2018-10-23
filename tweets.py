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
import math
import random
from joblib import Parallel, delayed
from afinn import Afinn
import carmen
from config import PATH


def get_coordinates(country, bad_locations=[]):
    '''
    A method to get the position of a country for a tweet by plotting the
    coordinates using a random angle a random distance away

    country: the country

    Return: a tuple with (x, y) values
    '''

    radius = random.randint(-2, 2)  # the radius of the circle
    angle = 0  # the angle to use

    # make sure the angle is not parallel or perpendicular to the center point
    while angle == 0 or angle == 90 or angle == 180 or angle == 270 or angle == 360:
        angle = random.randint(0, 360)

    # convert the angle to radians
    angle = math.radians(angle)

    # calculate the offset by using cosine and sine
    country_offset_x = float(radius * math.cos(angle))
    country_offset_y = float(radius * math.sin(angle))

    try:
        # country coordinates are stored N/S, E/W so the tuple needs to be
        # unpacked backwards
        y, x = COUNTRY_COORD[country]
        x += country_offset_x
        y += country_offset_y
        if (x, y) not in bad_locations:
            return(x, y)
        else:
            get_coordinates(country, bad_locations)
    except KeyError:
        print("{0} not found in country coordinates dictionary".format(
            country))
        return None


def add_positions(tweets):
    '''
    A method to append location information to a list of tweets and discard
    tweets without location information

    tweets: a list of tweets

    Return: a list of tweets that has location information appended
    '''

    located_tweets = list()

    resolver = carmen.get_resolver()
    resolver.load_locations()

    for tweet in tweets:
        # print("Current tweet:{0}".format(tweet["user"]["screen_name"]))
        try:
            if tweet.get("retweeted_status") is not None:
                if tweet["retweeted_status"] not in located_tweets:
                    try:
                        # find out what country this tweet was from
                        country = resolver.resolve_tweet(
                                tweet["retweeted_status"])[1].country
                        # get the position in that country
                        pos = get_coordinates(country)
                        if pos is not None:
                            # add the position informatoin to the tweet
                            tweet["retweeted_status"]["position"] = {
                                   "coordinates": pos,
                                   "country": country}
                            # append it to out list
                            located_tweets.append(tweet["retweeted_status"])
                    except TypeError:
                        continue

            # find out what country this tweet was from
            country = resolver.resolve_tweet(tweet)[1].country
            # get the coordinates in that country
            pos = get_coordinates(country)
            if pos is not None:
                # add the position informatoin to the tweet
                tweet["position"] = {"coordinates": pos, "country": country}
                # append to out list
                located_tweets.append(tweet)

        except TypeError:
            # The resolver returned a None value. Delete this tweet from the
            # list
            continue

    return located_tweets


def get_locations(directory):
    '''
    A method to parse through FlumeData and create a dictionary with its keys
    as countries and its values as lists of tweets

    directory: directory to search

    Return: a dictionary, key (str); value (list) of (tweets)
    '''
    locations = dict()

    tweets = get_tweets(directory)
    resolver = carmen.get_resolver()
    resolver.load_locations()

    for tweet in tweets:
        try:
            country = resolver.resolve_tweet(tweet)[1].country
            locations[country].append(tweet)
        except TypeError:
            continue
        except KeyError:
            locations[country] = [tweet]
        return locations


def print_locations(locations):
    # sort all the countries by the number of tweets from that country
    ls = sorted(locations.items(), key=lambda x: len(x[1]))
    for country, tweetlist in ls:
        print(country, end=" " * 10)
        for tweet in tweetlist:
            print("{0:^15.10}".format(tweet["user"]["screen_name"]), end="")
        print()


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


def get_users(dirs, prefix=None):
    '''
    A method to get a list of all the users in
    '''


def get_values(tweets, key):
    '''
    A function to get the value for a particular field from a list of tweets

    tweets: a list of tweets to parse
    field: field to get

    Returns a list of the values from the fields
    '''
    ls = list()  # the list to return
    # access the value from each field and store it to return
    for tweet in tweets:
        # catch any errors
        try:
            ls.append(tweet[key[0]])
        # print a message if the key is not found
        except KeyError:
            print("Key (\"{0}\") was not found for a tweet".format(
                    key[0]))

    if len(key) == 1:
        # base case
        # there's are no more layers to go down
        return ls
    else:
        # go down another layer
        return get_values(ls, key[1:])


def parse_key_argument(inp):
    '''
    A function to parse the input for the key argument
    '''
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
    if sys.argv[1] == "con":
        key = parse_key_argument(sys.argv[3])
        consolidate(directory, key)
    elif sys.argv[1] == "sent":
        tweets = get_tweets(directory)
        get_sentiment(tweets[0])
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
