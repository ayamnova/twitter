'''
User matrix
A script to build a matrix of the adjacencies between users

Modified by: Karsten Ladner
Date: 6/27/2018

Author: Ruchishya R.
Date: 6/26/2018
'''

import os
import sys
from os.path import join
import json
import pickle

path = "./crisis/crisis/2018/"
wordlist = []
users = set()

def save_users_to_file(dirs, fout):

    # Build the list of files
    files = list()
    for d in dirs:
        for dirp, dirn, fils in os.walk(d):
            files.extend([join(dirp, f) for f in fils])

    # Print the number of files
    length = len(files)
    print(length, dirs)

    # Read through every file and record the connections b/n retweeters and tweeters
    # Every element in wordlist looks like: username/tweet/username
    # (if it is not a reweet the second username will be N/A)
    wordlist = list()
    counter = 0
    for current in files:
        if counter % 10000 == 0:
            print("10,000 Completed")
        with open(current, "r") as f:
            for line in f:
                try:
                    parsed_json_tweets = json.loads(line)
                    if (parsed_json_tweets['lang'] == "en"):
                        username = parsed_json_tweets['user']['screen_name'].lstrip().strip()
                        tweet_text = parsed_json_tweets['text'].lstrip().strip()
                        users.add(username)
                        if 'retweeted_status' in parsed_json_tweets:
                            ownerName = parsed_json_tweets['retweeted_status']['user'][
                                'screen_name'].lstrip().strip()
                            users.add(ownerName)
                        else:
                            ownerName ="N/A"
                        wordlist.append(username+" ,/ "+tweet_text+" ,/ "+ownerName + "\n")
                except:
                    continue
        f.close()
        counter += 1
    out = open(fout, 'wb')
    pickle.dump(wordlist, out)
    out.close()

def build_matrix_from_file(fil, outfile):
    fin = open(fil, 'rb')
    wordlist = pickle.load(fin)
    fin.close()

    # Find the set of users
    userslist = set()
    userlist1 = set()
    for row in wordlist:
        lines = row.split(" ,/ ")
        if lines[2] != "N/A":
            userslist.add(lines[0])
            userlist1.add(lines[2])

    # Build the matrix
    userslist = list(userslist)
    userslist1 = list(userlist1)
    print(len(userslist), len(userlist1))
    Matrix = [[0 for x in range(len(userslist))] for y in range(len(userlist1))]

    # Print the number of users
    print(len(userslist))

    #
    for row in wordlist:
        lines = row.split(" ,/ ")
        if lines[2] != "N/A":
            j = userslist.index(lines[0])
            k = userlist1.index(lines[2])
            Matrix[j][k] += 1

    out = open(outfile, "w")
    for i in range(0,len(userslist)):
        for j in range(0,len(userlist1)): 
            out.write('%s'%Matrix[i][j])
            out.write("\t")
        out.write("\n")
    out.close()


if __name__ == '__main__':
     # outfile = sys.argv[2]
     # dirs = [join(path, d) for d in sys.argv[1].split(',')]
     # save_users_to_file(dirs, outfile)
     build_matrix_from_file("usermatrix-usernames-6_11-6_17.txt", sys.argv[1])
