'''
usergraph.py
Last Modified: 6/19/2018
A module to build a table based on retweets

Author: Karsten Ladner
Date: 6/1/2018
'''
import sys
import pickle
import random_color

import networkx as nx

import plotly.graph_objs as go
import plotly

from tweets import get_tweets, add_positions
import new_grapher as grapher

'''
AT THE MOMENT I HAVE CONSTRUCTED A TWEET-RETWEET GRAPH. EVERY NODE IS A USER
AND EVERY EDGE SIGNIFIES A LEVEL 1 USER RELATIONSHIP

'''

COLORS = list([
        (255, 255, 255),
        (0, 0, 143),
        (182, 0, 0),
        (0, 140, 0),
        (195, 79, 255),
        (1, 165, 202),
        (236, 157, 0),
        (118, 255, 0),
        (89, 83, 84),
        (255, 117, 152),
        (148, 0, 115),
        (0, 243, 204),
        (72, 83, 255),
        (166, 161, 154),
        (0, 67, 1),
        (237, 183, 255),
        (138, 104, 0),
        (97, 0, 163),
        (92, 0, 17),
        (255, 245, 133),
        (0, 123, 105),
        (146, 184, 83),
        (171, 212, 255),
        (126, 121, 163),
        (255, 84, 1),
        (10, 87, 125),
        (168, 97, 92),
        (231, 0, 185),
        (255, 195, 166),
        (91, 53, 0),
        (0, 180, 133),
        (126, 158, 255),
        (231, 2, 92),
        (184, 216, 183),
        (192, 130, 183),
        (111, 137, 91),
        (138, 72, 162),
        (91, 50, 90),
        (220, 138, 103),
        (79, 92, 44),
        (0, 225, 115),
        (255, 104, 255),
        (126, 193, 193),
        (120, 58, 61),
        (183, 252, 255),
        (136, 9, 255),
        (111, 140, 144),
        (172, 168, 204),
        (148, 67, 5),
        (0, 80, 74),
        (1, 0, 250),
        (86, 81, 148),
        (202, 216, 0),
        (9, 123, 192),
        (176, 255, 155),
        (173, 147, 75),
        (196, 104, 0),
        (218, 203, 215),
        (0, 186, 0),
        (173, 82, 137),
        (131, 119, 114),
        (156, 0, 59),
        (144, 110, 254),
        (213, 195, 115),
        (254, 172, 203),
        (0, 233, 255),
        (193, 146, 255),
        (130, 142, 0),
        (100, 0, 65),
        (87, 104, 120),
        (125, 94, 120),
        (0, 113, 52),
        (122, 90, 59),
        (53, 46, 119),
        (209, 72, 57),
        (87, 0, 227),
        (138, 178, 143),
        (190, 0, 205),
        (130, 23, 0),
        (244, 234, 193),
        (15, 131, 149),
        (255, 201, 23),
        (184, 134, 140),
        (72, 198, 255),
        (89, 109, 95),
        (194, 0, 118),
        (253, 255, 0),
        (67, 72, 95),
        (123, 153, 189),
        (117, 0, 132),
        (88, 114, 2),
        (78, 163, 79),
        (195, 175, 0),
        (9, 162, 157),
        (189, 212, 217),
        (171, 255, 214),
        (126, 210, 0),
        (209, 90, 119),
        (255, 0, 34),
        (255, 92, 194),
        (161, 114, 68),
        (73, 128, 255),
        (160, 109, 188),
        (215, 209, 255),
        (163, 59, 54),
        (200, 165, 188),
        (255, 132, 43),
        (155, 141, 160),
        (203, 191, 166),
        (208, 90, 206),
        (5, 86, 184),
        (254, 92, 89),
        (116, 212, 162),
        (104, 107, 196),
        (132, 63, 102),
        (0, 161, 252),
        (9, 147, 99),
        (239, 148, 221),
        (30, 85, 50),
        (182, 217, 117),
        (168, 0, 239),
        (254, 171, 99),
        (255, 159, 150),
        (151, 169, 178),
        (255, 22, 149),
        (0, 103, 112),
        (151, 142, 212),
        (105, 80, 0),
        (82, 255, 170),
        (170, 184, 255),
        (60, 67, 0),
        (85, 72, 45),
        (47, 91, 0),
        (80, 0, 108),
        (255, 216, 255),
        (99, 37, 17),
        (0, 59, 113),
        (210, 163, 152),
        (99, 155, 132),
        (0, 206, 180),
        (103, 75, 122),
        (151, 224, 209),
        (160, 114, 143),
        (135, 89, 202),
        (220, 255, 199),
        (224, 236, 255),
        (94, 126, 161),
        (173, 174, 123),
        (148, 141, 110),
        (114, 111, 62),
        (133, 2, 190),
        (195, 252, 83),
        (255, 226, 223),
        (66, 85, 88),
        (213, 242, 229),
        (0, 195, 215),
        (220, 140, 170),
        (165, 57, 93),
        (193, 9, 57),
        (130, 87, 89),
        (51, 0, 187),
        (188, 72, 0),
        (199, 106, 71),
        (154, 0, 162),
        (68, 101, 151),
        (198, 133, 0),
        (141, 183, 217),
        (172, 188, 179),
        (208, 164, 110),
        (209, 101, 164),
        (201, 158, 218),
        (96, 193, 112),
        (119, 25, 52),
        (251, 0, 244),
        (116, 169, 5),
        (80, 51, 113),
        (69, 133, 62),
        (103, 70, 86),
        (211, 126, 233),
        (132, 235, 100),
        (180, 36, 152),
        (139, 156, 81),
        (119, 122, 133),
        (89, 255, 249),
        (152, 222, 239),
        (255, 217, 138),
        (118, 64, 33),
        (220, 121, 124),
        (106, 166, 178),
        (67, 82, 65),
        (112, 135, 206),
        (107, 57, 181),
        (159, 130, 4),
        (103, 98, 134),
        (216, 217, 208),
        (78, 119, 120),
        (181, 136, 107),
        (171, 82, 173),
        (183, 179, 187),
        (202, 178, 254),
        (118, 81, 253),
        (185, 195, 220),
        (65, 0, 126),
        (48, 99, 84),
        (57, 64, 161),
        (250, 75, 121),
        (120, 134, 121),
        (160, 93, 13),
        (217, 27, 0),
        (255, 125, 90),
        (0, 234, 41),
        (100, 44, 67),
        (152, 200, 135),
        (122, 56, 124),
        (234, 187, 191),
        (224, 216, 92),
        (146, 80, 58),
        (219, 227, 153),
        (82, 131, 105),
        (213, 62, 140),
        (1, 111, 148),
        (206, 185, 221),
        (131, 99, 152),
        (219, 6, 251),
        (94, 2, 91),
        (75, 113, 70),
        (171, 118, 235),
        (137, 157, 149),
        (72, 145, 198),
        (166, 191, 0),
        (0, 75, 91),
        (90, 75, 202),
        (159, 232, 169),
        (166, 136, 188),
        (221, 144, 65),
        (96, 94, 72),
        (116, 35, 94),
        (139, 131, 66),
        (91, 178, 161),
        (204, 166, 67),
        (105, 73, 64),
        (109, 102, 109),
        (122, 182, 254),
        (165, 156, 36),
        (191, 66, 83),
        (34, 115, 0),
        (227, 109, 39),
        (70, 225, 217),
        (155, 85, 107),
        (155, 0, 24)
    ])

