# isis_gfx.py
# Graphics functions
#  - HUD update

import pygame, random
from isis_draw import *
from isis_keen import *
from isis_zip import *
pygame.init()

# HUD Graphics Positions
POS_LIGHT_X = 264
POS_LIGHT_Y = 105
POS_FACE_X = 275
POS_FACE_Y = 5
POS_KEYS_X = 279
POS_KEYS_Y = 142
POS_HEALTH_X = 269
POS_HEALTH_Y = 26
POS_WEAPONS_X = 295
POS_WEAPONS_Y = 44
POS_LIVES_X = 302
POS_LIVES_Y = 143
POS_SCORE_X = 270
POS_SCORE_Y = 186
POS_POWERUPS_X = 267
POS_POWERUPS_Y = 154
POS_INVENT_POWER_X = 305
POS_INVENT_POWER_Y = 154
POS_INVENT_ICON_X = 285
POS_INVENT_ICON_Y = 154
POS_INVENT_DOTS_X = 287
POS_INVENT_DOTS_Y = 174

# HUD Class
# Contains images and functions to update the HUD
class gcls_HUD():
    def __init__(self, inKeen, inSurface):
        # Variables
        self.flash = False
        self.blueHealth = True
        
        # Load graphics
        self.imgBlank = pygame.image.load(gfn_Zip("hud_blank.png")).convert(16)
        self.imgBlank.set_colorkey(TRANSCOLOUR)
        
        self.imgFaces = gfnLoad_Splice(40, 38, gfn_Zip("hud_faces.png"), 1, 1)
        self.imgHealth = gfnLoad_Splice(9, 79, gfn_Zip("hud_health.png"), 1, 1)
        self.imgHealthBlue = gfnLoad_Splice(9, 79, gfn_Zip("hud_health_blue.png"), 1, 1)
        self.imgLight = gfnLoad_Splice(17, 31, gfn_Zip("hud_light.png"), 1, 1)
        self.imgWeapons = gfnLoad_Splice(19, 13, gfn_Zip("hud_weapons.png"), 1, 1)
        self.imgPowerups = gfnLoad_Splice(17, 17, gfn_Zip("hud_powerups.png"), 1, 1)
        self.imgKeys = gfnLoad_Splice(13, 9, gfn_Zip("hud_keys.png"), 1, 1)
        self.imgFont1 = gfnLoad_Splice(5, 7, gfn_Zip("hud_font1.png"), 1, 1)
        self.imgFont2 = gfnLoad_Splice(4, 7, gfn_Zip("hud_font2.png"), 1, 1)
        self.imgInventory = gfnLoad_Splice(18, 17, gfn_Zip("hud_inventory.png"), 1, 1)
        self.imgInventoryPwr = gfnLoad_Splice(11, 29, gfn_Zip("hud_inventory_power.png"), 1, 1)
        self.imgInventoryDots = gfnLoad_Splice(17, 5, gfn_Zip("hud_inventory_dots.png"), 1, 1)

        # Initial update
        self.update(inKeen, inSurface)


    # Function to update the HUG, based on inKeen
    # HUD will be painted directly onto inSurface
    def update(self, inKeen, inSurface):

        # Draw blank HUG
        inSurface.blit(self.imgBlank, (0,0))

        # Light Globe
        if inKeen.powerUp == pwrGOD: inSurface.blit(self.imgLight[5], (POS_LIGHT_X, POS_LIGHT_Y))
        elif inKeen.powerUp == pwrCRAZY: inSurface.blit(self.imgLight[6], (POS_LIGHT_X, POS_LIGHT_Y))
        elif inKeen.powerUp == pwrSHOES or inKeen.powerUp == pwrPOINTS: inSurface.blit(self.imgLight[4], (POS_LIGHT_X, POS_LIGHT_Y))
        elif inKeen.healTimer > 0: inSurface.blit(self.imgLight[2], (POS_LIGHT_X, POS_LIGHT_Y))
        elif inKeen.hurtTimer > 0: inSurface.blit(self.imgLight[3], (POS_LIGHT_X, POS_LIGHT_Y))
        else:
            # Randomly Flash
            RND = int(random.random() * (1.0 / inKeen.timeElapsed / 3.0))
            if self.flash == False: inSurface.blit(self.imgLight[0], (POS_LIGHT_X, POS_LIGHT_Y))
            else: inSurface.blit(self.imgLight[1], (POS_LIGHT_X, POS_LIGHT_Y))
            if RND == 1:
                if self.flash == False:
                    self.flash = True
                else:
                    self.flash = False
        
        # Blue Health option
        if self.blueHealth == True:
            inSurface.blit(self.imgHealthBlue[0], (POS_HEALTH_X, POS_HEALTH_Y))
        # Keen Health Bars
        if inKeen.health <> 10:
            inSurface.blit(self.imgHealth[inKeen.health], (POS_HEALTH_X, POS_HEALTH_Y))

        # Keen Face
        if inKeen.state == kDYING: inSurface.blit(self.imgFaces[6], (POS_FACE_X, POS_FACE_Y))
        elif inKeen.powerUp == pwrGOD: inSurface.blit(self.imgFaces[2], (POS_FACE_X, POS_FACE_Y))
        elif inKeen.powerUp == pwrCRAZY: inSurface.blit(self.imgFaces[3], (POS_FACE_X, POS_FACE_Y))
        elif inKeen.health > 6 and inKeen.itemTimer > 0: inSurface.blit(self.imgFaces[1], (POS_FACE_X, POS_FACE_Y))
        elif inKeen.health > 6: inSurface.blit(self.imgFaces[0], (POS_FACE_X, POS_FACE_Y))
        elif inKeen.health > 4: inSurface.blit(self.imgFaces[4], (POS_FACE_X, POS_FACE_Y))
        elif inKeen.health > 0: inSurface.blit(self.imgFaces[5], (POS_FACE_X, POS_FACE_Y))
        
            
        # Keys
        for keyID in range(6):
            if inKeen.hasKey[keyID]: inSurface.blit(self.imgKeys[keyID], (POS_KEYS_X, POS_KEYS_Y))
            
        # Weapons
        # If weapon has been previously collected, show the grey version
        # If it has ammo, show the coloured version
        # If it is selected, show the highlited version
        #if inKeen.currentWeapon > -1:
        for w in range(7):
            # Font Stuff
            num1, num2 = 0, 0
            if inKeen.weapon[w].ammo <> -1:
                strW =str(inKeen.weapon[w].ammo)
                if len(strW) == 1:
                    num2 = inKeen.weapon[w].ammo
                elif len(strW) == 2:
                    num1 = int(strW[0])
                    num2 = int(strW[1])

            # Harpoon y offset for font
            if w == 6: harpoon = 1
            else: harpoon = 0
            
            # WEAPON SELECTED
            if inKeen.currentWeapon == w:
                inSurface.blit(self.imgWeapons[(w*3)+2], (POS_WEAPONS_X, POS_WEAPONS_Y + (w * 13) + w))
                inSurface.blit(self.imgFont1[num1+10], (POS_WEAPONS_X - 13, POS_WEAPONS_Y + (w * 13) + w + 3 - harpoon))
                inSurface.blit(self.imgFont1[num2+10], (POS_WEAPONS_X - 7, POS_WEAPONS_Y + (w * 13) + w + 3 - harpoon))
                
            # WEAPON AVAILABLE
            elif inKeen.weapon[w].ammo > 0:
                inSurface.blit(self.imgWeapons[(w*3)+1], (POS_WEAPONS_X, POS_WEAPONS_Y + (w * 13) + w))
                inSurface.blit(self.imgFont1[num1], (POS_WEAPONS_X - 13, POS_WEAPONS_Y + (w * 13) + w + 3 - harpoon))
                inSurface.blit(self.imgFont1[num2], (POS_WEAPONS_X - 7, POS_WEAPONS_Y + (w * 13) + w + 3 - harpoon))
                
            # WEAPON SEEN BEFORE
            elif inKeen.weapon[w].ammo > -1:
                inSurface.blit(self.imgWeapons[(w*3)], (POS_WEAPONS_X, POS_WEAPONS_Y + (w * 13) + w))
                inSurface.blit(self.imgFont1[num1], (POS_WEAPONS_X - 13, POS_WEAPONS_Y + (w * 13) + w + 3 - harpoon))
                inSurface.blit(self.imgFont1[num2], (POS_WEAPONS_X - 7, POS_WEAPONS_Y + (w * 13) + w + 3 - harpoon))

        if inKeen.currentWeapon == 7 or inKeen.currentWeapon == 8:
            w = inKeen.currentWeapon
            inSurface.blit(self.imgWeapons[(w*3)+2], (POS_WEAPONS_X - 29, POS_WEAPONS_Y + 112))

        # Powerups
        if inKeen.powerUp > 0:
            pwrIndex = (inKeen.powerUp - 1) * 5
            pwrOffset = 4 - int(round((inKeen.powerUpTimer / pwrTimes[inKeen.powerUp]) * 4))
            inSurface.blit(self.imgPowerups[pwrIndex + pwrOffset], (POS_POWERUPS_X, POS_POWERUPS_Y))
            pwrStr = str(int(round(inKeen.powerUpTimer)))
            num1, num2 = 0, 0
            if len(pwrStr) == 1:
                num2 = int(pwrStr[0])
            else:
                num1 = int(pwrStr[0])
                num2 = int(pwrStr[1])
                
            inSurface.blit(self.imgFont1[num1+10], (POS_POWERUPS_X + 3, POS_POWERUPS_Y + 20))
            inSurface.blit(self.imgFont1[num2+10], (POS_POWERUPS_X + 3 + 6, POS_POWERUPS_Y + 20))

        # Inventory
        if inKeen.invCurrent > -1:
            inSurface.blit(self.imgInventory[inKeen.invCurrent], (POS_INVENT_ICON_X, POS_INVENT_ICON_Y))

            if inKeen.inventory[inKeen.invCurrent].power == 20:
                inSurface.blit(self.imgInventoryPwr[inKeen.invCurrent], (POS_INVENT_POWER_X, POS_INVENT_POWER_Y))
            else:
                offset = 19 - inKeen.inventory[inKeen.invCurrent].power
                offsetY = 7 + offset
                inSurface.blit(self.imgInventoryPwr[inKeen.invCurrent].subsurface(0,offsetY, 11, 29 - offsetY), (POS_INVENT_POWER_X, POS_INVENT_POWER_Y + offsetY))

        for i in range(4):
            if inKeen.inventory[i].power <> -1:
                if inKeen.inventory[i].power == inKeen.invMaxPower:
                    inSurface.blit(self.imgInventoryDots[i], (POS_INVENT_DOTS_X, POS_INVENT_DOTS_Y))
                elif inKeen.inventory[i].power == 0:
                    inSurface.blit(self.imgInventoryDots[i+8], (POS_INVENT_DOTS_X, POS_INVENT_DOTS_Y))
                else:
                    inSurface.blit(self.imgInventoryDots[i + 4], (POS_INVENT_DOTS_X, POS_INVENT_DOTS_Y))
                    
                if inKeen.invCurrent == i: inSurface.blit(self.imgInventoryDots[i + 12], (POS_INVENT_DOTS_X, POS_INVENT_DOTS_Y))
            
        # Lives
        num1, num2 = 0, 0
        if inKeen.lives <> -1:
            strL =str(inKeen.lives)
            if len(strL) == 1:
                num2 = inKeen.lives
            elif len(strL) == 2:
                num1 = int(strL[0])
                num2 = int(strL[1])
        inSurface.blit(self.imgFont1[num1], (POS_LIVES_X, POS_LIVES_Y))
        inSurface.blit(self.imgFont1[num2], (POS_LIVES_X + 6, POS_LIVES_Y))
                    
        # Score
        #Up to 8 digitis
        num1, num2, num3, num4, num5, num6, num7, num8 = 0, 0, 0, 0, 0, 0, 0, 0
        strS =str(inKeen.score)
        if len(strS) == 1:
                num8 = inKeen.score
        elif len(strS) == 2:
            num7, num8 = int(strS[0]), int(strS[1])
        elif len(strS) == 3:
            num6, num7, num8 = int(strS[0]), int(strS[1]), int(strS[2])
        elif len(strS) == 4:
            num5, num6, num7, num8 = int(strS[0]), int(strS[1]), int(strS[2]), int(strS[3])
        elif len(strS) == 5:
            num5, num6, num7, num8 = int(strS[1]), int(strS[2]), int(strS[3]), int(strS[4])
            num4 = int(strS[0])
        elif len(strS) == 6:
            num5, num6, num7, num8 = int(strS[2]), int(strS[3]), int(strS[4]), int(strS[5])
            num3, num4 = int(strS[0]), int(strS[1])
        elif len(strS) == 7:
            num5, num6, num7, num8 = int(strS[3]), int(strS[4]), int(strS[5]), int(strS[6])
            num2, num3, num4 = int(strS[0]), int(strS[1]), int(strS[2])
        elif len(strS) == 8:
            num5, num6, num7, num8 = int(strS[4]), int(strS[5]), int(strS[6]), int(strS[7])
            num1, num2, num3, num4 = int(strS[0]), int(strS[1]), int(strS[2]), int(strS[3])

        inSurface.blit(self.imgFont2[num1], (POS_SCORE_X, POS_SCORE_Y))
        inSurface.blit(self.imgFont2[num2], (POS_SCORE_X + 5, POS_SCORE_Y))                
        inSurface.blit(self.imgFont2[num3], (POS_SCORE_X + 12, POS_SCORE_Y))
        inSurface.blit(self.imgFont2[num4], (POS_SCORE_X + 17, POS_SCORE_Y))
        inSurface.blit(self.imgFont2[num5], (POS_SCORE_X + 22, POS_SCORE_Y))
        inSurface.blit(self.imgFont2[num6], (POS_SCORE_X + 29, POS_SCORE_Y))
        inSurface.blit(self.imgFont2[num7], (POS_SCORE_X + 34, POS_SCORE_Y))
        inSurface.blit(self.imgFont2[num8], (POS_SCORE_X + 39, POS_SCORE_Y))

