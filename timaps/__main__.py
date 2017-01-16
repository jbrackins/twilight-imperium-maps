import sys

from planet import Planet
from rules  import RuleSet
from tile   import SystemTile
from parse  import XMLParser
if __name__ == "__main__":
    if(len(sys.argv) > 1):
        num = int(sys.argv[1])
    else:
        num = 8

    print("\nTI-Maps Demo:\n")

    r = RuleSet(players=num)

    d  = "Once a splendid place, now a sad devastated wasteland. "
    d += "Only the radiation-shielded Mecatol City, the seat of the "
    d += "powerful Galactic Council, remains habitable."
    p = Planet("Mecatol Rex", 1, 6, d)

    s = SystemTile(systype="Mecatol Rex",planets=[p])
    print(s,"\n")

    x1 = XMLParser("ti.xml")
    x1.test()
    x2 = XMLParser("shards.xml")
    x2.test()
    x3 = XMLParser("shattered.xml")
    x3.test()