def build_graph(directory):
    '''
    A function to build a table based on retweets

    directory: the directory with all the tweets in it

    Return: a dictionary with Tweet ID's for keys that map to a tuple of the
    form (username, relationship)

    relationship is an integer (1-2). 1 = author, 2 = retweeter
    '''

    g = nx.DiGraph()  # the one graph to rule them all

    # Get all the tweets in the directory
    raw_tweets = get_tweets(directory)
    # Append location data to tweets
    tweets = add_positions(raw_tweets)

    # Add all the users as nodes with the position data from the first tweet
    # of theirs that is discovered
    userlocs = list()
    for tweet in tweets:
        username = tweet["user"]["screen_name"]
        if username not in userlocs:
            userlocs.append(username)
            g.add_node(username, pos=tweet["position"])

    for tweet in tweets:
        try:
            # treat if first like a retweet
            head = tweet["retweeted_status"]["user"]["screen_name"]
            tail = tweet["user"]["screen_name"]
            g.add_edge(head, tail)
            g.edges[head, tail]['tweet'] = tweet["retweeted_status"]
        except KeyError:
            # it's not a retweet, so don't add any edges
            pass
    return g


def save_graph(graph, outfile):
    '''
    A method to save a graph to an outfile

    outfile: file to save graph to
    '''

    out = open(outfile, 'wb')
    pickle.dump(graph, out)
    out.close()


