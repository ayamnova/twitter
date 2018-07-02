'''
usergraph.py
Last Modified: 6/19/2018
A module to build a table based on retweets

Author: Karsten Ladner
Date: 6/1/2018
'''
import sys
from os.path import join as pjoin
import pickle

import networkx as nx

import plotly.graph_objs as go
import plotly

from tweets import get_tweets, add_positions
import new_grapher as grapher


PATH = "./crisis/crisis/2018/"


def build_graph(tweets):
    '''
    A function to build a table based on retweets

    directory: the directory with all the tweets in it

    Return: a dictionary with Tweet ID's for keys that map to a tuple of the
    form (username, relationship)

    relationship is an integer (1-2). 1 = author, 2 = retweeter
    '''

    g = nx.DiGraph()  # the one graph to rule them all

    # Append position information
    tweets = add_positions(tweets)

    for tweet in tweets:
        try:
            # Start Node
            g.add_node(
                   tweet["retweeted_status"]["user"]["screen_name"],
                   tweet=tweet["retweeted_status"],
                   pos=tweet["retweeted_status"]["position"]["coordinates"])
            # End Node
            g.add_node(
                    tweet["user"]["screen_name"],
                    tweet=tweet,
                    pos=tweet["position"]["coordinates"]
                    )
            g.add_edge(tweet["retweeted_status"]["user"]["screen_name"],
                    tweet["user"]["screen_name"])
        except KeyError:
            g.add_node(
                    tweet["user"]["screen_name"],
                    tweet=tweet,
                    pos=tweet["position"]["coordinates"]
                    )
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
    edge_trace = go.Scattergeo(
        locationmode="country names",
        lat=[],
        lon=[],
        text=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in graph.edges():
        x0, y0 = graph.node[edge[0]]['pos']
        x1, y1 = graph.node[edge[1]]['pos']
        edge_trace['lon'] += [x0, x1, None]
        edge_trace['lat'] += [y0, y1, None]

    node_trace = go.Scattergeo(
        locationmode="country names",
        lat=[],
        lon=[],
        text=[],
        hovertext=[],
        mode='marker',
        hoverinfo='text',
        selected=dict(
            marker=dict(
                opacity=1,
                size=30
                )
            ),
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='YIGnBu',
            reversescale=True,
            color=[],
            size=3,
            opacity=0.5,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in graph.nodes():
        x, y = graph.node[node]['pos']
        node_trace['lon'].append(x)
        node_trace['lat'].append(y)

    for node, adjacencies in graph.adjacency():
        node_trace['marker']['color'].append(len(adjacencies))
        '''
        if len(adjacencies) > 1:
            node_trace['marker']['size'] = len(adjacencies)
        else:
            node_trace['marker']['size'] = 1
        '''
        node_info = 'Tweet: {0} Retweet count: {1}'.format(
                graph.nodes[node]["tweet"]["text"],
                len(adjacencies))
        node_trace['hovertext'].append(node_info)
        node_trace['text'].append(
                graph.nodes[node]["tweet"]["user"]["screen_name"][:10])

    fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(dict(
                title='<br>Tweet-Retweet Relationships Across the Globe',
                titlefont=dict(size=16),
                showlegend=False,
                geo=dict(
                    scope="world",
                    showframe=False,
                    showcoastlines=True,
                    projection=dict(
                        type="Mercator"
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

    plotly.offline.plot(fig, filename='./out/map.html')


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

    for tweet in tweets:
        try:
            # treat it first like a retweet
            retweet = tweet["retweeted_status"]
            # add the edge with id string of the tweets as the id of the
            # vertices and the screen names as the data of the vertices
            g.addEdge(
                    retweet["id_str"],
                    tweet["id_str"],
                    f_data=retweet["user"]["screen_name"],
                    t_data=tweet["user"]["screen_name"]
                    )
        except KeyError:
            # not a retweet because the retweeted status not been found!

            # add the tweet to the relationship dictionary
            g.addVertex(tweet["id_str"], tweet["user"]["screen_name"])
    return g


def get_unique_users(graph):
    '''
    A method to get a list of all the unique users in the graph

    Returns: a sorted list of all the unique users
    '''
    users = list()  # the list to return

    # Find all the unique users
    for v in graph:
        if v.getData() not in users:
            users.append(v.getData())
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
    users = get_unique_users(graph)  # list of all the unique users
    originals = graph.getRoots()  # all the root tweets

    # get row-column information
    # user_indices maps a username to a unique column number
    # tweet_indices maps a tweet id to a unique row number
    user_indices = dict(zip(users, range(len(users))))
    tweet_indices = dict(zip(
        [o.getId() for o in originals], range(len(originals))))

    # Fill the matrix with 0's
    for i in range(0, len(originals)):
        matrix.append([0] * len(users))

    for og in originals:
        for retw in og.getConnections():
            matrix[tweet_indices[og.getId()]][user_indices[
                retw.getData()]] = 1

    return (matrix, users, tweet_indices, user_indices)


def print_user_graph(graph):
    '''
    A function to print the user graph/matrix. Each row is a different
    tweet and each column is a different user. A 1 indicates that the user
    in that column retweeted the tweet in that row

    graph: the graph to print the user matrix of
    '''

    # Create the matrix
    matrix, users, tweet_indices, user_indices = fill_matrix(graph)

    # Print everything in the matrix out

    # print a space before the first value of the first row
    print(" " * 5, end="")

    # print the first row (which is all the usernames)
    # get the list of users and sort the keys alphabetically
    for name in users:
        # fancy print all the screen_names of the users
        # truncate the name to 10 characters and right align at 15 chars
        print("{0:>15.10}".format(name), end="")
    for tw in graph.getRoots():
        # fancy print the screen_name of the user who tweeted
        # truncate it at 10 characters and right align it at 10 chars
        print("\n{0:>10.10}".format(tw.getData()), end=" " * 5)
        for value in matrix[tweet_indices[tw.getId()]]:
            # fancy print every value in the list associated with this
            print("{0:<15}".format(value), end="")


if __name__ == '__main__':
    if sys.argv[1] == "save":
        dirs = [pjoin(PATH, d) for d in sys.argv[2].split(',')]
        tweets = get_tweets(dirs)
        g = build_graph(tweets[0])
        save_graph(g, sys.argv[3])
    elif sys.argv[1] == "show":
        g = load_graph(sys.argv[2])
        display_graph(g)
    elif sys.argv[1] == "print":
        g = user_graph(sys.argv[2])
        print_user_graph(g)
    else:
        print("Please enter either 'save','show', or 'print'")
