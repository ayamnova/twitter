'''
A python script to find the most frequent words appearing in a file

Author: Karsten Ladner
Date: 7/03/2018
'''

import collections
from nltk.corpus import stopwords 
from afinn import Afinn
import sys

from tweets import load_values_from_file as load
from tweets import save_to_file as save


file_in = "25text.out"
file_out = "wc-06.dat"

sw = set(stopwords.words('english'))
sw.add("rt")


def count_words(text):
    '''
    A method to count all the important words in a text file

    text: a list of of strings

    Returns: a dictionary with word-frequency pairs and the count of filtered
    words
    '''

    filtered = 0  # the number of filtered words
    ls = list()  # the list of words

    # read through every line in the list
    for line in txt:
        try:
            # split into words
            for word in line.split(" "):
                # clean the word
                word = word.strip().lower().rstrip("…")

                # check if it is a valid word
                if word not in sw \
                and "http" not in word \
                and "@" not in word \
                and word.isalpha() \
                and len(word) > 2:
                    # get rid of the hashtags
                    # because a split with a # will lead to returning ''
                    # must loop through every item returned
                    for w in word.split("#\"'"):
                        if w is not '':
                            ls.append(w)
                else:
                    filtered += 1
        except:
            continue

    # Count the words
    count = collections.Counter(ls)

    return(count, filtered)


def save_count(count, num_filtered, fout):
    '''
    A method to put together the dictionary to be pickled using the 
    save_to_file method from tweets

    count: a counter dictionary
    num_filtered: the number of filtered words
    '''

    data = dict()  # the object to be pickled

    data["data"] = count
    data["num_filtered"] = num_filtered

    save(data, fout)


def load_count(fin):
    '''
    A method to load a word count dat file
    '''
    wc = load(fin)
    return wc


def top(count, num):
    '''
    A method to print the most common words along with their frequencies and
    sentimentality scores using the afinn package

    count: a counter dictionary
    num: the number of words to print
    '''

    afinn = Afinn()
    for w, c in count.most_common(num):
        sc = afinn.score(w)
        print("{0}\t{1}\t{2}".format(w, c, sc))


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'save':
        txt = load(sys.argv[2])
        (count, filt) = count_words(txt)
        save_count(count, filt, sys.argv[3])
        top(count, 20)
    elif action == 'load':
        wc = load_count(sys.argv[2])
        top(wc['data'], 20)
