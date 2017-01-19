# twilight-imperium-maps
Simple text-based generator for standard-style twilight imperium maps. Currently supports successful map generation for Twilight Imperium III games with 3 to 6 players. System Tile information for both the Ti-III base game and the Shards of The Throne expansion have been implemented at this point.

# Downloading TI-Maps
`git clone https://github.com/jbrackins/twilight-imperium-maps.git`

should suffice, you can also simply download the .zip...

# Running TI-Maps
TI-Maps uses python3.... Sorry.

`python3 timaps`

Will run the program, which will prompt you regarding which expansions you wish to use, as well as how many players you'd like to have. You will also be asked if you wish to play the Fall of The Empire game scenaro.

`python3 timaps <PLAYER_COUNT>`

will bypass all prompts (assumes all expansions are available, playing standard game type) if you want to generate a map ASAP. 

I have not tested this on Windows, but program should work.

# Caveats
I don't have Shattered Empire!! So this program has unfortunately not been set up to handle up to 8 players. Hopefully once I obtain this expansion, I can scale the program up to handle 7 and 8 player game types, but as of right now these maps will not generate successfully...

# Updates
Beyond updating the program to handle all expansions, additional functionality may be added to this program in the future. Each system tile has its detailed information stored in the .xml files, so additional features could be implemented to this program to provide information regarding each system, each planet, etc.

New map scenarios may be added in the future as well.

#Project Developer
* J. Anthony Brackins

Enjoy the program!!
