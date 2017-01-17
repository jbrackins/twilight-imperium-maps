import sys
from random import randint

from parse import XMLParser
from rules import RuleSet

class GalaxyMap:
    """Map of Twilight Imperium Galaxy

    The GalaxyMap Class

    Attributes:
        tbd
    """

    def __init__(self,
                 rules):
        """RuleSet class initialization method.
        """

        # The given defaults are for
        # a game of 3 players
        self.rules       = rules
        self.rings       = [1]
        self.map         = []
        self.pool        = []
        self.selection   = []
        self.rex         = []
        self.regPool     = [] # regular tiles (planets)
        self.specPool    = [] # special tiles (asteroids, supernovas, etc.)
        self.empPool     = [] # empty   tiles (no planets)
        self.setRings()
        self.setPool()
        self.setRex()
        self.prunePool()
        self.splitPool()
        self.combinePool()
        self.printPool()
        #print(self.selectFromPool(self.empPool))
        print(len(self.empPool))
        self.buildMap()

    def setRex(self):
        if self.rules.fall:
            rex = [ tile for tile in self.pool 
                        if  tile.getColor().upper() == "YELLOW"
                        and tile.getType( ).upper() == "MECATOL REX" ]
        else:
            rex = [ tile for tile in self.pool 
                        if  tile.getColor().upper() != "YELLOW"
                        and tile.getType( ).upper() == "MECATOL REX" ] 
        self.rex = rex[0]

    def buildMap(self):
        # Build Map around Mecatol Rex

        # set up the empty map first
        for i in self.rings:
            print(i, end="!\n")
            ring = []
            for j in range(i):
                ring.append(None)
                
            self.map.append(ring)
                #print(self.rex)
        print("")
        #print(self.map)

        # remove necessary from selection
        for i in range(self.rules.removeCount):
            self.selectFromPool(self.pool)

        for i in range(len(self.pool)):
            self.selection.append(None)
        # build full list
        self.selection[0] = self.rex



        # randomly select from the given pool
        i = 0
        while len(self.pool) > 0:
            self.selection[i] = self.selectFromPool(self.pool)
            i += 1


        #for i in range(self.rules.playerCount + 1):
        #    self.selectFromPool(self.pool)
        #print(len(self.selection),end=", ")


        print(self.selection,len(self.selection))


        #j = 1
        #for ring in self.map:
        #    if len(ring) == 1:
        #        ring[0] = self.rex
        #    else:
        #        for i in range(0,len(ring)):
        #            # randomly select tile from one of the pools
        #            ring[i] = self.selection[j]
        #            j += 1
        #            #print("")
        #    print(ring, len(ring))
        # map is done. just need to print

    def poolEmpty(self,pool):
        if len(pool) > 0:
            return False
        else:
            return True

    def resizePool(self,pool,size):
        while len(pool) > size:
            self.selectFromPool(pool)

    def selectFromPool(self,pool):
        """Select a random tile from a pool, deleting
           it from the pool as well.
        """
        if len(pool) > 1:
            maximum = len(pool) - 1
            location = randint(0, maximum)
            value = pool[location]
            del pool[location]
        elif len(pool) == 1:
            value = pool[0]
            del pool[0]
        else:
            value = None
        return value

    def printPool(self):
        for tile in self.pool:
            print(tile)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Pool Size", len(self.pool))
        print("Regular Pool Size", len(self.regPool))
        print("Special Pool Size", len(self.specPool))
        print("Empty   Pool Size", len(self.empPool))

    def combinePool(self):
        self.pool = self.regPool + self.specPool + self.empPool

    def splitPool(self):
        self.specPool = [ tile for tile in self.pool 
                            if  tile.getType().upper() == "SPECIAL" ]
        self.regPool  = [ tile for tile in self.pool 
                            if  tile.getType().upper() == "REGULAR" ]
        self.empPool  = [ tile for tile in self.pool 
                            if  tile.getType().upper() == "EMPTY"   ]
        self.resizePool(self.regPool,self.rules.regularCount)
        self.resizePool(self.specPool,self.rules.specialCount)
        self.resizePool(self.empPool,self.rules.emptyCount)

    def prunePool(self):
        # remove yellow spaces
        self.pool = [ tile for tile in self.pool 
                        if  tile.getColor().upper() != "YELLOW"
                        and tile.getType( ).upper() != "MECATOL REX" ] 

    def addToPool(self,tile):
        self.pool.append(tile)

    def setPool(self):
        tiXml = XMLParser("ti.xml")
        root = tiXml.getRoot()
        for tile in root:
            newTile = tiXml.getTile(tile)
            self.addToPool(newTile)
        if self.rules.shards:
            shardsXml    = XMLParser("shards.xml")
            root = shardsXml.getRoot()
            for tile in root:
                newTile = shardsXml.getTile(tile)
                self.addToPool(newTile)
        if self.rules.shattered:
            shatteredXml = XMLParser("shattered.xml")
            root = shatteredXml.getRoot()
            for tile in root:
                newTile = shatteredXml.getTile(tile)
                self.addToPool(newTile)

    def setRings(self):
        """Set the rings and number of systems
        """

        if self.rules.galaxySize == "normal" and self.rules.other == "None":
            p = self.rules.playerCount
            # Rings 1 and 2 are ALWAYS 6 and 12 for standard boards
            self.rings.append(6)
            self.rings.append(12)
            if p < 4:
                # 3rd ring is size 3 for 3 player games
                self.rings.append(9)
            else:
                # 3rd ring is size 18 for all other games
                self.rings.append(18)
            if p > 6:
                # 4th ring present in 7 player / 8 player games
                self.rings.append(24)



        # "Other" variable will allow for custom maps to 
        # be added in the future iterations of the program

    def __repr__(self):
        return "Galaxy Map"

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        num = int(sys.argv[1])
    else:
        num = 8
    print("\nGalaxyMap Demo:")

    # end