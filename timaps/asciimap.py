"""TIMaps ASCIIMaps Class.

This module contains the ASCIIMap class, which returns a specific 
map based on the ruleset the user has indicated. 

These maps are just visual representations of the hexagonal game 
boards for Twilight Imperium III.

Todo:
    * Generate cool, unconventional galaxy configurations someday.

.. TIMaps GitHub Repository:
   https://github.com/jbrackins/twilight-imperium-maps


"""

from rules import RuleSet

class ASCIIMap:
    """ASCII Maps of Twilight Imperium Galaxy

    The ASCIIMap Class will generate the graphical 
    representation of the game board.

    Attributes:
        rules   The RuleSet used for generating maps
    """

    def __init__(self,
                 rules=None):
        """ASCIIMap class initialization method.
        """

        self.map   = ""
        self.rules = rules

        if self.rules != None:
            self.setMap()
    
    def setMap(self):
        """Set the ASCII map based on the ruleset.
        """
        if self.rules.galaxySize == "normal" and self.rules.other == "None":
            p = self.rules.playerCount
            if   p == 3:
                self.map = self.players3()
            elif p == 4:
                self.map = self.players4()
            elif p == 5:
                self.map = self.players5()
            elif p == 6:
                self.map = self.players6()
            elif p == 7:
                self.map = self.players7()
            elif p == 8:
                self.map = self.players8()

    def getMap(self):
        """Return the ASCII map.
        """
        return self.map
        
    def printMap(self):
        """Print out the ASCII map.
        """
        print(self.map)

    def players3(self):
        """Standard 3 Player Map
        """

        msg  = ""
        msg += "\t             __             \n"
        msg += "\t          __/19\__          \n"
        msg += "\t         /27\__/20\         \n"
        msg += "\t         \__/07\__/         \n"
        msg += "\t       __/18\__/08\__       \n"
        msg += "\t      /17\__/01\__/09\      \n"
        msg += "\t      \__/06\__/02\__/      \n"
        msg += "\t    __/16\__/00\__/10\__    \n"
        msg += "\t   /26\__/05\__/03\__/21\   \n"
        msg += "\t   \__/15\__/04\__/11\__/   \n"
        msg += "\t   /25\__/14\__/12\__/22\   \n"
        msg += "\t   \__/24\__/13\__/23\__/   \n"
        msg += "\t      \__/  \__/  \__/      \n"

        return msg

    def players4(self):
        """Standard 4 Player Map
        """

        msg = ""
        msg += "\t             __             \n"
        msg += "\t          __/19\__          \n"
        msg += "\t       __/36\__/20\__       \n"
        msg += "\t    __/35\__/07\__/21\__    \n"
        msg += "\t   /34\__/18\__/08\__/22\   \n"
        msg += "\t   \__/17\__/01\__/09\__/   \n"
        msg += "\t   /33\__/06\__/02\__/23\   \n"
        msg += "\t   \__/16\__/00\__/10\__/   \n"
        msg += "\t   /32\__/05\__/03\__/24\   \n"
        msg += "\t   \__/15\__/04\__/11\__/   \n"
        msg += "\t   /31\__/14\__/12\__/25\   \n"
        msg += "\t   \__/30\__/13\__/26\__/   \n"
        msg += "\t      \__/29\__/27\__/      \n"
        msg += "\t         \__/28\__/         \n"
        msg += "\t            \__/            \n"

        return msg

    def players5(self):
        """Standard 5 Player Map
        """

        # Identical to 4 Player Map
        return self.players4()

    def players6(self):
        """Standard 6 Player Map
        """

        # Identical to 4 Player Map
        return self.players4()

    def players7(self):
        """Standard 7 Player Map
        """

        msg = ""
        msg += "\t             __                 \n"
        msg += "\t          __/37\__              \n"
        msg += "\t       __/60\__/38\__           \n"
        msg += "\t    __/59\__/19\__/39\__        \n"
        msg += "\t __/58\__/36\__/20\__/40\__     \n"
        msg += "\t/57\__/35\__/07\__/21\__/41\    \n"
        msg += "\t\__/34\__/18\__/08\__/22\__/    \n"
        msg += "\t/56\__/17\__/01\__/09\__/42\    \n"
        msg += "\t\__/33\__/06\__/02\__/23\__/    \n"
        msg += "\t/55\__/16\__/00\__/10\__/43\    \n"
        msg += "\t\__/32\__/05\__/03\__/24\__/    \n"
        msg += "\t/54\__/15\__/04\__/11\__/44\    \n"
        msg += "\t\__/31\__/14\__/12\__/25\__/    \n"
        msg += "\t/53\__/30\__/13\__/26\__/45\    \n"
        msg += "\t\__/52\__/29\__/27\__/46\__/    \n"
        msg += "\t   \__/51\__/28\__/47\__/       \n"
        msg += "\t      \__/50\__/48\__/          \n"
        msg += "\t         \__/49\__/             \n"
        msg += "\t            \__/                \n"

        return msg

    def players8(self):
        """Standard 8 Player Map
        """

        # Identical to 7 Player Map
        return self.players7()

    def __repr__(self):
        return self.getMap()

if __name__ == "__main__":
    """Main Function. 
       Running this module on its own will 
       simply print out every map available.
    """

    z = ASCIIMap()
    print(z.players3())
    print(z.players4())
    print(z.players5())
    print(z.players6())
    print(z.players7())
    print(z.players8())
    