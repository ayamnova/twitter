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
from tweets import get_tweets
from tweets import save_to_file as save
from constants import PATH, OUT, PROC

STATE_CODES = {
            "Alabama": "AL",
            "Alaska": "AK",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY"
        }

STATE_COORD = {
        "Alabama": (32.361538, -86.279118),
        "Alaska": (58.301935, -134.419740),
        "Arizona": (33.448457, -112.073844),
        "Arkansas": (34.736009, -92.331122),
        "California": (38.555605, -121.468926),
        "Colorado": (39.7391667, -104.984167),
        "Connecticut": (41.767, -72.677),
        "Delaware": (39.161921, -75.526755),
        "Florida": (30.4518, -84.27277),
        "Georgia": (33.76, -84.39),
        "Hawaii": (21.30895, -157.826182),
        "Idaho": (43.613739, -116.237651),
        "Illinois": (39.783250, -89.650373),
        "Indiana": (39.790942, -86.147685),
        "Iowa": (41.590939, -93.620866),
        "Kansas": (39.04, -95.69),
        "Kentucky": (38.197274, -84.86311),
        "Louisiana": (30.45809, -91.140229),
        "Maine": (44.323535, -69.765261),
        "Maryland": (38.972945, -76.501157),
        "Massachusetts": (42.2352, -71.0275),
        "Michigan": (42.7335, -84.5467),
        "Minnesota": (44.95, -93.094),
        "Mississippi": (32.320, -90.207),
        "Missouri": (38.572954, -92.189283),
        "Montana": (46.595805, -112.027031),
        "Nebraska": (40.809868, -96.675345),
        "Nevada": (39.160949, -119.753877),
        "New Hampshire": (43.220093, -71.549127),
        "New Jersey": (40.221741, -74.756138),
        "New Mexico": (35.667231, -105.964575),
        "New York": (42.659829, -73.781339),
        "North Carolina": (35.771, -78.638),
        "North Dakota": (48.813343, -100.779004),
        "Ohio": (39.962245, -83.000647),
        "Oklahoma": (35.482309, -97.534994),
        "Oregon": (44.931109, -123.029159),
        "Pennsylvania": (40.269789, -76.875613),
        "Rhode Island": (41.82355, -71.422132),
        "South Carolina": (34.000, -81.035),
        "South Dakota": (44.367966, -100.336378),
        "Tennessee": (36.165, -86.784),
        "Texas": (30.266667, -97.75),
        "Utah": (40.7547, -111.892622),
        "Vermont": (44.26639, -72.57194),
        "Virginia": (37.54, -77.46),
        "Washington": (47.042418, -122.893077),
        "West Virginia": (38.349497, -81.633294),
        "Wisconsin": (43.074722, -89.384444),
        "Wyoming": (41.145548, -104.802042)
        }

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
    no_state = 0  # the number of state-less tweets


    # initialize the sentiment engine
    afinn = Afinn(emoticons=True)

    # initialize the location engine
    r = carmen.get_resolver()
    r.load_locations()

    # loop through all the tweets
    for t in tweets:
        # set default values for state and city
        score = None
        state = ""

        try:
            # try to find a location
            loc = r.resolve_tweet(t)[1]

            # Skip countries that are not America
            if "United States" not in loc.country:
                continue

            if loc.state != "":
                state = loc.state
            else:
                no_state += 1
                continue

        except TypeError:
            # a location was not found
            num_none += 1
            continue

        # get the sentiment score
        if t.get("extended_tweet") is None:
            score = afinn.score(t["text"])
        else:
            score = afinn.score(t["extended_tweet"]["full_text"])

        # Add information to the dictionary
        if d.get(state) is None:
            # a new state was found
            # initializize
            d[state] = {
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
            # state and city were already added, increment value
            d[state]["total"] += 1
            # add user to set
            d[state]["users"].add(t["user"]["screen_name"])

        if score < 0:
            d[state]["sent"]["neg"] += 1
        elif score > 0:
            d[state]["sent"]["pos"] += 1
        else:
            d[state]["sent"]["neut"] += 1

        d[state]["sent"]["total"] += score

    return(d, num_none, no_state)


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
    d, none, no_state = get_country(tweets)

    # save_geo(d, filt, none, jn(PROC, sys.argv[2] + ".dat"))

    total_pos_tweets = 0
    for c in d:
        total_pos_tweets += d[c]['sent']['pos']
    print(total_pos_tweets)
    # Write a comma-separated file
    with open(fout, 'w') as fout:
        fout.write("State,Code,Sentiment,Users,Lat,Lon\n")
        for c in STATE_CODES:
            if d.get(c) is not None:
                s = d[c]["sent"]["pos"] / total_pos_tweets
                # s = d[c]["sent"]["pos"] - d[c]["sent"]["neg"]
                u = len(d[c]["users"])
            else:
                s = 0
                u = 0
            try:
                fout.write("{0},{1},{2},{3},{4},{5}\n".format(
                    c, STATE_CODES[c], s, u, STATE_COORD[c][0], STATE_COORD[c][1]))
            except KeyError:
                    print("Missing key {0}".format(c))
        fout.close()
