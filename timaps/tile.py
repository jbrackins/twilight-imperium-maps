from planet import Planet

class SystemTile:
    """System Tile Class holding information about tiles

    The SystemTile Class

    Attributes:
        tbd
    """

    def __init__(self,
                 color    = "None",
                 systype  = "Empty",
                 prop     = "None",
                 gates    = "None",
                 planets  =  None,
                 race     = "None"):
        """SystemTile class initialization method.
        """

        self.color    = color   # Red, Yellow, None
        self.type     = systype # Special, Empty, Regular, Mecatol Rex, Home
        self.property = prop    # Supernova, Nebula, etc. 
        self.gates    = gates   # Alpha, Beta, Delta
        self.planets  = planets # Planets located in system
        self.race     = race    # Races associated with system (if any)

    def getColor(self):
        return self.color

    def getType(self):
        return self.type 

    def setColor(self,color):
        self.color = color

    def setType(self,systype):
        self.type  = systype

    def setProperty(self,prop):
        self.property = prop

    def setGates(self,gates):
        self.gates = gates 

    def setPlanets(self, planets):
        self.planets = planets 

    def setRace(self,race):
        self.race = race 

    def __repr__(self):
        msg =  "<Tile Color:%s | Type:%s | "  % (self.color, self.type)
        msg += "Property:%s | Gates:%s>\n" % (self.property, self.gates)
        
        if self.race != "None":
            msg += "Associated Race: " + self.race + "\n"
        if self.planets != None:
            msg += "Planet Info:\n"
            for planet in self.planets:
                msg += str(planet) + "\n"

        # temp change
        #return msg
        return self.type

    def __str__(self):
        return self.type

if __name__ == "__main__":
    
    print("\nSystem Tile Demo: (Mecatol Rex)\n")
    d  = "Once a splendid place, now a sad devastated wasteland. "
    d += "Only the radiation-shielded Mecatol City, the seat of the "
    d += "powerful Galactic Council, remains habitable."
    p = Planet("Mecatol Rex", 1, 6, d)

    s = SystemTile(systype="Mecatol Rex",planets=[p])
    print(s,"\n")

    # end