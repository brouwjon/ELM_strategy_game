"""
REGIONS
"""

class region(object):
    def __init__(self, resrcType=None, resrcAmt=None, terrain=0):
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


"""
BUILDINGS
"""

class building(object):
    def __init__(self, location=None):
        self.location = location
        # TODO: Add superclass arguments to subclass instance initialization functions 


class factory(building):
# TODO: Determine default build TIMES
# TODO: Determine default build COSTS    
    
    default_build_times = {"CONSTRUCTOR":0, "PROSPECTOR":0, "HARVESTER":0, "TRANSPORT":0}
    default_build_costs = {"CONSTRUCTOR": {'X':0, 'Y':0, 'Z':0}, 
                           "PROSPECTOR": {'X':0, 'Y':0, 'Z':0}, 
                           "HARVESTER": {'X':0, 'Y':0, 'Z':0}, 
                           "TRANSPORT": {'X':0, 'Y':0, 'Z':0}
                           }
    
    def __init__(self):
        # Add capability for multiple build bays
        self.buildQueue = 0
        self.timeLeft = 0
        self.producedUnit = None
        self.build_time_bonus = 0 
        self.build_cost_bonus = {'X':0, 'Y':0, 'Z':0}
        
    def build(self):
        resourceCost = self.find_build_cost()
        if self.location.hasStock(resourceCost):
            self.location.removeResources(resourceCost)
            # TODO: Must decrement self.timeLeft at each Game timeStep
            """ stuff happens """
            self.location.addUnit(self.producedUnit)
    
    def find_build_cost(self):
        realCost = {'X':0, 'Y':0, 'Z':0}
        defaultCost = factory.default_build_costs[self.producedUnit]
        for resource in ['X', 'Y', 'Z']:
            realCost[resource] = defaultCost[resource] - self.build_cost_bonus[resource]
        return realCost
        
        

class extractor(building):
    def __init__(self, resrcType=None):
        self.resrcType = resrcType
        self.volume = 0
        self.maxVolume = 0
        assert "_raw" in resrcType
    
    def processResrc(self):
        self.location.addResources({self.resrcType: self.volume})
    
    def expand(self):
        # TODO: Takes time and resources to do this
        # TODO: Make sure incrementing self.volume won't push it past self.maxVolume 
        self.volume += 1


class refinery(building):
    def __init__(self, resrcType=None):
        self.resrcType = resrcType
        self.raw_rsrcType = resrcType+"_raw"
        self.volume = 0
    
    def processResrc(self):
        # TODO: Only process the quantity of raw_resource self.location has in stock
        # ... don't go into negative values
        if self.location.stockpile[self.raw_resrcType] > 0:
            self.location.removeResources({self.raw_rsrcType: self.volume})
            self.location.addResources({self.resrcType: self.volume})


class infrastructure(building):
    def __init__(self):
        return None

class road(infrastructure):
    def __init__(self, graphEdge):
        return None

class pipeline(infrastructure):
    def __init__(self):
        return None




"""
UNITS
"""

class unit(object):
    def __init__(self, baseSpeed, terrainMod, currentPath=None, currentRegion=None):
        self.baseSpeed = baseSpeed
        self.modTerrain = terrainMod
        self.currentPath = currentPath
        self.currentRegion = currentRegion
        
        self.path = []
    
    def embark(self, target): 
        # TODO: Go from currentRegion to Target... only use when departing a region/vertex
        return None
    
    def move(self):
        if self.currentRegion.terrain > 0:
            terrainBonus = self.terrainMod
        else:
            terrainBonus = 0
        
        totalMovement = (self.baseSpeed + self.currentPath.hasRoad * self.currentPath.roadBonus)
        totalMovement *= [1 - (self.currentRegion.terrain - terrainBonus)]
        
            
"""
unit.move
     terrain = unit.currentRegion.terrain
     totalMovement = (unit.baseMovement + unit.currentPath.hasRoad * roadBonus) * [1 - (terrain.penalty - unit.terrainBonus)]
     unit.distMoved += totalMovement

if unit.travelProgress >= 0.5:
          unit.currentLocation = unit.destination
     if unit.travelProgress >= 1.0:
          unit.traveling = False
          unit.currentPath, destination, origin = None
          unit.distMoved = 0
          unit.location.addUnit(unit)

"""