# isis_tmx64.py
# Program to read in the TMX file, (with gzipped base64 compression)
# This is not a standalone TMX reader since it ignores a lot of the properties and assumes certain formats
# Parts of this script were adapted from http://www.pygame.org/project-map+loader+for+'tiled'-1158-.html

import base64
import gzip
import StringIO
from xml.dom.minidom import parse, parseString
from isis_zip import *

# Loads the TMX file    
def gfn_LoadTMX(inFile, inLevel, inGame):
    # Parse the file (open it from disk if it is custom file)
    if inGame.custom == False: dom = parse(gfn_Zip(inFile))
    #if inGame.custom == False: dom = parse("data/" + inFile)              # This line is a hack to allow only levels to not be read from zipfile
    else: dom = parse(inFile)
    
    # Contains the full XML code
    fullXML = dom.toxml()   

    # Find <layer>, return <data> for each layer
    for node1 in dom.getElementsByTagName("layer"):

        # Extract the level data for each layer
        if node1.attributes["name"].nodeValue == "TransBG":
            WIDTH = int(node1.attributes["width"].nodeValue)
            HEIGHT = int(node1.attributes["height"].nodeValue)
            for node2 in node1.getElementsByTagName("data"):
                datBG_TRANS = str(node2.childNodes[0].nodeValue)
                
        if node1.attributes["name"].nodeValue == "BG1":
            for node2 in node1.getElementsByTagName("data"):
                datBG1 = str(node2.childNodes[0].nodeValue)

        if node1.attributes["name"].nodeValue == "BG2":
            for node2 in node1.getElementsByTagName("data"):
                datBG2 = str(node2.childNodes[0].nodeValue)

        if node1.attributes["name"].nodeValue == "FG1":
            for node2 in node1.getElementsByTagName("data"):
                datFG1 = str(node2.childNodes[0].nodeValue)

        if node1.attributes["name"].nodeValue == "FG2":
            for node2 in node1.getElementsByTagName("data"):
                datFG2 = str(node2.childNodes[0].nodeValue)

        if node1.attributes["name"].nodeValue == "TransFG":
            for node2 in node1.getElementsByTagName("data"):
                datFG_TRANS = str(node2.childNodes[0].nodeValue)
                
        if node1.attributes["name"].nodeValue == "Info":
            for node2 in node1.getElementsByTagName("data"):
                datINFO = str(node2.childNodes[0].nodeValue)

        if node1.attributes["name"].nodeValue == "Sprites":
            for node2 in node1.getElementsByTagName("data"):
                datSPRITES = str(node2.childNodes[0].nodeValue)
                
    # Decode and Decompress
    inLevel.BG_TRANS = gfn_ConvertTMX(datBG_TRANS, WIDTH, HEIGHT)
    inLevel.BG1 = gfn_ConvertTMX(datBG1, WIDTH, HEIGHT)
    inLevel.BG2 = gfn_ConvertTMX(datBG2, WIDTH, HEIGHT)
    inLevel.FG1 = gfn_ConvertTMX(datFG1, WIDTH, HEIGHT)
    inLevel.FG2 = gfn_ConvertTMX(datFG2, WIDTH, HEIGHT)
    inLevel.FG_TRANS = gfn_ConvertTMX(datFG_TRANS, WIDTH, HEIGHT)
    inLevel.INFO = gfn_ConvertTMX(datINFO, WIDTH, HEIGHT)
    inLevel.SPRITES = gfn_ConvertTMX(datSPRITES, WIDTH, HEIGHT)

    # Set the width & height
    inLevel.width = WIDTH
    inLevel.height = HEIGHT
                


# Converts a 1D, gzipped compressed, base64 encoded string into a 2D array
def gfn_ConvertTMX(inString, inWidth, inHeight):

    # BASE 64 - Decode
    inString = base64.decodestring(inString)

    # GZIP - Uncompress
    # GZIP can only handle file objects, therefore using StringIO
    copmressed_stream = StringIO.StringIO(inString)
    gzipper = gzip.GzipFile(fileobj=copmressed_stream)
    inString2 = gzipper.read()
    gzipper.close()

    # Define empty layer arrays
    layer_1D = []
    layer_2D = []

    # Fix something here
    for idx in xrange(0, len(inString2), 4):
        val = ord(str(inString2[idx])) | (ord(str(inString2[idx + 1])) << 8) | (ord(str(inString2[idx + 2])) << 16) | (ord(str(inString2[idx + 3])) << 24)
        layer_1D.append(val)

    # Generate 2D Array
    for xpos in xrange(inWidth):
        layer_2D.append([])
    # fill them
    for xpos in xrange(inWidth):
        for ypos in xrange(inHeight):
            layer_2D[xpos].append(layer_1D[xpos + ypos * inWidth])
                    
    return layer_2D
