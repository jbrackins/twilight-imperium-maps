import xml.etree.ElementTree as ET
import sys
from planet import Planet
from tile   import SystemTile

class XMLParser:
    """XML Parser Methods

    The XMLParser Class

    Attributes:
        tbd
    """

    def __init__(self,f=None):
        """XMLParser class initialization method.
        """
        self.setFile(f)
        if f != None:
            self.setTree()
        else:
            self.tree = None

    def __repr__(self):
        return "XMLParser Class"

    def setTree(self):
        self.tree = ET.parse(self.filename)
    
    def setFile(self,file):
        self.filename = file
        #print(file)
        if file != None:
            self.setTree()

    def getRoot(self):
        return self.tree.getroot()

    def getPlanets(self, tile):
        lst = []
        for planet in tile.findall('planet'):
            p = Planet()

            n   = planet.attrib['name']
            d   = planet.attrib['description']
            res = int(planet.attrib['resources'])
            inf = int(planet.attrib['influence'])
            r   = int(planet.attrib['red'])
            g   = int(planet.attrib['green'])
            b   = int(planet.attrib['blue'])
            y   = int(planet.attrib['yellow'])

            p.setName(n)
            p.setDescription(d)
            p.setStats(res,inf)
            p.setTech(r,g,b,y)

            # add planet to list
            lst.append(p) 

        # return list of planets in the system
        return lst

    def getTile(self,tile):
        newTile = SystemTile()
        for color in tile.findall('color'):
            newTile.setColor(color.text)
        for systype in tile.findall('type'):
            newTile.setType(systype.text)
        for prop in tile.findall('property'):
            newTile.setProperty(prop.text)
        for gates in tile.findall('gates'):
            newTile.setGates(str(gates.text))
        for race in tile.findall('race'):
            newTile.setRace(str(race.text))
        planets = self.getPlanets(tile)
        newTile.setPlanets(planets)
        return newTile
            

    def test(self):
        count = 0
        root = self.getRoot()
        for tile in root:
            count += 1
            for info in tile:
                print(info.tag.upper(), ":", info.text)
            for planet in tile.findall('planet'):
                print("\t", planet.attrib['name'])
        return count

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        file = sys.argv[1]
    else:
        file = None
    if file != None:
        x = XMLParser(file)
        x.test()
        
