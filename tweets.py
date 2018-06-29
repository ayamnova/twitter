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
import math
import random
from joblib import Parallel, delayed
from afinn import Afinn
import carmen


COUNTRY_COORDINATES = {
    "Andorra": (42.546245, 1.601554),
    "United Arab Emirates": (23.424076, 53.847818),
    "Afghanistan": (33.93911, 67.709953),
    "Antigua and Barbuda": (17.060816, -61.796428),
    "Anguilla": (18.220554, -63.068615),
    "Albania": (41.153332, 20.168331),
    "Armenia": (40.069099, 45.038189),
    "Netherlands Antilles": (12.226079, -69.060087),
    "Angola": (-11.202692, 17.873887),
    "Antarctica": (-75.250973, -0.071389),
    "Argentina": (-38.416097, -63.616672),
    "American Samoa": (-14.270972, -170.132217),
    "Austria": (47.516231, 14.550072),
    "Australia": (-25.274398, 133.775136),
    "Aruba": (12.52111, -69.968338),
    "Azerbaijan": (40.143105, 47.576927),
    "Bosnia and Herzegovina": (43.915886, 17.679076),
    "Barbados": (13.193887, -59.543198),
    "Bangladesh": (23.684994, 90.356331),
    "Belgium": (50.503887, 4.469936),
    "Burkina Faso": (12.238333, -1.561593),
    "Bulgaria": (42.733883, 25.48583),
    "Bahrain": (25.930414, 50.637772),
    "Burundi": (-3.373056, 29.918886),
    "Benin": (9.30769, 2.315834),
    "Bermuda": (32.321384, -64.75737),
    "Brunei": (4.535277, 114.727669),
    "Bolivia": (-16.290154, -63.588653),
    "Brazil": (-14.235004, -51.92528),
    "Bahamas": (25.03428, -77.39628),
    "Bhutan": (27.514162, 90.433601),
    "Bouvet Island": (-54.423199, 3.413194),
    "Botswana": (-22.328474, 24.684866),
    "Belarus": (53.709807, 27.953389),
    "Belize": (17.189877, -88.49765),
    "Canada": (56.130366, -106.346771),
    "Cocos [Keeling] Islands": (-12.164165, 96.870956),
    "Congo [DRC]": (-4.038333, 21.758664),
    "Central African Republic": (6.611111, 20.939444),
    "Congo [Republic]": (-0.228021, 15.827659),
    "Switzerland": (46.818188, 8.227512),
    "Côte d'Ivoire": (7.539989, -5.54708),
    "Cook Islands": (-21.236736, -159.777671),
    "Chile": (-35.675147, -71.542969),
    "Cameroon": (7.369722, 12.354722),
    "China": (35.86166, 104.195397),
    "Colombia": (4.570868, -74.297333),
    "Costa Rica": (9.748917, -83.753428),
    "Cuba": (21.521757, -77.781167),
    "Cape Verde": (16.002082, -24.013197),
    "Christmas Island": (-10.447525, 105.690449),
    "Cyprus": (35.126413, 33.429859),
    "Czech Republic": (49.817492, 15.472962),
    "Germany": (51.165691, 10.451526),
    "Djibouti": (11.825138, 42.590275),
    "Denmark": (56.26392, 9.501785),
    "Dominica": (15.414999, -61.370976),
    "Dominican Republic": (18.735693, -70.162651),
    "Algeria": (28.033886, 1.659626),
    "Ecuador": (-1.831239, -78.183406),
    "Estonia": (58.595272, 25.013607),
    "Egypt": (26.820553, 30.802498),
    "Western Sahara": (24.215527, -12.885834),
    "Eritrea": (15.179384, 39.782334),
    "Spain": (40.463667, -3.74922),
    "Ethiopia": (9.145, 40.489673),
    "Finland": (61.92411, 25.748151),
    "Fiji": (-16.578193, 179.414413),
    "Falkland Islands [Islas Malvinas]": (-51.796253, -59.523613),
    "Micronesia": (7.425554, 150.550812),
    "Faroe Islands": (61.892635, -6.911806),
    "France": (46.227638, 2.213749),
    "Gabon": (-0.803689, 11.609444),
    "United Kingdom": (55.378051, -3.435973),
    "Grenada": (12.262776, -61.604171),
    "Georgia": (42.315407, 43.356892),
    "French Guiana": (3.933889, -53.125782),
    "Guernsey": (49.465691, -2.585278),
    "Ghana": (7.946527, -1.023194),
    "Gibraltar": (36.137741, -5.345374),
    "Greenland": (71.706936, -42.604303),
    "Gambia": (13.443182, -15.310139),
    "Guinea": (9.945587, -9.696645),
    "Guadeloupe": (16.995971, -62.067641),
    "Equatorial Guinea": (1.650801, 10.267895),
    "Greece": (39.074208, 21.824312),
    "South Georgia and the South Sandwich Islands": (-54.429579, -36.587909),
    "Guatemala": (15.783471, -90.230759),
    "Guam": (13.444304, 144.793731),
    "Guinea-Bissau": (11.803749, -15.180413),
    "Guyana": (4.860416, -58.93018),
    "Gaza Strip": (31.354676, 34.308825),
    "Hong Kong": (22.396428, 114.109497),
    "Heard Island and McDonald Islands": (-53.08181, 73.504158),
    "Honduras": (15.199999, -86.241905),
    "Croatia": (45.1, 15.2),
    "Haiti": (18.971187, -72.285215),
    "Hungary": (47.162494, 19.503304),
    "Indonesia": (-0.789275, 113.921327),
    "Ireland": (53.41291, -8.24389),
    "Israel": (31.046051, 34.851612),
    "Isle of Man": (54.236107, -4.548056),
    "India": (20.593684, 78.96288),
    "British Indian Ocean Territory": (-6.343194, 71.876519),
    "Iraq": (33.223191, 43.679291),
    "Iran": (32.427908, 53.688046),
    "Iceland": (64.963051, -19.020835),
    "Italy": (41.87194, 12.56738),
    "Jersey": (49.214439, -2.13125),
    "Jamaica": (18.109581, -77.297508),
    "Jordan": (30.585164, 36.238414),
    "Japan": (36.204824, 138.252924),
    "Kenya": (-0.023559, 37.906193),
    "Kyrgyzstan": (41.20438, 74.766098),
    "Cambodia": (12.565679, 104.990963),
    "Kiribati": (-3.370417, -168.734039),
    "Comoros": (-11.875001, 43.872219),
    "Saint Kitts and Nevis": (17.357822, -62.782998),
    "North Korea": (40.339852, 127.510093),
    "South Korea": (35.907757, 127.766922),
    "Kuwait": (29.31166, 47.481766),
    "Cayman Islands": (19.513469, -80.566956),
    "Kazakhstan": (48.019573, 66.923684),
    "Laos": (19.85627, 102.495496),
    "Lebanon": (33.854721, 35.862285),
    "Saint Lucia": (13.909444, -60.978893),
    "Liechtenstein": (47.166, 9.555373),
    "Sri Lanka": (7.873054, 80.771797),
    "Liberia": (6.428055, -9.429499),
    "Lesotho": (-29.609988, 28.233608),
    "Lithuania": (55.169438, 23.881275),
    "Luxembourg": (49.815273, 6.129583),
    "Latvia": (56.879635, 24.603189),
    "Libya": (26.3351, 17.228331),
    "Morocco": (31.791702, -7.09262),
    "Monaco": (43.750298, 7.412841),
    "Moldova": (47.411631, 28.369885),
    "Montenegro": (42.708678, 19.37439),
    "Madagascar": (-18.766947, 46.869107),
    "Marshall Islands": (7.131474, 171.184478),
    "Macedonia [FYROM]": (41.608635, 21.745275),
    "Mali": (17.570692, -3.996166),
    "Myanmar [Burma]": (21.913965, 95.956223),
    "Mongolia": (46.862496, 103.846656),
    "Macau": (22.198745, 113.543873),
    "Northern Mariana Islands": (17.33083, 145.38469),
    "Martinique": (14.641528, -61.024174),
    "Mauritania": (21.00789, -10.940835),
    "Montserrat": (16.742498, -62.187366),
    "Malta": (35.937496, 14.375416),
    "Mauritius": (-20.348404, 57.552152),
    "Maldives": (3.202778, 73.22068),
    "Malawi": (-13.254308, 34.301525),
    "Mexico": (23.634501, -102.552784),
    "Malaysia": (4.210484, 101.975766),
    "Mozambique": (-18.665695, 35.529562),
    "Namibia": (-22.95764, 18.49041),
    "New Caledonia": (-20.904305, 165.618042),
    "Niger": (17.607789, 8.081666),
    "Norfolk Island": (-29.040835, 167.954712),
    "Nigeria": (9.081999, 8.675277),
    "Nicaragua": (12.865416, -85.207229),
    "Netherlands": (52.132633, 5.291266),
    "Norway": (60.472024, 8.468946),
    "Nepal": (28.394857, 84.124008),
    "Nauru": (-0.522778, 166.931503),
    "Niue": (-19.054445, -169.867233),
    "New Zealand": (-40.900557, 174.885971),
    "Oman": (21.512583, 55.923255),
    "Panama": (8.537981, -80.782127),
    "Peru": (-9.189967, -75.015152),
    "French Polynesia": (-17.679742, -149.406843),
    "Papua New Guinea": (-6.314993, 143.95555),
    "Philippines": (12.879721, 121.774017),
    "Pakistan": (30.375321, 69.345116),
    "Poland": (51.919438, 19.145136),
    "Saint Pierre and Miquelon": (46.941936, -56.27111),
    "Pitcairn Islands": (-24.703615, -127.439308),
    "Puerto Rico": (18.220833, -66.590149),
    "Palestinian Territories": (31.952162, 35.233154),
    "Portugal": (39.399872, -8.224454),
    "Palau": (7.51498, 134.58252),
    "Paraguay": (-23.442503, -58.443832),
    "Qatar": (25.354826, 51.183884),
    "Réunion": (-21.115141, 55.536384),
    "Romania": (45.943161, 24.96676),
    "Serbia": (44.016521, 21.005859),
    "Russia": (61.52401, 105.318756),
    "Rwanda": (-1.940278, 29.873888),
    "Saudi Arabia": (23.885942, 45.079162),
    "Solomon Islands": (-9.64571, 160.156194),
    "Seychelles": (-4.679574, 55.491977),
    "Sudan": (12.862807, 30.217636),
    "Sweden": (60.128161, 18.643501),
    "Singapore": (1.352083, 103.819836),
    "Saint Helena": (-24.143474, -10.030696),
    "Slovenia": (46.151241, 14.995463),
    "Svalbard and Jan Mayen": (77.553604, 23.670272),
    "Slovakia": (48.669026, 19.699024),
    "Sierra Leone": (8.460555, -11.779889),
    "San Marino": (43.94236, 12.457777),
    "Senegal": (14.497401, -14.452362),
    "Somalia": (5.152149, 46.199616),
    "Suriname": (3.919305, -56.027783),
    "São Tomé and Príncipe": (0.18636, 6.613081),
    "El Salvador": (13.794185, -88.89653),
    "Syria": (34.802075, 38.996815),
    "Swaziland": (-26.522503, 31.465866),
    "Turks and Caicos Islands": (21.694025, -71.797928),
    "Chad": (15.454166, 18.732207),
    "French Southern Territories": (-49.280366, 69.348557),
    "Togo": (8.619543, 0.824782),
    "Thailand": (15.870032, 100.992541),
    "Tajikistan": (38.861034, 71.276093),
    "Tokelau": (-8.967363, -171.855881),
    "Timor-Leste": (-8.874217, 125.727539),
    "Turkmenistan": (38.969719, 59.556278),
    "Tunisia": (33.886917, 9.537499),
    "Tonga": (-21.178986, -175.198242),
    "Turkey": (38.963745, 35.243322),
    "Trinidad and Tobago": (10.691803, -61.222503),
    "Tuvalu": (-7.109535, 177.64933),
    "Taiwan": (23.69781, 120.960515),
    "Tanzania": (-6.369028, 34.888822),
    "Ukraine": (48.379433, 31.16558),
    "Uganda": (1.373333, 32.290275),
    "United States": (37.09024, -95.712891),
    "Uruguay": (-32.522779, -55.765835),
    "Uzbekistan": (41.377491, 64.585262),
    "Vatican City": (41.902916, 12.453389),
    "Saint Vincent and the Grenadines": (12.984305, -61.287228),
    "Venezuela": (6.42375, -66.58973),
    "British Virgin Islands": (18.420695,  -64.639968),
    "U.S. Virgin Islands": (18.335765, -64.896335),
    "Vietnam": (14.058324, 108.277199),
    "Vanuatu": (-15.376706, 166.959158),
    "Wallis and Futuna": (-13.768752, -177.156097),
    "Samoa": (-13.759029, -172.104629),
    "Kosovo": (42.602636, 20.902977),
    "Yemen": (15.552727, 48.516388),
    "Mayotte": (-12.8275, 45.166244),
    "South Africa": (-30.559482, 22.937506),
    "Zimbabwe": (-22.328474, 24.684866),
    "Zambia": (-13.133897, 27.849332)}


