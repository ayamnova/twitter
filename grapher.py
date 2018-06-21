'''
Graph
A module to build a graph to build a graph of the relationships between many different
tweets

Author: Karsten Ladner
Date: 6/1/2018
'''


class Edgenode:
    '''
    Node Class:

    end: the other edge node connected to this edge
    next: the next edge starting from this node
    weight: the weight of this edge
    tweet: the tweet associated with this node
    '''

    def __init__(self, end=None, nxt=None, weight=None, tweet=None):

        self.end = end
        self.next = nxt
        self.weight = weight
        self.tweet = tweet

    def __str__(self):
        return "Edgenode:\n\tWeight:{0}\n\tEnd:{1}".format( 
                self.weight, self.end) + "\n\tTweeter:{0}".format(
                self.tweet["user"]["screen_name"]) + "\n\tNext:{0}".format(self.next)


class Graph(Edgenode):
    '''
    Graph class

    edges: the dictionary of all the edges in the graph, each edge is the head
           of a respective list
    is_directed: a bool to indicate whether the graph is directed

    originals: a list of originals
    '''

    def __init__(self, direct=True):
        self.is_directed = direct
        self.edges = dict()

    def insert_edge(self, start, end=None, directed=True):
        '''
        Inserts a new edge into the graph's list of edges at the head of its
        respective edges list

        start: the node where the edge begins
        end: the node where the edge ends
        directed: whether the graph is directed or not
        '''

        # initialize a temp node
        temp = Edgenode()
        # set the temp node's end to the end
        if end is not None:
            temp.end = Edgenode(None, None, None, end)
        else:
            temp.end = None

        # set the temp node's tweet information
        temp.tweet = start

        # Insert the temp node at the front of its respective list

        # don't lose the front of the list
        # make the temp node's next value point to the current front node
        try:
            temp.next = self.edges[start["id_str"]]
        except KeyError:
            temp.next = None

        # make the graph see this new edge first
        self.edges[start["id_str"]] = temp

        # if the graph is undirected, insert the reverse of this
        if directed is False:
            self.insert_edge(end, start, True)

    def __str__(self):
        e = ""
        for ed in self.edges.keys():
            e += str(self.edges[ed]) + "\n"
        return("Graph object:\nEdges:\n\t" + e)

    def depth_first_search(self):
        '''
        A function to get the relationships between tweets and retweets in a
        graph.

        Returns a tuple.
            1st value is a string. Every line contains the username of the
                who tweeted. Lines that contain indentation are retweets.
                Indentation comes in multiples of 5.
            2nd values is a list of tuples. The tuples are pairs of id_str
                and username
        '''

        out = ""  # the out string to return
        info = []  # the info list to return
        stack = []  # a stack of tweets to process
        depth = 0  # the depth at which the tweet is located in the graph
        discovered = []  # a list of tweets that have already been visited

        for node in self.edges.keys():
            # Since this is a directed graph, every key in the edges list is
            # a node that does not have anything pointing to it

            current = self.edges[node]
            # print("Search starting from {0}".format(
            #       current.tweet["user"]["screen_name"]))
            while True:
                # a loop that breaks when it reaches the end of
                # this tweet train

                    # keep track of whether this node has siblings
                    has_siblings = False

                    # keep track of whether this node has a child
                    has_child = False

                    if current.tweet["id_str"] not in discovered:
                        # only append unique nodes to the output
                        # the heart of the output is \t * depth
                        out += "\t" * depth + \
                                current.tweet["user"]["screen_name"] + \
                                ":" + current.tweet["id_str"] + "\n"
                        # append the id-username tuple to the info list
                        temp = (current.tweet["id_str"],
                                current.tweet["user"]["screen_name"])
                        info.append(temp)

                    # add this node to the list of discovered nodes
                    discovered.append(current.tweet["id_str"])

                    # Add all siblings to the sibling queue
                    next_node = current.next
                    while next_node is not None:
                        has_siblings = True
                        stack.append(next_node)
                        next_node = next_node.next

                    # Follow the end pointers and add them all to the end 
                    # queue
                    end = current.end
                    if end is not None:
                        has_child = True
                        stack.append(end)

                    # Switch to the first child
                    if len(stack) > 0:
                        current = stack.pop()
                        if has_child:
                            depth += 1
                        elif has_siblings is False:
                            depth -= 1
                    else:
                        depth = 0
                        break
        return out, info

