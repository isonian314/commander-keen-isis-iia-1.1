# isis_cutscenes.py
import pygame, array
pygame.init()
from isis_draw import *
from isis_zip import *
from isis_font import *
from isis_constants import *

# Loads Cut-Scenes into a 2D array of (320x200) surfaces
# If there are N levels:
#   CutScene[0  ][0...m] = Intro
#   CutScene[i  ][0...m] = Level i
#   CutScene[N+1][0...m] = Ending

srfcCheckPoints = gfnLoad_Splice(16, 16, gfn_Zip("checkpoints.png"), 1, 1)

def gfn_LoadCutscenes():
    tempCutScenes = []
    tempCutScenes.append(gfnLoad_Splice(320, 200, gfn_Zip("cutscene-intro.png"), 0, 0))
    tempCutScenes.append(gfnLoad_Splice(320, 200, gfn_Zip("cutscene1.png"), 0, 0))
    tempCutScenes.append(gfnLoad_Splice(320, 200, gfn_Zip("cutscene2.png"), 0, 0))
    tempCutScenes.append(gfnLoad_Splice(320, 200, gfn_Zip("cutscene3.png"), 0, 0))
    tempCutScenes.append(gfnLoad_Splice(320, 200, gfn_Zip("cutscene4.png"), 0, 0))
    tempCutScenes.append(gfnLoad_Splice(320, 200, gfn_Zip("cutscene5.png"), 0, 0))
    tempCutScenes.append(gfnLoad_Splice(320, 200, gfn_Zip("cutscene6.png"), 0, 0))
    tempCutScenes.append(gfnLoad_Splice(320, 200, gfn_Zip("cutscene7.png"), 0, 0))
    tempCutScenes.append(gfnLoad_Splice(320, 200, gfn_Zip("cutscene8.png"), 0, 0))
    tempCutScenes.append(gfnLoad_Splice(320, 200, gfn_Zip("cutscene9.png"), 0, 0))
    tempCutScenes.append(gfnLoad_Splice(320, 200, gfn_Zip("cutscene-ending.png"), 0, 0))
    return tempCutScenes

def gfn_LoadCutSceneNames():
    tempCSNames = []
    tempCSNames.append("cutscene-intro.png")
    tempCSNames.append("cutscene1.png")
    tempCSNames.append("cutscene2.png")
    tempCSNames.append("cutscene3.png")
    tempCSNames.append("cutscene4.png")
    tempCSNames.append("cutscene5.png")
    tempCSNames.append("cutscene6.png")
    tempCSNames.append("cutscene7.png")
    tempCSNames.append("cutscene8.png")
    tempCSNames.append("cutscene9.png")
    tempCSNames.append("cutscene-ending.png")
    tempCSNames.append("cutscene5.png")
    tempCSNames.append("cutscene5.png")
    tempCSNames.append("cutscene5.png")
    tempCSNames.append("cutscene5.png")
    tempCSNames.append("cutscene5.png")
    tempCSNames.append("cutscene5.png")
    tempCSNames.append("cutscene-ending.png")
    return tempCSNames

# Load Level list - should match # of cut-scenes
def gfn_LoadLevels():
    tempLevels = []

    #tempLevels.append("dummy1.tmx")
    #tempLevels.append("dummy2.tmx")
    #tempLevels.append("dummy3.tmx")
    #tempLevels.append("dummy4.tmx")
    #tempLevels.append("dummy5.tmx")
    #tempLevels.append("doortest.tmx")
    #tempLevels.append("clock.tmx")
    #tempLevels.append("level1-test.tmx")
    tempLevels.append("level1-jungle.tmx")
    tempLevels.append("level2-jungle.tmx")
    tempLevels.append("level3-mountain.tmx")
    tempLevels.append("level4-cave.tmx")
    tempLevels.append("level5-minefield.tmx")
    tempLevels.append("level6-artillery.tmx")
    tempLevels.append("level7-hangar.tmx")
    tempLevels.append("level8-central_command.tmx")
    tempLevels.append("level9-dungeon.tmx")
    
    return tempLevels

