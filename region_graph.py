"""
MERGE GRAPH FUNCTIONALITY WITH REGIONS 
"""

# TODO: Build unit tests



class Graph(object):
    
    def __init__(self, letters=''): 
        self.vertices = {char:Vertex(self, char) for char in letters}
        self.edges = {}
    
    
    """ CONSTRUCTION """
    
    def add_vertex(self, name):
        self.vertices[name] = Vertex(self, name)


    def remove_vertex(self, x):
        for e in x.edges:
            self.remove_edge(e)
        del self.vertices[x.name]
        

    def add_edge(self, x, y, value=1):
        if self.adjacent(x, y):
            self.remove_edge(x, y)
        new_edge = Edge(self, x, y, length=value)
        self.edges[(x.name, y.name)] = new_edge
        
        x.edges.append(new_edge)
        y.edges.append(new_edge)


    def remove_edge(self, edge_instance):
        x = edge_instance.vertex_A
        y = edge_instance.vertex_B
        x.edges.remove(edge_instance)
        y.edges.remove(edge_instance)
        del self.edges[(x.name, y.name)]



    """ DATA MANAGEMENT """
    
    def adjacent(self, x, y):
        if type(x) is str and type(y) is str:
            x, y = self.vertices[x], self.vertices[y]

        if y in self.get_neighbors_of(x) and x in self.get_neighbors_of(y):
            return True
        else:
            return False


    def get_edge(self, x, y):
        if type(x) is str and type(y) is str:
            x, y = self.vertices[x], self.vertices[y]
            
        for e in x.edges:
            if e.has_vertex(y):
                return e


    def get_neighbors_of(self, x):
        if type(x) is str:
            x = self.vertices[x]
        return [e.get_other_vertex(x) for e in x.edges]
    



"""
Vertices represent the geographic regions and positions the player works with
"""

class Vertex(object):
    def __init__(self, graph, name, terrain, resrcType, resrcAmt):
        self.graph = graph
        self.name = name
        self.edges = []
        
        self.resources = {'X_raw':0, 'Y_raw':0, 'Z_raw':0}
        self.terrain = terrain
        self.owner = None
        self.buildings = []
        self.units = []
        self.stockPile = {'X':0, 'Y':0, 'Z':0,
                          'X_raw':0, 'Y_raw':0, 'Z_raw':0}
        # Asserts and checks
        if resrcType != None and resrcAmt != None:
            assert resrcType in self.resources.keys()
            assert resrcAmt >= 1 and resrcAmt <= 3
            self.resources[resrcType] = resrcAmt
    
    def hasStock(self, resourceAmts):
        for resource in resourceAmts.keys():
            if self.stockPile[resource] < resourceAmts[resource]:
                return False
        return True
    
    def addResources(self, resourceAmts):
        for resource in resourceAmts.keys():
            self.stockPile[resource] += resourceAmts[resource]

    def removeResources(self, resourceAmts):
        for resource in resourceAmts.keys():
            self.stockPile[resource] -= resourceAmts[resource]
    
    def addUnit(self, newUnit):
        self.units.append(newUnit)
    
    def addBuilding(self, newBuilding):
        self.buildings.append(newBuilding)
    
    

    def __str__(self):
        return self.name 
    
    def get_neighbors(self):
        return [e.get_other_vertex(self) for e in self.edges]
        




class Edge(object):
    def __init__(self, graph, vertex_A, vertex_B, length=0):
        self.graph = graph
        self.hasRoad = False
        self.length = length
        self.vertex_A = vertex_A
        self.vertex_B = vertex_B
    
    def __str__(self):
        return self.vertex_A.name + self.vertex_B.name
    
    
    def has_vertex(self, x):
        if x == self.vertex_A or x == self.vertex_B:
            return True
        else:
            return False
    
    
    def has_vertices(self, x, y):
        if x == self.vertex_A or x == self.vertex_B:
            if y == self.vertex_A or y == self.vertex_B:
                return True
        return False
    
    
    def get_other_vertex(self, x):
        if x == self.vertex_A:
            return self.vertex_B
        elif x == self.vertex_B:
            return self.vertex_A
        else:
            print "I don't have that vertex"
            assert False