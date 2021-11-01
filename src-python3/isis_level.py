# isis_level.py
# Contains level class and any level related functions
import pygame
from isis_constants import *
from isis_tiles import *
from isis_tiles_anim import *
from isis_draw import *
from isis_items import *
from isis_enemies import *
from isis_doors import *
from isis_keen import *
from isis_weather import *
from isis_zip import *
from isis_music import *
from isis_cutscenes import *

# Load tiles
srfcTiles = gfnLoad_Splice(TILESIZE, TILESIZE, gfn_Zip("tiles.png"), 0, 0)

# Load Tile Surfaces
srfcTilesAnim = gfnLoad_Splice(TILESIZE, TILESIZE, gfn_Zip("tiles_anim.png"), 1, 1)

# Set the TRANSCOLOR to the top-left of the icon
icon = pygame.image.load(os.path.join("data", "icon.png"))
TRANSCOLOUR = icon.get_at((0,0))

#TRANSCOLOUR = (129, 255, 44)
#TRANSCOLOUR = (103, 255, 94)

# Door Class
class gclsDoor():
    def __init__(self, door_num, x, y):
        self.x1 = x
        self.y1 = y
        self.x2 = 0
        self.y2 = 0
        self.id = door_num

    def update(self, x2, y2):
        self.x2 = x2
        self.y2 = y2


                
srfcMasks = gfnLoad_Splice(16, 16, gfn_Zip("tiles_masks.png"), 0, 1)
MASK_SOLID = 0
MASK_UP_RIGHT_45 = 1
MASK_DOWN_RIGHT_45 = 2
MASK_UP_RIGHT_30_1 = 3
MASK_UP_RIGHT_30_2 = 4
MASK_DOWN_RIGHT_30_1 = 5
MASK_DOWN_RIGHT_30_2 = 6
MASK_ONE_WAY_UP = 7
MASK_ONE_WAY_DOWN = 8
MASK_ONE_WAY_LEFT = 9
MASK_ONE_WAY_RIGHT = 10

# Masked Level Class
class gcls_Mask(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID):
        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.image = srfcMasks[self.id]
        self.image.set_alpha(0.5 * 255)
        self.rect = pygame.Rect(round(self.x), round(self.y), TILESIZE, TILESIZE)
        
    def update(self, inLevel):
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, TILESIZE, TILESIZE)

# HURT tiles class
class gcls_Hurt(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID):
        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.image = srfcMasks[0]
        self.rect = pygame.Rect(round(self.x), round(self.y), TILESIZE, TILESIZE)
        
    def update(self, inLevel):
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, TILESIZE, TILESIZE)
        
# Exit Class
class gcls_Exit(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID):
        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.rect = pygame.Rect(round(self.x), round(self.y), TILESIZE, TILESIZE)
        self.image = srfcMasks[0]
        self.image.set_alpha(0.5 * 255)
        
    def update(self, inLevel):
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, TILESIZE, TILESIZE)

