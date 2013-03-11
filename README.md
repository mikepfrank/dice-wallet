dice-wallet
===========

Short Python console script for deriving Bitcoin brainwallet passphrases from rolls of a 6-sided die.  Supports generating passphrases with 64, 128, or 256 bits of entropy (256 is recommended).

INSTALLATION INSTRUCTIONS:
--------------------------

First install Python 3.1 or later (script has been tested with 3.1.4 and 3.3.0.  Extract dice-wallet repository from ZIP file.

FILES:
------

* README.md - This file.
* dicewallet.py - The Python script.
* diceware.wordlist.asc.txt - Diceware dictionary, from 
	http://world.std.com/~reinhold/diceware.html

INSTRUCTIONS FOR USE:
---------------------

Run the python executable on dicewallet.py in a terminal window.  The file diceware.wordlist.asc.txt must be in the same folder.  The script uses text I/O on the console to communicate with the user.  Have a six-sided die ready, and follow the prompts.
