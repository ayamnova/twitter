'''
WCloud
A script to create a wordcloud from a save list of frequencies using the
wordcloud package

Author: Karsten Ladner
Date: 7/12/2018
'''
import sys
from os.path import join as jn

import wordcloud

from tweets import load_values_from_file as load

from constants import PROC, OUT

freq = load(jn(PROC, sys.argv[1]))
for keyword, counts in freq['data'].items():
    wc = wordcloud.WordCloud(height=800, width=1600, scale=1.0, max_words=250)
    wc.generate_from_frequencies(counts)
    wc.to_file(jn(OUT, keyword + '.png'))
