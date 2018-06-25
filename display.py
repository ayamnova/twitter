"""
Display
A program to display data from a term document matrix as a bar chart

Author: Karsten Ladner
Date: 6/13/2018
"""

import sys
import tdm
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
from matplotlib.colors import cnames


def graph(matrix, names):
    """
    A method to graph a matrix

    matrix: a tdm
    names: a list of strings
    """
    clean_matrix = list()
    keywords = ["syria", "refuge", "assad"]
    sorted_keys = []
    colors = list(cnames.keys())
    bad_colors = ["aliceblue", "antiquewhite", "floralwhite", "hotpink",
            "ivory", "khaki", "lavenderblush", "lightblue", "lightcoral", "lightcyan",
            "lightgoldenrodyellow", "lightgreen", "lightgray", "lightpink",
            "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray",
            "lightyellow", "white", "whitesmoke", "peachpuff", "pink", "beige",
            "azure", "bisque", "silver", "lavender", "gainsboro", "honeydew",
            "linen", "powderblue", "snow", "blanchedalmond", "ghostwhite",
            "lemonchiffon", "papayawhip"]
    colors = [color for color in colors if color not in bad_colors]
    rectangles = list()

    for key in sorted(matrix.keys(), key=lambda x: x):
        if key in keywords:
            clean_matrix.append(matrix[key])
            sorted_keys.append(key)

    bars = list()
    for i in range(len(names)):
        values = [value[1][i] for value in clean_matrix]
        bars.append(values)

    N = len(bars[0])
    ind = np.arange(N)
    width = 1.0 / (len(bars) + 10)

    fig, ax = plt.subplots()
    ax.set_facecolor("lightblue")
    count = 0
    print(len(bars))
    for country in bars:
        print(country)
        rectangles.append(ax.bar(ind + width * count, country, width, alpha=1, color=colors[count], label=names[count]))
        count += 1
    for country in rectangles:
        for rect in country:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                    '%d' % int(height),
                    ha='center', va='bottom')
    ax.set_ylabel("Number of Tweets")
    ax.set_title("Number of Tweets in each country for each keyword")
    ax.set_xticks(ind + (len(bars))/2 * width)
    ax.set_xticklabels(sorted_keys)
    ax.legend()
    plt.show()


if __name__ == "__main__":
    docs = tdm.build_documents_country(sys.argv[1])
    t = tdm.fill_matrix(docs)
    graph(t[0], t[1])