# Enemy Teleporter Class
class gcls_EnemyTele():
    def __init__(self, inX, inY):
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        
# Level class
# This class contains all information relevent to the current level
# This includes all the tile layers, sprites, etc
class gcls_Level():
    def __init__(self):
        # Level Properties
        self.width = 0
        self.height = 0
        self.background_ID = 0
        self.music_ID = 0
        self.weather_ID = 0
        self.night = False
        
        # Keen start properties
        self.initX = 0
        self.initY = 0
        self.initDirection = 0
        self.initWater = False
        
        # Camera
        self.mapX = 0       # Camera X position
        self.mapY = 0       # Camera Y position
        self.playX = 4      # Start of playfield X (inside of border)
        self.playY = 4      # Start of playfield Y (inside of border)
        self.playWidth = 256
        self.playHeight = 192
        self.bgX = 0
        self.bgY = 0
        self.bgMoveX = 0
        self.bgMoveY = 0
        
        # Tiled layers
        self.BG_TRANS = []
        self.BG1 = []
        self.BG2 = []
        self.FG1 = []
        self.FG2 = []
        self.FG_TRANS = []
        self.INFO = []
        self.SPRITES = []
        self.sprite_MaskAll = pygame.sprite.RenderPlain()
        self.DoorList = []
        self.TeleList = []
        self.EnemyTeleList = []
        
        # Statistics
        self.stats_NumItems = 0
        self.stats_NumItems_Tot = 0.0
        self.stats_NumPoints = 0
        self.stats_NumPoints_Tot = 0.0
        self.stats_NumEnemies = 0
        self.stats_NumEnemies_Tot = 0.0
        
        # Sprite Groups
        self.sprite_AnimBG = pygame.sprite.RenderPlain()
        self.sprite_AnimFG = pygame.sprite.RenderPlain()
        self.sprite_Items = pygame.sprite.RenderPlain()
        self.sprite_Floats = pygame.sprite.RenderPlain()
        self.sprite_Projectiles = pygame.sprite.RenderPlain()
        self.sprite_Explosions = pygame.sprite.RenderPlain()
        self.sprite_Particles = pygame.sprite.RenderPlain()
        self.sprite_Enemies = pygame.sprite.RenderPlain()
        self.sprite_Doors = pygame.sprite.RenderPlain()
        self.sprite_Exits = pygame.sprite.RenderPlain()
        self.sprite_Hurt = pygame.sprite.RenderPlain()
        self.sprite_WeatherBG = pygame.sprite.RenderPlain()
        self.sprite_WeatherFG = pygame.sprite.RenderPlain()
        self.sprite_Platforms = pygame.sprite.RenderPlain()
        self.sprite_PlatformDirections = pygame.sprite.RenderPlain()
        self.sprite_Switches = pygame.sprite.RenderPlain()
        self.sprite_CheckPoints = pygame.sprite.RenderPlain()

        # Night stuff
        self.totalNight = 0
        self.maxNight = 60 * 10.0
        
        # Surfaces
        self.srfcPBG = None
        self.srfcBG_TRANS = None
        self.srfcBG = None
        self.srfcFG = None
        self.srfcFG_TRANS = None

        # Reload (if killed, don't re-draw the graphics
        self.reload = False
        
    def reset(self):
        if self.reload == False:
            # Tiled layers
            self.BG_TRANS = []
            self.BG1 = []
            self.BG2 = []
            self.FG1 = []
            self.FG2 = []
            self.FG_TRANS = []
            self.INFO = []
            self.SPRITES = []
            self.DoorList = []
            self.TeleList = []
            self.EnemyTeleList = []
            self.night = False

            # Surfaces
            self.srfcPBG = None
            self.srfcBG_TRANS = None
            self.srfcBG = None
            self.srfcFG = None
            self.srfcFG_TRANS = None

            # Keen start properties
            self.initX = 0
            self.initY = 0
            self.initDirection = 0
            self.initWater = False
        
        # Statistics
        self.stats_NumItems = 0
        self.stats_NumItems_Tot = 0.0
        self.stats_NumPoints = 0
        self.stats_NumPoints_Tot = 0.0
        self.stats_NumEnemies = 0
        self.stats_NumEnemies_Tot = 0.0
        
        # Sprite Groups
        self.sprite_MaskAll.empty()
        self.sprite_AnimBG.empty()
        self.sprite_AnimFG.empty()
        self.sprite_Items.empty()
        self.sprite_Floats.empty()
        self.sprite_Projectiles.empty()
        self.sprite_Explosions.empty()
        self.sprite_Particles.empty()
        self.sprite_Enemies.empty()
        self.sprite_Doors.empty()
        self.sprite_Exits.empty()
        self.sprite_Hurt.empty()
        self.sprite_WeatherBG.empty()
        self.sprite_WeatherFG.empty()
        self.sprite_Platforms.empty()
        self.sprite_PlatformDirections.empty()
        self.sprite_Switches.empty()
        self.sprite_CheckPoints.empty()

        # Night stuff
        self.totalNight = 0
        
    # Updates Sprite Containers etc based on current Level data
    def update(self, inGame, inKeen):

        
        # Create surfaces for level layers (BG & FG, Trans, etc)
        srfcBG1 = pygame.Surface((TILESIZE * self.width, TILESIZE * self.height), depth=16)
        srfcBG2 = pygame.Surface((TILESIZE * self.width, TILESIZE * self.height), depth=16)
        self.srfcBG = pygame.Surface((TILESIZE * self.width, TILESIZE * self.height), depth=16)
        srfcFG1 = pygame.Surface((TILESIZE * self.width, TILESIZE * self.height), depth=16)
        srfcFG2 = pygame.Surface((TILESIZE * self.width, TILESIZE * self.height), depth=16)
        self.srfcFG = pygame.Surface((TILESIZE * self.width, TILESIZE * self.height), depth=16)
        self.srfcBG_TRANS = pygame.Surface((TILESIZE * self.width, TILESIZE * self.height), depth=16)
        self.srfcFG_TRANS = pygame.Surface((TILESIZE * self.width, TILESIZE * self.height), depth=16)
        srfcBG2.set_colorkey(TRANSCOLOUR)
        srfcFG2.set_colorkey(TRANSCOLOUR)
        self.srfcBG_TRANS.set_alpha(0.5 * 255)
        self.srfcBG_TRANS.set_colorkey(TRANSCOLOUR)
        self.srfcFG_TRANS.set_alpha(0.5 * 255)
        self.srfcFG_TRANS.set_colorkey(TRANSCOLOUR)

        # Draw initial level layers
        for x in range(self.width):
            for y in range(self.height):
                bg_flag = 0
                fg_flag = 0
                # Build animation table while we are here
                # This checks the current tile against all possible animated tiles (not very efficient, but only done once at the beginning)
                # If one is found, add it to the table, and set a flag so it is not drawn on the original BG/FG sheet
                for i in range(len(ANIMATED_TILES)):
                    anim = ANIMATED_TILES[i]
                    if self.BG1[x][y] == anim or self.BG2[x][y] == anim:
                        self.sprite_AnimBG.add(gcls_AnimTile(x,y,i))
                        if self.BG1[x][y] == anim: bg_flag = 1
                    if self.FG1[x][y] == anim or self.FG2[x][y] == anim:
                        self.sprite_AnimFG.add(gcls_AnimTile(x,y,i))
                        if self.FG1[x][y] == anim: fg_flag = 1

                if self.BG_TRANS[x][y] == 0: self.BG_TRANS[x][y] = 1
                if self.BG1[x][y] == 0: self.BG1[x][y] = 1
                if self.BG2[x][y] == 0: self.BG2[x][y] = 1
                if self.FG1[x][y] == 0: self.FG1[x][y] = 1
                if self.FG2[x][y] == 0: self.FG2[x][y] = 1
                if self.FG_TRANS[x][y] == 0: self.FG_TRANS[x][y] = 1

                # Out of range tile (INFO, SPRITE) correction
                if self.BG_TRANS[x][y] > MAXTILES: self.BG_TRANS[x][y] = 1
                if self.BG1[x][y] > MAXTILES: self.BG1[x][y] = 1
                if self.BG2[x][y] > MAXTILES: self.BG2[x][y] = 1
                if self.FG1[x][y] > MAXTILES: self.FG1[x][y] = 1
                if self.FG2[x][y] > MAXTILES: self.FG2[x][y] = 1
                if self.FG_TRANS[x][y] > MAXTILES: self.FG_TRANS[x][y] = 1
                
                if bg_flag == 0:
                    self.srfcBG_TRANS.blit(srfcTiles[self.BG_TRANS[x][y]-1], (x * TILESIZE, y * TILESIZE))
                    srfcBG1.blit(srfcTiles[self.BG1[x][y]-1], (x * TILESIZE, y * TILESIZE))
                    srfcBG2.blit(srfcTiles[self.BG2[x][y]-1], (x * TILESIZE, y * TILESIZE))
                    
                else:
                    self.srfcBG_TRANS.blit(srfcTiles[self.BG_TRANS[x][y]-1], (x * TILESIZE, y * TILESIZE))
                    srfcBG1.blit(srfcTiles[0], (x * TILESIZE, y * TILESIZE))
                    srfcBG2.blit(srfcTiles[0], (x * TILESIZE, y * TILESIZE))
                    
                if fg_flag == 0:
                    srfcFG1.blit(srfcTiles[self.FG1[x][y]-1], (x * TILESIZE, y * TILESIZE))
                    srfcFG2.blit(srfcTiles[self.FG2[x][y]-1], (x * TILESIZE, y * TILESIZE))
                    self.srfcFG_TRANS.blit(srfcTiles[self.FG_TRANS[x][y]-1], (x * TILESIZE, y * TILESIZE))
                    
                else:
                    srfcFG1.blit(srfcTiles[0], (x * TILESIZE, y * TILESIZE))
                    srfcFG2.blit(srfcTiles[0], (x * TILESIZE, y * TILESIZE))
                    self.srfcFG_TRANS.blit(srfcTiles[self.FG_TRANS[x][y]-1], (x * TILESIZE, y * TILESIZE))


                # INFO / SPRITE stuff
                testSprite = self.SPRITES[x][y]
                testInfo = self.INFO[x][y]
                switchNum = 0
                
                # Set random direction
                RND = int(round(random.random() * 1))
                if RND == 0: tempDir = -1
                else: tempDir = 1
                        
                if testInfo != 0:
                    # Draw Masks (for Debugging)
                    if testInfo == INFO_SOLID: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_SOLID))
                    elif testInfo == INFO_SOLID_NO_GRAB: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_SOLID))
                    elif testInfo == INFO_UP_RIGHT_45: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_UP_RIGHT_45))
                    elif testInfo == INFO_DOWN_RIGHT_45: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_DOWN_RIGHT_45))                    
                    elif testInfo == INFO_UP_RIGHT_30_1: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_UP_RIGHT_30_1))
                    elif testInfo == INFO_UP_RIGHT_30_2: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_UP_RIGHT_30_2))
                    elif testInfo == INFO_DOWN_RIGHT_30_1: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_DOWN_RIGHT_30_1))
                    elif testInfo == INFO_DOWN_RIGHT_30_2: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_DOWN_RIGHT_30_2))
                    
                    elif testInfo == INFO_SOLID_FROM_TOP: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_ONE_WAY_UP))
                    elif testInfo == INFO_SOLID_FROM_BOTTOM: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_ONE_WAY_DOWN))
                    elif testInfo == INFO_SOLID_FROM_LEFT: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_ONE_WAY_LEFT))
                    elif testInfo == INFO_SOLID_FROM_RIGHT: self.sprite_MaskAll.add(gcls_Mask(x, y, MASK_ONE_WAY_RIGHT))
                    
                    # Exits
                    elif testInfo >= INFO_EXIT_1 and testInfo <= INFO_EXIT_1 + 10:
                        exitID = (testInfo - INFO_EXIT_1) + 1
                        self.sprite_Exits.add(gcls_Exit(x, y, exitID))

                    # Door stuff
                    elif testInfo >= INFO_DOOR_1 and testInfo <= INFO_DOOR_1 + 15:
                        door_num = 0
                        doorFound = False
                        door_num = testInfo - INFO_DOOR_1 + 1
                        
                        # If a door was found, check if that door is already in the door list
                        # If it is in the list, set coords to (x2,y2).  Otherwise, initate it in the list with coords (x1,y1)
                        if len(self.DoorList) > 0:
                            for door in self.DoorList:
                                if door.id == door_num:
                                    doorFound = True
                                    door.update(x, y)
                                    
                        if doorFound == False:
                            self.DoorList.append(gclsDoor(door_num, x, y))

                    # Platform directions
                    elif testInfo >= INFO_PLATFORM_UP and testInfo <= INFO_PLATFORM_DOWN_RIGHT:
                        self.sprite_PlatformDirections.add(gcls_Platform_Directions(x, y, testInfo))

                    # Platform numbers
                    elif testInfo >= INFO_PLATFORM_1 and testInfo <= INFO_PLATFORM_8:
                        switchNum = testInfo - INFO_PLATFORM_1 + 1
                        
                    # Tele stuff
                    elif testInfo >= INFO_TELE_1 and testInfo <= INFO_TELE_1 + 15:
                        door_num = 0
                        doorFound = False
                        door_num = testInfo - INFO_DOOR_1 + 1
                        
                        # If a door was found, check if that door is already in the door list
                        # If it is in the list, set coords to (x2,y2).  Otherwise, initate it in the list with coords (x1,y1)
                        if len(self.DoorList) > 0:
                            for door in self.DoorList:
                                if door.id == door_num:
                                    doorFound = True
                                    door.update(x, y)
                                    
                        if doorFound == False:
                            self.DoorList.append(gclsDoor(door_num, x, y))
                            
                    # Hurt Tiles
                    elif testInfo == INFO_HURT_1 or testInfo == INFO_HURT_1w: self.sprite_Hurt.add(gcls_Hurt(x, y, 1))
                    elif testInfo == INFO_HURT_2 or testInfo == INFO_HURT_2w: self.sprite_Hurt.add(gcls_Hurt(x, y, 2))
                    elif testInfo == INFO_HURT_5 or testInfo == INFO_HURT_5w: self.sprite_Hurt.add(gcls_Hurt(x, y, 5))
                    elif testInfo == INFO_DIE or testInfo == INFO_DIEw: self.sprite_Hurt.add(gcls_Hurt(x, y, 10))
                    
                        
                    # Check to see if INFO tile was an ENEMY DIRECTION
                    # If so, set the direction to that, if not - make it random
                    elif testInfo == INFO_ENEMY_LEFT: tempDir = -1
                    elif testInfo == INFO_ENEMY_RIGHT: tempDir = 1

                    # Check to see if it's an ENEMY TELEPORTER tile
                    elif testInfo == INFO_ENEMY_TELE: self.EnemyTeleList.append(gcls_EnemyTele(x, y))
                    
                if testSprite != 0:
                    # Keen Starting Positions
                    if inKeen.checkPoint == False:
                        if testSprite == SPRITE_KEEN_LEFT:
                            self.initX = x * TILESIZE
                            self.initY = y * TILESIZE
                            self.initDirection = -1
                        elif testSprite == SPRITE_KEEN_RIGHT:
                            self.initX = x * TILESIZE
                            self.initY = y * TILESIZE
                            self.initDirection = 1
                        if testSprite == SPRITE_KEEN_LEFT_WATER:
                            self.initX = x * TILESIZE
                            self.initY = y * TILESIZE
                            self.initDirection = -1
                            self.initWater = True
                        elif testSprite == SPRITE_KEEN_RIGHT_WATER:
                            self.initX = x * TILESIZE
                            self.initY = y * TILESIZE
                            self.initDirection = 1
                            self.initWater = True
                    else:
                        self.initX = inKeen.checkX
                        self.initY = inKeen.checkY
                        self.initDirection = 1
                        
                    # Health starts
                    if testSprite == SPRITE_HEALTH1: inKeen.health -= 1
                    elif testSprite == SPRITE_HEALTH2: inKeen.health -= 2
                    elif testSprite == SPRITE_HEALTH5: inKeen.health -= 5

                    # EGA
                    elif testSprite == SPRITE_EGA: inKeen.sprite = kSPRITE_EGA
                    
                    # Backgrounds
                    elif testSprite >= SPRITE_BG and testSprite < SPRITE_BG + 10: self.background_ID = testSprite - SPRITE_BG

                    # Music
                    elif testSprite >= SPRITE_MUSIC and testSprite < SPRITE_MUSIC + 10: self.music_ID = testSprite - SPRITE_MUSIC
                        
                    # Night Mode
                    elif testSprite == SPRITE_NIGHT: self.night = True

                    # Weather
                    elif testSprite == SPRITE_RAIN:
                        #SFX[SFX_WX_RAIN].play(-1)
                        
                        for i in range(40):
                            self.sprite_WeatherBG.add(gcls_Weather(weatherRAIN, y))

                    elif testSprite == SPRITE_SNOW:
                        for i in range(40):
                            self.sprite_WeatherBG.add(gcls_Weather(weatherSNOW, y))

                    elif testSprite == SPRITE_CLOUD:
                        self.sprite_WeatherFG.add(gcls_Weather(weatherCLOUDS1, y + 2))
                        self.sprite_WeatherFG.add(gcls_Weather(weatherCLOUDS2, y + 2))
                    elif testSprite == SPRITE_LIGHTNING:
                        self.sprite_WeatherBG.add(gcls_Weather(weatherLIGHTNING, y))
                        
                    # Doors
                    elif testSprite >= SPRITE_DOOR_RED and testSprite <= SPRITE_DOOR_MAGENTA:
                        self.sprite_Doors.add(gcls_Door(x, y, testSprite - SPRITE_DOOR_RED))

                    # Platforms
                    elif testSprite == SPRITE_PLATFORM_1: self.sprite_Platforms.add(gcls_Platform(x, y, testSprite, switchNum))
                    elif testSprite == SPRITE_PLATFORM_2: self.sprite_Platforms.add(gcls_Platform(x, y, testSprite, switchNum))
                    elif testSprite == SPRITE_PLATFORM_3: self.sprite_Platforms.add(gcls_Platform(x, y, testSprite, switchNum))
                    # Switches
                    elif testSprite == SPRITE_SWITCH_1: self.sprite_Switches.add(gcls_Switch(x, y, testSprite, switchNum))
                    elif testSprite == SPRITE_SWITCH_2: self.sprite_Switches.add(gcls_Switch(x, y, testSprite, switchNum))
                    elif testSprite == SPRITE_SWITCH_3: self.sprite_Switches.add(gcls_Switch(x, y, testSprite, switchNum))
                    
                    # Collectables
                    # Keys
                    elif testSprite == SPRITE_KEY_RED: self.sprite_Items.add(gcls_Item(x, y, ITEM_KEY_RED))
                    elif testSprite == SPRITE_KEY_YELLOW: self.sprite_Items.add(gcls_Item(x, y, ITEM_KEY_YELLOW))
                    elif testSprite == SPRITE_KEY_GREEN: self.sprite_Items.add(gcls_Item(x, y, ITEM_KEY_GREEN))
                    elif testSprite == SPRITE_KEY_CYAN: self.sprite_Items.add(gcls_Item(x, y, ITEM_KEY_CYAN))
                    elif testSprite == SPRITE_KEY_BLUE: self.sprite_Items.add(gcls_Item(x, y, ITEM_KEY_BLUE))
                    elif testSprite == SPRITE_KEY_MAGENTA: self.sprite_Items.add(gcls_Item(x, y, ITEM_KEY_MAGENTA))

                    # Points
                    elif testSprite == SPRITE_JBEAN_RED:
                        self.sprite_Items.add(gcls_Item(x, y, ITEM_JBEAN_RED))
                        self.stats_NumPoints_Tot += 100
                    elif testSprite == SPRITE_JBEAN_YELLOW:
                        self.sprite_Items.add(gcls_Item(x, y, ITEM_JBEAN_YELLOW))
                        self.stats_NumPoints_Tot += 100
                    elif testSprite == SPRITE_JBEAN_GREEN:
                        self.sprite_Items.add(gcls_Item(x, y, ITEM_JBEAN_GREEN))
                        self.stats_NumPoints_Tot += 100
                    elif testSprite == SPRITE_JBEAN_CYAN:
                        self.sprite_Items.add(gcls_Item(x, y, ITEM_JBEAN_CYAN))
                        self.stats_NumPoints_Tot += 100
                    elif testSprite == SPRITE_JBEAN_BLUE:
                        self.sprite_Items.add(gcls_Item(x, y, ITEM_JBEAN_BLUE)) 
                        self.stats_NumPoints_Tot += 100
                    elif testSprite == SPRITE_JBEAN_PURPLE:
                        self.sprite_Items.add(gcls_Item(x, y, ITEM_JBEAN_PURPLE))
                        self.stats_NumPoints_Tot += 100
                    elif testSprite == SPRITE_COLA:
                        self.sprite_Items.add(gcls_Item(x, y, ITEM_COLA))
                        self.stats_NumPoints_Tot += 200
                    elif testSprite == SPRITE_BURGER:
                        self.sprite_Items.add(gcls_Item(x, y, ITEM_BURGER))
                        self.stats_NumPoints_Tot += 500
                    elif testSprite == SPRITE_GINGER:
                        self.sprite_Items.add(gcls_Item(x, y, ITEM_GINGER))
                        self.stats_NumPoints_Tot += 1000
                    elif testSprite == SPRITE_SUGAR:
                        self.sprite_Items.add(gcls_Item(x, y, ITEM_SUGAR))
                        self.stats_NumPoints_Tot += 2000
                    elif testSprite == SPRITE_CEREAL:
                        self.sprite_Items.add(gcls_Item(x, y, ITEM_CEREAL))
                        self.stats_NumPoints_Tot += 5000

                    # Health
                    elif testSprite == SPRITE_PYAPA_FRUIT: self.sprite_Items.add(gcls_Item(x, y, ITEM_PYAPA_FRUIT))
                    elif testSprite == SPRITE_PEETA_BERRIES: self.sprite_Items.add(gcls_Item(x, y, ITEM_PEETA_BERRIES))
                    elif testSprite == SPRITE_ISIS_FRUIT: self.sprite_Items.add(gcls_Item(x, y, ITEM_ISIS_FRUIT))
                    elif testSprite == SPRITE_NEPHTHYS_FRUIT: self.sprite_Items.add(gcls_Item(x, y, ITEM_NEPHTHYS_FRUIT))
                    elif testSprite == SPRITE_POTION: self.sprite_Items.add(gcls_Item(x, y, ITEM_POTION))
                    elif testSprite == SPRITE_YORP: self.sprite_Items.add(gcls_Item(x, y, ITEM_YORP))

                    # Powerups
                    elif testSprite == SPRITE_SHOES: self.sprite_Items.add(gcls_Item(x, y, ITEM_SHOES))
                    elif testSprite == SPRITE_POINTS: self.sprite_Items.add(gcls_Item(x, y, ITEM_POINTS))
                    elif testSprite == SPRITE_GOD: self.sprite_Items.add(gcls_Item(x, y, ITEM_GOD))
                    elif testSprite == SPRITE_CRAZY: self.sprite_Items.add(gcls_Item(x, y, ITEM_CRAZY))
                    elif testSprite == SPRITE_ANTI: self.sprite_Items.add(gcls_Item(x, y, ITEM_ANTI))
                    elif testSprite == SPRITE_REGEN: self.sprite_Items.add(gcls_Item(x, y, ITEM_REGEN))
                    elif testSprite == SPRITE_DEGEN: self.sprite_Items.add(gcls_Item(x, y, ITEM_DEGEN))
                    
                    # Inventory
                    elif testSprite == SPRITE_BATTERY: self.sprite_Items.add(gcls_Item(x, y, ITEM_BATTERY))
                    elif testSprite == SPRITE_SHIELD: self.sprite_Items.add(gcls_Item(x, y, ITEM_SHIELD))
                    elif testSprite == SPRITE_IONSCANNER: self.sprite_Items.add(gcls_Item(x, y, ITEM_IONSCANNER))
                    elif testSprite == SPRITE_UNKNOWN: self.sprite_Items.add(gcls_Item(x, y, ITEM_UNKNOWN))
                    
                    # Weapons
                    elif testSprite == SPRITE_BLOWGUN: self.sprite_Items.add(gcls_Item(x, y, ITEM_BLOWGUN))      
                    elif testSprite == SPRITE_ZEFFER: self.sprite_Items.add(gcls_Item(x, y, ITEM_ZEFFER))
                    elif testSprite == SPRITE_PULSAR: self.sprite_Items.add(gcls_Item(x, y, ITEM_PULSAR))
                    elif testSprite == SPRITE_SOLARIZER: self.sprite_Items.add(gcls_Item(x, y, ITEM_SOLARIZER))
                    elif testSprite == SPRITE_HR42 and inGame.custom == False: self.sprite_Items.add(gcls_Item(x, y, ITEM_HR42))
                    elif testSprite == SPRITE_PLUTEZARP and inGame.custom == False: self.sprite_Items.add(gcls_Item(x, y, ITEM_PLUTEZARP))
                    elif testSprite == SPRITE_HARPOON: self.sprite_Items.add(gcls_Item(x, y, ITEM_HARPOON))
                    elif testSprite == SPRITE_RAYGUN: self.sprite_Items.add(gcls_Item(x, y, ITEM_RAYGUN))
                    elif testSprite == SPRITE_NEURAL: self.sprite_Items.add(gcls_Item(x, y, ITEM_NEURAL))

                    # Enemies
                    elif testSprite == SPRITE_FOOG: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_FOOG, tempDir))
                    elif testSprite == SPRITE_FOOGJUMP: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_FOOGJUMP, tempDir))
                    elif testSprite == SPRITE_SPIDER: self.sprite_Enemies.add(gcls_Enemy_Shooter(x, y, SPRITE_SPIDER, tempDir))
                    elif testSprite == SPRITE_FROG_WALK: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_FROG_WALK, tempDir))
                    elif testSprite == SPRITE_FROG_SWIM: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_FROG_SWIM, tempDir))
                    elif testSprite == SPRITE_HOLEMONSTER: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_HOLEMONSTER, tempDir))
                    elif testSprite == SPRITE_BLUEMOUTH: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_BLUEMOUTH, tempDir))
                    elif testSprite == SPRITE_GARNAK: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_GARNAK, tempDir))
                    elif testSprite == SPRITE_YELLOW: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_YELLOW, tempDir))
                    elif testSprite == SPRITE_DEMON: self.sprite_Enemies.add(gcls_Enemy_Shooter(x, y, SPRITE_DEMON, tempDir))
                    elif testSprite == SPRITE_PLANTGUY: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_PLANTGUY, tempDir))
                    
                    elif testSprite == SPRITE_REDFISH: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_REDFISH, tempDir))
                    elif testSprite == SPRITE_CHOMPERFISH: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_CHOMPERFISH, tempDir))
                    elif testSprite == SPRITE_URCHIN: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_URCHIN, tempDir))
                    elif testSprite == SPRITE_FLOPPY: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_FLOPPY, tempDir))
                    elif testSprite == SPRITE_YELLOWFISH: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_YELLOWFISH, tempDir))
                    elif testSprite == SPRITE_GREENFISH: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_GREENFISH, tempDir))
                    elif testSprite == SPRITE_BLUEFISH: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_BLUEFISH, tempDir))
                    elif testSprite == SPRITE_ROCK_GREY: self.sprite_Enemies.add(gcls_Enemy_Rock(x, y, SPRITE_ROCK_GREY, tempDir))
                    elif testSprite == SPRITE_ROCK_MOSS: self.sprite_Enemies.add(gcls_Enemy_Rock(x, y, SPRITE_ROCK_MOSS, tempDir))
                    elif testSprite == SPRITE_ROCK_BROWN: self.sprite_Enemies.add(gcls_Enemy_Rock(x, y, SPRITE_ROCK_BROWN, tempDir))
                    elif testSprite == SPRITE_MINE: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_MINE, tempDir))
                    
                    elif testSprite == SPRITE_RAT: self.sprite_Enemies.add(gcls_Enemy_Shooter(x, y, SPRITE_RAT, 1))
                    elif testSprite == SPRITE_LEMMING: self.sprite_Enemies.add(gcls_Enemy_Shooter(x, y, SPRITE_LEMMING, tempDir))
                    elif testSprite == SPRITE_TRUCKGUY1: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_TRUCKGUY1, tempDir))
                    elif testSprite == SPRITE_TRUCKGUY2: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_TRUCKGUY2, tempDir))
                    elif testSprite == SPRITE_TRUCKGUY1_WALK: self.sprite_Enemies.add(gcls_Enemy_Shooter(x, y, SPRITE_TRUCKGUY1_WALK, tempDir))
                    elif testSprite == SPRITE_TRUCKGUY2_WALK: self.sprite_Enemies.add(gcls_Enemy_Shooter(x, y, SPRITE_TRUCKGUY2_WALK, tempDir))
                    elif testSprite == SPRITE_ROBOT_GREY: self.sprite_Enemies.add(gcls_Enemy_Shooter(x, y, SPRITE_ROBOT_GREY, tempDir))
                    elif testSprite == SPRITE_ROBOT_RED: self.sprite_Enemies.add(gcls_Enemy_Shooter(x, y, SPRITE_ROBOT_RED, tempDir))
                    elif testSprite == SPRITE_ROBOT_FLASHER: self.sprite_Enemies.add(gcls_Enemy_Shooter(x, y, SPRITE_ROBOT_FLASHER, tempDir))
                    elif testSprite == SPRITE_ROBOT_HOVER: self.sprite_Enemies.add(gcls_Enemy_Shooter(x, y, SPRITE_ROBOT_HOVER, tempDir))
                    elif testSprite == SPRITE_TELETURRET: self.sprite_Enemies.add(gcls_Enemy_TeleTurret(x, y, SPRITE_TELETURRET, tempDir))
                    
                    elif testSprite == SPRITE_CATERPILLAR: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_CATERPILLAR, tempDir))
                    elif testSprite == SPRITE_SNAIL: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_SNAIL, tempDir))               
                    elif testSprite == SPRITE_BIGFROG: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_BIGFROG, tempDir))
                    elif testSprite == SPRITE_DRAGONFLY: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_DRAGONFLY, tempDir))
                    elif testSprite == SPRITE_BIRD: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_BIRD, tempDir))
                    elif testSprite == SPRITE_FOOG_WARRIOR: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_FOOG_WARRIOR, tempDir))
                    elif testSprite == SPRITE_SHAPESHIFTER and inGame.custom == False: self.sprite_Enemies.add(gcls_Enemy_ShapeShifter(x, y, SPRITE_SHAPESHIFTER, tempDir))
                    elif testSprite == SPRITE_EVILKEEN and inGame.custom == False: self.sprite_Enemies.add(gcls_Enemy_EvilKeen(x, y, SPRITE_EVILKEEN, tempDir))
                    
                    elif testSprite == SPRITE_ISONIAN_GREEN: self.sprite_Enemies.add(gcls_Enemy_Isonian(x, y, SPRITE_ISONIAN_GREEN, tempDir))
                    elif testSprite == SPRITE_ISONIAN_RED: self.sprite_Enemies.add(gcls_Enemy_Isonian(x, y, SPRITE_ISONIAN_RED, tempDir))
                    elif testSprite == SPRITE_ISONIAN_WHITE: self.sprite_Enemies.add(gcls_Enemy_Isonian(x, y, SPRITE_ISONIAN_WHITE, tempDir))                    
                    elif testSprite == SPRITE_ISONIAN_GIANT1: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_ISONIAN_GIANT1, tempDir))
                    elif testSprite == SPRITE_ISONIAN_GIANT2: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_ISONIAN_GIANT2, tempDir))
                    elif testSprite == SPRITE_ISONIAN_FLY: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_ISONIAN_FLY, tempDir))
                    elif testSprite == SPRITE_YORPY: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_YORPY, tempDir))
                    elif testSprite == SPRITE_GARG: self.sprite_Enemies.add(gcls_Enemy_Walker(x, y, SPRITE_GARG, tempDir))
                    elif testSprite == SPRITE_SLUG: self.sprite_Enemies.add(gcls_Enemy_Shooter(x, y, SPRITE_SLUG, tempDir))
                    
                    elif testSprite == SPRITE_WATER_DROP: self.sprite_Enemies.add(gcls_Enemy_Drop(x, y, SPRITE_WATER_DROP, tempDir))
                    elif testSprite == SPRITE_ACID_DROP: self.sprite_Enemies.add(gcls_Enemy_Drop(x, y, SPRITE_ACID_DROP, tempDir))

                    # Checkpoints
                    elif testSprite == SPRITE_CHECKPOINT: self.sprite_CheckPoints.add(gcls_CheckPoint(x, y))
                    
                    # Statistics
                    if gfn_IsEnemy(testSprite): self.stats_NumEnemies_Tot +=1
                    if gfn_IsItem(testSprite): self.stats_NumItems_Tot +=1

        # Correct Keen health
        if inKeen.health <= 0: inKeen.health = 1
        
        # Merge BG1+BG2, and FG1+FG2
        self.srfcBG.blit(srfcBG1, (0,0))
        self.srfcBG.blit(srfcBG2, (0,0))
        self.srfcBG.set_colorkey(TRANSCOLOUR)
        self.srfcFG.blit(srfcFG1, (0,0))
        self.srfcFG.blit(srfcFG2, (0,0))
        self.srfcFG.set_colorkey(TRANSCOLOUR)

        # Remove temp surfaces
        srfcBG1 = None
        srfcBG2 = None
        srfcFG1 = None
        srfcFG2 = None
        
                

        # Update Keen stuff
        inKeen.x = self.initX
        inKeen.y = self.initY
        inKeen.rect = pygame.Rect(inKeen.x - self.mapX + self.playX, inKeen.y - self.mapY + self.playY, 48, 48)
        inKeen.direction = self.initDirection
        inKeen.timeElapsed = 0.1
        
        if self.initWater == False:
            inKeen.state = kFALLING
        else:
            inKeen.state = kIN_WATER
        
        # Load Parallaxing Background
        self.srfcPBG = pygame.image.load(gfn_Zip(inGame.backgrounds[self.background_ID])).convert()
        self.bgMoveX = (self.srfcPBG.get_width() - self.playWidth) / (self.width * TILESIZE)
        self.bgMoveY = (self.srfcPBG.get_height() - self.playHeight) / (self.height * TILESIZE)

        # Reset enemy time elapsed
        for enemy in self.sprite_Enemies:
            enemy.oldTime = pygame.time.get_ticks()
            enemy.timeElapsed = 0.1

        # Initial camera Y
        self.mapY = inKeen.y - (self.playHeight / 2)

        
    # Snaps the camera right away (eg new level, through a door)
    def snapCamera(self, inKeen):
            middleGroundX = inKeen.x + (inKeen.width / 2.0) - (self.playWidth / 2)
            if middleGroundX < 0: middleGroundX = 0
            if middleGroundX > (self.width * TILESIZE) - self.playWidth: middleGroundX = (self.width * TILESIZE) - self.playWidth

            middleGroundY = inKeen.y - (self.playHeight / 2) + int(inKeen.lookOffsetY)
            if middleGroundY < 0: middleGround = 0
            if middleGroundY > (self.height * TILESIZE) - self.playHeight: middleGround = (self.height * TILESIZE) - self.playHeight
            
            # Map limits
            if inKeen.y - TILESIZE + int(inKeen.lookOffsetY) <= 0:
                self.mapY = 0
            elif inKeen.y + inKeen.height + (TILESIZE * 2) + int(inKeen.lookOffsetY) >= (self.height * TILESIZE):
                self.mapY = (self.height * TILESIZE) - self.playHeight - 1

            else:
                self.mapX = middleGroundX
                self.mapY = middleGroundY
        
    def updateCamera(self, inKeen):
        # Update Camera
        if inKeen.state != kON_LEDGE:
            
            # CAMERA X
            """
            # OLD CAMERA - keeps Keen centered
            if inKeen.x + int(inKeen.lookOffsetX) <= self.playWidth / 2:
                self.mapX = 0
            elif inKeen.x + int(inKeen.lookOffsetX) >= (self.width * TILESIZE) - (self.playWidth / 2):
                self.mapX = (self.width * TILESIZE) - self.playWidth
            else:
                self.mapX = inKeen.x - (self.playWidth / 2) + int(inKeen.lookOffsetX)
            """

            # NEW CAMERA - gives a buffer where the camera doesn't move
            tileBuffer = 6.5 * TILESIZE # How much Keen can move in the middle without scrolling is 16 - (6.5 * 2) = 3
            testKeenX = inKeen.x + (inKeen.width / 2.0) + int(inKeen.lookOffsetX)
            if (testKeenX - self.mapX) < tileBuffer:
                self.mapX = testKeenX - tileBuffer
            elif (self.mapX + self.playWidth - testKeenX) < tileBuffer:
                self.mapX = testKeenX + tileBuffer - self.playWidth

            if self.mapX < 0: self.mapX = 0
            elif self.mapX > (self.width * TILESIZE) - self.playWidth: self.mapX = (self.width * TILESIZE) - self.playWidth

                
            # CAMERA Y
            cameraVy = 150
            middleGround = inKeen.y - (self.playHeight / 2) + int(inKeen.lookOffsetY)
            if middleGround < 0: middleGround = 0
            if middleGround > (self.height * TILESIZE) - self.playHeight: middleGround = (self.height * TILESIZE) - self.playHeight
            
            # Map limits
            if inKeen.y - TILESIZE + int(inKeen.lookOffsetY) <= 0:
                self.mapY = 0
            elif inKeen.y + inKeen.height + (TILESIZE * 2) + int(inKeen.lookOffsetY) >= (self.height * TILESIZE):
                self.mapY = (self.height * TILESIZE) - self.playHeight - 1

            # Land on something
            elif inKeen.state == kON_GROUND or inKeen.state == kIN_WATER or inKeen.state == kON_POLE or inKeen.state == kON_LEDGE:
                # Camera moves up
                if self.mapY > middleGround:
                    self.mapY -= inKeen.timeElapsed * cameraVy
                    if self.mapY < middleGround: self.mapY = middleGround
                # Camera moves down
                elif self.mapY < middleGround:
                    self.mapY += inKeen.timeElapsed * cameraVy
                    if self.mapY > middleGround: self.mapY = middleGround

            # Falling / Jumping 
            elif inKeen.state == kFALLING:

                # Falling off bottom
                if inKeen.y + inKeen.height + (TILESIZE * 2) > self.mapY + self.playHeight:
                    self.mapY = inKeen.y + inKeen.height + (TILESIZE * 2) - self.playHeight
                # Jumping high
                elif inKeen.y - TILESIZE < self.mapY:
                    self.mapY = inKeen.y - TILESIZE

                # Adjust lookOffset if looking
                if inKeen.lookOffsetY != 0:
                    inKeen.lookOffsetY += (self.mapY - middleGround)

            # Update PBG
            self.bgX = round(self.mapX * self.bgMoveX)
            self.bgY = round(self.mapY * self.bgMoveY)

            # Round mapX, mapY
            self.mapX, self.mapY = round(self.mapX), round(self.mapY)
            