def load_graph(infile):
    '''
    A method to load a graph from an infile

    infile: the file where a graph object has been saved

    Return: a graph
    '''

    fin = open(infile, 'rb')
    g = pickle.load(fin)
    fin.close()
    return g


def display_graph(graph):
    node_trace = go.Scattergeo(
                locationmode="country names",
                lat=[],
                lon=[],
                text=[],
                hovertext=[],
                mode='marker',
                hoverinfo='text',
                marker=dict(
                    showscale=True,
                    # colorscale options
                    # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
                    # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
                    # colorscale='YIGnBu',
                    # reversescale=True,
                    color=[],
                    size=10,
                    opacity=0.5,
                    colorbar=dict(
                        thickness=15,
                        title='Node Connections',
                        xanchor='left',
                        titleside='right'
                        )
                    )
            )

    for node in graph.nodes():
        x, y = graph.node[node]['pos']['coordinates']
        node_trace['lon'] += [x, None]
        node_trace['lat'] += [y, None]
        node_trace['hovertext'] += node
        node_trace['marker']['color'] = 'red'

    e = dict()
    color_num = 0
    for edge in graph.edges():
        i_d = edge['tweet']['id_str']
        if e.get(i_d) is None:
            e[i_d] = go.Scattergeo(
                        locationmode="country names",
                        lat=[],
                        lon=[],
                        text=[],
                        hovertext=[],
                        mode='lines+marker',
                        hoverinfo='text',
                        marker=dict(
                            size=10,
                            opacity=0
                            ),
                        line=dict(
                            size=0.2,
                            opacity=0.3,
                            color=COLORS[color_num]
                            )
                        )
            if color_num < len(COLORS):
                color_num += 1
            else:
                COLORS.append(random_color.random_color())
                color_num += 1

        x0, y0 = graph.node[edge[0]]['pos']
        x1, y1 = graph.node[edge[1]]['pos']
        e[i_d]['lat'] += [x0, x1, None]
        e[i_d]['lon'] += [y0, y1, None]
        e[i_d]['hovertext'].append(edge['tweet']['text'])

    traces = [tr for tr in e.values()]
    traces.append(node_trace)

    fig = go.Figure(data=traces, layout=go.Layout(dict(
                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                geo=dict(
                    scope="world",
                    showframe=False,
                    showcoastlines=True,
                    projection=dict(
                        type="natural earth"
                        )
                    ),
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[dict(
                    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002)],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))))

    plotly.offline.plot(fig, filename='d3-world-map')


def user_graph(directory):
    '''
    A function to build a graph based on retweets. Every vertex is a
    different tweet and every edge connects a tweet with a retweet.

    directory: the directory with all the tweets in it

    Returns: a graph of the tweet-retweet relationship
    '''

    g = grapher.Graph()  # the dictionary to return

    # Get all the tweets in the directory
    tweets = get_tweets(directory)

    print("Retrieved all tweets in {0}".format(directory))  # Log
    print("Number of tweets: {0}".format(len(tweets)))  # Log

    for tweet in tweets:
        t_user = tweet["user"]["screen_name"]
        if tweet.get("retweeted_status") is None:
            g.addVertex(t_user)
        else:
            o_user = tweet["retweeted_status"]["user"]["screen_name"]
            head = g.getVertex(o_user)
            tail = g.getVertex(t_user)
            # Case 1: Neither User exists in the graph
            if head is None or tail is None:
                # Make a new edge and two new users
                g.addEdge(
                        o_user,
                        t_user,
                        cost=1
                        )
            # Case 2: An edge already exists between both users
            elif tail in head.getConnections():
                # increase the weight of the edge
                g.modifyWeight(head, tail, 1)
            # Remaining cases (both users exist but there's no link)
            else:
                # Make a new edge
                g.addEdge(
                        o_user,
                        t_user,
                        cost=1
                        )

    print("Finished constructing graph")  # Log

    return g


