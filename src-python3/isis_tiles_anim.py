#_____________________________________________________________________________________________
# ANIMATED TILES: isis_tiles_anim.py
#
# This contains all the ANIMATED TILE definitions, as well as the animated tile class
#_____________________________________________________________________________________________

import pygame
pygame.init()
from isis_draw import *
from isis_tiles import *
from isis_zip import *

# Animation Speed
ANIM_FPS = 4
animLastUpdate = pygame.time.get_ticks()
animFrame = 0
srfcTilesAnim = gfnLoad_Splice(TILESIZE, TILESIZE, gfn_Zip("tiles_anim.png"), 1, 1)

# Animted Tile class
class gcls_AnimTile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_id):
        pygame.sprite.Sprite.__init__(self)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.id = tile_id
        self.changed = False
        self.image = srfcTilesAnim[tile_id * 4]
        self.rect = pygame.Rect(self.x + 4, self.y + 4, 16, 16)
        
    def update(self, inFrame, inLevel):
        self.rect = pygame.Rect(self.x - inLevel.mapX + 4, self.y - inLevel.mapY + 4, 16, 16)
        self.image = srfcTilesAnim[(self.id * 4) + inFrame]

            
       
# Define the sprite groups that will contains all the animated tiles for a level
sprite_AnimBG = pygame.sprite.RenderPlain()
sprite_AnimFG = pygame.sprite.RenderPlain()

# Animated Tile IDs
ANIM_TILE_PURPLE_PATPAT = 2
ANIM_TILE_GREEN_PATPAT = 3
ANIM_TILE_BLUE_PATPAT = 4
ANIM_TILE_EXIT_1 = 4551
ANIM_TILE_EXIT_2 = 4552
ANIM_TILE_CIRCUIT1 = 4553
ANIM_TILE_CIRCUIT2 = 4554
ANIM_TILE_BLUETHING = 4555

ANIM_TILE_WATER1 = 1602
ANIM_TILE_WATER2 = 1603
ANIM_TILE_WATER3 = 1604
ANIM_TILE_WATER4 = 1605
ANIM_TILE_WATER5 = 1633
ANIM_TILE_WATER6 = 1634
ANIM_TILE_WATER7 = 1635
ANIM_TILE_WATER8 = 1636

ANIM_TILE_HANGARSWITCH = 4556
ANIM_TILE_BEAKER1 = 5606
ANIM_TILE_FLAME1 = 5638
ANIM_TILE_BEAKER2 = 5607
ANIM_TILE_FLAME2 = 5639
ANIM_TILE_BEAKER3 = 5608
ANIM_TILE_FOOGCAGE_TL = 5609
ANIM_TILE_FOOGCAGE_TR = 5610
ANIM_TILE_FOOGCAGE_BL = 5641
ANIM_TILE_FOOGCAGE_BR = 5642

ANIM_TILE_BLUECAGE_BL = 5643
ANIM_TILE_BLUECAGE_BR = 5644
ANIM_TILE_BLUECAGE_TR = 5612

# List of the above - the order should match the Animated Tile sheet
ANIMATED_TILES = []
ANIMATED_TILES.append(ANIM_TILE_PURPLE_PATPAT)
ANIMATED_TILES.append(ANIM_TILE_GREEN_PATPAT)
ANIMATED_TILES.append(ANIM_TILE_BLUE_PATPAT)
ANIMATED_TILES.append(ANIM_TILE_EXIT_1)
ANIMATED_TILES.append(ANIM_TILE_EXIT_2)
ANIMATED_TILES.append(ANIM_TILE_CIRCUIT1)
ANIMATED_TILES.append(ANIM_TILE_CIRCUIT2)
ANIMATED_TILES.append(ANIM_TILE_BLUETHING)
ANIMATED_TILES.append(ANIM_TILE_WATER1)
ANIMATED_TILES.append(ANIM_TILE_WATER2)
ANIMATED_TILES.append(ANIM_TILE_WATER3)
ANIMATED_TILES.append(ANIM_TILE_WATER4)
ANIMATED_TILES.append(ANIM_TILE_WATER5)
ANIMATED_TILES.append(ANIM_TILE_WATER6)
ANIMATED_TILES.append(ANIM_TILE_WATER7)
ANIMATED_TILES.append(ANIM_TILE_WATER8)
ANIMATED_TILES.append(ANIM_TILE_HANGARSWITCH)
ANIMATED_TILES.append(ANIM_TILE_BEAKER1)
ANIMATED_TILES.append(ANIM_TILE_FLAME1)
ANIMATED_TILES.append(ANIM_TILE_BEAKER2)
ANIMATED_TILES.append(ANIM_TILE_FLAME2)
ANIMATED_TILES.append(ANIM_TILE_BEAKER3)
ANIMATED_TILES.append(ANIM_TILE_FOOGCAGE_TL)
ANIMATED_TILES.append(ANIM_TILE_FOOGCAGE_TR)
ANIMATED_TILES.append(ANIM_TILE_FOOGCAGE_BL)
ANIMATED_TILES.append(ANIM_TILE_FOOGCAGE_BR)
ANIMATED_TILES.append(ANIM_TILE_BLUECAGE_BL)
ANIMATED_TILES.append(ANIM_TILE_BLUECAGE_BR)
ANIMATED_TILES.append(ANIM_TILE_BLUECAGE_TR)