def gfn_GetInfo(inLevel, inRect):
    layerInfo = inLevel.INFO
    checkTiles = []

    # Check the 9 positions
    checkTiles.append(layerInfo[int(inRect.topleft[0] / TILESIZE)][int(inRect.topleft[1] / TILESIZE)])
    checkTiles.append(layerInfo[int(inRect.midtop[0] / TILESIZE)][int(inRect.midtop[1] / TILESIZE)])
    checkTiles.append(layerInfo[int(inRect.topright[0] / TILESIZE)][int(inRect.topright[1] / TILESIZE)])
    checkTiles.append(layerInfo[int(inRect.midleft[0] / TILESIZE)][int(inRect.midleft[1] / TILESIZE)])
    checkTiles.append(layerInfo[int(inRect.center[0] / TILESIZE)][int(inRect.center[1] / TILESIZE)])
    checkTiles.append(layerInfo[int(inRect.midright[0] / TILESIZE)][int(inRect.midright[1] / TILESIZE)])
    checkTiles.append(layerInfo[int(inRect.bottomleft[0] / TILESIZE)][int(inRect.bottomleft[1] / TILESIZE)])
    checkTiles.append(layerInfo[int(inRect.midbottom[0] / TILESIZE)][int(inRect.midbottom[1] / TILESIZE)])
    checkTiles.append(layerInfo[int(inRect.bottomright[0] / TILESIZE)][int(inRect.bottomright[1] / TILESIZE)])
    
    # Return the result
    return checkTiles
