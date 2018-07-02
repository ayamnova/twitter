'''
Geo.py
A python module to find the distribution of users and tweets across the globe

Author: Karsten Ladner
Date: 6/29/2018
'''


import sys
import carmen
from os.path import join as jn
from tweets import get_tweets


PATH = "./crisis/crisis/2018/"
# PATH = "./data/"


def get_country_distribution(tweets):
    '''
    A method to get the distribution of tweets across countries and cities. If
    a city is not found, then the value will be added to "null"

    tweets: the list of tweets

    Return a dictionary of countries to cities and the number of non-located 
    tweets
    '''

    d = dict()  # the dictionary of countries-values
    num_none = 0  # the number of non-located tweets

    # initialize the location engine
    r = carmen.get_resolver()
    r.load_locations()

    # loop through all the tweets
    for t in tweets:
        # set default values for country and city
        city = "null"
        country = ""

        try:
            # try to find a location
            loc = r.resolve_tweet(t)[1]
            country = loc.country
            # try to find the city  
            if loc.city is not "":
                city = loc.city
        except TypeError:
            # a location was not found
            num_none += 1
            continue
        # Add information to the dictionary
        if d.get(country) is None:
            # a new country was found
            d[country] = [1, {city: 1}]
        elif d[country][1].get(city) is None:
            # a new city was found
            d[country][0] += 1
            d[country][1][city] = 1
        else:
            # country and city were already added, increment value
            d[country][0] += 1
            d[country][1][city] += 1

    return(d, num_none)


if __name__ == '__main__':

    dirs = [jn(PATH, d) for d in sys.argv[1].split(',')]
    tweets, filt = get_tweets(dirs)
    d, none = get_country_distribution(tweets)

    # Write a tab-separated file with each country on a different line
    with open(sys.argv[2], 'w') as fout:
        fout.write("Total tweets\t{0}\tNon-English\t{1}\tNo location\t{2}\n".format(
            len(tweets), filt, none))
        for country, info in sorted(d.items(), key=lambda x: x[1][0], reverse=True):
            total = info[0]
            out = country + "\t"
            cits = ""
            for city, value in info[1].items():
                cits += city + "\t" + str(value) + "\t"
                total += value
            out += "Total " + "\t" + str(total) + "\t" + cits + "\n"
            fout.write(out)
    fout.close()