def get_unique_users(graph):
    '''
    A method to get a list of all the unique users in the graph

    Returns: a sorted list of all the unique users
    '''
    users = set()  # the list to return

    # Find all the unique users
    users = set(graph.getVertices())

    print("Retrieved all users. Number of Users: {0}".format(
        len(users)))  # Log

    return(sorted(users))


def fill_matrix(graph):
    '''
    A function to fill a 2d matrix with the user graph information. 
    There is one row for each unique tweet and there is one column for 
    each unique user. A one in a cell indicates that a given user
    retweeted the tweet on that row

    graph: the graph of tweet-retweets

    Returns: a four-part tuple (matrix, users, tweets_nums, users_nums)
    1. matrix: a 2-D matrix of tweet-retweets
    2. users: a sorted list of unique users
    3. tweets_nums: a dictionary of tweet_id-row_num
    4. users_nums: a dictionary of user_names-col_num

    '''

    matrix = list()  # Store the matrix data in a list
    users = sorted(list(graph.getVertices()))  # list of all the unique users
    users_length = len(users)

    print("Number of users: {0}".format(users_length))  # Log

    # get row-column information
    # user_indices maps a username to a unique column number
    # tweet_indices maps a tweet id to a unique row number
    user_indices = dict(zip(users, range(users_length)))

    print("Finished constructing user indices")  # Log

    # Fill the matrix with 0's
    empty_data = [0] * users_length
    matrix = [list(empty_data) for i in range(0, users_length)]

    print("Matrix filled with 0's")  # Log

    for user in graph:
        for neighbor in user.getConnections():
            matrix[user_indices[neighbor.getId()]][
                    user_indices[user.getId()]] = user.getWeight(neighbor)

    print("Matrix constructed")  # Log

    return (matrix, users, user_indices)


def print_user_graph(graph):
    '''
    A function to print the user graph/matrix. Each row is a different
    tweet and each column is a different user. A 1 indicates that the user
    in that column retweeted the tweet in that row

    graph: the graph to print the user matrix of
    '''

    # Create the matrix
    matrix, users, user_indices = fill_matrix(graph)

    # Print everything in the matrix out

    # print a space before the first value of the first row
    print(" " * 5, end="")

    # print the first row (which is all the usernames)
    # get the list of users and sort the keys alphabetically
    for name in users:
        # fancy print all the screen_names of the users
        # truncate the name to 10 characters and right align at 15 chars
        print("{0:>15.10}".format(name), end="")

    for name in users:
        # fancy print the screen_name of the user who tweeted
        # truncate it at 10 characters and right align it at 10 chars
        print("\n{0:>10.10}".format(name), end=" " * 5)
        for value in matrix[user_indices[name]]:
            # fancy print every value in the list associated with this
            print("{0:<15}".format(value), end="")


def save_matrix(graph, fil):
    fout = open(fil, 'w')
    m, u, u_i = fill_matrix(graph)
    for row in m:
        out = ""
        for col in row:
            out += str(col) + "\t"
        out.rstrip("\t")
        out += "\n"
        fout.write(out)
    fout.close()


if __name__ == '__main__':
    if sys.argv[1] == "save":
        g = build_graph(sys.argv[2])
        parts = sys.argv[2].strip(".").split("/")
        fileparts = [
                p + "-" for p in parts[1:] if p is not "crisis"]
        filename = "".join(fileparts) + "data"
        save_graph(g, filename)
    elif sys.argv[1] == "show":
        g = load_graph(sys.argv[2])
        display_graph(g)
    elif sys.argv[1] == "print":
        g = user_graph(sys.argv[2])
        print_user_graph(g)
    elif sys.argv[1] == "mout":
        g = user_graph(sys.argv[2])
        save_matrix(g, sys.argv[3])
    else:
        g = build_graph("./data/25crisis")
        print("Please enter either 'save','show', or 'print'")
