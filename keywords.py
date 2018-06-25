'''
Keywords
A script to determine what words are associated with each keyword and find the
union of those sets


Author: Karsten Ladner
Written: 6/25/2018
'''

from tweets import get_tweets


d = "./data/25crisis"

keywords = {
        "refugee": set(),
        "syria": set(),
        "syrian": set(),
        "assad": set(),
        "chemical attack": set(),
        "isis": set(),
        "isil": set()
        }

processed = list()
for t in get_tweets(d):
    txt = ""
    try:
        txt = t[""]

