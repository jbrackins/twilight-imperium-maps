import sys
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
        self.pool        = []
        self.setRings()
        self.setPool()
        self.printPool()

    def printPool(self):
        for tile in self.pool:
            print(tile)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")

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