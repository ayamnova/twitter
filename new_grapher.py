"""
New_Grapher.py
A module to build a graph implemented with an adjacency list

Original Code found on:
http://interactivepython.org/courselib/static/pythonds/Graphs/Implementation.html

Modified by:
Karsten Ladner

Date: 6/14/2018
"""


class Vertex:
    def __init__(self, key, data):
        self.id = key
        self.connectedTo = {}
        self.data = data

    def __comp__(self, other):
        if self.getData() < other.getData():
            return -1
        elif self.getData() == other.getData():
            return 0
        elif self.getData() > other.getData():
            return 1

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str(
                [x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getData(self):
        return self.data

    def getWeight(self, nbr):
        return self.connectedTo[nbr]


class Graph:
    def __init__(self):
        self.vertList = dict()
        self.numVertices = 0
        self.roots = list()

    def addVertex(self, key, data):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key, data)
        self.vertList[key] = newVertex
        self.roots.append(newVertex)
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __len__(self):
        return(len([v for v in self if len(v.getConnections()) is not 0]))

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, f_data=None, t_data=None, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f, f_data)
        if t not in self.vertList:
            nv = self.addVertex(t, t_data)
        self.vertList[f].addNeighbor(self.vertList[t], cost)
        # Remove tail vertex from roots list
        try:
            self.roots.remove(self.getVertex(t))
        except ValueError:
            pass

    def getVertices(self):
        return self.vertList.keys()

    def getRoots(self):
        return self.roots

    def __iter__(self):
        return iter(self.vertList.values())

    def depth_first_search(self):
        '''
        This method is currently broken
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

        for vertex in self:
            # Since this is a directed graph, every key in the edges list is
            # a vertex that does not have anything pointing to it
            current = vertex
            print("Current: {0}".format(current.getData()))
            # print("Search starting from {0}".format(
            #       current.tweet["user"]["screen_name"]))
            while True:
                # a loop that breaks when it reaches the end of
                # this tweet train

                    # keep track of whether this vertex has a child
                    has_child = False

                    if current.getId() not in discovered:
                        # only append unique nodes to the output
                        # the heart of the output is \t * depth
                        out += "\t" * depth + \
                                str(current.getData()) + \
                                ":" + str(current.getId()) + "\n"
                        # append the id-username tuple to the info list
                        temp = (str(current.getId()),
                                str(current.getData()))
                        info.append(temp)

                        # Add all siblings to the sibling queue
                        tails = current.getConnections()
                        if tails is not None:
                            has_child = True
                            print("Current: {0} Number of tails: {1}".format(current.getData(), len(tails)))
                            for v in tails:
                                print("Appending {0} to stack".format(v.getData()))
                                stack.append(v)
                    # add this vertex to the list of discovered nodes
                    discovered.append(current.getId())

#  I AM FIXING HOW THIS PROGRAM RUNS THROUGH THE VERTICES
                    # Switch to the first tail
                    if len(stack) > 0:
                        current = stack.pop()
                        if has_child:
                            depth += 1
                        else:
                            depth -= 1
                    else:
                        depth = 0
                        break
        return(info, out)


if __name__ == "__main__":
    g = Graph()
    g.addVertex(0, "Pooh")
    g.addVertex(1, "Eor")
    g.addVertex(2, "Tigger")
    g.addVertex(3, "Rabit")

    g.addEdge(0, 1)
    g.addEdge(0, 3)
    g.addEdge(1, 2)
    g.addEdge(1, 3)
    g.addEdge(2, 3)

    for v in g:
        print(v.getData())
        print(type(v.getConnections()))
        for w in v.getConnections():
            print("( %s , %s )" % (v.getId(), w.getId()))
    for v in g.roots:
        print(v.getData())
