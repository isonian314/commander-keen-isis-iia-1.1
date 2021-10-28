# isis_menu.py
# Contains input handling for Menus
import pygame
#from wxPython.wx import *
import wx
from pygame.locals import *
from isis_draw import *
from isis_zip import *
from isis_font import *
from isis_music import *
from isis_constants import *
import os

#TRANSCOLOUR = (129, 255, 44)

# Menu Constants
# Menu Related Variables

# Level 1
MENU_MAIN = 0
MENU_HELP = 1
MENU_DISPLAYTEXT = 2
MENU_LOAD = 3
MENU_OPTIONS = 4

# Level 1-1
MENU1_NEW = 0
MENU1_LOAD = 1
MENU1_OPTIONS = 2
MENU1_QUIT = 3

# Level 2-1
MENUHELP_CONTROLS = 0
MENUHELP_STORY = 1
MENUHELP_ITEMS = 2
MENUHELP_HISTORY = 3

# Level load text
txt_Levels = []
for i in range(16):
    txt_Levels.append("Level " + str(i+1))


# Menu class
# Tells us where we are in the menu structure
class gcls_Menu():
    def __init__(self):
        # Menu variables & indexes
        self.menuType = MENU_MAIN
        self.menuIndex = MENU1_NEW
        self.menuIndexMax = 3
        self.menuHelpIndex = MENUHELP_CONTROLS
        self.menuHelpIndexMax = 4
        self.menuHelpTextY = 0
        self.menuOptionsIndex = 0
        self.menuOptionsMax = 3
        
        self.moveSpeed = 100
        self.active = True

        self.menuLoadIndex = 0
        self.menuLoadMax = 15
        
        # Menu images
        self.srfcBlank = pygame.image.load(gfn_Zip("menu_blank.png")).convert()
        self.srfcMain = gfnLoad_Splice(320, 200, gfn_Zip("menu_main.png"), 0, 0)
        self.srfcHelp = gfnLoad_Splice(320, 200, gfn_Zip("menu_help.png"), 0, 0)

        self.HelpTextNames = []
        #self.srfcHelpText.append(pygame.image.load(gfn_Zip("menu_controls.png")).convert_alpha())
        #self.srfcHelpText.append(pygame.image.load(gfn_Zip("menu_story.png")).convert_alpha())
        #self.srfcHelpText.append(pygame.image.load(gfn_Zip("menu_isis.png")).convert_alpha())
        #self.srfcHelpText.append(pygame.image.load(gfn_Zip("menu_items.png")).convert_alpha())
        #self.srfcHelpText.append(pygame.image.load(gfn_Zip("menu_history.png")).convert_alpha())
        self.HelpTextNames.append("menu_controls.png")
        self.HelpTextNames.append("menu_story.png")
        self.HelpTextNames.append("menu_isis.png")
        self.HelpTextNames.append("menu_items.png")
        self.HelpTextNames.append("menu_history.png")
        self.srfcHelpText = None
        
        self.srfcHelpTitles = gfnLoad_Splice(188, 18, gfn_Zip("menu_help_titles.png"), 0, 0)

        self.srfcOptions = gfnLoad_Splice(320, 200, gfn_Zip("menu_options.png"), 0, 0)
        self.srfcOnOff = gfnLoad_Splice(52, 10, gfn_Zip("menu_onoff.png"), 0, 1)
        # Level selected (for load levels)
        self.level_selected = 0
        
        # Set initial menu
        self.srfcCurrent = self.srfcMain[0].copy()

    def update(self, inGame):
        if self.menuType == MENU_MAIN:
            self.srfcCurrent.blit(self.srfcMain[self.menuIndex], (0,0))
        elif self.menuType == MENU_HELP:
            self.srfcCurrent.blit(self.srfcHelp[self.menuHelpIndex], (0,0))
        elif self.menuType == MENU_OPTIONS:
            self.srfcCurrent.blit(self.srfcOptions[self.menuOptionsIndex], (0,0))

            if inGame.sound == True: self.srfcCurrent.blit(self.srfcOnOff[0], (172, 84))
            else: self.srfcCurrent.blit(self.srfcOnOff[1], (172, 84))

            if inGame.music == True: self.srfcCurrent.blit(self.srfcOnOff[0], (172, 102))
            else: self.srfcCurrent.blit(self.srfcOnOff[1], (172, 102))
            
        elif self.menuType == MENU_DISPLAYTEXT:
            srfcTempText = self.srfcHelpText.subsurface(0, self.menuHelpTextY, 320, 84)
            self.srfcCurrent.blit(self.srfcBlank, (0, 0))
            self.srfcCurrent.blit(srfcTempText, (0, 58))
            self.srfcCurrent.blit(self.srfcHelpTitles[self.menuHelpIndex], (65, 37))
            # Remove big files
            srfcTempTextFull = None
            srfcTempText = None
            
        elif self.menuType == MENU_LOAD:
            self.srfcCurrent.blit(self.srfcBlank, (0, 0))
            self.srfcCurrent.blit(self.srfcHelpTitles[5], (65, 37))
            for i in range(8):
                if int(inGame.SAVED_DATA[i].ranking) == -1 and i <> 0: tempText = fontCK_SMALL.render(txt_Levels[i], 1, (100, 100, 200))
                else: tempText = fontCK_SMALL.render(txt_Levels[i], 1, (255, 255, 255))
                self.srfcCurrent.blit(tempText, (100, 62 + (i*10)))

            for i in range(8):
                if int(inGame.SAVED_DATA[i+8].ranking) == -1: tempText = fontCK_SMALL.render(txt_Levels[i+8], 1, (100, 100, 200))
                else: tempText = fontCK_SMALL.render(txt_Levels[i+8], 1, (255, 255, 255))
                self.srfcCurrent.blit(tempText, (170, 62 + (i*10)))

            tempCol = (255, 0, 0)
            if self.menuLoadIndex < 8: tempRect = pygame.Rect(96, 60 + (self.menuLoadIndex * 10), 50, 10)
            else:  tempRect = pygame.Rect(166, 60 + ((self.menuLoadIndex - 8) * 10), 50, 10)
            
            pygame.draw.rect(self.srfcCurrent, tempCol, tempRect, 1)
            
