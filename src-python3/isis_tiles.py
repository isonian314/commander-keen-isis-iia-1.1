# TILES: isis_tiles.py
#
# This contains all the INFO TILE definitions, as well as functions to check for particular tiles
# New tile definitions can be added easily, and then added to whatever groups you want
# This saves horrendously complex and ugly code during collision detection

import pygame
from isis_constants import *

TILESIZE = 16.0

# Tile Check functions - return TRUE if the input TILE ID matches
# Each tile should be added to the appropriate groups, with common tiles at the top of the list
#_____________________

# Solid for ENEMY
def gfnTile_SolidEnemy(inTile):
    if (
           inTile == INFO_SOLID
        or inTile == INFO_ENEMY_SOLID
        or inTile == INFO_ENEMY_SOLIDw
        or inTile == INFO_SOLID_FROM_TOP
        or inTile == INFO_SOLID_FROM_BOTTOM
        or inTile == INFO_SOLID_FROM_LEFT
        or inTile == INFO_SOLID_FROM_RIGHT
        or inTile == INFO_SOLID_NO_GRAB
       ):
        return True
    else:
        return False

#_____________________    
# Solid from top
def gfnTile_SolidFromTop(inTile):
    if (
           inTile == INFO_SOLID
        or inTile == INFO_SOLID_FROM_TOP
        or inTile == INFO_SOLID_NO_GRAB
       ):
        return True
    else:
        return False
#_____________________
    
# Solid from Bottom
def gfnTile_SolidFromBottom(inTile):
    if (
           inTile == INFO_SOLID
        or inTile == INFO_SOLID_FROM_BOTTOM
        or inTile == INFO_SOLID_NO_GRAB
        or inTile == INFO_UP_RIGHT_45
        or inTile == INFO_UP_RIGHT_45w
        or inTile == INFO_DOWN_RIGHT_45
        or inTile == INFO_DOWN_RIGHT_45w
        or inTile == INFO_UP_RIGHT_30_1
        or inTile == INFO_UP_RIGHT_30_1w
        or inTile == INFO_UP_RIGHT_30_2
        or inTile == INFO_UP_RIGHT_30_2w
        or inTile == INFO_DOWN_RIGHT_30_1
        or inTile == INFO_DOWN_RIGHT_30_1w
        or inTile == INFO_DOWN_RIGHT_30_2
        or inTile == INFO_DOWN_RIGHT_30_2
       ):
        return True
    else:
        return False
#_____________________
    
# Solid from Left
def gfnTile_SolidFromLeft(inTile):
    if (
           inTile == INFO_SOLID
        or inTile == INFO_SOLID_FROM_LEFT
        or inTile == INFO_SOLID_NO_GRAB
       ):
        return True
    else:
        return False
#_____________________
    
# Solid from Right
def gfnTile_SolidFromRight(inTile):
    if (
           inTile == INFO_SOLID
        or inTile == INFO_SOLID_FROM_RIGHT
        or inTile == INFO_SOLID_NO_GRAB
       ):
        return True
    else:
        return False
#_____________________
    
# Up Right 45 /
def gfnTile_UpRight45(inTile):
    if (
           inTile == INFO_UP_RIGHT_45
        or inTile == INFO_UP_RIGHT_45w
       ):
        return True
    else:
        return False
#_____________________
    
# Down Right 45 \
def gfnTile_DownRight45(inTile):
    if (
           inTile == INFO_DOWN_RIGHT_45
        or inTile == INFO_DOWN_RIGHT_45w
       ):
        return True
    else:
        return False
#_____________________

# Up Right 30-1 /
def gfnTile_UpRight30_1(inTile):
    if (
           inTile == INFO_UP_RIGHT_30_1
        or inTile == INFO_UP_RIGHT_30_1w
       ):
        return True
    else:
        return False
#_____________________

# Up Right 30-2 /
def gfnTile_UpRight30_2(inTile):
    if (
           inTile == INFO_UP_RIGHT_30_2
        or inTile == INFO_UP_RIGHT_30_2w
       ):
        return True
    else:
        return False
#_____________________

# Down Right 30-1 \
def gfnTile_DownRight30_1(inTile):
    if (
           inTile == INFO_DOWN_RIGHT_30_1
        or inTile == INFO_DOWN_RIGHT_30_1w
       ):
        return True
    else:
        return False
#_____________________

# Down Right 30-2 \
def gfnTile_DownRight30_2(inTile):
    if (
           inTile == INFO_DOWN_RIGHT_30_2
        or inTile == INFO_DOWN_RIGHT_30_2
       ):
        return True
    else:
        return False    
#_____________________

# Ledge-Grab Tiles
def gfnTile_CanGrab(inTile):
    if (
           inTile == INFO_SOLID
       ):
        return True
    else:
        return False
#_____________________

# Pole
def gfnTile_Pole(inTile):
    if (
           inTile == INFO_POLE
       ):
        return True
    else:
        return False    
#_____________________

# Door
def gfnTile_Door(inTile):
    if (
            inTile >= INFO_DOOR_1
        and inTile <= INFO_DOOR_1 + 15
       ):
        return True
    else:
        return False       
#_____________________

