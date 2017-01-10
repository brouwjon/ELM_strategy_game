"""
SKELETON IMPLEMENTATION OF DJIKSTRA'S ALGORITHM
WILL BE USED TO FIND TRANSPORT PATHS THROUGH FACILITY NETWORK

NODES ARE FACILITIES
EDGES ARE ROADS CONNECTING THEM, WEIGHTED BY DISTANCE
"""

class Graph(object):
    """
    Node connections are maintained in a single adjacency list, with a parallel list storing distances

    Use adjacency list. Each vertex has a list of all connected vertices. The list consists of tuples... [0] is the neighboring vertex, [1] is the distance    
    
    """
    def __init__(self, letters): 
        self.vertices = {char:Vertex(char) for char in letters}
        self.edges = {char:[] for char in letters}

    def adjacent(self, x, y):
        if x in self.neighbors(y) and y in self.neighbors(x):
            return True
        return False


    def neighbors(self, x):
        edge_distance_pairs = self.edges[x]
        neighbors = [pair[0] for pair in edge_distance_pairs]
        return neighbors


    def add_vertex(self, x):
        self.vertices[x] = Vertex(x)
        self.edges[x] = []


    def remove_vertex(self, x):
        for y in self.neighbors(x):
            self.remove_edge(x, y)
        del self.vertices[x]
        del self.edges[x]


    def add_edge(self, x, y, value=1):
        if self.adjacent(x, y):
            self.remove_edge(x, y)
        self.edges[x].append((y, value))
        self.edges[y].append((x, value))


    def remove_edge(self, x, y):
        if not self.adjacent(x, y):
            return False
        for edge in self.edges[x]:
            if edge[0] == y:
                del edge
                break
        for edge in self.edges[y]:
            if edge[0] == x:
                del edge
                break
        return True


    def get_vertex_val(self, x):
        return self.vertices[x].value


    def set_vertex_val(self, x, new_value):
        self.vertices[x].value = new_value


    def set_vertex_parent(self, x, parent_vertex):
        self.vertices[x].parent = parent_vertex


    def get_edge_val(self, x, y):
        for edge in self.edges[x]:
            if edge[0] == y:
                return edge[1]


    def set_edge_val(self, x, y, new_value):
        for edge in self.edges[x]:
            if edge[0] == y:
                edge[1] = new_value
                break
        for edge in self.edges[y]:
            if edge[0] == x:
                edge[1] = new_value
                break
        return True




    def dijkstra(self, x, y):
        unvisited = self.vertices.keys()
        self.set_vertex_val(x, 0)
        current = x
        while y in unvisited:
            neighbors = [vertex for vertex in self.neighbors(current) if vertex in unvisited]
            for vertex in neighbors:
                self.dk_update_distance(current, vertex)
                unvisited.remove(current)
                unvisited.sort()
                current = unvisited[0]
        return self.dk_trace_path(x, y), self.get_vertex_val(y)
            
            
    def dk_update_distance(self, current, y):
        new_distance = self.get_vertex_val(current) + self.get_edge_val(current, y)
        if new_distance < self.get_vertex_val(y):
            self.set_vertex_val(y, new_distance)
        self.set_vertex_parent(y, current)
        return True


    def dk_get_next_closest(self, unvisited):
        closest = unvisited[0]
        for vertex in unvisited[1:]:
            if self.get_vertex_val(vertex) < self.get_vertex_val(closest):
                closest = vertex
        return closest


    def dk_trace_path(self, origin, destination):
        path = [destination]
        current = destination
        while origin not in path:
            path = [self.vertices[current.parent]] + path
            current = current.parent
        return path






class Vertex(object):
    def __init__(self, name):
        self.name = name
        self.value = 9999
        self.parent = None


    def __lt__(self, other):
        return self.value < other.value


    def __str__(self):
        return self.value


G = Graph("ABCZ")
G.add_edge('A','B')
G.add_edge('B','C')
G.add_edge('B','Z',9)
G.add_edge('C','Z')

path = G.dijkstra('A','Z')
if path != ['B', 'C', 'Z']:
    print "okay!"
else:
    print "nope"
    print path