def gfn_LoadLevelNames():
    tempNames = []
    tempNames.append("Jungle")
    tempNames.append("Jungle Nights")
    tempNames.append("Mountain")
    tempNames.append("Cave")
    tempNames.append("Minefield")
    tempNames.append("Artillery Division")
    tempNames.append("Hangar")
    tempNames.append("Central Command")
    tempNames.append("Dungeon")
    tempNames.append("Barracks")
    tempNames.append("Missile Tower")
    tempNames.append("Ocean Moat")
    tempNames.append("Secret Island")
    tempNames.append("Castle Garden")
    tempNames.append("Imperial Castle")
    tempNames.append("Rooftop Showdown")
    return tempNames
    
# Background List
def gfn_LoadBackgrounds():
    tempBGs = []
    tempBGs.append("bg0.png")
    tempBGs.append("bg1.png")
    tempBGs.append("bg2.png")
    tempBGs.append("bg3.png")
    tempBGs.append("bg4.png")
    tempBGs.append("bg5.png")
    tempBGs.append("bg6.png")
    tempBGs.append("bg7.png")
    return tempBGs

class gcls_CheckPoint(pygame.sprite.Sprite):
    def __init__(self, inX, inY):
        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.image = srfcCheckPoints[0]
        self.active = True
        self.rect = pygame.Rect(round(self.x), round(self.y), TILESIZE, TILESIZE)
        
    def update(self, inLevel):
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, TILESIZE, TILESIZE)
    
# Game State
STATE_MENU = 0
STATE_LEVEL = 1
STATE_CUTSCENE = 2
STATE_FADEOUT_NEXTLEVEL = 3
STATE_FADEOUT_KILL = 4
STATE_FADEOUT_GAMEOVER = 5

# Progress Screen Surfaces
srfcStarOutline = pygame.image.load(gfn_Zip("progress_star-outline.png")).convert_alpha()
srfcStarFilled = pygame.image.load(gfn_Zip("progress_star-filled.png")).convert_alpha()
srfcStarShadow = pygame.image.load(gfn_Zip("progress_star-shadow.png")).convert_alpha()
srfcBoxRed = pygame.image.load(gfn_Zip("progress_box-red.png")).convert_alpha()
srfcBoxGreen = pygame.image.load(gfn_Zip("progress_box-green.png")).convert_alpha()
srfcBoxGrey = pygame.image.load(gfn_Zip("progress_box-grey.png")).convert_alpha()
srfcInventory = gfnLoad_Splice(16, 16, gfn_Zip("progress_inventory.png"), 1, 1)


