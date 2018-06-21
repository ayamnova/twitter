'''
usergraph.py
Last Modified: 6/19/2018
A module to build a table based on retweets

Author: Karsten Ladner
Date: 6/1/2018
'''

'''
AT THE MOMENT I HAVE CONSTRUCTED A TWEET-RETWEET GRAPH. EVERY NODE IS A USER
AND EVERY EDGE SIGNIFIES A LEVEL 1 USER RELATIONSHIP

'''

import sys
import pickle
# import random_color

import networkx as nx

import plotly.graph_objs as go
import plotly

from tweets import get_tweets, add_positions
import new_grapher as grapher


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
            g.add_edge(tweet["retweeted_status"]["user"]["screen_name"],
                    tweet["user"]["screen_name"],
                    tweet=tweet["retweeted_status"])
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
    networks = dict()
    islands = go.Scattergeo(
                    locationmode="country names",
                    lat=[],
                    lon=[],
                    text=[],
                    hovertext=[],
                    mode='marker',
                    hoverinfo='text',
                    marker=dict(
                        size=10,
                        opacity=0.75,
                        color='red'
                        )
                    )

    for node in graph.nodes():
        if g.in_degree(node) == 0:
            networks[node] = go.Scattergeo(
                    locationmode="country names",
                    lat=[],
                    lon=[],
                    text=[],
                    hovertext=[],
                    mode='marker',
                    hoverinfo='text',
                    marker=dict(
                        size=10,
                        opacity=1,
                        )
                    )

    for node in graph.nodes():
        if node not in networks.keys():
            x, y = graph.node[node]['pos']
            islands['lon'] += [x, None]
            islands['lat'] += [y, None]
            islands['hovertext'].append("Country: {0}. {1}".format(
                        graph.node[node]["tweet"]["position"]["country"],
                        graph.node[node]["tweet"]["text"]))

    edge_trace = go.Scattergeo(
        locationmode="country names",
        lat=[],
        lon=[],
        text=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # THE HOVER TEXT IS NOT RIGHT.

    for edge in graph.edges():
        if edge[0] in networks.keys():
            x0, y0 = graph.node[edge[0]]['pos']
            x1, y1 = graph.node[edge[1]]['pos']
            networks[edge[0]]['lon'] += [x0, x1, None]
            networks[edge[0]]['lat'] += [y0, y1, None]
            networks[edge[0]]['hovertext'].append("Country: {0}. {1}".format(
                        graph.node[edge[0]]["tweet"]["position"]["country"],
                        graph.node[edge[0]]["tweet"]["text"]))
            networks[edge[0]]['hovertext'].append("Country: {0}. {1}".format(
                        graph.node[edge[1]]["tweet"]["position"]["country"],
                        graph.node[edge[1]]["tweet"]["text"]))

    for network, trace in networks.items():
        trace['marker']['color'] = random_color.random_color()
        if len(trace['lon']) == 0:
            trace['lon'], trace['lat'] = graph.node[network]['pos']




    traces = [tr for tr in networks.values()]

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
            size=10,
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
        node_info = '{0}: Tweet: {1} Retweet count: {2}'.format(
                graph.nodes[node]["tweet"]["position"]["country"],
                graph.nodes[node]["tweet"]["text"],
                len(adjacencies))
        node_trace['hovertext'].append(node_info)
        node_trace['text'].append(
                graph.nodes[node]["tweet"]["user"]["screen_name"][:10])

    # traces.append(islands)
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
            matrix[user_indices[user.getId()]][
                    user_indices[neighbor.getId()]] = user.getWeight(neighbor)

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
    else:
        g = build_graph("./data/25crisis")
        print("Please enter either 'save','show', or 'print'")
