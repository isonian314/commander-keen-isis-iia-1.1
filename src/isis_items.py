import pygame
pygame.init()
from isis_tiles import *
from isis_draw import *
from isis_weapons import *
from isis_keen import *
from isis_zip import *
from isis_constants import *
from isis_music import *
                
srfcItems = gfnLoad_Splice(24, 24, gfn_Zip("items.png"), 1, 1)
srfcFloats = gfnLoad_Splice(32, 32, gfn_Zip("floatups.png"), 1, 1)

# Item Class - for collectables (keys, points, health powerups)
class gcls_Item(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID):
        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.image = srfcItems[self.id * 4]
        self.rect = pygame.Rect(self.x + 4, self.y + 4, 24, 24)
        self.collected = False
        
    def update(self, inFrame, inLevel, inKeen, inFloats, inGame):
        self.rect = pygame.Rect(self.x - inLevel.mapX + 4, self.y - inLevel.mapY + 5, 24, 24)
        self.image = srfcItems[(self.id * 4) + inFrame]

        if self.collected == True:
            
            # Keys
            if self.id >= ITEM_KEY_RED and self.id <= ITEM_KEY_MAGENTA and inKeen.hasKey[self.id - ITEM_KEY_RED] == False:
                gfn_PlaySound(SFX_ITEM_KEY)
                keyID = self.id - ITEM_KEY_RED
                inKeen.hasKey[keyID] = True

            # Point Items
            elif self.id >= ITEM_JBEAN_RED and self.id <= ITEM_CEREAL and inKeen.score < 99999999:
                gfn_PlaySound(SFX_ITEM_POINTS)
                if self.id == ITEM_JBEAN_RED:
                    inKeen.score += 100 * inKeen.pointMultiplier
                    inLevel.stats_NumPoints += 100
                    inLevel.stats_NumItems += 1
                elif self.id == ITEM_JBEAN_YELLOW:
                    inKeen.score += 100 * inKeen.pointMultiplier
                    inLevel.stats_NumPoints += 100
                    inLevel.stats_NumItems += 1
                elif self.id == ITEM_JBEAN_GREEN:
                    inKeen.score += 100 * inKeen.pointMultiplier
                    inLevel.stats_NumPoints += 100
                    inLevel.stats_NumItems += 1
                elif self.id == ITEM_JBEAN_CYAN:
                    inKeen.score += 100 * inKeen.pointMultiplier
                    inLevel.stats_NumPoints += 100
                    inLevel.stats_NumItems += 1
                elif self.id == ITEM_JBEAN_BLUE:
                    inKeen.score += 100 * inKeen.pointMultiplier
                    inLevel.stats_NumPoints += 100
                    inLevel.stats_NumItems += 1
                elif self.id == ITEM_JBEAN_PURPLE:
                    inKeen.score += 100 * inKeen.pointMultiplier
                    inLevel.stats_NumPoints += 100
                    inLevel.stats_NumItems += 1
                elif self.id == ITEM_COLA:
                    inKeen.score += 200 * inKeen.pointMultiplier
                    inLevel.stats_NumPoints += 200
                    inLevel.stats_NumItems += 1
                elif self.id == ITEM_BURGER:
                    inKeen.score += 500 * inKeen.pointMultiplier
                    inLevel.stats_NumPoints += 500
                    inLevel.stats_NumItems += 1
                elif self.id == ITEM_GINGER:
                    inKeen.score += 1000 * inKeen.pointMultiplier
                    inLevel.stats_NumPoints += 1000
                    inLevel.stats_NumItems += 1
                elif self.id == ITEM_SUGAR:
                    inKeen.score += 2000 * inKeen.pointMultiplier
                    inLevel.stats_NumPoints += 2000
                    inLevel.stats_NumItems += 1
                elif self.id == ITEM_CEREAL:
                    inKeen.score += 5000 * inKeen.pointMultiplier
                    inLevel.stats_NumPoints += 5000
                    inLevel.stats_NumItems += 1

            # Health Items
            elif self.id >= ITEM_PYAPA_FRUIT and self.id <= ITEM_POTION and self.id <> ITEM_NEPHTHYS_FRUIT and inKeen.health < 10:
                gfn_PlaySound(SFX_ITEM_POINTS)
                if self.id == ITEM_PYAPA_FRUIT: inKeen.heal(1)
                elif self.id == ITEM_PEETA_BERRIES: inKeen.heal(3)
                elif self.id == ITEM_ISIS_FRUIT: inKeen.heal(5)
                elif self.id == ITEM_POTION: inKeen.heal(10)
                
            elif self.id == ITEM_NEPHTHYS_FRUIT: inKeen.hurt(3, inGame, inLevel)
            
            elif self.id == ITEM_YORP and inKeen.lives < 99:
                gfn_PlaySound(SFX_ITEM_1UP)
                inKeen.lives += 1

            # Powerups
            elif self.id == ITEM_SHOES:
                inKeen.powerUp = pwrSHOES
                inKeen.powerUpTimer = pwrTimes[pwrSHOES]
                inKeen.physics = physSHOES
                inKeen.sprite = kSPRITE_NORMAL
                inKeen.pointMultiplier = 1
            elif self.id == ITEM_POINTS:
                inKeen.powerUp = pwrPOINTS
                inKeen.powerUpTimer = pwrTimes[pwrPOINTS]
                inKeen.pointMultiplier = 4
                self.physics = physNORMAL
                inKeen.sprite = kSPRITE_NORMAL
            elif self.id == ITEM_GOD:
                inKeen.powerUp = pwrGOD
                inKeen.powerUpTimer = pwrTimes[pwrGOD]
                inKeen.sprite = kSPRITE_GOD
                inKeen.pointMultiplier = 1
                inKeen.physics = physGOD
            elif self.id == ITEM_CRAZY:
                inKeen.powerUp = pwrCRAZY
                inKeen.powerUpTimer = pwrTimes[pwrCRAZY]
                inKeen.sprite = kSPRITE_CRAZY
                inKeen.pointMultiplier = 1
                inKeen.physics = physCRAZY
            elif self.id == ITEM_ANTI:
                inKeen.powerUp = pwrANTI
                inKeen.powerUpTimer = pwrTimes[pwrANTI]
                inKeen.pointMultiplier = 0
                inKeen.sprite = kSPRITE_NORMAL
                inKeen.pointMultiplier = 1
                inKeen.physics = physNORMAL
            elif self.id == ITEM_REGEN:
                inKeen.powerUp = pwrREGEN
                inKeen.sprite = kSPRITE_NORMAL
                inKeen.physics = physNORMAL
                inKeen.powerUpTimer = pwrTimes[pwrREGEN]
                inKeen.regenUpdate = pygame.time.get_ticks()
                inKeen.pointMultiplier = 1
            elif self.id == ITEM_DEGEN:
                inKeen.powerUp = pwrDEGEN
                inKeen.sprite = kSPRITE_NORMAL
                inKeen.physics = physNORMAL
                inKeen.powerUpTimer = pwrTimes[pwrDEGEN]
                inKeen.regenUpdate = pygame.time.get_ticks()
                inKeen.pointMultiplier = 1

            # Weapons
            elif self.id == ITEM_BLOWGUN and inKeen.weapon[W_BLOWGUN].ammo < 99:
                if inKeen.currentWeapon == -1: inKeen.currentWeapon = W_BLOWGUN
                if inKeen.weapon[W_BLOWGUN].ammo == -1: inKeen.weapon[W_BLOWGUN].ammo = 0
                inKeen.weapon[W_BLOWGUN].ammo += 5
                if inKeen.weapon[W_BLOWGUN].ammo > 99: inKeen.weapon[W_BLOWGUN].ammo = 99
                gfn_PlaySound(SFX_ITEM_WEAPON)
                
            elif self.id == ITEM_ZEFFER and inKeen.weapon[W_ZEFFER].ammo < 99:
                if inKeen.currentWeapon == -1: inKeen.currentWeapon = W_ZEFFER
                if inKeen.weapon[W_ZEFFER].ammo == -1: inKeen.weapon[W_ZEFFER].ammo = 0
                inKeen.weapon[W_ZEFFER].ammo += 5
                if inKeen.weapon[W_ZEFFER].ammo > 99: inKeen.weapon[W_ZEFFER].ammo = 99
                gfn_PlaySound(SFX_ITEM_WEAPON)
                
            elif self.id == ITEM_PULSAR and inKeen.weapon[W_PULSAR].ammo < 99:
                if inKeen.currentWeapon == -1: inKeen.currentWeapon = W_PULSAR
                if inKeen.weapon[W_PULSAR].ammo == -1: inKeen.weapon[W_PULSAR].ammo = 0
                inKeen.weapon[W_PULSAR].ammo += 5
                if inKeen.weapon[W_PULSAR].ammo > 99: inKeen.weapon[W_PULSAR].ammo = 99
                gfn_PlaySound(SFX_ITEM_WEAPON)
                
            elif self.id == ITEM_SOLARIZER and inKeen.weapon[W_SOLARIZER].ammo < 99:
                if inKeen.currentWeapon == -1: inKeen.currentWeapon = W_SOLARIZER
                if inKeen.weapon[W_SOLARIZER].ammo == -1: inKeen.weapon[W_SOLARIZER].ammo = 0
                inKeen.weapon[W_SOLARIZER].ammo += 5
                if inKeen.weapon[W_SOLARIZER].ammo > 99: inKeen.weapon[W_SOLARIZER].ammo = 99
                gfn_PlaySound(SFX_ITEM_WEAPON)
                
            elif self.id == ITEM_HR42 and inKeen.weapon[W_HR42].ammo < 99:
                if inKeen.currentWeapon == -1: inKeen.currentWeapon = W_HR42
                if inKeen.weapon[W_HR42].ammo == -1: inKeen.weapon[W_HR42].ammo = 0
                inKeen.weapon[W_HR42].ammo += 5
                if inKeen.weapon[W_HR42].ammo > 99: inKeen.weapon[W_HR42].ammo = 99
                gfn_PlaySound(SFX_ITEM_WEAPON)
                
            elif self.id == ITEM_PLUTEZARP and inKeen.weapon[W_PLUTEZARP].ammo < 99:
                if inKeen.currentWeapon == -1: inKeen.currentWeapon = W_PLUTEZARP
                if inKeen.weapon[W_PLUTEZARP].ammo == -1: inKeen.weapon[W_PLUTEZARP].ammo = 0
                inKeen.weapon[W_PLUTEZARP].ammo += 5
                if inKeen.weapon[W_PLUTEZARP].ammo > 99: inKeen.weapon[W_PLUTEZARP].ammo = 99
                gfn_PlaySound(SFX_ITEM_WEAPON)
                
            elif self.id == ITEM_HARPOON and inKeen.weapon[W_HARPOON].ammo < 99:
                if inKeen.currentWeapon == -1 and inKeen.state == kIN_WATER: inKeen.currentWeapon = W_HARPOON
                if inKeen.weapon[W_HARPOON].ammo == -1: inKeen.weapon[W_HARPOON].ammo = 0
                inKeen.weapon[W_HARPOON].ammo += 5
                if inKeen.weapon[W_HARPOON].ammo > 99: inKeen.weapon[W_HARPOON].ammo = 99
                gfn_PlaySound(SFX_ITEM_WEAPON)
                
            elif self.id == ITEM_RAYGUN and inKeen.weapon[W_RAYGUN].ammo < 99:
                if inKeen.weapon[W_RAYGUN].ammo == -1: inKeen.weapon[W_RAYGUN].ammo = 0
                inKeen.weapon[W_RAYGUN].ammo += 5
                if inKeen.weapon[W_RAYGUN].ammo > 99: inKeen.weapon[W_RAYGUN].ammo = 99
                gfn_PlaySound(SFX_ITEM_WEAPON)
                
            elif self.id == ITEM_NEURAL and inKeen.weapon[W_NEURAL].ammo < 99:
                if inKeen.weapon[W_NEURAL].ammo == -1: inKeen.weapon[W_NEURAL].ammo = 0
                inKeen.weapon[W_NEURAL].ammo += 5
                if inKeen.weapon[W_NEURAL].ammo > 99: inKeen.weapon[W_NEURAL].ammo = 99
                gfn_PlaySound(SFX_ITEM_WEAPON_NEURAL)
                
            # Inventory
            elif self.id == ITEM_BATTERY:
                gfn_PlaySound(SFX_ITEM_INVENTORY)
                if inKeen.invMaxPower < 20: inKeen.invMaxPower += 1
                if inKeen.inventory[0].power == -1: inKeen.inventory[0].power = 1
                elif inKeen.inventory[0].power < 20: inKeen.inventory[0].power += 1
                inLevel.stats_NumItems += 1
                
            elif self.id == ITEM_SHIELD:
                gfn_PlaySound(SFX_ITEM_INVENTORY)
                if inKeen.inventory[1].power == -1: inKeen.inventory[1].power = 1
                inLevel.stats_NumItems += 1
                
            elif self.id == ITEM_IONSCANNER:
                gfn_PlaySound(SFX_ITEM_INVENTORY)
                if inKeen.inventory[2].power == -1: inKeen.inventory[2].power = 1
                inLevel.stats_NumItems += 1
                
            elif self.id == ITEM_UNKNOWN:
                gfn_PlaySound(SFX_ITEM_INVENTORY)
                if inKeen.inventory[3].power == -1: inKeen.inventory[3].power = 1
                inLevel.stats_NumItems += 1
                
            else:
                self.collected = False

            # Start the item Timer, which makes Keen's eyes flash blue
            if self.collected == True: inKeen.itemTimer = 0.5
            
            # Check condition again, since it may have been changed if Keen already had item etc
            if self.collected == True:
                # Check we haven't exceeded limits
                if inKeen.score > 99999999: inKeen.score = 99999999
                if inKeen.health > 10: inKeen.health = 10
                if inKeen.lives > 99: inKeen.lives = 99
                inFloats.add(gcls_Float(self.x, self.y, self.id, inLevel))   
                self.kill()
                

    # To modify the kill() method
    #def kill(self):
    #    pygame.sprite.Sprite.kill(self)

