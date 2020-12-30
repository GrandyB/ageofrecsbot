# Age of Recs
An Age of Empires II: Definitive Edition Discord-based recorded games summary bot.

Made in python, utilising [happyleavesaoc](https://github.com/happyleavesaoc/aoc-mgz)'s recorded game parser library.
Provides some basic functionality for looking at attached files on discord, and if it's a `.aoe2record` it'll pump out a basic embed with player names, map, civs and the winner (if found). Also looks at the root level inside .zip files for any as well.

## To setup

1. Setup a bot account on the [Discord developer portal](https://discord.com/developers/applications), get the token for it and add it to your server using the OAuth link
1. Download this repo and extract to a folder
1. Download [the parser repo](https://github.com/happyleavesaoc/aoc-mgz) and extract into the same place (yes, readme and another file may want to be overridden; your choice
1. Open up `ageofrecs.py` in your best text editor and slap your token in at the bottom where I have put `YOUR_TOKEN_HERE`.
1. `python ageofrecs.py`

## Notes
*From original contributor (Mark "Grandy" Bishop):*

I do not use python very much, nor am I that familiar with its conventions or libraries - was just a quick thing I threw together for a need I saw for a particular tournament I was helping with. happyleavesaoc's parser does all of the heavy lifting, was the only one I could find and happened to be in python!

"Why not use pip for the parser repo" I hear you ask? Well, that version didn't seem to like the latest rec game files I tried with it, but a downloaded copy did.
In terms of actual hosting of the bot, I'm personally using a digitalocean droplet, using `nohup` to run the files - keeps it up while I'm not connected to it.

Suggestions are very welcome, as are pull requests and bug reports - use the relevant tabs above for that.
Enjoy!