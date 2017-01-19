import sys
from random import randint

from parse    import XMLParser
from rules    import RuleSet
from asciimap import ASCIIMap


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

    def validate(self):
        valid = True
        tileCount = 0
        msg = ""
        for i in self.rings:
            tileCount += int(i)

        # Remove Mec Rex and Home Systems
        tileCount = tileCount - self.rules.playerCount - 1

        if self.rules.playerCount < 3 or self.rules.playerCount > 8:
            valid = False
            msg += "\nInvalid Player Count... \n[3-6], or "
            msg += "[3-8] With Shattered Empire Expansion."            
        elif tileCount > len(self.pool):
            valid = False
            msg += "\nNot enough Tiles available for\n"
            msg += "This Map Size....\n"
        return valid, msg

    def run(self):
        # set up the rings, set up the pool, 
        # decide mec rex type
        self.setRings()
        self.setPool()
        self.setRex()

        # reduce pool to correct proportions 
        # of Regular, Special, Empty
        self.prunePool()
        self.splitPool()
        self.combinePool()

        self.printPool()
        # Validate that you can even build 
        # a galaxy with this ruleset
        valid,msg = self.validate()
        if valid:


            # Generate the Map
            self.buildMap()

            # Print Out Galaxy
            self.printGalaxy()
        else:
            print("\nERROR:")
            print(msg)

    def printGalaxy(self):
        a = ASCIIMap(self.rules)
        a.printMap()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        split = int(len(self.map) / 3)
        for i in range(len(self.map)):
            msg = "{:02d}".format(i) + " " + str(self.map[i])
            print(msg,end="\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


    def setPlayers(self):
        """Set Player locations on the map
        """
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
            ring = []
            for j in range(i):
                ring.append(None)
                self.map.append(None)


        # remove necessary from selection
        for i in range(self.rules.removeCount):
            self.selectFromPool(self.pool)

        for i in range(len(self.pool)):
            self.selection.append(None)
        # build full list
        #self.selection[0] = self.rex



        # randomly select from the given pool
        i = 0
        while len(self.pool) > 0:
            self.selection[i] = self.selectFromPool(self.pool)
            i += 1


        self.generatePlayers()

        self.map[0] = self.rex
        for i in range(1,len(self.map)):
            if self.map[i] == None:
                self.map[i] = self.selection[0]
                del self.selection[0]

    def poolEmpty(self,pool):
        if len(pool) > 0:
            return False
        else:
            return True

    def generatePlayers(self):
        playerPool = []
        for i in range(1,self.rules.playerCount+1):
            msg  = "[Player " 
            msg += str(i) 
            msg += " Home Planet]"
            playerPool.append(msg)

        # set locations for 5 player game:
        if self.rules.playerCount == 5:
            self.map[31] = playerPool[0]
            self.map[35] = playerPool[1]
            self.map[21] = playerPool[2]
            self.map[25] = playerPool[3]
            self.map[28] = playerPool[4]

        # set locations for SOME of 7 
        elif self.rules.playerCount == 7:
            rng = [60,40,46,50]
            self.map[53] = playerPool[0]
            self.map[57] = playerPool[1]
            self.map[43] = playerPool[2]
            
            del playerPool[0]
            del playerPool[1]
            del playerPool[2]

            while len(playerPool) > 0:
                length = len(playerPool)
                location = randint(0,length-1)
                self.map[rng[0]] = playerPool[location]
                del rng[0]
                del playerPool[location]

        else:
            if self.rules.playerCount == 3:
                rng = [19,22,25]
            elif self.rules.playerCount == 4:
                rng = [21, 26, 30, 35]
            elif self.rules.playerCount == 6:
                rng = [19, 22, 25, 28, 31, 34]
            elif self.rules.playerCount == 8:
                rng = [37, 40, 43, 46, 49, 52, 55, 58]
            while len(playerPool) > 0:
                length = len(playerPool)
                location = randint(0,length-1)
                self.map[rng[0]] = playerPool[location]
                del rng[0]
                del playerPool[location]



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
        print("Total Pool Size:", len(self.pool))
        print("\tRegular:", len(self.regPool))
        print("\tSpecial:", len(self.specPool))
        print("\tEmpty  :", len(self.empPool))
        if self.rules.removeCount > 0:
            print("\tRemove", self.rules.removeCount)

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