FLOAT_LENGTH = 2 # Second
FLOAT_SPEED = 20 # Pixels / second

FLOAT_KEY = 0
FLOAT_100 = 6
FLOAT_200 = 7
FLOAT_500 = 8
FLOAT_1000 = 9
FLOAT_2000 = 10
FLOAT_5000 = 11
FLOAT_1 = 12
FLOAT_3 = 13
FLOAT_5 = 14
FLOAT_10 = 15
FLOAT_neg3 = 16
FLOAT_1UP = 18

FLOAT_SHOES = 27
FLOAT_POINTS = 28
FLOAT_GOD = 29
FLOAT_CRAZY = 30
FLOAT_ANTI = 31
FLOAT_REGEN = 32
FLOAT_DEGEN = 33

FLOAT_BLOWGUN = 34
FLOAT_ZEFFER = 35
FLOAT_PULSAR = 36
FLOAT_SOLARIZER = 37
FLOAT_HR42 = 38
FLOAT_PLUTEZARP = 39
FLOAT_HARPOON = 40
FLOAT_RAYGUN = 41
FLOAT_NEURAL = 42

FLOAT_BATTERY = 43
FLOAT_SHIELD = 44
FLOAT_IONSCANNER = 45
FLOAT_UNKNOWN = 46

# Item Class - for collectables (keys, points, health powerups)
class gcls_Float(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inLevel):
        pygame.sprite.Sprite.__init__(self)
        self.x = inX
        self.y = inY - 10
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.last_frame_update = pygame.time.get_ticks()
        self.timer = 0
        
        if inID >= ITEM_KEY_RED and inID <= ITEM_KEY_MAGENTA: self.id = FLOAT_KEY
        elif inID >= ITEM_JBEAN_RED and inID <= ITEM_JBEAN_PURPLE: self.id = FLOAT_100
        elif inID == ITEM_COLA: self.id = FLOAT_200
        elif inID == ITEM_BURGER:self.id = FLOAT_500
        elif inID == ITEM_GINGER: self.id = FLOAT_1000
        elif inID == ITEM_SUGAR: self.id = FLOAT_2000
        elif inID == ITEM_CEREAL: self.id = FLOAT_5000
        elif inID == ITEM_PYAPA_FRUIT: self.id = FLOAT_1
        elif inID == ITEM_PEETA_BERRIES: self.id = FLOAT_3
        elif inID == ITEM_ISIS_FRUIT: self.id = FLOAT_5
        elif inID == ITEM_NEPHTHYS_FRUIT: self.id = FLOAT_neg3
        elif inID == ITEM_POTION: self.id = FLOAT_10
        elif inID == ITEM_YORP:
            self.id = FLOAT_1UP
            self.x -= 7

        elif inID == ITEM_SHOES: self.id = FLOAT_SHOES
        elif inID == ITEM_POINTS: self.id = FLOAT_POINTS
        elif inID == ITEM_GOD: self.id = FLOAT_GOD
        elif inID == ITEM_CRAZY: self.id = FLOAT_CRAZY
        elif inID == ITEM_ANTI: self.id = FLOAT_ANTI
        elif inID == ITEM_REGEN: self.id = FLOAT_REGEN
        elif inID == ITEM_DEGEN: self.id = FLOAT_DEGEN

        elif inID == ITEM_BATTERY: self.id = FLOAT_BATTERY
        elif inID == ITEM_SHIELD: self.id = FLOAT_SHIELD
        elif inID == ITEM_IONSCANNER: self.id = FLOAT_IONSCANNER
        elif inID == ITEM_UNKNOWN: self.id = FLOAT_UNKNOWN
        
        elif inID == ITEM_BLOWGUN: self.id = FLOAT_BLOWGUN
        elif inID == ITEM_ZEFFER: self.id = FLOAT_ZEFFER
        elif inID == ITEM_PULSAR: self.id = FLOAT_PULSAR
        elif inID == ITEM_SOLARIZER: self.id = FLOAT_SOLARIZER
        elif inID == ITEM_HR42: self.id = FLOAT_HR42
        elif inID == ITEM_PLUTEZARP: self.id = FLOAT_PLUTEZARP
        elif inID == ITEM_HARPOON: self.id = FLOAT_HARPOON
        elif inID == ITEM_RAYGUN: self.id = FLOAT_RAYGUN
        elif inID == ITEM_NEURAL: self.id = FLOAT_NEURAL
                                                        
        self.image = srfcFloats[self.id].copy()
        self.rect = pygame.Rect(self.x - inLevel.mapX + inLevel.playX, self.y - inLevel.mapY + inLevel.playY, 24, 24)

    def update(self, t, inLevel):
        self.timer += (t - self.last_update) / 1000.0

        if ((t - self.last_frame_update) / 1000.0) > (FLOAT_LENGTH / 7.0) and self.id == FLOAT_KEY and self.frame < 5:
            self.frame += 1
            self.last_frame_update = t
        elif ((t - self.last_frame_update) / 1000.0) > (FLOAT_LENGTH / 10.0) and self.id == FLOAT_1UP and self.frame < 7:
            self.frame += 1
            self.last_frame_update = t
            
        if self.timer < FLOAT_LENGTH:
            self.y -= ((t - self.last_update) / 1000.0) * FLOAT_SPEED
            self.rect = pygame.Rect(self.x - inLevel.mapX + 4, self.y - inLevel.mapY + 4, 24, 24)
            self.image = srfcFloats[self.id + self.frame].copy()
            if self.timer > FLOAT_LENGTH / 2.0: self.image.set_alpha(255 - ((self.timer - (FLOAT_LENGTH / 2.0))/ (FLOAT_LENGTH / 2.0)) * 255)
        else:
            self.kill()

        
        self.last_update = t
        
sprite_Items = pygame.sprite.RenderPlain()
sprite_Floats = pygame.sprite.RenderPlain()
