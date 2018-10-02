'''
WCloud
A script to create a wordcloud from a save list of frequencies using the
wordcloud package

Author: Karsten Ladner
Date: 7/12/2018
'''

import sys
from os import mkdir
from PIL import Image
import numpy as np
from os.path import join as jn
import wordcloud
from tweets import load_values_from_file as load
from config import PROC, OUT

keys = ["chemical", "isis", "isil", "assad", "syria", "syrian", "refugee"]

if "wcd" in sys.argv[1]:
    d = sys.argv[1].strip(".dat")
elif "wc" in sys.argv[1]:
    d = "clouds"
elif "tx-" in sys.argv[1]:
    d = sys.argv[1].strip(".dat")
else:
    d = sys.argv[1].strip(".dat")

try:
    mkdir(jn(OUT, d))
except FileExistsError:
    pass

freq = load(jn(PROC, sys.argv[1]))
for k in keys:
    del freq['data'][k]

# sten = np.array(Image.open(jn(PROC, 'fleeing.png')))
wc = wordcloud.WordCloud(
        height=400,
        width=800,
        scale=1.0,
        max_words=250,
        background_color="white",
        )
wc.generate_from_frequencies(freq['data'])
wc.to_file(jn(OUT, d + "/", sys.argv[1].strip(".dat") + '.png'))

'''
for keyword, counts in freq['data'].items():
    wc = wordcloud.WordCloud(
            height=400,
            width=800,
            scale=1.0,
            max_words=250,
            background_color="white",
            )
# mask=sten
    wc.generate_from_frequencies(counts)
    wc.to_file(jn(OUT, d + "/", keyword + '.png'))
'''
