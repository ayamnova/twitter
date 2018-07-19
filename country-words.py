import sys
import carmen
from afinn import Afinn
from os.path import join as jn
from tweets import get_tweets
from tweets import save_to_file as save 
from constants import PATH, OUT, PROC


if __name__ == '__main__':
    dirs = [d for d in sys.argv[1].split(',') if d is not ""]
    fout = sys.argv[2]
    d = {
            "United States": [],
            "United Kingdom": [],
            "India": [],
            "France": []
            }
    tw, filt = get_tweets(dirs, prefix=PATH)

    # initialize the location engine
    r = carmen.get_resolver()
    r.load_locations()

    # look through every tweet and see if it's in a country of interest
    for t in tw:
        try:
            # try to find a location
            loc = r.resolve_tweet(t)[1]
            country = loc.country
            # if it's a country of interest append it's text to the country's
            # tweet list
            if country in d:
                if t.get("extended_tweet") is None:
                    d[country].append(t["text"])
                else:
                    d[country].append(t["extended_tweet"]["full_text"])
        except TypeError:
            continue
    # save each country into a separate file
    for c in d:
        save({'data': d[c]}, jn(PROC, c + "-" + fout + ".dat"))

