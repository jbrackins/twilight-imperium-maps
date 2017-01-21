"""TIMaps Maps Class.

This module contains the GalaxyMap class, which handles the 
generation of the "Tile Pools," which are a reduced-down 
collection of System Tiles.

This module will simulate selecting the appropriate amounts of 
Regular (tiles with planets), Special (red bordered tiles), and 
Empty (tiles without planets or red borders) System Tiles for a 
given game size.

The result of properly using this class is a simulation of the 
map generation step of a Twilight Imperium III game. The goal 
of this project is to speed up the process of setting up a 
TI III game by speeding the map creation process. 


Todo:
    * Figure out 7 and 8 Player Map generation whenever I get 
      info from Shattered Empire stuff.
    * Generate cool, unconventional galaxy configurations someday.

.. TIMaps GitHub Repository:
   https://github.com/jbrackins/twilight-imperium-maps


"""

import sys
from random import randint

from parse    import XMLParser
from rules    import RuleSet
from asciimap import ASCIIMap

class GalaxyMap:
    """Map of Twilight Imperium Galaxy

    The GalaxyMap Class

    Attributes:
        rules       RuleSet generated for the campaign
        rings       List containing the sizes of each ring of hex tiles
        map         Final Map Structure containing selected tiles + player locations
        pool        Combined Pool of potential tiles
        selection   Tiles selected from Pool
        rex         Mecatol Rex (Either Stock Tile or Fall of The Empire Tile)
        regPool     Pool of Regular Tiles, Non Mec Rex, Non-Yellow Planet Systems
        specPool    Pool of Special (Red) Tiles
        empPool     Pool of empty Tiles
    """

    def __init__(self, rules=None):
        """
        GalaxyMap class initialization method.

           This initialization expects a RuleSet class 
           as the first parameter. If this is not supplied, 
           the class will still initialize but won't be 
           able to accomplish much...
        """

        # The given defaults are for
        # a game of 3 players
        if rules != None:
            self.rules   = rules
        else:
            self. rules  = RuleSet(quick=True)
        self.rings       = [1]  # Hex Rings
        self.map         = [ ]  # Final Map
        self.pool        = [ ]  # Main Pool
        self.selection   = [ ]  # Selections from Pool
        self.rex         = [ ]  # Mec Rex
        self.regPool     = [ ]  # regular tiles (planets)
        self.specPool    = [ ]  # special tiles (asteroids, supernovas, etc.)
        self.empPool     = [ ]  # empty   tiles (no planets)

    def validate(self):
        """validation method. 

           Checks if the ruleset provided will generate 
           a legal map based on what tiles are present.
        """

        valid = True
        tileCount = 0
        msg = ""
        
        # Count How Many Tiles are needed to be drawn
        for i in self.rings:
            tileCount += int(i)

        # Remove Mec Rex and Home Systems
        tileCount = tileCount - self.rules.playerCount - 1

        # Check for invalid game setups
        if self.rules.playerCount < 3 or self.rules.playerCount > 8:
            # Too many or not enough players, SORRY
            valid = False
            msg += "\nInvalid Player Count... \n[3-6], or "
            msg += "[3-8] With Shattered Empire Expansion."            
        elif tileCount > len(self.pool):
            # Not enough Tiles
            valid = False
            msg += "\nNot enough Tiles available for\n"
            msg += "This Map Size....\n"

        # If valid is False, then error message is second param
        return valid, msg

    def run(self):
        """run the galaxy map generation. 

           Calls all of the appropriate methods to create 
           the Twilight Imperium III map.
        """

        if self.rules != None:
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

            # Print out the Pool information
            self.printPool()

            # Validate that you can even build 
            # a galaxy with this ruleset
            valid,msg = self.validate()
            if valid:
                # Generate the Map
                self.buildMap()

                # Print Out Galaxy
                self.printGalaxy()
                self.writeGalaxyToFile()
            else:
                # Display Error Message
                print("\nERROR:")
                print(msg)
        else:
            # No ruleset present, can't generate a map!!
            print("Cannot run map generation without ruleset!")

    def printGalaxy(self):
        """Print out a successfully generated map. 

           Has corresponding information for each tile's
           placement.
        """

        # Print out the ASCII of the galaxy map.
        a = ASCIIMap(self.rules)
        a.printMap()

        # Print out each of the tiles
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        split = int(len(self.map) / 3)
        for i in range(len(self.map)):
            msg = "{:02d}".format(i) + " " + str(self.map[i])
            print(msg,end="\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    def writeGalaxyToFile(self,fname="lastmap.txt"):
        """Write a successfully generated map to a file. 

           Has corresponding information for each tile's 
           placement. 

           Currently just set to write to lastmap.txt file
        """

        # Create file
        f = open(fname, 'w')

        # Initialize ASCII Map
        a = ASCIIMap(self.rules)

        # Write map info to file.
        f.write(a.getMap())
        f.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        for i in range(len(self.map)):
            msg = "{:02d}".format(i) + " " + str(self.map[i])
            f.write(msg + "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    def setRex(self):
        """Determine what Mecatol Rex type you will be using. 
        """
        if self.rules.fall:
            rex = [ tile for tile in self.pool 
                        if  tile.getColor().upper() == "YELLOW"
                        and tile.getType( ).upper() == "MECATOL REX" ]
        else:
            rex = [ tile for tile in self.pool 
                        if  tile.getColor().upper() != "YELLOW"
                        and tile.getType( ).upper() == "MECATOL REX" ] 
        if len(rex) > 0:
            self.rex = rex[0]
        else:
            self.rex = None

    def buildMap(self):
        """Build The Twilight Imperium III map. 

           Based on the rules provided by the user, 
           generate a TI III game map. 
        """

        # set up the empty map first
        for i in self.rings:
            ring = []
            for j in range(i):
                ring.append(None)
                self.map.append(None)

        # Randomly remove a few tiles from 
        # the pool if necessary
        for i in range(self.rules.removeCount):
            self.selectFromPool(self.pool)

        # Set up the empty selection list
        for i in range(len(self.pool)):
            self.selection.append(None)

        # Randomly fill the selection list by grabbing 
        # tiles from the pool.
        i = 0
        while len(self.pool) > 0:
            self.selection[i] = self.selectFromPool(self.pool)
            i += 1

        # Determine Player Home Planet Locations.
        self.generatePlayers()

        # Fill in the remainder of the map based 
        # on what tiles you selected.
        self.map[0] = self.rex
        for i in range(1,len(self.map)):
            if self.map[i] == None:
                self.map[i] = self.selection[0]
                del self.selection[0]

    def poolEmpty(self,pool):
        """Check if the System Tile pool is empty.
        """
        if len(pool) > 0:
            return False
        else:
            return True

    def generatePlayers(self):
        """Generate Player Tile locations. 

           Based on how many players you have in your 
           session, this method determines where each 
           player will place their Home System.
        """

        playerPool = []

        # Generate player pool
        for i in range(1,self.rules.playerCount+1):
            msg  = "[Player " 
            msg += str(i) 
            msg += " Home Planet]"
            playerPool.append(msg)

        # In 5 Player games, all Players 
        # have set positions.
        if self.rules.playerCount == 5:
            self.map[31] = playerPool[0]
            self.map[35] = playerPool[1]
            self.map[21] = playerPool[2]
            self.map[25] = playerPool[3]
            self.map[28] = playerPool[4]

        # in 7 player games, Players 
        # 1, 2, 3 have set positions, and 
        # the remaining players have random 
        # positions.
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

        # In every other game type, all Players 
        # have random positions. 
        else:
            if self.rules.playerCount == 3:
                rng = [19,22,25]
            elif self.rules.playerCount == 4:
                rng = [21, 26, 30, 35]
            elif self.rules.playerCount == 6:
                rng = [19, 22, 25, 28, 31, 34]
            elif self.rules.playerCount == 8:
                rng = [37, 40, 43, 46, 49, 52, 55, 58]

            # Fill the player pool by randomly choosing 
            # Each player's location from the rng list
            while len(playerPool) > 0:
                length = len(playerPool)
                location = randint(0,length-1)
                self.map[rng[0]] = playerPool[location]
                del rng[0]
                del playerPool[location]



    def resizePool(self,pool,size):
        """Randomly remove tiles from pool until the 
           pool is reduced to the desired size. 

           Attributes:
                pool    Current Pool being resized
                size    Desired size for pool
        """
        while len(pool) > size:
            self.selectFromPool(pool)

    def selectFromPool(self,pool):
        """Select a random tile from a pool, deleting
           it from the pool as well.

           Attributes:
                pool    Pool containing tiles for selection
        """

        # Check if pool has any tiles. 
        # Grab a random tile if you can.
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
        """Print a given Pool's Information.

           This information should match the 
           Twilight Imperium III rules info for 
           your game type. 
        """

        # Print total pool size, plus the breakdown
        print("Total Pool Size:", len(self.pool))
        print("\tRegular:", len(self.regPool))
        print("\tSpecial:", len(self.specPool))
        print("\tEmpty  :", len(self.empPool))

        # Indicate how many random tiles to remove
        if self.rules.removeCount > 0:
            print("\tRemove", self.rules.removeCount)

    def combinePool(self):
        """Recombine all of the pools. 

           After reducing down all of the other pools, all of 
           the tiles should be placed into the same list.
        """
        self.pool = self.regPool + self.specPool + self.empPool

    def splitPool(self):
        """Split the pool into Regular Tiles, Special Tiles, and 
           Empty Tiles.
        """

        # Determine which tiles belong to each pool
        self.specPool = [ tile for tile in self.pool 
                            if  tile.getType().upper() == "SPECIAL" ]
        self.regPool  = [ tile for tile in self.pool 
                            if  tile.getType().upper() == "REGULAR" ]
        self.empPool  = [ tile for tile in self.pool 
                            if  tile.getType().upper() == "EMPTY"   ]

        # Reduce each pool the the sizes specified in the rules
        self.resizePool( self.regPool,  self.rules.regularCount )
        self.resizePool( self.specPool, self.rules.specialCount )
        self.resizePool( self.empPool,  self.rules.emptyCount   )

    def prunePool(self):
        """Quickly remove all the unneeded tiles for creating the tile 
           pool. 

           This essentially removes all Yellow tiles (Home Planet Tiles)
           and Mecatol Rex, since these tiles are never placed randomly. 

           (Although you could argue that Home Planet tiles are placed 
           randomly... However this program doesn't handle which race 
           each player is.)
        """

        # remove yellow spaces and Mec Rex
        self.pool = [ tile for tile in self.pool 
                        if  tile.getColor().upper() != "YELLOW"
                        and tile.getType( ).upper() != "MECATOL REX" ] 

    def addToPool(self,tile):
        """Add a tile to the general pool. 

           Attributes:
                tile    a tile being added to the System Tile pool.
        """
        self.pool.append(tile)

    def setPool(self):
        """Read the .xml files to fill the System Tile pool.
        """

        # Add Base Tiles
        tiXml = XMLParser("ti.xml")
        if tiXml.fileExists():
            root = tiXml.getRoot()
            for tile in root:
                newTile = tiXml.getTile(tile)
                self.addToPool(newTile)
        
        # Add Shards Tiles
        if self.rules.shards:
            shardsXml    = XMLParser("shards.xml")
            if shardsXml.fileExists():
                root = shardsXml.getRoot()
                for tile in root:
                    newTile = shardsXml.getTile(tile)
                    self.addToPool(newTile)
        
        # Add Shattered Tiles
        if self.rules.shattered:
            shatteredXml = XMLParser("shattered.xml")
            if shatteredXml.fileExists():
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
        return "GalaxyMap Class"

if __name__ == "__main__":
    g = GalaxyMap() 
    g.run()
    # end