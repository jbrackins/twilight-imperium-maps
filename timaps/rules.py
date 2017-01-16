import sys

class RuleSet:
    """Rules to determine how board is generated

    The RuleSet Class

    Attributes:
        tbd
    """

    def __init__(self,
                 players = 3,
                 spec    = 3,
                 emp     = 5,
                 reg     = 16,
                 other   = "None"):
        """RuleSet class initialization method.
        """

        # The given defaults are for
        # a game of 3 players
        self.playerCount  = players
        self.galaxySize   = "normal"
        self.specialCount = spec
        self.emptyCount   = emp
        self.regularCount = reg
        self.other        = other
        self.randRemove   = 0
        self.shards       = True  # shards of the throne
        self.shattered    = False # shattered empire
        self.generateRules()

    def setRules(self,s,e,r,rand=0):
        self.specialCount = s 
        self.emptyCount   = e 
        self.regularCount = r 
        self.randRemove   = rand

    def generateRules(self):
        if self.galaxySize == "normal" and self.other == "None":
            p = self.playerCount
            if   p == 3:
                self.setRules(3,5,16)
            elif p == 4:
                self.setRules(4,8,20)
            elif p == 5:
                self.setRules(4,8,20,1)
            elif p == 6:
                self.setRules(4,8,20,2)
            elif p == 7:
                self.setRules(9,12,34,4)
            elif p == 8:
                self.setRules(9,12,34,5)
        elif self.galaxySize == "larger" and self.other == "None":
            if p == 5:
                self.setRules(9,12,34)
            elif p == 6:
                self.setRules(9,12,34,1)
        # "Other" variable will allow for custom maps to 
        # be added in the future iterations of the program

    def __repr__(self):
        if self.playerCount < 3 or self.playerCount > 8:
            msg = "Invalid Player Count (3-6 or 3-8 with Shattered Empire)"
        else:
            msg  =  "Player Count : %d\n"  % (self.playerCount)
            msg +=  "Galaxy Size  : %s\n"  % (self.galaxySize)
            msg +=  "Special Tiles: %d\n"  % (self.specialCount)
            msg +=  "Empty   Tiles: %d\n"  % (self.emptyCount)
            msg +=  "Regular Tiles: %d"  % (self.regularCount)
            if self.randRemove > 0:
                msg +=  "\nRandomly Remove %d Tile"  % (self.randRemove)
                if self.randRemove > 1:
                    msg +=  "s"
                msg += "."
        return msg

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        num = int(sys.argv[1])
    else:
        num = 8
    print("\nRuleSet Demo:", num, "Players\n")
    
    r = RuleSet(players=num)
    print(r,"\n")

    # end