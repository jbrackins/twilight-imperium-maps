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

    def __repr__(self):
        msg =  "<Planet Name:%s | Resources:%d | " % (self.name, 
                                                      self.resources)
        msg += "Influence:%d>\n%s"                 % (self.influence, 
                                                      self.description)
        return msg


if __name__ == "__main__":

    print("\nPlanet Demo: (Mecatol Rex)\n")
    d  = "Once a splendid place, now a sad devastated wasteland. "
    d += "Only the radiation-shielded Mecatol City, the seat of the "
    d += "powerful Galactic Council, remains habitable."
    p = Planet("Mecatol Rex", 1, 6, d)
    print(p,"\n")

    # end