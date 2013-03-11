#|=========================================================================================
#|
#|   dicewallet.py                                           [Python console script]
#|
#|       This simple utility facilitates using "Diceware" technology
#|       (http://world.std.com/~reinhold/diceware.html) to securely
#|       generate a Bitcoin private key using passphrases or raw hex
#|       strings derived from repeated rolls of an ordinary 6-sided
#|       die.  Passphrases with 64, 128, and 256 bits of entropy are
#|       supported.  Passphrase-hashing functionality is not included.
#|
#|   Language:   Python version 3.x
#|                   (Tested with 3.1.4 & 3.3.0 on MacOS X 10.6.8,
#|                      and 3.3.0 on Windows XP Professional 2002 SP3.
#|
#|   Revision history:
#|       v0.1 (3/10/13) by Michael P. Frank - Initial working revision.
#|       v0.1.1 (3/11/13) by M.P. Frank - Minor cleanup.
#|          - Renamed 'map' dict to 'dicemap' to avoid collision w. reserved word.
#|          - Fixed off-by-1 error in display of word indices in summary table.
#|
#|   Licensing:
#|       GPLv3 (http://opensource.org/licenses/GPL-3.0)
#|
#|vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

print();
print("========================================================================");
print("DiceWallet: A Diceware-based Bitcoin wallet generator, v0.1 by M. Frank.");
print("------------------------------------------------------------------------");
print();
print("\t" + "This tool helps you create an offline Bitcoin wallet using rolls");
print("\t" + "of an ordinary 6-sided die as a random-number generator.  This saves");
print("\t" + "you from having to verify or trust that the tool you are using to");
print("\t" + "generate random numbers is not doing so in an insecure way (pre-");
print("\t" + "determining the numbers, or sending them to an attacker).  This");
print("\t" + "program itself is simple, thus very easy to inspect and verify.");
print();
print("\t" + "The basic procedure is to use groups of 5 die rolls (\"pentahexes\")");
print("\t" + "to select words from the 7,776-word Diceware dictionary, and string");
print("\t" + "these together to form a passphrase that is relatively easy to write");
print("\t" + "down, memorize, or convey verbally.  This can then be used with your");
print("\t" + "favorite brain-wallet address generator (we recommend downloaning the");
print("\t" + "one at BitAddress.org and running it offline) to generate your private");
print("\t" + "key, or alternatively, in the case of a passphrase that already has");
print("\t" + "256 bits of entropy, the random data can be used as the key directly.");
print();
print("How many bits' worth of passphrase entropy do you want?  (More = more secure.)");
print();
print("Your choices are:");
print("\t" + "1. 64 bits (25 die rolls, 5-word passphrase)");
print("\t" + "2. 128 bits (50 die rolls, 10-word passphrase)");
print("\t" + "3. 256 bits (100 die rolls, 20-word passphrase)");
print();
print("(NOTE: If you choose option 3, you'll have the option of ignoring the passphrase");
print("and generating a 256-bit private key directly.)");
print();

while 1:
    choice = input("Enter 1, 2, or 3 here> ");
    try:
        choice_asint = int(choice);
    except ValueError:
        print("Please enter only 1, 2, or 3 at the prompt!");
        continue;
    if (choice_asint < 1 or choice_asint > 3):
        print("Please enter only 1, 2, or 3 at the prompt!");
    else:
        break;

if (choice_asint == 1):
    nbits = 64
    nchunks = 1             # A "chunk" is a sequence of 5 dicewords
elif (choice_asint == 2):
    nbits = 128
    nchunks = 2
elif (choice_asint == 3):
    nbits = 256
    nchunks = 4

nwords = nchunks * 5;
nrolls = nwords * 5;

print();
print("You selected:");
print("\t" + str(nbits), "bits");
print("\t" + str(nchunks), "chunks of 5 words");
print("\t" + str(nwords), "words");
print("\t" + str(nrolls), "die rolls");
print();

dict_filename = "diceware.wordlist.asc.txt"
print("Reading Diceware word-list file [" + dict_filename + "]...");

dict_file = open(dict_filename, "r");

dicemap = dict();   # Create empty hash table to store pentahex->diceword mapping
nentries = 0;

while 1:
    line = dict_file.readline();
    if line == "":                  # indicates end of file
        break;
    words = line.split();
    if len(words) != 2 or words[0] == "Charset:":
#        print("Skipping line: [" + line.strip() + "]");
        continue;
    pentahex = words[0];
    diceword = words[1];
    dicemap[pentahex] = diceword;
    nentries = nentries + 1;

print("I read", nentries, "dicewords from the word list.");
if nentries != 7776:
    print("Something went wrong; the word list should contain exactly 7776 entries.");
    print("Quitting...");
    exit();

print();
print("OK, now it's time for you to start rolling a 6-sided die.");
print("Enter the roll results, 5 rolls per line, like this: 32451");
print("When we're done, we'll summarize the results for you.");
print();

wordi = 0;

pentahexes = [];
base6vals = [];
dicewords = [];

for chunki in range(nchunks):
    print("Chunk #" + str(chunki+1) + ":");
    for word in range(5):
        base6val = "";
        while 1:
            entry = input("\t" + "Pentahex #" + str(wordi+1) + ": ");
            if len(entry) !=5:
                print("You must type exactly 5 digits.  Try again.");
                continue;
            problem = False;
            for i in range(5):
                if entry[i] < '1' or entry[i] > '6':
                    print("Each character typed must be a numeral 1-6.  Try again.");
                    problem = True;
                    break;
                base6val = base6val + chr(ord(entry[i]) - 1);   # subtract 1 from each digit
            if not problem:
                break;
        print("\t\tYou entered the pentahex:", entry);
        pentahexes[wordi:] = [entry];
        print("\t\tIts base-6 value is:", base6val);
        base6vals[wordi:] = [base6val];
        diceword = dicemap[entry];
        print("\t\tIts diceword is: [" + diceword + "]");
        dicewords[wordi:] = [diceword];
        wordi = wordi + 1;

print();
print(" --- DATA SUMMARY ---");
print();
print("Chunk",  "Word",   "Penta-", "Base6", "Dice-", sep='\t');
print("No.",    "No.",    "hex",    "Value", "word",  sep='\t');
print("-----",  "-----",  "-----",  "-----", "------------", sep='\t');

wordi = 0;
for chunki in range(nchunks):
    print(str(chunki+1)+":");
    for word in range(5):
        print("", (wordi+1), pentahexes[wordi], base6vals[wordi], dicewords[wordi], sep='\t');
        wordi = wordi + 1;

print();
print("Your diceware passphrase is:");
print("\t" + (" ".join(dicewords)));

print();
print("Your base-6 pass code is:");
print("\t" + (",".join(base6vals)));

base6val = "".join(base6vals);
intval = int(base6val, 6);

print();
print("Your decimal pass code is:");
print("\t", "{:,d}".format(intval));

hexval = hex(intval)[2:].upper();

print();
print("Your hexadecimal pass code is:");
print("\t", hexval);

print();
print("NOTE: The passphrase and the various passcodes above are equivalent");
print("in terms of their entropy, so, you can use whichever of them is easiest");
print("for you to utilize as your brain-wallet passphrase/mini-key.");

if (nbits == 256):
    rawpriv = hexval[-64:]
    print();
    print("You may also use these 32 hex bytes as a private key directly:");
    print("\t", rawpriv);

print();
input("Copy the data you want, then press enter to exit. > ");