# Water
def gfnTile_Water(inTile):
    if (
           inTile == INFO_WATER
        or inTile == INFO_UP_RIGHT_45w
        or inTile == INFO_DOWN_RIGHT_45w
        or inTile == INFO_UP_RIGHT_30_1w
        or inTile == INFO_UP_RIGHT_30_2w
        or inTile == INFO_DOWN_RIGHT_30_1w
        or inTile == INFO_DOWN_RIGHT_30_2w
        or inTile == INFO_ENEMY_SOLIDw
        or inTile == INFO_HURT_1w
        or inTile == INFO_HURT_2w
        or inTile == INFO_HURT_5w
        or inTile == INFO_DIEw
           ):
        return True
    else:
        return False

# BLANK INFO TILE
def gfnSolid_Info(inTile):
    if (
           inTile == INFO_SOLID
        or inTile == INFO_SOLID_FROM_TOP
        or inTile == INFO_SOLID_FROM_BOTTOM
        or inTile == INFO_SOLID_FROM_LEFT
        or inTile == INFO_SOLID_FROM_RIGHT
        or inTile == INFO_SOLID_NO_GRAB
        or inTile == INFO_UP_RIGHT_45
        or inTile == INFO_DOWN_RIGHT_45
        or inTile == INFO_UP_RIGHT_30_1
        or inTile == INFO_UP_RIGHT_30_2
        or inTile == INFO_DOWN_RIGHT_30_1
        or inTile == INFO_DOWN_RIGHT_30_2
        #or inTile == INFO_POLE
       ):
        return True
    else:
        return False       
#_____________________


# Items
def gfn_IsItem(inTile):
    if (
           inTile == SPRITE_JBEAN_RED
        or inTile == SPRITE_JBEAN_YELLOW
        or inTile == SPRITE_JBEAN_GREEN
        or inTile == SPRITE_JBEAN_CYAN
        or inTile == SPRITE_JBEAN_BLUE
        or inTile == SPRITE_JBEAN_PURPLE
        or inTile == SPRITE_COLA
        or inTile == SPRITE_BURGER
        or inTile == SPRITE_GINGER
        or inTile == SPRITE_SUGAR
        or inTile == SPRITE_CEREAL
        or inTile == SPRITE_BATTERY
        or inTile == SPRITE_SHIELD
        or inTile == SPRITE_IONSCANNER
        or inTile == SPRITE_UNKNOWN        
       ):
        return True
    else:
        return False       
#_____________________

# Enemies
def gfn_IsEnemy(inTile):
    if (
           inTile == SPRITE_FOOG
        or inTile == SPRITE_FOOGJUMP
        or inTile == SPRITE_SPIDER
        or inTile == SPRITE_FROG_WALK
        or inTile == SPRITE_FROG_SWIM
        or inTile == SPRITE_HOLEMONSTER
        or inTile == SPRITE_BLUEMOUTH
        or inTile == SPRITE_GARNAK
        or inTile == SPRITE_YELLOW
        or inTile == SPRITE_DEMON
        or inTile == SPRITE_PLANTGUY
        or inTile == SPRITE_REDFISH
        or inTile == SPRITE_CHOMPERFISH
        or inTile == SPRITE_URCHIN
        or inTile == SPRITE_FLOPPY
        or inTile == SPRITE_YELLOWFISH
        or inTile == SPRITE_GREENFISH
        or inTile == SPRITE_BLUEFISH
        or inTile == SPRITE_RAT
        or inTile == SPRITE_LEMMING
        or inTile == SPRITE_TRUCKGUY1
        or inTile == SPRITE_TRUCKGUY2
        or inTile == SPRITE_TRUCKGUY1_WALK
        or inTile == SPRITE_TRUCKGUY2_WALK
        or inTile == SPRITE_ROBOT_GREY
        or inTile == SPRITE_ROBOT_RED
        or inTile == SPRITE_ROBOT_FLASHER
        or inTile == SPRITE_ROBOT_HOVER
        or inTile == SPRITE_TELETURRET
        or inTile == SPRITE_CATERPILLAR
        or inTile == SPRITE_SNAIL
        or inTile == SPRITE_BIGFROG
        or inTile == SPRITE_DRAGONFLY
        or inTile == SPRITE_BIRD
        or inTile == SPRITE_FOOG_WARRIOR
        or inTile == SPRITE_ROBO_GREY
        or inTile == SPRITE_ROBO_BLUE
        or inTile == SPRITE_SHAPESHIFTER
        or inTile == SPRITE_EVILKEEN
        or inTile == SPRITE_ISONIAN_GREEN
        or inTile == SPRITE_ISONIAN_RED
        or inTile == SPRITE_ISONIAN_WHITE
        or inTile == SPRITE_ISONIAN_FLY
        or inTile == SPRITE_ISONIAN_GIANT1
        or inTile == SPRITE_ISONIAN_GIANT2
        or inTile == SPRITE_DEVIL
        or inTile == SPRITE_YORPY
        or inTile == SPRITE_GARG
        or inTile == SPRITE_SLUG
           
       ):
        return True
    else:
        return False       
#_____________________

# Enemies
def gfn_IsPushEnemy(inTile):
    if (
           inTile == SPRITE_YORPY
        or inTile == SPRITE_DRAGONFLY
          
       ):
        return True
    else:
        return False       
#_____________________
