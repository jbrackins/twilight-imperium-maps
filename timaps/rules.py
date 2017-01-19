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
                 other   = "None",
                 quick   = False):
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
        self.removeCount  = 0
        self.shards       = True  # shards of the throne expansion
        self.shattered    = True # shattered empire expansion
        self.fall         = False # Fall of The Empire scenario

        if not quick:
            self.rulePrompt()
        self.generateRules()

    def rulePrompt(self):
        self.promptShards()
        self.promptShattered()
        if self.shards:
            self.promptFall()
        self.promptPlayers()

    def promptShards(self):
        valid = ["Y","YES","N","NO"]
        loop = True
        while loop:
            choice = input("Play With Shards Of The Throne Expansion? [y/n]: ")
            if choice.upper() in valid:
                loop = False
                choice = choice.upper()
            else:
                print("Invalid Choice...")
        if choice == "Y" or choice == "YES":
            choice = True 
        elif choice == "N" or choice == "NO":
            choice = False
        self.setShards(choice)

    def promptShattered(self):
        valid = ["Y","YES","N","NO"]
        loop = True
        while loop:
            choice = input("Play With Shattered Empire Expansion? [y/n]: ")
            if choice.upper() in valid:
                loop = False
                choice = choice.upper()
            else:
                print("Invalid Choice...")
        if choice == "Y" or choice == "YES":
            choice = True 
        elif choice == "N" or choice == "NO":
            choice = False
        self.setShattered(choice)

    def promptFall(self):
        valid = ["Y","YES","N","NO"]
        loop = True
        while loop:
            choice = input("Play The Fall of The Empire Game Type? [y/n]: ")
            if choice.upper() in valid:
                loop = False
                choice = choice.upper()
            else:
                print("Invalid Choice...")
        if choice == "Y" or choice == "YES":
            choice = True 
        elif choice == "N" or choice == "NO":
            choice = False
        self.setFall(choice)

    def promptPlayers(self):
        valid = [3,4,5,6,7,8]
        loop = True
        while loop:
            choice = input("How Many Players? [3-8]: ")
            if choice.isdigit():
                choice = int(choice)
                if choice in valid:
                    if choice > 6 and self.shattered == False:
                        msg  = str(choice) + " Player Games "
                        msg += "are Unavailable unless you "
                        msg += "are\n playing with the Shattered "
                        msg += "Empire Expansion..."
                        print(msg)
                        self.promptShattered()
                    else:
                        loop = False
                else:
                    print("Player Count must be between 3 and 8")
            else:
                print("Invalid Choice...")
        self.setPlayerCount(choice)

    def setPlayerCount(self,value):
        self.playerCount = value

    def setShards(self,value):
        self.shards = value

    def setShattered(self,value):
        self.shattered = value

    def setFall(self,value):
        self.fall = value

    def setRules(self,s,e,r,rndom=0):
        self.specialCount = s 
        self.emptyCount   = e 
        self.regularCount = r 
        self.removeCount  = rndom

    def generateRules(self):

        # 7 and 8 can only happen if you have 
        # shattered empire expansion.
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