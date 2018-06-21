'''
Graphing.py
A simple program to grab json data from a tweet and plot it

Author: Karsten Ladner
Date: 5/25/2018
'''

import json
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

fin = open("tweets", 'r', encoding="utf8")

dat = dict()

for line in fin.readlines():
    clean = json.loads(line)
    dat[clean["user"]["screen_name"]] = clean["user"]["friends_count"]


for key in dat:
    print("Key: {0}, Value: {1}".format(key, dat[key]))

objects = dat.keys()
y_pos = np.arange(len(objects))

performance = list()
for key in dat.keys(): 
    performance.append(dat[key])
 
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Friends Count')
plt.title('Twitter users with lots of friends')
 
plt.show()

fin.close()
