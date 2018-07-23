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
from constants import PROC, OUT

if "wc" in sys.argv[1]:
    d = "clouds"
else:
    d = sys.argv[1].strip(".dat")

try:
    mkdir(jn(OUT, d))
except FileExistsError:
    pass

freq = load(jn(PROC, sys.argv[1]))

sten = np.array(Image.open(jn(PROC, 'fleeing.png')))

for keyword, counts in freq['data'].items():
    wc = wordcloud.WordCloud(
            height=1000,
            width=1000,
            scale=1.0,
            max_words=250,
            background_color="white",
            mask=sten
            )
    wc.generate_from_frequencies(counts)
    wc.to_file(jn(OUT, d + "/", keyword + '.png'))
