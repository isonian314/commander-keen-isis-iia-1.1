import pygame
from pygame.locals import *
from isis_zip import *

#TRANSCOLOUR = pygame.Color(132, 255, 41, 255) # Actual?
#TRANSCOLOUR = (129, 255, 44) # Windows
#TRANSCOLOUR = (103, 255, 94) # Mac?

# Set the TRANSCOLOR to the top-left of the icon
icon = pygame.image.load(os.path.join("data", "icon.png"))
TRANSCOLOUR = icon.get_at((0,0))

# Function to load a spliced image (eg sprite sheet, tiles)
def gfnLoad_Splice(w, h, filename, border, trans):
    images = []
    master_image = pygame.image.load(filename).convert(16)

    # Set transparency
    if trans: master_image.set_colorkey(TRANSCOLOUR)
    
    master_width, master_height = master_image.get_size()
                 
    if border:
        for y in xrange(int((master_height-1)/(h+1))):
            for x in xrange(int((master_width-1)/(w+1))):
                images.append(master_image.subsurface(1 + (x * w) + x, 1 + (y * h) + y, w, h))

    else:
        for y in xrange(int(master_height/h)):
            for x in xrange(int(master_width/w)):
                images.append(master_image.subsurface(x * w, y * h, w, h))

    master_image = None
    return images

# Function to draw sprites from a sprite group, manually
# The pyGame mass-draw method seems to mess up the coordinates
def gfn_IsisDraw(inSurface, inSpriteGroup, inLevel):
    for testSprite in inSpriteGroup:
        inSurface.blit(testSprite.image, (round(testSprite.x - inLevel.mapX) + inLevel.playX, round(testSprite.y - inLevel.mapY) + inLevel.playY))
        #drawX, drawY = testSprite.rect[0], testSprite.rect[1]
        #inSurface.blit(testSprite.image, (drawX, drawY))



