'''
Geo.py
A python module to find the distribution of users and tweets across the globe

Author: Karsten Ladner
Date: 6/29/2018
'''


import sys
import carmen
from afinn import Afinn
from os.path import join as jn
from tweets import get_tweets, COUNTRY_CODES, COUNTRY_COORD as COORD
from tweets import save_to_file as save
from constants import PATH, OUT, PROC


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


    # initialize the sentiment engine
    afinn = Afinn(emoticons=True)

    # initialize the location engine
    r = carmen.get_resolver()
    r.load_locations()

    # loop through all the tweets
    for t in tweets:
        # set default values for country and city
        city = "null"
        country = ""
        score = None

        try:
            # try to find a location
            loc = r.resolve_tweet(t)[1]
            country = loc.country
            # try to find the city
            if loc.city is not "":
                city = loc.city
            else:
                city = "null"
            # get the sentiment score
            if t.get("extended_tweet") is None:
                score = afinn.score(t["text"])
            else:
                score = afinn.score(t["extended_tweet"]["full_text"])
        except TypeError:
            # a location was not found
            num_none += 1
            continue
        # Add information to the dictionary
        if d.get(country) is None:
            # a new country was found
            # initializize
            d[country] = {
                    "sent": {
                        "total": score,
                        "pos": 0,
                        "neg": 0,
                        "neut": 0
                        },
                    "total": 1,
                    "cities": {
                        city: 1
                        }
                    }
        elif d[country]["cities"].get(city) is None:
            # a new city was found
            d[country]["total"] += 1
            d[country]["cities"][city] = 1
        else:
            # country and city were already added, increment value
            d[country]["total"] += 1
            d[country]["cities"][city] += 1

        if score < 0:
            d[country]["sent"]["neg"] += 1
        elif score > 0:
            d[country]["sent"]["pos"] += 1
        else:
            d[country]["sent"]["neut"] += 1

        d[country]["sent"]["total"] += score

    return(d, num_none)

def get_country(tweets):
    '''
    A method to get the distribution of tweets across countries and cities. If
    a city is not found, then the value will be added to "null"

    tweets: the list of tweets

    Return a dictionary of countries to cities and the number of non-located 
    tweets
    '''

    d = dict()  # the dictionary of countries-values
    num_none = 0  # the number of non-located tweets


    # initialize the sentiment engine
    afinn = Afinn(emoticons=True)

    # initialize the location engine
    r = carmen.get_resolver()
    r.load_locations()

    # loop through all the tweets
    for t in tweets:
        # set default values for country and city
        country = ""
        score = None

        try:
            # try to find a location
            loc = r.resolve_tweet(t)[1]
            country = loc.country
            # get the sentiment score
            if t.get("extended_tweet") is None:
                score = afinn.score(t["text"])
            else:
                score = afinn.score(t["extended_tweet"]["full_text"])
        except TypeError:
            # a location was not found
            num_none += 1
            continue
        # Add information to the dictionary
        if d.get(country) is None:
            # a new country was found
            # initializize
            d[country] = {
                    "sent": {
                        "total": score,
                        "pos": 0,
                        "neg": 0,
                        "neut": 0
                        },
                    "total": 1,
                    "users": {t["user"]["screen_name"]}
                    }
        else:
            # country and city were already added, increment value
            d[country]["total"] += 1
            # add user to set
            d[country]["users"].add(t["user"]["screen_name"])

        if score < 0:
            d[country]["sent"]["neg"] += 1
        elif score > 0:
            d[country]["sent"]["pos"] += 1
        else:
            d[country]["sent"]["neut"] += 1

        d[country]["sent"]["total"] += score

    return(d, num_none)


def save_geo(dat, filt, none, fout):
    data = {
            "data": dat,
            "num_filtered": filt,
            "nolocation": none
            }
    save(data, fout)


if __name__ == '__main__':
    fout = jn(OUT, sys.argv[2] + ".csv")
    dirs = [jn(PATH, d) for d in sys.argv[1].split(',')]
    tweets, filt = get_tweets(dirs)
    # d, none = get_country_distribution(tweets)
    d, none = get_country(tweets)

    # save_geo(d, filt, none, jn(PROC, sys.argv[2] + ".dat"))

    # Write a tab-separated file with each country on a different line
    '''
    with open(fout, 'w') as fout:
        fout.write("Total tweets\t{0}\tNon-English\t{1}\tNo location\t{2}\n".format(
            len(tweets), filt, none))
        # sort the countries by the totals
        for country, dat in sorted(d.items(), key=lambda x: x[1]["total"], reverse=True):
            total = dat["total"]
            out = country + ","
            cits = ""
            cits = ",".join([str(c) + "," + str(v) for c, v in sorted(dat["cities"].items(), key=lambda x: x[1], reverse=True)])
            # for city, value in sorted(dat["cities"].items(), key=lambda x: x[1], reverse=True):
            #    cits += city + "," + str(value) + "\t"
            out += "{0},{1},{2},{3},".format(total, dat["sent"]["neg"], dat["sent"]["neut"], dat["sent"]["pos"]) + cits + "\n"
            fout.write(out)
    fout.close()
    '''
    total_pos_tweets = 0
    for c in d:
        total_pos_tweets += d[c]['sent']['pos']
    # Write a comma-separated file
    with open(fout, 'w') as fout:
        fout.write("Country,Code,Sentiment,Users,Lat,Lon\n")
        for c in COUNTRY_CODES:
            if d.get(c) is not None:
                s = d[c]["sent"]["pos"] / total_pos_tweets
                u = len(d[c]["users"])
            else:
                s = 0
                u = 0
            try:
                fout.write("{0},{1},{2},{3},{4},{5}\n".format(
                    c, COUNTRY_CODES[c], s, u, COORD[c][0], COORD[c][1]))
            except KeyError:
                    print("Missing key {0}".format(c))
        fout.close()