def get_relationship(directory):
    '''
    A function to build a table based on retweets

    directory: the directory with all the tweets in it

    Return: a dictionary with Tweet ID's for keys that map to a tuple of the
    form (username, relationship)

    relationship is an integer (1-2). 1 = author, 2 = retweeter
    '''

    rel = dict()  # the dictionary to return

    # Get all the tweets in the directory
    tweets = get_tweets(directory)

    for tweet in tweets:
        try:
            # treat it first like a retweet

            # get the screen name of the retweeter
            screen_name = tweet["user"]["screen_name"]

            # get the ID of the original tweet
            original = tweet["retweeted_status"]["id_str"]

            if original not in rel.keys():
                # add the original tweet to the dictionary
                add_tweet(rel, tweet["retweeted_status"])

            # add the retweet information
            data = (screen_name, 2)
            rel[original].append(data)

        except KeyError:
            # not a retweet because the retweeted status has not been found!

            # add the tweet to the relationship dictionary
            add_tweet(rel, tweet)

    return rel


def add_tweet(rel, tweet):
    '''
    A function to add a tweet to the relationship dictionary

    rel: the relationship dictionary
    tweet: the tweet to add
    '''
    rel[tweet["id_str"]] = list()
    data = (tweet["user"]["screen_name"], 1)
    rel[tweet["id_str"]].append(data)


def consolidate(directory, key, outfile=None):
    '''
    A function to consolidate all the values in all the tweets in a given
    directory and save that data to a new file

    If no output file is specified, it will print to the screen

    directory: directory to run in
    key: the field to get the value from
    outfile: output file
    '''

    # get all the tweets from directory
    tweets = get_tweets(directory)
    # get all the values from the tweets
    values = get_values(tweets, key)

    # output values
    if outfile is None:
        for v in values:
            print(v)
    else:
        # Create the out file
        out = open(outfile, 'w', encoding="utf8")
        # write the values returned after converting each value to a string
        out.writelines([str(v) + "\n" for v in values])

        out.close()


def get_sentiment(tweets):
    '''
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
    text = ""
    sc = afinn.score(tweet)

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
        y, x = COUNTRY_COORDINATES[country]
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
                            ls.append(tweet[key])
                    else:
                        # the tweet isn't English. Filter it!
                        num_filtered += 1
    except:
        pass
    return(ls, num_filtered)


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
    else:
        print("I didin't understand what method you are calling."
                + "Please enter 'con', 'loc' or 'sent'")
