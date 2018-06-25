"""
Term Document Matrix

Author: Karsten Ladner
Date: 5/30/2018
"""

import sys
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from tweets import get_tweets
import re
import carmen


PUNCTUATION = re.compile(r"[#\.\|,\'?!:\‘\+\$()\[\]-_\"]|[0-9]|['][a-z]|[…]")
stopwords = set(stopwords.words("english"))
stopwords.add("rt")
stopwords.add("")
stopwords.add(" ")


def print_tdm(tdm, docs):
    print(" Count  Word", end="")
    for doc in docs:
        print("{0:^15.10}".format(doc), end="")
    # sort the tdm based on the total count for each word
    # the 1 index corresponds to the value of each key-value pair
    # the 0 index corresponds to the first item in each value list which is
    # the total count for that word
    sorted_dict = sorted(tdm.items(), key=lambda x: x[1][0], reverse=True)
    # the sorted_dict is a list of tuples and each tuple is a key, value pair
    for tup in sorted_dict:
        # print the total frequency
        print("\n{0:>5}".format(tup[1][0]), end="")
        # print the keys (words)
        print("{0:>10.10}".format(tup[0]), end=" " * 5)
        # print the values
        # from the value in the key-value pair, access the second element
        # and print every value in that list
        for value in tup[1][1]:
            print("{0:<15}".format(value), end="")


def fill_matrix(documents):
    '''
    Fill a Term Document Matrix with given documents

    documents: a dictionary, with each key being a separate document and each
        value being a string of all their tweets

    Returns a tuple with two dictionary with strings as keys to lists
    '''

    # A dictionary that holds all the frequency data
    # It is a dictionary with each word being a key to a list
    freq = dict()

    # store the number of documents to use later
    length = len(documents)
    # keep track of which document we are reading
    count = 0

    docs = sorted(documents.keys())

    for doc in docs:
        for word in documents[doc].split(" "):
            if word.isalnum():
                try:
                    freq[word][0] += 1
                    # update word frequency for given column
                    freq[word][1][count] += 1
                except KeyError:
                    # add new words to the dictionary
                    ls = [1]
                    ls.append(add_word(count, length))
                    freq[word] = ls
        count += 1

    return freq, docs


def add_word(count, length):
    '''
    A function to add a new word into the dictionary

    count: what document was being read when the word was discovered

    Returns a list with the length of the number of documents filled with 0's
    except for the index that corresponds to the document at which it was
    found
    '''

    ls = list()
    for i in range(length):
        if i == count:
            ls.append(1)
        else:
            ls.append(0)
    return ls


def build_documents_user(directory):
    '''
    A function to build the documents separated by user
    to get a TDM from a directory

    directory: a directory with Flume files
    '''

    documents = dict()

    raw_tweets = get_tweets(directory)

    for tweet in raw_tweets:
        text = clean_text(tweet["text"])
        try:
            documents[tweet["user"]["screen_name"]] += text
        except KeyError:
            documents[tweet["user"]["screen_name"]] = text

    return documents


def build_documents_country(directory):
    '''
    A function to build the documents separated by country
    to get a TDM from a directory

    directory: a directory with Flume files
    '''

    documents = dict()

    resolver = carmen.get_resolver()
    resolver.load_locations()

    raw_tweets = get_tweets(directory)

    for tweet in raw_tweets:
        country = str()
        try:
            country = resolver.resolve_tweet(tweet)[1].country
        except TypeError:
            continue

        text = clean_text(tweet["text"])
        try:
            documents[country] += text
        except KeyError:
            documents[country] = text

    return documents


def clean_text(text):
    """
    A function to clean input text

    text: input string

    Returns a string of important words separated by a space
    """
    out = str()  # output

    ps = PorterStemmer()

    # separate words at spaces
    for huge in text.split(" "):
        for word in huge.split("’"):
            if len(word) > 4 and word.find("https") == -1 \
                    and word.find("@") == -1 \
                    and word.find("&amp;") == -1 \
                    and word.find("\n") == -1:

                # remove punctuation
                word = PUNCTUATION.sub("", word)
                word.replace("…", "")
                word.replace("'s", "")
                # process each word
                word = word.lower()

                word = ps.stem(word)

                # only prcess important words
                if word not in stopwords:
                    out += word + " "
    return out


if __name__ == '__main__':
    docs = build_documents_user(sys.argv[1])
    # docs = build_documents_country(sys.argv[1])
    tdm = fill_matrix(docs)
    # print(tdm)
    print_tdm(tdm[0], tdm[1])
