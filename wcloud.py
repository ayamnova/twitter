import wordcloud
from tweets import load_values_from_file as load

freq = load('./out/wc-06_01-07_10.dat')
wc = wordcloud.WordCloud()
wc.generate_from_frequencies(freq['data']['refugees'])
wc.to_file('test.png')
