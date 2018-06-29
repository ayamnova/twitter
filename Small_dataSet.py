import json
import re
from nltk.corpus import stopwords
import os
sw = set(stopwords.words('english'))
punctuation = re.compile(r'[\[?!"💀#*;+()@|0-9|\]]')
index = ['' for y in range(10)]
newindex = [[]for y in range(10)]
k = 0
wordcount = {}
word_list = []
index = set()
i = 0
wordlist = []
path = "./crisis/crisis/2018/06/10/03/"
length = 1
length = sum([len(files) for r, d, files in os.walk(path)])
print(length, path)
fil1 = [files for r, d, files in os.walk(path)]
for i in range(0, length):
with open(path + fil1[0][i],"r") as f:
#with open("C:\\Users\\ruchishya\\Desktop\\FlumeData.1524360165346", "r",encoding="utf8",errors="ignore") as f:
    for line in f:
        try:
            parsed_json_tweets = json.loads(line)
            if (parsed_json_tweets['lang'] == "en"):
                if('extended_tweet' in parsed_json_tweets):
                    wordlist.append(parsed_json_tweets['extended_tweet']['full_text'])
                    i=i+1
                else:
                    wordlist.append(parsed_json_tweets['text'])
                    i=i+1
        except:
            continue
print(len(wordlist))
for i in range(0,len(wordlist)):
            for huge in wordlist[i].split():
                for word in huge.split("\'"):
                    word = word.lower()
                    # word = word.strip("\n")
                    word = word.replace(".", "")
                    # print(word)
                    word = punctuation.sub("", word)
                    word = word.strip()
                    if (len(word.split()) > 1):
                        for i in range(0, len(word.split())):
                            if word[i] not in wordcount:
                                if word[i] in sw:
                                    u = 0
                                else:
                                    if (len(word[i]) > 26 or len(word[i]) < 3 or word[i].startswith("https")):
                                        l = 0
                                    elif ("/" not in word and word.isalpha() == True):
                                        index.add(word[i])  # no duplicates
                            else:
                                if word[i] in sw:
                                    u = 0
                                else:
                                    if (len(word[i]) > 26 or len(word[i]) < 3 or word[i].startswith("https")):
                                        l = 0
                                    elif ("/" not in word and word.isalpha() == True):
                                        index.add(word[i])  # no duplicates
                    else:
                        if word not in wordcount:
                            if word in sw:
                                u = 0
                            else:
                                if (len(word) > 26 or len(word) < 4 or word.startswith("https")):
                                    l = 0
                                elif ("/" not in word and word.isalpha() == True):
                                    index.add(word)  # no duplicates
                        else:
                            if word in sw:
                                u = 0
                            else:
                                if (len(word) > 26 or len(word) < 3 or word.startswith("https")):
                                    l = 0
                                elif ("/" not in word and word.isalpha() == True):
                                    index.add(word)  # no duplicates
index = list(index)
print(len(index))
# print(index)
anchor_list = ["syria","refugee", "assad", "isis", "chemical attack"]
newindex = [['' for x in range (len(anchor_list))] for y in range(len(index))]
Matrix = [[0 for x in range(len(anchor_list))] for y in range(len(index))]
for j in range(0, len(index)):
  for k in range(0, len(anchor_list)):
    temp = []
    for i in range(0, len(wordlist)):
        if (index[j] in wordlist[i]):
                if(anchor_list[k] in wordlist[i]):
                    temp.append(wordlist[i])
                newindex[j][k] = temp
for i in range(0, len(index)):
    # print(index[i], end="\t")
    for j in range(0, len(anchor_list)):
        Matrix[i][j] = len(newindex[i][j])
    if Matrix[i][3] > 3 \
            and Matrix[i][0] == 0 \
            and Matrix[i][1] == 0 \
            and Matrix[i][2] == 0 \
            and Matrix[i][4] == 0:

        print(index[i], Matrix[i][3])
        for tweet in newindex[i][3]:
            print(tweet)
        # print('%s' % Matrix[i][j], end="\t")
    # print("\n")
