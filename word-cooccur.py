'''
Word Coocurrence
Modified by Karsten Ladner
Date: 7/10/2018

Author: Ruchishya
'''

import os.path
from os.path import join as jn
import re
import sys
from nltk.corpus import stopwords
import collections

from tweets import load_values_from_file as load
from tweets import save_to_file as save

from constants import OUT, PROC


fout = jn(PROC, sys.argv[2])
key = sys.argv[1]
sw = set(stopwords.words('english'))
punctuation = re.compile(r'[\[?!"💀#*;+()@|0-9|\]]')
anchor_list = ["syria", "syrian", "refugee", "refugees", "assad", "isis"]

out = {
        "syria": [],
        "syrian": [],
        "refugee": [],
        "refugees": [],
        "assad": [],
        "isis": []
        }
words = {
        "syria": [],
        "syrian": [],
        "refugee": [],
        "refugees": [],
        "assad": [],
        "isis": []
        }

index = ['' for y in range(10)]
newindex = [[]for y in range(10)]
k = 0
wordcount = {}
word_list = []
index = set()
wordlist = []
t_data = list()

fins = [load(jn(PROC, f)) for f in os.listdir(PROC) if key in f]

tweets = list()
num_filtered = 0
for f in fins:
    tweets.extend(f['data'])
    # num_filtered += f['num_filtered']

for t in tweets:
    # print(t)
    clean_words = list()
    keywords = set()
    for huge in t.split():
        for word in huge.split("\'"):
            word = word.lower()
            word = word.replace(".", "")
            word = word.rstrip("…")
            word = punctuation.sub("", word)
            word = word.strip()
            if (len(word.split()) > 1):
                for i in range(0, len(word.split())):
                    if word[i] not in wordcount:
                        if word[i] in sw:
                            u = 0
                        else:
                            if (len(word[i]) > 26 or len(word[i])
                                    < 3 or word[i].startswith("https")):
                                l = 0
                            elif ("/" not in word and word.isalpha()):
                                index.add(word[i])  # no duplicates
                                clean_words.append(word[i])
                                if word[i] in anchor_list:
                                    keywords.add(word[i])

                    else:
                        if word[i] in sw:
                            u = 0
                        else:
                            if (len(word[i]) > 26 or len(word[i])
                                    < 3 or word[i].startswith("https")):
                                l = 0
                            elif ("/" not in word and word.isalpha()):
                                index.add(word[i])  # no duplicates
                                clean_words.append(word[i])
                                if word[i] in anchor_list:
                                    keywords.add(word[i])
            else:
                if word not in wordcount:
                    if word in sw:
                        u = 0
                    else:
                        if (len(word) > 26 or len(word) <
                                4 or word.startswith("https")):
                            l = 0
                        elif ("/" not in word and word.isalpha()):
                            index.add(word)  # no duplicates
                            clean_words.append(word)
                            if word in anchor_list:
                                keywords.add(word)
                else:
                    if word in sw:
                        u = 0
                    else:
                        if (len(word) > 26 or len(word) <
                                3 or word.startswith("https")):
                            l = 0
                        elif ("/" not in word and word.isalpha()):
                            index.add(word)  # no duplicates
                            clean_words.append(word[i])
                            if word in anchor_list:
                                keywords.add(word)

    for keyword in keywords:
        words[keyword].extend(clean_words)

print("Finished building list of clean words")

for keyword in anchor_list:
    out[keyword] = collections.Counter(words[keyword])

print("Finished counting frequencies")

# data for filtered 
#data = {
        #'data': out,
        #'num_filtered': num_filtered
        #}

data = {
        'data': out,
        }
save(data, fout)

for key in out:
    print(key)
    for w, v in sorted(out[key].items(), key=lambda x: x[1], reverse=True)[:20]:
        print(w, v)
    print()
'''
print(len(index))
index = list(index)
# print(index)
newindex = [[[] for x in range(len(anchor_list))] for y in range(len(index))]
Matrix = [[0 for x in range(len(anchor_list))] for y in range(len(index))]

# Figure out which tweets are associated with each anchor word and sign. word
# then make a list that contains those related tweets
for keywords, cleanwords, t in t_data:
    # print("NEW TWEET")
    # print("keywords: {0}\ncleanwords: {1}".format(keywords, cleanwords))
    for cleanword in cleanwords:
        # print("Cleanword: {0}".format(cleanword))
        imp_word_index = index.index(cleanword)
        for keyword in keywords:
            # print(("Keyword: {0}".format(keyword)))
            newindex[imp_word_index][anchor_list.index(keyword)].append(t)

print("Finished indexing tweets")
for j in range(0, len(index)):
    for k in range(0, len(anchor_list)):
        temp = []
        for t in tweets:
            if index[j] in t and anchor_list[k] in t:
                    temp.append(t)
        newindex[j][k] = temp
for i in range(0, len(index)):
        # print(index[i], end="\t")
        # print(index[i], end="\t")
        for j in range(0, len(anchor_list)):
            # The number of tweets associated with each anchor word and sign. word
            # fills the matrix cell
            # Matrix[i][j] = len(newindex[i][j])
            dat = (index[i], len(newindex[i][j]))
            out[anchor_list[j]].append(dat)
            # print(Matrix[i][j], end="\t")
        # print()

for keyword in out:
    print(keyword)
    for v in sorted(out[keyword][:50], key=lambda x: x[1], reverse=True):
        print(v)
     for word, value in sorted(out[keyword][:21], key=lambda x: x[1]):
         if value != 0:
            print(word, value)
    print("\n\n")

print("cleanword: refugee")
for num, col in enumerate(newindex[index.index("refugee")]):
    print(anchor_list[num], len(col))
        if Matrix[i][3] > 1 \
                and Matrix[i][0] == 0 \
                and Matrix[i][1] == 0 \
                and Matrix[i][2] == 0 \
                and Matrix[i][4] == 0:
            print(index[i], Matrix[i][3])

        # print('%s' % Matrix[i][j], end="\t")
    # print("\n")
'''
