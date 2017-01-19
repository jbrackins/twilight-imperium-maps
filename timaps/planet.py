class Planet:
    """Planet properties (Resources / Influence)

    The Planet Class

    Attributes:
        tbd
    """

    def __init__(self,
                 name = "None",
                 res  = 0,
                 inf  = 0,
                 des  = "None"):
        """RuleSet class initialization method.
        """

        # default is just empty planet class,
        # should never happen
        self.name        = name
        self.resources   = res
        self.influence   = inf
        self.description = des
        self.red         = 0 # Warfare
        self.green       = 0 # Biotechnology
        self.blue        = 0 # Propulsion
        self.yellow      = 0 # General

    def setName(self,name):
        self.name = name

    def setStats(self, resources=-1,influence=-1):
        if resources > 0:
            self.resources = resources
        if influence > 0:
            self.influence = influence

    def setTech(self,red=-1,green=-1,blue=-1,yellow=-1):
        if red > 0:
            self.red = red 
        if green > 0:
            self.green = green
        if blue > 0:
            self.blue = blue
        if yellow > 0:
            self.yellow = yellow

    def setDescription(self,description):
        self.description = description

    def __repr__(self):
        msg =  "<Planet Name:%s | Resources:%d | " % (self.name, 
                                                      self.resources)
        msg += "Influence:%d>\n%s"                 % (self.influence, 
                                                      self.description)
        return msg

    def __str__(self):
        return self.name


if __name__ == "__main__":

    print("\nPlanet Demo: (Mecatol Rex)\n")
    d  = "Once a splendid place, now a sad devastated wasteland. "
    d += "Only the radiation-shielded Mecatol City, the seat of the "
    d += "powerful Galactic Council, remains habitable."
    p = Planet("Mecatol Rex", 1, 6, d)
    print(p,"\n")

    # end