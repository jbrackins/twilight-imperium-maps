import xml.etree.ElementTree as ET
import sys

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
        print(file)
        if file != None:
            self.setTree()

    def getRoot(self):
        return self.tree.getroot()

    def test(self):
        root = self.getRoot()
        for tile in root:
            for info in tile:
                print(info.tag.upper(), ":", info.text)
            for planet in tile.findall('planet'):
                print("\t", planet.attrib['name'])

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        file = sys.argv[1]
    else:
        file = None
    if file != None:
        x = XMLParser(file)
        x.test()
        