# Handle Menu Input
def gfn_MenuInput(inMenu, inEventKey, inTimeElapsed, inGame, inKeen):
    willQuit = False
    
    if inMenu.menuType == MENU_MAIN:
                    
        if inEventKey == K_DOWN:
            if inMenu.menuIndex < inMenu.menuIndexMax:
                inMenu.menuIndex += 1
        if inEventKey == K_UP:
            if inMenu.menuIndex > 0:
                inMenu.menuIndex -= 1
        if inEventKey == K_F1:
                inMenu.menuType = MENU_HELP
        if inEventKey == K_ESCAPE:
            willQuit = True
        if inEventKey == K_RETURN:
            if inMenu.menuIndex == 0:
                # NEW GAME - reset Keen stuff and Game stuff
                inKeen.reset()
                inGame.level_ID = 1
                inGame.srfcCutScenes = gfnLoad_Splice(320, 200, gfn_Zip(inGame.CSNames[0]), 0, 0)
                inGame.cutScene_ID = 0
                inMenu.active = False
                
            elif inMenu.menuIndex == 1: inMenu.menuType = MENU_LOAD
            elif inMenu.menuIndex == 2: inMenu.menuType = MENU_OPTIONS
            elif inMenu.menuIndex == 3: willQuit = True
            
    elif inMenu.menuType == MENU_LOAD:
        if inEventKey == K_DOWN:
            if inMenu.menuLoadIndex < inMenu.menuLoadMax:
                if inGame.SAVED_DATA[inMenu.menuLoadIndex + 1].ranking >= 0:
                    inMenu.menuLoadIndex += 1
                    
        if inEventKey == K_UP:
            if inMenu.menuLoadIndex > 0:
                if inGame.SAVED_DATA[inMenu.menuLoadIndex - 1].ranking >= 0:
                    inMenu.menuLoadIndex -= 1
                    
        if inEventKey == K_RETURN:
            inGame.level_ID = inMenu.menuLoadIndex + 1
            inGame.cutScene_ID = 1
            inMenu.active = False

            # Now load saved data into Keen object
            inKeen.hasKey = [False, False, False, False, False, False]
            inKeen.lives = inGame.SAVED_DATA[inGame.level_ID - 2].lives
            inKeen.health = inGame.SAVED_DATA[inGame.level_ID - 2].health
            inKeen.score = inGame.SAVED_DATA[inGame.level_ID - 2].points
            for i in range(9):
                inKeen.weapon[i].ammo = inGame.SAVED_DATA[inGame.level_ID - 2].ammo[i]
            for i in range(4):
                inKeen.inventory[i].power = inGame.SAVED_DATA[inGame.level_ID - 2].inventory[i]
            inKeen.invMaxPower = inGame.SAVED_DATA[inGame.level_ID - 2].inventory[4]

            # Select weapon
            inKeen.currentWeapon = 0
            count = 0
            # Choose another weapon
            while inKeen.weapon[inKeen.currentWeapon].ammo <= 0 and count < 6:
                inKeen.currentWeapon += 1
                if inKeen.currentWeapon == 6: inKeen.currentWeapon = 0
                count += 1
            if count == 6: inKeen.currentWeapon = -1
                
                
        if inEventKey == K_ESCAPE:
            inMenu.menuType = MENU_MAIN

    elif inMenu.menuType == MENU_OPTIONS:
        if inEventKey == K_DOWN:
            if inMenu.menuOptionsIndex < inMenu.menuOptionsMax: inMenu.menuOptionsIndex += 1
        if inEventKey == K_UP:
            if inMenu.menuOptionsIndex > 0: inMenu.menuOptionsIndex -= 1
        if inEventKey == K_RETURN:
            if inMenu.menuOptionsIndex == 0:
                fileFilters = 'Tiled levels (*.tmx)|*.tmx|All files (*.*)|*.*'
                wxApp = wx.App()
                # Create an open file dialog
                dialog = wx.FileDialog (None, message='Choose a Level....', wildcard=fileFilters, style=wx.FD_OPEN)
                # Show the dialog and get user input
                if dialog.ShowModal() == wx.ID_OK:
                   openFile = dialog.GetPath()
                else:
                   openFile = None
                dialog.Destroy()
                #wxApp.Destroy()
                #print openFile

                # Now load the custom level
                if openFile <> None:
                # NEW GAME - reset Keen stuff and Game stuff
                    inKeen.reset()
                    inGame.level_ID = 1
                    inGame.srfcCutScenes = gfnLoad_Splice(320, 200, gfn_Zip(inGame.CSNames[0]), 0, 0)
                    inGame.cutScene_ID = 0
                    inGame.custom = True
                    inGame.customLevel = openFile
                    inMenu.active = False
                    inGame.fadeOut = True
                    inGame.fadeTimer = 0
                            
            elif inMenu.menuOptionsIndex == 1:
                if inGame.sound == True:
                    inGame.sound = False
                    for sound in SFX:
                        sound.set_volume(0)
                else:
                    gfn_PlaySound(SFX_KEEN_SWITCH)
                    inGame.sound = True
                    for sound in SFX:
                        sound.set_volume(1)
                        
            elif inMenu.menuOptionsIndex == 2:
                if inGame.music == True:
                    inGame.music = False
                    pygame.mixer.music.set_volume(0)
                else:
                    gfn_PlaySound(SFX_KEEN_SWITCH)
                    inGame.music = True
                    pygame.mixer.music.set_volume(1)

            # Clear statistics
            elif inMenu.menuOptionsIndex == 3:

                if os.path.exists("savegame.bak"): os.remove("savegame.bak")                    # Delete backup if exists
                if os.path.exists("savegame.is2"): os.rename("savegame.is2", "savegame.bak")    # Backup savegame
                inGame.SAVED_DATA = gfn_LoadSaveDataNew()                                       # Write a new one
                gfn_PlaySound(SFX_KEEN_SWITCH)
                inMenu.menuLoadIndex = 0
                
        if inEventKey == K_ESCAPE:
            inMenu.menuType = MENU_MAIN
            
    elif inMenu.menuType == MENU_HELP:
        if inEventKey == K_DOWN:
            if inMenu.menuHelpIndex < inMenu.menuHelpIndexMax:
                inMenu.menuHelpIndex += 1
        if inEventKey == K_UP:
            if inMenu.menuHelpIndex > 0:
                inMenu.menuHelpIndex -= 1
        if inEventKey == K_RETURN:
            inMenu.menuType = MENU_DISPLAYTEXT
            inMenu.menuHelpTextY = 0
            inMenu.srfcHelpText = pygame.image.load(gfn_Zip(inMenu.HelpTextNames[inMenu.menuHelpIndex])).convert_alpha()
            
        if inEventKey == K_ESCAPE:
            inMenu.menuType = MENU_MAIN
            
    elif inMenu.menuType == MENU_DISPLAYTEXT:
        if inEventKey == K_ESCAPE:
            inMenu.menuType = MENU_HELP

    return willQuit

# Handle Menu Input
def gfn_MenuInput2(inMenu, inTimeElapsed):
    keys = pygame.key.get_pressed()
    if keys[K_DOWN]:
        if inMenu.menuHelpTextY < inMenu.srfcHelpText.get_height() - 84:
            inMenu.menuHelpTextY += (inTimeElapsed * inMenu.moveSpeed)
            
    elif keys[K_UP]:
        if inMenu.menuHelpTextY > 0:
            inMenu.menuHelpTextY -= (inTimeElapsed * inMenu.moveSpeed)
            if inMenu.menuHelpTextY < 0: inMenu.menuHelpTextY = 0
