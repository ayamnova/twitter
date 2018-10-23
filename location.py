"""
Location
A module of tools to interact with the location information within tweets

Author: Karsten Ladner
Date: 10/23/2018
"""

import carmen
import math
import random

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
