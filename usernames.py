'''
Usernames
A script to save the usernames of the users for each day
'''

import sys
from tweets import get_tweets, save_to_file as save
from config import PATH


if __name__ == '__main__':
    dirs = sys.argv[1].split(',')
    for d in dirs:
        out = "./out/users-" + d.replace("/", "_") + ".dat"
        tweets = get_tweets([d], key='names', prefix=PATH)
        data = {
                'data': tweets[0],
                'num_filtered': tweets[1]
                }
        save(data, out)