class gcls_Game():
    def __init__(self):
        self.level = gfn_LoadLevels()
        self.level_names = gfn_LoadLevelNames()
        self.level_ID = 0
        self.CSNames = gfn_LoadCutSceneNames()
        self.srfcCutScenes = gfnLoad_Splice(320, 200, gfn_Zip(self.CSNames[0]), 0, 0)
        self.cutScene_ID = 0
        self.state = STATE_CUTSCENE
        self.displayWidth = 320
        self.displayHeight = 200
        self.backgrounds = gfn_LoadBackgrounds()
        self.srfcNight = pygame.image.load(gfn_Zip("night.png")).convert(16)
        self.srfcNight.set_alpha(0.40 * 255)
        self.fadeIn = True
        self.fadeOut = False
        self.fadeTime = 0.5
        self.fadeTimer = self.fadeTime

        self.sound = True
        self.music = True
        
        # Availability of Levels (if they've been completed before), as well as lives & points to start from
        #self.level_rankings, self.level_lives, self.level_points, self.level_weapons, self.level_inventory = gfn_LoadSavedData()
        
        # LOAD SAVEGAME.IS2 (if exists) OTHERWISE FILL WITH DEFAULTS
        self.SAVED_DATA = gfn_LoadSaveDataNew()
        
        # Debug
        self.debug = gcls_Debug()

        # Custom level
        self.custom = False
        self.customLevel = None
        
    def reset(self):
        self.level_ID = 1
        self.cutScene_ID = 0
        self.custom = False
        self.customLevel = None
        
    def drawStats(self, inLevel, inKeen, inOldLevel, inNextLevel):
        
        # Calculations
        if inLevel.stats_NumItems_Tot != 0: tempItemsPercent = round((inLevel.stats_NumItems / inLevel.stats_NumItems_Tot) * 100.0, 1)
        else: tempItemsPercent = 100
        
        if inLevel.stats_NumPoints_Tot != 0: tempPointsPercent = round((inLevel.stats_NumPoints / inLevel.stats_NumPoints_Tot) * 100.0, 1)
        else: tempPointsPercent = 100
        
        if inLevel.stats_NumEnemies_Tot != 0: tempEnemiesPercent = round((inLevel.stats_NumEnemies / inLevel.stats_NumEnemies_Tot) * 100.0, 1)
        else: tempEnemiesPercent = 100
        
        """
        # Star calc here - OLD RATING
        # Stars (Level Rating)
        # 10 - 100% points, items, enemies
        #  9 - 100% points, items
        #  8 - 100% points
        #  7 - points <= 90%
        #  6 - points <= 70%
        #  5 - points <= 50%
        #  4 - points <= 30%
        #  3 - points <= 20%
        #  2 - points > 0%
        #  1 - all 0%

        if tempPointsPercent == 100 and tempItemsPercent == 100 and tempEnemiesPercent == 100: tempRating = 10
        elif tempPointsPercent == 100 and tempItemsPercent == 100:  tempRating = 9
        elif tempPointsPercent == 100 : tempRating = 8
        elif tempPointsPercent >= 90: tempRating = 7
        elif tempPointsPercent >= 70: tempRating = 6
        elif tempPointsPercent >= 50: tempRating = 5
        elif tempPointsPercent >= 30: tempRating = 4
        elif tempPointsPercent >= 10: tempRating = 3
        elif tempPointsPercent > 0: tempRating = 2
        else: tempRating = 1
        """
        
        # NEW RATING
        # 10 - 100% items, enemies
        #  9 - 100% items
        #  8 - items >= 90%
        #  7 - items >= 75%
        #  6 - items >= 60%
        #  5 - items >= 45%
        #  4 - items >= 30%
        #  3 - items >= 15%
        #  2 - items > 0%
        #  1 - all 0%

        """
        # OLD RATING
        if tempItemsPercent == 100 and tempEnemiesPercent == 100: tempRating = 10
        elif tempItemsPercent == 100:  tempRating = 9
        elif tempItemsPercent >= 90 : tempRating = 8
        elif tempItemsPercent >= 75: tempRating = 7
        elif tempItemsPercent >= 60: tempRating = 6
        elif tempItemsPercent >= 45: tempRating = 5
        elif tempItemsPercent >= 30: tempRating = 4
        elif tempItemsPercent >= 15: tempRating = 3
        elif tempItemsPercent > 0: tempRating = 2
        else: tempRating = 1        
        """

        if tempItemsPercent == 100:  tempRating = 10
        elif tempItemsPercent >= 90: tempRating = 9
        elif tempItemsPercent >= 80: tempRating = 8
        elif tempItemsPercent >= 70: tempRating = 7
        elif tempItemsPercent >= 60: tempRating = 6
        elif tempItemsPercent >= 50: tempRating = 5
        elif tempItemsPercent >= 40: tempRating = 4
        elif tempItemsPercent >= 30: tempRating = 3
        elif tempItemsPercent >= 20: tempRating = 2
        else: tempRating = 1 
        

        # Set points, lives, stars, weapons, inventory
        #if inKeen.score > self.level_points[self.level_ID - 1]: self.level_points[self.level_ID - 1] = inKeen.score
        #if inKeen.lives > self.level_lives[self.level_ID - 1]: self.level_lives[self.level_ID - 1] = inKeen.lives
        #if tempRating > self.level_rankings[self.level_ID - 1]: self.level_rankings[self.level_ID - 1] = tempRating
        #if self.level_rankings[inNextLevel - 1] == -1: self.level_rankings[inNextLevel - 1] = 0
        
        # Write new file
        #gfn_WriteSavedData(self.level_rankings, self.level_lives, self.level_points)

        # UPDATE SAVED_DATA and SAVE NEW FILE
        self.SAVED_DATA[inOldLevel - 1].ranking = tempRating
        self.SAVED_DATA[inOldLevel - 1].lives = inKeen.lives
        self.SAVED_DATA[inOldLevel - 1].health = inKeen.health
        self.SAVED_DATA[inOldLevel - 1].points = inKeen.score
        self.SAVED_DATA[inOldLevel - 1].ammo = [inKeen.weapon[i].ammo for i in range(9)]
        self.SAVED_DATA[inOldLevel - 1].inventory = [inKeen.inventory[i].power for i in range(4)]
        self.SAVED_DATA[inOldLevel - 1].inventory.append(inKeen.invMaxPower)
        if self.SAVED_DATA[inNextLevel - 1].ranking == -1: self.SAVED_DATA[inNextLevel - 1].ranking = 0
        gfn_WriteSaveDataNew(self.SAVED_DATA)
        
        # Text
        txt_Heading1 = "Commander Keen in..."
        txt_Heading2 = "The Mystery of Isis IIa"
        txt_Heading3 = "Level " + str(inOldLevel) + " - '" + self.level_names[inOldLevel - 1] + "' - Complete!"
        txt_Item1 = "- Items Collected: " + str(inLevel.stats_NumItems) + "/" + str(int(inLevel.stats_NumItems_Tot)) + " (" + str(tempItemsPercent) + "%)"
        txt_Item2 = "- Points Scored: " + str(inLevel.stats_NumPoints) + "/" + str(int(inLevel.stats_NumPoints_Tot)) + " (" + str(tempPointsPercent) + "%)"
        txt_Item3 = "- Enemies Killed: " + str(inLevel.stats_NumEnemies) + "/" + str(int(inLevel.stats_NumEnemies_Tot)) + " (" + str(tempEnemiesPercent) + "%)"
        txt_LevelRating = "Your rating:"
        txt_GameProgress = "Overall Game Progress:"
        #txt_GameRatings = self.level_rankings
        txt_Battery = "17/20"
        txt_Code = "KEEN"

        # Sizes
        STAR_SPACING = 3
        width_h2, height_h2 = fontGREMLINS.size(txt_Heading2)
        width_h3, height_h3 = fontCK_MEDIUM.size(txt_Heading3)
        width_item1, height_item1 = fontCK_MEDIUM.size(txt_Item1)
        width_star, height_star = srfcStarOutline.get_width(), srfcStarOutline.get_height()
        width_stars = (width_star * 10) + (STAR_SPACING * 9)
        width_box, height_box = srfcBoxRed.get_width(), srfcBoxRed.get_height()
        width_boxes = width_box * 16
        width_inventory, height_inventory = srfcInventory[0].get_width(), srfcInventory[0].get_height()
        width_battery, height_battery = fontCK_SMALL.size(txt_Battery)
        width_code, height_code = fontSGA_ROUND.size(txt_Code)

        # Positions
        POS_HEAD1 = [10, 10]
        POS_HEAD2 = [(self.displayWidth - width_h2) / 2.0, 20]
        POS_HEAD3 = [(self.displayWidth - width_h3) / 2.0, 50]
        POS_INDENT = [40, 70]
        POS_EXTRA = 3
        POS_ITEM1 = [POS_INDENT[0], POS_INDENT[1] + ((height_item1 + POS_EXTRA) * 0)]
        POS_ITEM2 = [POS_INDENT[0], POS_INDENT[1] + ((height_item1 + POS_EXTRA) * 1)]
        POS_ITEM3 = [POS_INDENT[0], POS_INDENT[1] + ((height_item1 + POS_EXTRA) * 2)]
        POS_LEVEL_RATING = [POS_INDENT[0], POS_INDENT[1] +((height_item1 + POS_EXTRA) * 3.6)]
        POS_STAR = [(self.displayWidth - width_stars) / 2.0, POS_LEVEL_RATING[1] + 14]
        POS_GAME_PROGRESS = [POS_HEAD1[0], POS_STAR[1] + height_star + 10]
        POS_BOXES = [(self.displayWidth - width_boxes) / 2.0, POS_GAME_PROGRESS[1] + 11]
        POS_INVENTORY = [270, 55]
        POS_CODE = [self.displayWidth - width_code - 5, 5]

        # Headings
        txtr_Heading1 = fontCK_SMALL.render(txt_Heading1, 1, (255, 255, 255))
        txtr_Heading2 = fontGREMLINS.render(txt_Heading2, 1, (255, 255, 255))
        txtr_Heading2s = fontGREMLINS.render(txt_Heading2, 1, (100, 100, 100))
        txtr_Heading3 = fontCK_MEDIUM.render(txt_Heading3, 1, (100, 100, 255))
        txtr_Item1 = fontCK_MEDIUM.render(txt_Item1, 1, (255, 255, 255))
        txtr_Item2 = fontCK_MEDIUM.render(txt_Item2, 1, (255, 255, 255))
        txtr_Item3 = fontCK_MEDIUM.render(txt_Item3, 1, (255, 255, 255))
        txtr_LevelRating = fontCK_MEDIUM.render(txt_LevelRating, 1, (255, 255, 255))
        txtr_GameProgress = fontCK_SMALL.render(txt_GameProgress, 1, (255, 255, 255))
        txtr_Battery = fontCK_SMALL.render(txt_Battery, 1, (129, 255, 44))
        txtr_Code = fontSGA_ROUND.render(txt_Code, 1, (255, 75, 75))
                                   
        # Display
        self.srfcCutScenes[0].fill((0, 0, 0))
        self.srfcCutScenes[0].blit(txtr_Heading1, (POS_HEAD1[0], POS_HEAD1[1]))
        self.srfcCutScenes[0].blit(txtr_Heading2s, (POS_HEAD2[0]+1, POS_HEAD2[1]+1))
        self.srfcCutScenes[0].blit(txtr_Heading2, (POS_HEAD2[0], POS_HEAD2[1]))
        self.srfcCutScenes[0].blit(txtr_Heading3, (POS_HEAD3[0], POS_HEAD3[1]))
        self.srfcCutScenes[0].blit(txtr_Item1, (POS_ITEM1[0], POS_ITEM1[1]))
        self.srfcCutScenes[0].blit(txtr_Item2, (POS_ITEM2[0], POS_ITEM2[1]))
        self.srfcCutScenes[0].blit(txtr_Item3, (POS_ITEM3[0], POS_ITEM3[1]))
        self.srfcCutScenes[0].blit(txtr_LevelRating, (POS_LEVEL_RATING[0], POS_LEVEL_RATING[1]))
        self.srfcCutScenes[0].blit(txtr_GameProgress, (POS_GAME_PROGRESS[0], POS_GAME_PROGRESS[1]))

        for i in range(10):
            posX = POS_STAR[0] + ((width_star + STAR_SPACING) * i)
            posY = POS_STAR[1]
            self.srfcCutScenes[0].blit(srfcStarShadow, (posX + 1, posY + 1))
            if i < tempRating: self.srfcCutScenes[0].blit(srfcStarFilled, (posX, posY))
            else: self.srfcCutScenes[0].blit(srfcStarOutline, (posX, posY))

        # Boxes (Game Progress)
        for i in range(16):
            posX = POS_BOXES[0] + (width_box * i)
            posY = POS_BOXES[1]
            
            #tempTextRating = str(txt_GameRatings[i])
            tempTextRating = str(self.SAVED_DATA[i].ranking)
            txtr_tempTextRating = fontCK_SMALL.render(tempTextRating, 1, (255, 255, 255))
            width_tempTextRating, height_tempTextRating = fontCK_SMALL.size(tempTextRating)
            posX2 = posX + ((width_box - width_tempTextRating) / 2.0)
            posY2 = posY + ((height_box - height_tempTextRating) / 2.0)

            if self.SAVED_DATA[i].ranking > 0:
                self.srfcCutScenes[0].blit(srfcBoxGreen, (posX, posY))
                self.srfcCutScenes[0].blit(txtr_tempTextRating, (posX2, posY2))
            elif i < len(self.level):
                self.srfcCutScenes[0].blit(srfcBoxRed, (posX, posY))
                if self.SAVED_DATA[i].ranking > 0: self.srfcCutScenes[0].blit(txtr_tempTextRating, (posX2, posY2))
            else:
                self.srfcCutScenes[0].blit(srfcBoxGrey, (posX, posY))

DEBUG_NIL = 0
DEBUG_HELLO = 1
DEBUG_STATS = 2

# Debug class
class gcls_Debug():
    def __init__(self):
        self.COLS = [(255, 255, 255), (128, 128, 128), (0, 0, 0)]
        self.on = False
        self.hidden = False
        self.message = DEBUG_NIL
        self.messageCol = 0
        self.jump = False
