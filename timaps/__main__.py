import sys

from planet import Planet
from rules  import RuleSet
from tile   import SystemTile
from parse  import XMLParser
from maps   import GalaxyMap

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        num = int(sys.argv[1])
        quick = True
    else:
        num = 6
        quick = False

    print("\nTI-Maps:\n")

    r = RuleSet(players=num,quick=quick)
    g = GalaxyMap(r)
    g.run()