# isis_zip.py
# Function for retrieving a file-like object from an encypted ZIP file

#import zipfile
import czipfile, StringIO
import string, random
import os
import cPickle as pickle
import base64, bz2

PWD = "314ThEmYsTeRyOfIsIsIiAsCbCtIg314"
ZIPDATAr = czipfile.ZipFile(os.path.join("data", "keendata.is2"), 'r')             # Open the zip file


def gfn_Zip(inFile):
    
    testFile = ZIPDATAr.read(inFile, PWD)                       # Retrieve the file
    fileObj = StringIO.StringIO(testFile)                       # Convert it to a string representation
    return fileObj                                              # Return the file-like Object
    
    #return "data/" + inFile        
    


# --- SAVE GAME STUFF ---
class gcls_SAVED():
    def __init__(self):
        self.ranking = -1
        self.lives = 3
        self.health = 10
        self.points = 0
        self.ammo = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.inventory = [-1, -1, -1, -1, 0]

def gfn_LoadSaveDataNew():
    # If savegame file does not exist, load the default values
    if not os.path.exists("savegame.is2"):
        SAVED_DATA = []
        for i in range(16):
            SAVED_DATA.append(gcls_SAVED())
        SAVED_DATA[0].ranking = 0

        return SAVED_DATA
    
    # Otherwise, load (decompress/decrpyt/depickle) the data from the save file
    else:
        OPEN_FILE = bz2.BZ2File("savegame.is2", "r")
        SAVE_FILE = open("temp.is2", "w")
        TEXT1 = OPEN_FILE.read()
        TEXT2 = bz2.decompress(TEXT1)
        TEXT3 = base64.b64decode(TEXT2)
        SAVE_FILE.write(TEXT3)
        SAVE_FILE.close()
        OPEN_FILE.close()

        OPEN_FILE = open("temp.is2", "r")
        SAVED_DATA = pickle.load(OPEN_FILE)
        OPEN_FILE.close()
        os.remove("temp.is2")

        # DEBUG allow all levels
        #for i in range(9):
        #    SAVED_DATA[i].ranking = 0
            
        return SAVED_DATA

def gfn_WriteSaveDataNew(inGameData):
    SAVE_FILE = open("temp.is2", "w")               # Open file to write pickled class to
    pickle.dump(inGameData, SAVE_FILE)              # Dump the pickled class
    SAVE_FILE.close()                               # Close the file

    OPEN_FILE = open("temp.is2", "r")               # Open the file to read (pickled class)
    SAVE_FILE = bz2.BZ2File("savegame.is2", "w")    # Open the file to save (encrypted pickled class)
    TEXT1 = OPEN_FILE.read()                        # Read the pickled garbage into one string
    TEXT2 = base64.b64encode(TEXT1)                 # Encode it!
    TEXT3 = bz2.compress(TEXT2)                     # Compress it!
    SAVE_FILE.write(TEXT3)                          # Write it!
    SAVE_FILE.close()                               # Close it!
    OPEN_FILE.close()                               # Close temp file
    os.remove("temp.is2")                           # Delete temp file

