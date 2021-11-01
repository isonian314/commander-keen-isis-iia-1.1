# isis_enemies.py
# Contains all Enemy related graphics & AI

import pygame, math, random
pygame.init()
from isis_constants import *
from isis_draw import *
from isis_level import *
from isis_tiles import *
from isis_particle import *
import isis_weapons
from isis_zip import *
from isis_music import *

ENEMY_STATE_WALK = 0
ENEMY_STATE_JUMP = 1
ENEMY_STATE_IDLE = 2
ENEMY_STATE_ATTACK = 3
ENEMY_STATE_DIE = 4
ENEMY_STATE_WAKEUP = 5

SPRITE_RAT_BULLET = 1
SPRITE_SPIDER_PROJ = 2
SPRITE_DEMON_FIREBALL = 3
SPRITE_ROBOT_GREY_BULLET = 4
SPRITE_ROBOT_RED_BULLET = 5
SPRITE_HOVER_BULLET = 6
SPRITE_SLUG_PROJ = 7
SPRITE_SHAPESHIFTER_PROJ = 8
SPRITE_TELETURRET_PROJ = 9
SPRITE_EVILKEEN_PROJ = 10
SPRITE_ISONIAN_PROJ1g = 11 #green
SPRITE_ISONIAN_PROJ1r = 12 #red
SPRITE_ISONIAN_PROJ1w = 13 #white
SPRITE_ISONIAN_PROJ2 = 14

def gfn_IonScan(inSurface, inEnemy):
    width, height = 20, 4
    image = pygame.Surface((width, height))
    #image.fill(TRANSCOLOUR)
    energy = (inEnemy.hitPoints / inEnemy.maxHit) * width
    pygame.draw.rect(image, (255,0,0) , (0,0,energy,height), 0)
    #image.set_colorkey(TRANSCOLOUR)
    inSurface.blit(image, (inEnemy.rect[0] + ((inEnemy.width - width) / 2.0), inEnemy.rect[1] - height))

"""        
# Enemy Class
class gcls_Enemy(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir):

        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.vx = 1
        self.vy = 0
        self.moveAmountX = 0
        self.moveAmountY= 0
        self.onGround = False
        self.last_update = pygame.time.get_ticks()
        self.oldTimer = pygame.time.get_ticks()
        self.time_elapsed = 0.1
        self.frame = 0
        self.dirChange = 0
        self.direction = inDir
        
        if inID == SPRITE_RAT:
            self.image = srfcEnemyRat[self.frame]
            self.hitPoints = 5
            self.maxHit = 5.0
            self.damage = 1
            self.rectOffsetX = 1
            self.rectOffsetY = 1
            self.rectW = self.image.get_width() - 2
            self.rectH = self.image.get_height() - 2
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.speedRun = 75
            #self.speedJump = -200
            self.gravity = 450
            self.FPS = 1000 / 8.0
            self.state = ENEMY_STATE_WALK
            self.DIR_CHANGE_TIME = 2
            self.bullet = False
            
        if inID == SPRITE_RAT_BULLET:
            self.frame = 20
            if self.direction == -1: self.image = srfcEnemyRat[self.frame]
            elif self.direction == 1: self.image = pygame.transform.flip(srfcEnemyRat[self.frame], True, False)
            self.hitPoints = 99999
            self.maxHit = 99999.0
            self.damage = 2
            self.rectOffsetX = 1
            self.rectOffsetY = 1
            self.rectW = self.image.get_width() - 2
            self.rectH = self.image.get_height() - 2
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.speedRun = 200
            #self.speedJump = -200
            self.gravity = 0
            #self.FPS = 1000 / 8.0
            self.state = ENEMY_STATE_WALK
            #self.DIR_CHANGE_TIME = 5
            self.bullet = True

        if inID == SPRITE_SPIDER_PROJ:
            self.frame = 0
            if self.direction == -1: self.image = srfcEnemySpiderProj[self.frame]
            elif self.direction == 1: self.image = pygame.transform.flip(srfcEnemySpiderProj[self.frame], True, False)
            self.hitPoints = 99999
            self.maxHit = 99999.0
            self.damage = 2
            self.rectOffsetX = 1
            self.rectOffsetY = 1
            self.x += 10 * self.direction
            self.y += 20
            self.rectW = self.image.get_width() - 2
            self.rectH = self.image.get_height() - 2
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.speedRun = 100
            self.vy = -150
            self.gravity = 450
            self.FPS = 1000 / 8.0
            self.state = ENEMY_STATE_WALK
            self.bullet = True
            
        if inID == SPRITE_SPIDER:
            self.image = srfcEnemySpider[self.frame]
            self.hitPoints = 1
            self.maxHit = 1.0
            self.damage = 1
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.speedRun = 50
            #self.speedJump = -200
            self.gravity = 450
            self.FPS = 1000 / 4.0
            self.state = ENEMY_STATE_WALK
            #self.DIR_CHANGE_TIME = 2
            self.bullet = False
            
        self.rect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def updateSubRect(self):
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def update(self, t, inLevel, inKeen):

        self.time_elapsed = (t - self.oldTimer) / 1000.0
        self.oldTimer = t
        self.dirChange -= t_elapsed
        if self.dirChange < 0: self.dirChange = 0
        
        if self.id == SPRITE_RAT:
            if self.state == ENEMY_STATE_WALK:
                self.moveAmountX = t_elapsed * self.speedRun

                if t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.frame > 6: self.frame = 0
                    self.last_update = t

                # AI to change state here
                # Change direction AI
                if ((self.x - inKeen.x) * self.direction) > 0 and ((self.x - inKeen.x) * self.direction) < 100:
                    if abs(self.y - inKeen.y) < 100 and self.dirChange == 0:
                        self.direction = self.direction * -1
                        self.dirChange = self.DIR_CHANGE_TIME

                #if self.direction == 1 and inKeen.x < self.x and (self.x - inKeen.x) < 100 and abs(self.y - inKeen.y) < 50: self.direction = -1
                #elif self.direction == -1 and inKeen.x > self.x and (inKeen.x - self.x) < 100 and abs(self.y - inKeen.y) < 50: self.direction = 1

                # Shoot AI
                elif abs(self.x - inKeen.x) < 100 and abs(self.subRect.midbottom[1] - inKeen.subRect.midbottom[1]) < 5:
                    if self.x > inKeen.x: self.direction = -1
                    else: self.direction = 1
                    self.state = ENEMY_STATE_ATTACK
                    self.moveAmountX = 0
                    
            elif self.state == ENEMY_STATE_ATTACK:
                if self.frame < 7:
                    self.frame = 7
                    self.last_update = t
                elif t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.frame == 8:
                        bullet = gcls_Enemy(self.x / TILESIZE, self.y / TILESIZE, SPRITE_RAT_BULLET, self.direction)
                        inLevel.sprite_Enemies.add(bullet)
                    if self.frame == 10:
                        self.frame = 0
                        self.state = ENEMY_STATE_WALK
                    self.last_update = t

            elif self.state == ENEMY_STATE_DIE:
                if self.frame < 10:
                    self.frame = 10
                    self.last_update = t
                elif t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.frame > 13: self.frame = 13
                    self.last_update = t
                    
            if self.direction == -1: self.image = srfcEnemyRat[self.frame]
            elif self.direction == 1: self.image = pygame.transform.flip(srfcEnemyRat[self.frame], True, False)

        elif self.id == SPRITE_RAT_BULLET:
            if self.state == ENEMY_STATE_WALK:
                self.moveAmountX = t_elapsed * self.speedRun

            self.rect = pygame.Rect(round(self.x), round(self.y), self.width, self.height)
            bulletCollide = pygame.sprite.spritecollide(self, inLevel.sprite_MaskAll, False, pygame.sprite.collide_rect)
            for possibleCollide in bulletCollide:
                if pygame.sprite.collide_mask(self, possibleCollide):
                    self.kill()

        elif self.id == SPRITE_SPIDER_PROJ:
            if self.state == ENEMY_STATE_WALK:
                self.moveAmountX = t_elapsed * self.speedRun

                if t - self.last_update > self.FPS:
                        if self.frame < 6:
                            self.frame += 1
                            self.last_update = t
                            
            if self.direction == -1: self.image = srfcEnemySpiderProj[self.frame]
            elif self.direction == 1: self.image = pygame.transform.flip(srfcEnemySpiderProj[self.frame], True, False)
            
            #self.rect = pygame.Rect(round(self.x), round(self.y), self.width, self.height)
            #bulletCollide = pygame.sprite.spritecollide(self, inLevel.sprite_MaskAll, False, pygame.sprite.collide_rect)
            #for possibleCollide in bulletCollide:
            #    if pygame.sprite.collide_mask(self, possibleCollide):
            #        self.kill()
                    
        elif self.id == SPRITE_SPIDER:
            if self.state == ENEMY_STATE_WALK:
                self.moveAmountX = t_elapsed * self.speedRun

                if t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.frame > 7: self.frame = 0
                    self.last_update = t
                    
                # Shoot AI
                RND = int(random.random() * (1 / t_elapsed) * 4)
                if RND == 1:
                    self.state = ENEMY_STATE_ATTACK
                    self.moveAmountX = 0

            if self.state == ENEMY_STATE_ATTACK:
                if self.frame < 8:
                    self.frame = 8
                    self.last_update = t
                elif t - self.last_update > (self.FPS * 2):
                    self.frame += 1
                    if self.frame == 9:
                        bullet = gcls_Enemy(self.x / TILESIZE, self.y / TILESIZE, SPRITE_SPIDER_PROJ, self.direction)
                        inLevel.sprite_Enemies.add(bullet)
                    if self.frame == 10:
                        self.frame = 0
                        self.state = ENEMY_STATE_WALK
                    self.last_update = t
                    
            elif self.state == ENEMY_STATE_DIE:
                if self.frame < 11:
                    self.frame = 11
                    self.last_update = t
                elif t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.frame > 13: self.frame = 13
                    self.last_update = t
                    
            if self.direction == -1: self.image = srfcEnemySpider[self.frame]
            elif self.direction == 1: self.image = pygame.transform.flip(srfcEnemySpider[self.frame], True, False)                    

                    
        if self.bullet == False:
            # Push player left/right, in 1-pixel increments
            if self.direction != 0:
                for i in range(int(abs(self.moveAmountX))):
                    gfn_PushEnemy(self, inLevel, 1 * self.direction, 0)
                gfn_PushEnemy(self, inLevel, (self.moveAmountX % 1) * self.direction, 0)
                
            # GRAVITY:
            if self.moveAmountY < 0:
                for i in range(int(abs(self.moveAmountY))):
                    gfn_PushEnemy(self, inLevel, 0, -1)
                gfn_PushEnemy(self, inLevel, 0, (self.moveAmountY % -1))
            elif self.moveAmountY > 0:
                for i in range(int(abs(self.moveAmountY))):
                    if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, 1)
                if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, self.moveAmountY % 1)
            
        else:
            self.x += self.moveAmountX * self.direction
            self.y += self.moveAmountY
            
        self.vy += t_elapsed * self.gravity
        self.moveAmountY = t_elapsed * self.vy

        self.updateSubRect()
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)

        # If a dead enemy is out of sight by half a playing field, remove it
        if self.state == ENEMY_STATE_DIE:
            if self.rect[0] + self.rect.width + (inLevel.playWidth / 2) < 0 or self.rect[0] - (inLevel.playWidth / 2) > inLevel.playWidth:
                self.kill()
            elif self.rect[1] + self.rect.height + (inLevel.playHeight / 2) < 0 or self.rect[1] - (inLevel.playHeight / 2) > inLevel.playHeight:
                self.kill()
"""
#_______________________________________________________________________________________________
# Enemy Class - SIMPLE WALKING ENEMY
# This simple enemy can have a number of properties: jumping, idle frames, proximity frames, and attack frames, and float when dead (ie Fish)
class gcls_Enemy_Walker(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir):

        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.vx = 1
        self.vy = 0
        self.moveAmountX = 0
        self.moveAmountY= 0
        self.onGround = False
        self.last_update = pygame.time.get_ticks()
        self.oldTimer = pygame.time.get_ticks()
        t_elapsed = 0.1
        self.frame = 0
        self.dirChange = 0
        self.direction = inDir
        self.state = ENEMY_STATE_WALK
        self.bullet = False

        # Set a few initial properties
        # By default these won't change unless specified under a particular enemy
        self.hasIdle = False
        self.canJump = False
        self.willFloat = False
        self.canAttack = False
        self.hasClose = False
        
        self.dieLag = 1
        self.dieFrame = 0
        self.dieMax = 0
        self.fadeTime = 0
        self.fadeMax = 1.5
        self.idleFreq = 0
        self.idleLag = 1
        self.idleFrame = 0
        self.idleMax = 0
        self.jumpFreq = 0
        self.jumpAmount = 0
        self.jumpFrame = 0
        self.attackProximityX = 0
        self.attackProximityY = 0
        self.attackFrame = 0
        self.attackMax = 0
        self.attackLag = 0
        self.closeFrame = 0
        self.closeMax = 0
        self.isClose = False
        self.floatSpeed = 0
        
        # Now set stuff specific to all the individual enemies
        if inID == SPRITE_FOOG or inID == SPRITE_FOOGJUMP or inID == SPRITE_FOOG_WARRIOR:
            # Hit Points
            if inID != SPRITE_FOOG_WARRIOR:
                self.hitPoints = 2
                self.maxHit = 2.0
                self.damage = 1
            else:
                self.hitPoints = 500
                self.maxHit = 500.0
                self.damage = 2
                
            # Extra enemy abilities
            self.hasIdle = True
            if inID == SPRITE_FOOGJUMP: self.canJump = True
            # Extra ability properties
            self.idleFreq = 5
            self.idleLag = 3
            self.dieLag = 3
            if inID == SPRITE_FOOGJUMP:
                self.jumpAmount = -250
                self.jumpFreq = 3               
            # Frame definitions
            if inID != SPRITE_FOOG_WARRIOR: self.images = gfnLoad_Splice(32, 32, gfn_Zip("enemy_foog.png"), 1, 1)
            else: self.images = gfnLoad_Splice(32, 32, gfn_Zip("enemy_foog_warrior.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            self.walkFrame = 0
            self.walkMax = 3
            self.jumpFrame = 4
            self.idleFrame = 6
            self.idleMax = 8
            self.dieFrame = 9
            self.dieMax = 10
            # Physical properties
            self.speedRun = 35
            self.gravity = 450
            self.floatSpeed = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_FROG_WALK:
            # Hit Points
            self.hitPoints = 2
            self.maxHit = 2.0
            self.damage = 1
            # Extra ability properties
            self.dieLag = 0.75
            # Frame definitions
            self.images = gfnLoad_Splice(25, 23, gfn_Zip("enemy_frog_walk.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            self.walkFrame = 0
            self.walkMax = 5
            self.dieFrame = 6
            self.dieMax = 11
            # Physical properties
            self.speedRun = 35
            self.gravity = 450
            self.floatSpeed = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_FROG_SWIM:
            # Hit Points
            self.hitPoints = 2
            self.maxHit = 2.0
            self.damage = 1
            # Extra ability properties
            self.dieLag = 0.75
            # Frame definitions
            self.images = gfnLoad_Splice(25, 23, gfn_Zip("enemy_frog_swim.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            self.walkFrame = 0
            self.walkMax = 5
            self.dieFrame = 6
            self.dieMax = 11
            # Physical properties
            self.speedRun = 35
            self.gravity = 0
            self.floatSpeed = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_PLANTGUY:
            # Hit Points
            self.hitPoints = 2
            self.maxHit = 2.0
            self.damage = 1
            # Extra ability properties
            self.dieLag = 0.75
            # Frame definitions
            self.images = gfnLoad_Splice(32, 32, gfn_Zip("enemy_plantguy.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            self.walkFrame = 0
            self.walkMax = 5
            # Physical properties
            self.speedRun = 35
            self.gravity = 450
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
        elif inID == SPRITE_REDFISH:
            # Hit Points
            self.hitPoints = 2
            self.maxHit = 2.0
            self.damage = 1
            # Extra enemy abilities
            self.willFloat = True
            # Extra ability properties
            self.dieLag = 0.75
            # Frame definitions
            self.images = gfnLoad_Splice(32, 32, gfn_Zip("enemy_redfish.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 4
            self.walkFrame = 0
            self.walkMax = 1
            self.dieFrame = 2
            self.dieMax = 8
            # Physical properties
            self.speedRun = 35
            self.gravity = 0
            self.floatSpeed = 40
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
        elif inID == SPRITE_CHOMPERFISH:
            # Hit Points
            self.hitPoints = 2
            self.maxHit = 2.0
            self.damage = 3
            # Extra enemy abilities
            self.hasIdle = True
            self.willFloat = True
            self.canAttack = True
            self.hasClose = True
            # Extra ability properties
            self.dieLag = 0.75
            self.idleFreq = 5
            self.idleLag = 0.5
            self.idleFrame = 14
            self.idleMax = 18
            self.attackProximityX = 32
            self.attackProximityY = 32
            self.attackFrame = 19
            self.attackMax = 20
            self.attackLag = 0.5
            self.closeFrame = 7
            self.closeMax = 13
            # Frame definitions
            self.images = gfnLoad_Splice(32, 32, gfn_Zip("enemy_chomperfish.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 4
            self.walkFrame = 0
            self.walkMax = 6
            self.dieFrame = 21
            self.dieMax = 24
            # Physical properties
            self.speedRun = 55
            self.gravity = 0
            self.floatSpeed = 40
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_MINE:
            # Hit Points
            self.hitPoints = 9999999
            self.maxHit = 9999999
            self.damage = 0
            # Extra enemy abilities
            self.hasClose = True
            # Extra ability properties - NB the "close proximity" is 2x attack proximity
            self.attackProximityX = 6
            self.attackProximityY = 8
            self.closeFrame = 1
            self.closeMax = 4
            # Frame definitions
            self.images = gfnLoad_Splice(18, 14, gfn_Zip("enemy_mine.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 12
            self.walkFrame = 0
            self.walkMax = 0
            # Physical properties
            self.speedRun = 0
            self.gravity = 450
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
        elif inID == SPRITE_YELLOW:
            # Hit Points
            self.hitPoints = 8
            self.maxHit = 8.0
            self.damage = 4
            # Extra enemy abilities
            self.canAttack = True
            # Extra ability properties
            self.attackProximityX = 128.0
            self.attackProximityY = 64
            self.attackFrame = 5
            self.attackMax = 9
            self.attackLag = 1
            self.yellowPull = 200
            # Frame definitions
            self.images = gfnLoad_Splice(32, 64, gfn_Zip("enemy_yellow.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 4
            self.walkFrame = 0
            self.walkMax = 4
            self.dieFrame = 10
            self.dieMax = 16
            self.dieLag = 0.5
            # Physical properties
            self.speedRun = 20
            self.gravity = 450
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
        elif inID == SPRITE_FLOPPY:
            # Hit Points
            self.hitPoints = 2
            self.maxHit = 2.0
            self.damage = 1
            # Frame definitions
            self.images = gfnLoad_Splice(96, 32, gfn_Zip("enemy_floppy.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 4
            self.walkFrame = 0
            self.walkMax = 3
            # Physical properties
            self.speedRun = 35
            self.gravity = 450
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 7
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()         
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
        elif inID == SPRITE_HOLEMONSTER:
            # Hit Points
            self.hitPoints = 4
            self.maxHit = 4.0
            self.damage = 2
            # Extra enemy abilities
            self.hasIdle = True
            self.canAttack = True
            self.hasClose = True
            # Extra ability properties
            self.idleFreq = 3
            self.idleLag = 3
            self.idleFrame = 2
            self.idleMax = 2
            self.attackProximityX = 32
            self.attackProximityY = 32
            self.attackFrame = 3
            self.attackMax = 11
            self.attackLag = 0.5
            self.closeFrame = 1
            self.closeMax = 1
            # Frame definitions
            self.images = gfnLoad_Splice(38, 21, gfn_Zip("enemy_holemonster.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 4
            self.walkFrame = 0
            self.walkMax = 0
            self.dieFrame = 12
            self.dieMax = 12
            # Physical properties
            self.speedRun = 0
            self.gravity = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            # Fine tune the position so its in the center of the hole
            self.y += 10
            self.x -= 2
            
        elif inID == SPRITE_URCHIN:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 1
            # Extra enemy abilities
            self.canAttack = True
            # Extra ability properties
            self.attackProximityX = 50
            self.attackProximityY = 50
            self.attackFrame = 8
            self.attackMax = 11
            self.attackLag = 1
            # Frame definitions
            self.images = gfnLoad_Splice(16, 16, gfn_Zip("enemy_urchin.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 4
            self.walkFrame = 0
            self.walkMax = 7
            # Physical properties
            self.speedRun = 0
            self.gravity = 450
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
        elif inID == SPRITE_BLUEMOUTH:
            # Hit Points
            self.hitPoints = 8
            self.maxHit = 8.0
            self.damage = 3
            # Extra enemy abilities
            self.canAttack = True
            # Extra ability properties
            self.attackProximityX = 16
            self.attackProximityY = 48
            self.attackFrame = 6
            self.attackMax = 16
            self.attackLag = 0.5
            # Frame definitions
            self.images = gfnLoad_Splice(64, 64, gfn_Zip("enemy_bluemouth.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            self.walkFrame = 0
            self.walkMax = 5
            self.dieFrame = 17
            self.dieMax = 29
            self.dieLag = 0.8
            # Physical properties
            self.speedRun = 50
            self.gravity = 450       
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 32
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height() - 32        
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
        elif inID == SPRITE_CATERPILLAR:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 2.0
            self.damage = 0
            # Extra enemy abilities
            self.hasClose = True
            # Extra ability properties
            self.attackProximityX = 50
            self.attackProximityY = 20
            self.attackFrame = 19
            self.attackMax = 20
            self.attackLag = 0.5
            self.closeFrame = 1
            self.closeMax = 5
            # Frame definitions
            self.images = gfnLoad_Splice(75, 38, gfn_Zip("enemy_caterpillar.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            self.walkFrame = 0
            self.walkMax = 0
            # Physical properties
            self.speedRun = 0
            self.gravity = 450
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
        elif inID == SPRITE_SNAIL:
            # Hit Points
            self.hitPoints = 2
            self.maxHit = 2.0
            self.damage = 1
            # Frame definitions
            self.images = gfnLoad_Splice(64, 32, gfn_Zip("enemy_snail.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 4
            self.walkFrame = 0
            self.walkMax = 1
            # Physical properties
            self.speedRun = 10
            self.gravity = 450
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_GARNAK:
            # Hit Points
            self.hitPoints = 10
            self.maxHit = 10.0
            self.damage = 5
            # Frame definitions
            self.images = gfnLoad_Splice(96, 64, gfn_Zip("enemy_garnak.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            self.walkFrame = 0
            self.walkMax = 10
            self.dieFrame = 12
            self.dieMax = 19
            # Physical properties
            self.speedRun = 40
            self.gravity = 450
            # Rect properties
            self.rectOffsetX = 24
            self.rectOffsetY = 0
            self.rectW = self.image.get_width() - 48
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
        elif inID == SPRITE_TRUCKGUY1 or inID == SPRITE_TRUCKGUY2:
            # Hit Points
            self.hitPoints = 2
            self.maxHit = 2.0
            self.damage = 1
            # Extra ability properties
            self.dieLag = 1
            # Frame definitions
            if inID == SPRITE_TRUCKGUY1: self.images = gfnLoad_Splice(72, 64, gfn_Zip("enemy_truckguy2.png"), 1, 1)
            elif inID == SPRITE_TRUCKGUY2: self.images = gfnLoad_Splice(72, 64, gfn_Zip("enemy_truckguy1.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            self.walkFrame = 0
            self.walkMax = 3
            self.dieFrame = 0
            self.dieMax = 0
            self.fadeMax = 0.1
            # Physical properties
            self.speedRun = 50
            self.gravity = 450
            self.floatSpeed = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_YORPY:
            # Hit Points
            self.hitPoints = 1
            self.maxHit = 1.0
            self.damage = 0
            # Extra enemy abilities
            self.hasIdle = True
            # Extra ability properties
            self.idleFreq = 5              
            # Frame definitions
            self.images = gfnLoad_Splice(16, 24, gfn_Zip("enemy_yorp.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 4
            self.walkFrame = 0
            self.walkMax = 1
            self.idleFrame = 2
            self.idleMax = 5
            self.idleLag = 1.5
            self.dieFrame = 6
            self.dieMax = 7
            # Physical properties
            self.speedRun = 40
            self.gravity = 450
            self.floatSpeed = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_GARG:
            # Hit Points
            self.hitPoints = 1
            self.maxHit = 1.0
            self.damage = 1
            # Extra enemy abilities
            self.hasIdle = True
            # Extra ability properties
            self.idleFreq = 5              
            # Frame definitions
            self.images = gfnLoad_Splice(24, 32, gfn_Zip("enemy_garg.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 4
            self.walkFrame = 0
            self.walkMax = 1
            self.idleFrame = 2
            self.idleMax = 5
            self.dieFrame = 6
            self.dieMax = 7
            # Physical properties
            self.speedRun = 40
            self.gravity = 450
            self.floatSpeed = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        # UNFINISHED ENEMIES
        elif inID == SPRITE_YELLOWFISH or inID == SPRITE_GREENFISH or inID == SPRITE_BLUEFISH or inID == SPRITE_BIGFROG or inID == SPRITE_DRAGONFLY or inID == SPRITE_BIRD or inID == SPRITE_ISONIAN_GIANT1 or inID == SPRITE_ISONIAN_GIANT2 or inID == SPRITE_ISONIAN_FLY:
            # Hit Points
            self.hitPoints = 2
            self.maxHit = 2.0
            self.damage = 1
            # Physical properties
            self.speedRun = 35
            self.gravity = 0
            # Frame definitions
            if inID == SPRITE_YELLOWFISH: self.images = gfnLoad_Splice(32, 64, gfn_Zip("enemy_yellowfish.png"), 1, 1)
            elif inID == SPRITE_GREENFISH: self.images = gfnLoad_Splice(64, 32, gfn_Zip("enemy_greenfish.png"), 1, 1)
            elif inID == SPRITE_BLUEFISH: self.images = gfnLoad_Splice(128, 64, gfn_Zip("enemy_bluefish.png"), 1, 1)
            elif inID == SPRITE_BIGFROG: self.images = gfnLoad_Splice(46, 46, gfn_Zip("enemy_bigfrog.png"), 1, 1)
            elif inID == SPRITE_DRAGONFLY: self.images = gfnLoad_Splice(62, 62, gfn_Zip("enemy_dragonflyg.png"), 1, 1)
            elif inID == SPRITE_ISONIAN_FLY:
                self.images = gfnLoad_Splice(112, 38, gfn_Zip("enemy_isonian-fly.png"), 1, 1)
                self.speedRun = 70
                self.hitPoints = 10
                self.maxHit = 10.0
                self.damage = 5
                
            elif inID == SPRITE_BIRD:
                self.images = gfnLoad_Splice(64, 72, gfn_Zip("enemy_bird.png"), 1, 1)
                self.gravity = 450
            elif inID == SPRITE_ISONIAN_GIANT1:
                self.images = gfnLoad_Splice(64, 96, gfn_Zip("enemy_isonian_giant1.png"), 1, 1)
                self.gravity = 450
            elif inID == SPRITE_ISONIAN_GIANT2:
                self.images = gfnLoad_Splice(64, 96, gfn_Zip("enemy_isonian_giant2.png"), 1, 1)
                self.gravity = 450
                
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 4
            self.walkFrame = 0
            self.walkMax = 0            
            
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()         
            self.width = self.image.get_width()
            self.height = self.image.get_height()

            if inID == SPRITE_DRAGONFLY:
                self.hitPoints = 4
                self.maxHit = 4.0
                self.damage = 0
                self.walkMax = 3
                self.FPS = 1000.0 / 8
                self.dieFrame = 7
                self.dieMax = 7
                self.dieLag = 0.5
                self.jumpFrame = 3
                self.rectOffsetX = 12
                self.rectOffsetY = 24
                self.rectW = 42
                self.rectH = 19     
                
        self.rect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def updateSubRect(self):
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def update(self, t, t_elapsed, inLevel, inKeen):

        
        self.dirChange -= t_elapsed
        if self.dirChange < 0: self.dirChange = 0
               
        if self.state == ENEMY_STATE_WALK:
            self.moveAmountX = t_elapsed * self.speedRun

            # Special YORPY stuff - push Keen!
            if gfn_IsPushEnemy(self.id):
                if pygame.sprite.collide_mask(self, inKeen):
                    centreX , centreY  = self.x   + (self.width / 2.0)  , self.y   + (self.height / 2.0)
                    centreXk, centreYk = inKeen.x + (inKeen.width / 2.0), inKeen.y + (inKeen.height / 2.0)

                    if self.id == SPRITE_DRAGONFLY:
                        if self.direction == -1: centreX = self.x + 43
                        elif self.direction == 1: centreX = self.x + 19
                        
                    if ((self.direction == -1 and centreX > centreXk) or (self.direction == 1 and centreX < centreXk)):
                        inKeen.moveAmountX = self.moveAmountX
                        inKeen.vx = self.direction
                        inKeen.direction = self.direction
                        
                        for i in range(int(abs(self.moveAmountX))):
                            inKeen.keenPush(inLevel, 1 * inKeen.direction, 0)
                        inKeen.keenPush(inLevel, (self.moveAmountX % 1) * inKeen.direction, 0)

                        # Update Keen Rects & camera
                        inKeen.rect = pygame.Rect(inKeen.x - inLevel.mapX + inLevel.playX, inKeen.y - inLevel.mapY + inLevel.playY, 48, 48)
                        inKeen.updateSubRect()
                        inLevel.updateCamera(inKeen)
                        inKeen.idleTimer = 0
                        
                    
                            
            # Switch to close frames if applicable
            if self.hasClose == True and self.isClose == False:
                testX = (self.x + (self.width / 2.0)) - (inKeen.x + (inKeen.width / 2.0))
                testY = (self.y + (self.height / 2.0)) - (inKeen.y + (inKeen.height / 2.0))
                if abs(testX) < 2 * self.attackProximityX and abs(testY) < 2 * self.attackProximityY:
                    self.isClose = True
                    oldWalk, oldWalkMax = self.walkFrame, self.walkMax
                    self.walkFrame, self.walkMax = self.closeFrame, self.closeMax
                    self.closeFrame, self.closeMax = oldWalk, oldWalkMax
                    if self.id == SPRITE_CATERPILLAR or self.id == SPRITE_MINE: self.hasClose = False
                    
                    
            elif self.hasClose == True and self.isClose == True:
                if not abs(self.x - inKeen.x) < 2 * self.attackProximityX or not abs(self.y - inKeen.y) < 2 * self.attackProximityY:
                    self.isClose = False
                    oldWalk, oldWalkMax = self.walkFrame, self.walkMax
                    self.walkFrame, self.walkMax = self.closeFrame, self.closeMax
                    self.closeFrame, self.closeMax = oldWalk, oldWalkMax
                    
            # Walking (or Swimming)
            if self.onGround == True or self.gravity == 0:
                if t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.id == SPRITE_MINE and self.frame == self.walkMax:
                        self.damage = 10
                        
                    if self.frame > self.walkMax:
                        self.frame = self.walkFrame
                        # Special thing for Caterpillar
                        if self.id == SPRITE_CATERPILLAR and self.walkMax != 0:
                            self.walkFrame = 6
                            self.walkMax = 9
                            self.speedRun = 8
                            self.hitPoints = 2
                            self.maxHit = 2.0
                            self.damage = 1
                            self.FPS = 1000.0 / 2
                            self.frame = self.walkFrame
                        # Special thing for mine
                        elif self.id == SPRITE_MINE and self.isClose == True:
                            for i in range(50):
                                inLevel.sprite_Explosions.add(gcls_Particle(self.x + (random.random() * self.width), self.y + (random.random() * self.height), pTYPE_OTHER, pygame.time.get_ticks(),(255, 0, 255)))
                            self.kill()
                            gfn_PlaySound(SFX_ENEMY_MINE)
                            
                    self.last_update = t
                    
            # Jumping
            else:
                if self.vy < 0: self.frame = self.jumpFrame
                else:
                    if self.jumpFrame != 0: self.frame = self.jumpFrame + 1

            # Check for Idle State change
            if self.hasIdle == True:
                RND1 = int(random.random() * (1 / t_elapsed) * self.idleFreq)
                if RND1 == 1 and self.onGround == True:
                    self.state = ENEMY_STATE_IDLE
                    self.moveAmountX = 0

            # Check for Jumping State change
            if self.canJump == True and self.onGround == True:
                RND2 = int(random.random() * (1 / t_elapsed) * self.jumpFreq)
                if RND2 == 1:
                    self.vy = self.jumpAmount
                    self.moveAmountY = t_elapsed * self.vy
                    self.onGround = False
                    
                    # Play jump sound if within range
                    if self.x > inLevel.mapX and self.x < inLevel.mapX + inLevel.playWidth:
                        if self.y > inLevel.mapY and self.y < inLevel.mapY + inLevel.playHeight:
                            gfn_PlaySound(SFX_ENEMY_FOOG_JUMP)
                        
            # Check if within attack range
            closeX = abs((self.x + (self.width / 2.0)) - (inKeen.x + (inKeen.width / 2.0)))
            closeY = abs((self.y + (self.height / 2.0)) - (inKeen.y + (inKeen.height / 2.0)))
            if self.canAttack == True and closeX < self.attackProximityX and closeY < self.attackProximityY:
                #if self.id != SPRITE_YELLOW or (self.id == SPRITE_YELLOW and inKeen.idleTimer) > 0.1:
                self.state = ENEMY_STATE_ATTACK
                self.moveAmountX = 0
                # Change yellow direction
                if self.id == SPRITE_YELLOW:
                    if self.x < inKeen.x: self.direction = 1
                    else: self.direction = -1

                # Adjust Bluemouth position
                elif self.id == SPRITE_BLUEMOUTH:
                    self.x -= 15 * self.direction
                self.frame = self.attackFrame
            
        elif self.state == ENEMY_STATE_IDLE:
            if self.frame < self.idleFrame:
                self.frame = self.idleFrame
                self.last_update = t
            if t - self.last_update > (self.FPS * self.idleLag):
                self.frame += 1
                self.last_update = t
                if self.frame > self.idleMax:
                    self.frame = self.walkFrame
                    self.state = ENEMY_STATE_WALK
                    
                    # Set random direction
                    RND = int(round(random.random() * 3))
                    if RND == 0: self.direction = self.direction * -1


                        
        elif self.state == ENEMY_STATE_ATTACK:
            if self.frame < self.attackFrame:
                self.frame = self.attackFrame
                self.last_update = t

            # Yellow guy stuff here
            if self.id == SPRITE_YELLOW and self.frame == self.attackMax:
                
                # Re-check direction facing
                if self.dirChange == 0:
                    if self.x < inKeen.x:
                        self.direction = 1
                        self.dirChange = 2
                    else:
                        self.direction = -1
                        self.dirChange = 2

                # Check if within attack range
                closeX = abs((self.x + (self.width / 2.0)) - (inKeen.x + (inKeen.width / 2.0)))
                closeY = abs((self.y + (self.height / 2.0)) - (inKeen.y + (inKeen.height / 2.0)))

                if closeX < self.attackProximityX and closeY < self.attackProximityY:

                    # moveAmount is scaled by how far away Keen is from the enemy
                    moveAmount = t_elapsed * self.yellowPull * (((self.attackProximityX - closeX)**2) / (self.attackProximityX**2))

                    # Only push if on the ground or in the air
                    if inKeen.state == kON_GROUND or inKeen.state == kFALLING:
                        if self.x > inKeen.x:
                            #inKeen.extraX = moveAmount
                            #inKeen.vx = 1
                            #inKeen.direction = 1

                            #inKeen.x += moveAmount

                            inKeen.moveAmountX = moveAmount
                            inKeen.vx = 1
                            inKeen.direction = 1
                            for i in range(int(abs(moveAmount))):
                                inKeen.keenPush(inLevel, 1 * inKeen.direction, 0)
                            inKeen.keenPush(inLevel, (moveAmount % 1) * inKeen.direction, 0)

                            # Update Keen Rects & camera
                            inKeen.rect = pygame.Rect(inKeen.x - inLevel.mapX + inLevel.playX, inKeen.y - inLevel.mapY + inLevel.playY, 48, 48)
                            inKeen.updateSubRect()
                            inLevel.updateCamera(inKeen)
                            inKeen.idleTimer = 0
                            
                        else:
                            #inKeen.extraX = moveAmount
                            #inKeen.vx = -1
                            #inKeen.direction = -1

                            #inKeen.x -= moveAmount

                            inKeen.moveAmountX = moveAmount
                            inKeen.vx = -1
                            inKeen.direction = -1
                            for i in range(int(abs(moveAmount))):
                                inKeen.keenPush(inLevel, 1 * inKeen.direction, 0)
                            inKeen.keenPush(inLevel, (moveAmount % 1) * inKeen.direction, 0)

                            # Update Keen Rects & camera
                            inKeen.rect = pygame.Rect(inKeen.x - inLevel.mapX + inLevel.playX, inKeen.y - inLevel.mapY + inLevel.playY, 48, 48)
                            inKeen.updateSubRect()
                            inLevel.updateCamera(inKeen)
                            inKeen.idleTimer = 0
                            
                    # If on a pole, or on a ledge, make him fall
                    elif inKeen.state == kON_POLE or inKeen.state == kON_LEDGE:
                        inKeen.state = kFALLING

                else:
                    self.frame = self.walkFrame
                    self.state = ENEMY_STATE_WALK
                    
            # Normal frame change here  
            elif t - self.last_update > (self.FPS * self.attackLag):
                self.frame += 1
                self.last_update = t
                if self.frame > self.attackMax:
                    if self.id != SPRITE_YELLOW:
                        self.frame = self.walkFrame
                        self.state = ENEMY_STATE_WALK
                    if self.id == SPRITE_BLUEMOUTH:
                        self.x += 15 * self.direction
                            
        elif self.state == ENEMY_STATE_DIE:
            if self.dieFrame != 0:
                if self.frame < self.dieFrame:
                    self.frame = self.dieFrame
                    self.last_update = t
                elif t - self.last_update > self.FPS * self.dieLag:
                    self.frame += 1
                    self.last_update = t
                    if self.frame > self.dieMax:
                        self.frame = self.dieMax
                        
            else:
                self.fadeTime += t_elapsed
                
                
            # If Enemy "floats" when dead, move it up until it is at the top of the water
            if self.frame == self.dieMax and self.willFloat == True:
                TileX = int(round((self.x + (self.width / 2.0)) / TILESIZE))
                TileY = int(round(self.y / TILESIZE))
                if inLevel.INFO[TileX][TileY] == INFO_WATER:
                    self.y -= t_elapsed * self.floatSpeed
        
        if self.direction == -1: self.image = self.images[self.frame]
        elif self.direction == 1: self.image = pygame.transform.flip(self.images[self.frame], True, False)                    

        # Added extra to cope with fading deaths
        if self.state == ENEMY_STATE_DIE and self.dieFrame == 0:
            self.image.set_alpha(255 - ((self.fadeTime / self.fadeMax) * 255))
            if 255 - ((self.fadeTime / self.fadeMax) * 255) <= 0: self.kill()
            
        # Push player left/right, in 1-pixel increments
        if self.direction != 0:
            for i in range(int(abs(self.moveAmountX))):
                gfn_PushEnemy(self, inLevel, 1 * self.direction, 0)
            gfn_PushEnemy(self, inLevel, (self.moveAmountX % 1) * self.direction, 0)
            
        # GRAVITY:
        if self.moveAmountY < 0:
            for i in range(int(abs(self.moveAmountY))):
                gfn_PushEnemy(self, inLevel, 0, -1)
            gfn_PushEnemy(self, inLevel, 0, (self.moveAmountY % -1))
        elif self.moveAmountY > 0:
            for i in range(int(abs(self.moveAmountY))):
                if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, 1)
            if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, self.moveAmountY % 1)
            
            
        if self.onGround == False:
            self.vy += t_elapsed * self.gravity
            self.moveAmountY = t_elapsed * self.vy

        self.updateSubRect()
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)


        #inKeen.message = "(X,Y) = (" + str(self.x) + "," + str(self.y) + "), Rect: " + str(self.rect[0]) + "," + str(self.rect[1]) + "," + str(self.rect[2]) + "," + str(self.rect[3])
        #inKeen.message = "(X,Y) = (" + str(self.x) + "," + str(self.y) + "), Rect X - 270: " + str(self.rect[0] - round(270 - inLevel.mapX + inLevel.playX))
        
        """
        # If a dead enemy is out of sight by half a playing field, remove it
        if self.state == ENEMY_STATE_DIE:
            if self.rect[0] + self.rect.width + (inLevel.playWidth / 2) < 0 or self.rect[0] - (inLevel.playWidth / 2) > inLevel.playWidth:
                self.kill()
            elif self.rect[1] + self.rect.height + (inLevel.playHeight / 2) < 0 or self.rect[1] - (inLevel.playHeight / 2) > inLevel.playHeight:
                self.kill()
        """


#_______________________________________________________________________________________________
# Enemy Class - SIMPLE SHOOTING ENEMY
# This enemy can shoot and jump, that's all
# We can specify the criteria when the enemy will shoot, as well as the type of bullet
class gcls_Enemy_Shooter(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir):

        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.vx = 1
        self.vy = 0
        self.moveAmountX = 0
        self.moveAmountY= 0
        self.onGround = False
        self.last_update = pygame.time.get_ticks()
        self.oldTimer = pygame.time.get_ticks()
        t_elapsed = 0.1
        self.frame = 0
        self.dirChange = 0
        self.direction = inDir
        self.state = ENEMY_STATE_WALK
        self.bullet = False
        self.fadeTime = 0
        self.fadeMax = 1.5
        
        # Set a few initial properties
        # By default these won't change unless specified under a particular enemy
        self.canJump = False
        self.hasIdle = False
        self.jumpFreq = 0
        self.jumpAmount = 0
        self.jumpFrame = 0
        self.dieFrame = 0
        self.dieLag = 1
        self.idleFreq = 0
        self.idleLag = 0
        self.idleFrame = 0
        self.idleMax = 0
        self.shotRandom = False
        self.shotRandomFreq = 0
        self.shootProximityX = 0
        self.shootProximityY = 0
            
        # Now set stuff specific to all the individual enemies
        if inID == SPRITE_RAT:
            # Hit Points
            self.hitPoints = 20
            self.maxHit = 20.0
            self.damage = 5              
            # Frame definitions
            self.images = gfnLoad_Splice(64, 48, gfn_Zip("enemy_rat.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            self.walkFrame = 0
            self.walkMax = 6
            self.shootFrame = 7
            self.shootRelease = 8
            self.shootMax = 9
            self.dieFrame = 10
            self.dieMax = 13
            # Physical properties
            self.speedRun = 65
            self.gravity = 450
            self.bulletSprite = SPRITE_RAT_BULLET
            self.shootProximityX = 50
            self.shootProximityY = 10
            self.shotDelay = 3
            self.shotTimer = 0
            # Rect properties
            self.rectOffsetX = 16
            self.rectOffsetY = 0
            self.rectW = self.image.get_width() - 32
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_LEMMING:
            # Hit Points
            self.hitPoints = 4
            self.maxHit = 4.0
            self.damage = 2              
            # Frame definitions
            self.images = gfnLoad_Splice(64, 48, gfn_Zip("enemy_lemming.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            self.walkFrame = 0
            self.walkMax = 6
            self.shootFrame = 7
            self.shootRelease = 8
            self.shootMax = 9
            self.dieFrame = 10
            self.dieMax = 13
            # Physical properties
            self.speedRun = 40
            self.gravity = 450
            self.bulletSprite = SPRITE_RAT_BULLET
            self.shootProximityX = 100
            self.shootProximityY = 16
            self.shotDelay = 3
            self.shotTimer = 0
            # Rect properties
            self.rectOffsetX = 16
            self.rectOffsetY = 0
            self.rectW = self.image.get_width() - 32
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_SPIDER:
            # Hit Points
            self.hitPoints = 2
            self.maxHit = 2.0
            self.damage = 2              
            # Frame definitions
            self.images = gfnLoad_Splice(32, 32, gfn_Zip("enemy_spider.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            self.walkFrame = 0
            self.walkMax = 7
            self.shootFrame = 8
            self.shootRelease = 9
            self.shootMax = 10
            self.dieFrame = 11
            self.dieMax = 13
            # Physical properties
            self.speedRun = 50
            self.gravity = 450
            self.bulletSprite = SPRITE_SPIDER_PROJ
            self.shotRandom = True
            self.shotRandomFreq = 3
            self.shotDelay = 3
            self.shotTimer = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = -5
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_TRUCKGUY1_WALK:
            # Hit Points
            self.hitPoints = 4
            self.maxHit = 4.0
            self.damage = 2              
            # Frame definitions
            self.images = gfnLoad_Splice(64, 48, gfn_Zip("enemy_truckguy2_walk.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            self.walkFrame = 0
            self.walkMax = 6
            self.shootFrame = 7
            self.shootRelease = 8
            self.shootMax = 9
            self.dieFrame = 10
            self.dieMax = 13
            # Physical properties
            self.vy = -100
            self.speedRun = 40
            self.gravity = 450
            self.bulletSprite = SPRITE_RAT_BULLET
            self.shootProximityX = 100
            self.shootProximityY = 20
            self.shotDelay = 0.2
            self.shotTimer = 0
            # Rect properties
            self.rectOffsetX = 16
            self.rectOffsetY = 0
            self.rectW = self.image.get_width() - 32
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_TRUCKGUY2_WALK:
            # Hit Points
            self.hitPoints = 6
            self.maxHit = 6.0
            self.damage = 2              
            # Frame definitions
            self.images = gfnLoad_Splice(64, 48, gfn_Zip("enemy_truckguy1_walk.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            self.walkFrame = 0
            self.walkMax = 6
            self.shootFrame = 7
            self.shootRelease = 8
            self.shootMax = 9
            self.dieFrame = 10
            self.dieMax = 13
            # Physical properties
            self.vy = -100
            self.speedRun = 40
            self.gravity = 450
            self.bulletSprite = SPRITE_RAT_BULLET
            self.shootProximityX = 100
            self.shootProximityY = 20
            self.shotDelay = 1
            self.shotTimer = 0
            # Rect properties
            self.rectOffsetX = 16
            self.rectOffsetY = 0
            self.rectW = self.image.get_width() - 32
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_ROBOT_GREY:
            # Hit Points
            self.hitPoints = 8
            self.maxHit = 8.0
            self.damage = 3              
            # Extra Properties
            self.hasIdle = True
            self.idleFreq = 3
            self.idleLag = 1
            self.idleFrame = 4
            self.idleMax = 5
            # Frame definitions
            self.images = gfnLoad_Splice(32, 48, gfn_Zip("enemy_robot_grey.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            self.walkFrame = 0
            self.walkMax = 3
            self.shootFrame = 6
            self.shootRelease = 7
            self.shootMax = 8
            self.dieFrame = 9
            self.dieMax = 11
            # Physical properties
            self.speedRun = 40
            self.gravity = 450
            self.bulletSprite = SPRITE_ROBOT_GREY_BULLET
            self.shootProximityX = 100
            self.shootProximityY = 10
            self.shotDelay = 3
            self.shotTimer = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_ROBOT_RED:
            # Hit Points
            self.hitPoints = 8
            self.maxHit = 8.0
            self.damage = 3              
            # Frame definitions
            self.images = gfnLoad_Splice(48, 48, gfn_Zip("enemy_robot_red.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            self.walkFrame = 0
            self.walkMax = 7
            self.shootFrame = 8
            self.shootRelease = 13
            self.shootMax = 19
            self.dieFrame = 20
            self.dieMax = 26
            # Physical properties
            self.speedRun = 40
            self.gravity = 450
            self.bulletSprite = SPRITE_ROBOT_RED_BULLET
            self.shootProximityX = 50
            self.shootProximityY = 10
            self.shotDelay = 5
            self.shotTimer = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
        elif inID == SPRITE_ROBOT_FLASHER:
            # Hit Points
            self.hitPoints = 8
            self.maxHit = 8.0
            self.damage = 3
            # Extra Properties
            self.hasIdle = True
            self.idleFreq = 2
            self.idleLag = 1
            self.idleFrame = 4
            self.idleMax = 7
            # Frame definitions
            self.images = gfnLoad_Splice(78, 46, gfn_Zip("enemy_flasher.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            self.walkFrame = 0
            self.walkMax = 3
            self.shootFrame = 8
            self.shootRelease = 11
            self.shootMax = 13
            self.dieFrame = 14
            self.dieMax = 19
            self.shotDelay = 3
            self.shotTimer = 0
            # Physical properties
            self.speedRun = 75
            self.gravity = 450
            self.bulletSprite = SPRITE_ROBOT_RED_BULLET
            self.shootProximityX = 100
            self.shootProximityY = 10
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_ROBOT_HOVER:
            # Hit Points
            self.hitPoints = 8
            self.maxHit = 8.0
            self.damage = 3
            # Frame definitions
            self.images = gfnLoad_Splice(47, 40, gfn_Zip("enemy_hover.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            self.walkFrame = 0
            self.walkMax = 3
            self.shootFrame = 4
            self.shootRelease = 5
            self.shootMax = 6
            # Physical properties
            self.speedRun = 75
            self.gravity = 0
            self.bulletSprite = SPRITE_HOVER_BULLET
            self.shootProximityX = 50
            self.shootProximityY = 200
            self.shotDelay = 0.5
            self.shotTimer = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
        elif inID == SPRITE_DEMON:
            # Hit Points
            self.hitPoints = 6
            self.maxHit = 6.0
            self.damage = 3
            # Extra Properties
            self.hasIdle = True
            self.idleFreq = 3
            self.idleLag = 1
            self.idleFrame = 4
            self.idleMax = 13
            # Frame definitions
            self.images = gfnLoad_Splice(48, 48, gfn_Zip("enemy_demon.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            self.walkFrame = 0
            self.walkMax = 3
            self.shootFrame = 14
            self.shootRelease = 15
            self.shootMax = 16
            self.dieFrame = 17
            self.dieMax = 19
            self.dieLag = 2
            # Physical properties
            self.speedRun = 100
            self.gravity = 450
            self.bulletSprite = SPRITE_DEMON_FIREBALL
            self.shootProximityX = 50
            self.shootProximityY = 10
            self.shotDelay = 3
            self.shotTimer = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        elif inID == SPRITE_SLUG:
            # Hit Points
            self.hitPoints = 2
            self.maxHit = 2.0
            self.damage = 1              
            # Frame definitions
            self.images = gfnLoad_Splice(32, 32, gfn_Zip("enemy_slug.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 4
            self.walkFrame = 0
            self.walkMax = 1
            self.shootFrame = 2
            self.shootRelease = 3
            self.shootMax = 3
            self.dieFrame = 4
            self.dieMax = 7
            # Physical properties
            self.speedRun = 30
            self.gravity = 450
            self.bulletSprite = SPRITE_SLUG_PROJ
            self.shotRandom = True
            self.shotRandomFreq = 2
            self.shotDelay = 3
            self.shotTimer = 0
            # Rect properties
            self.rectOffsetX = 0
            self.rectOffsetY = 0
            self.rectW = self.image.get_width()
            self.rectH = self.image.get_height()           
            self.width = self.image.get_width()
            self.height = self.image.get_height()

            
        self.rect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def updateSubRect(self):
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def update(self, t, t_elapsed, inLevel, inKeen):

        self.dirChange -= t_elapsed
        if self.dirChange < 0: self.dirChange = 0

        # Adjust shot timer
        if self.shotTimer > 0: self.shotTimer -= t_elapsed
        if self.shotTimer <= 0: self.shotTimer = 0

        
        if self.state == ENEMY_STATE_WALK:
            self.moveAmountX = t_elapsed * self.speedRun
                    
            # Walking (or Swimming)
            if self.onGround == True or self.gravity == 0:
                if t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.frame > self.walkMax: self.frame = self.walkFrame     
                    self.last_update = t

            # Jumping
            else:
                if self.vy < 0: self.frame = self.jumpFrame
                else: self.frame = self.jumpFrame + 1

            # Check for Jumping State change
            if self.canJump == True and self.onGround == True:
                RND2 = int(random.random() * (1 / t_elapsed) * self.jumpFreq)
                if RND2 == 1:
                    self.vy = self.jumpAmount
                    self.moveAmountY = t_elapsed * self.vy
                    self.onGround = False
                    
            # Check for Idle State change
            if self.hasIdle == True:
                RND1 = int(random.random() * (1 / t_elapsed) * self.idleFreq)
                if RND1 == 1:
                    self.state = ENEMY_STATE_IDLE
                    # Speed up the Grey Robot for the "Idle" phase
                    if self.id == SPRITE_ROBOT_GREY: self.moveAmountX = self.moveAmountX * 2.5
                    # Otherwise halt movement
                    else: self.moveAmountX = 0
            
            # If shotTimer is zero (ie they can shoot)
            
            # Precision Shooters
            if self.shotRandom == False:
                if self.id != SPRITE_ROBOT_HOVER:
                    # Check if within shoot range, and if shooter is facing Keen (otherwise they shoot away from him)
                    checkEnemyX = self.x + self.rectOffsetX + (self.rectW / 2.0)
                    checkEnemyY = self.y + self.height
                    checkKeenX = inKeen.x + (inKeen.width / 2.0)
                    checkKeenY = inKeen.y + inKeen.height
                    checkFacing = False
                    if (self.direction == -1 and self.x > inKeen.x) or (self.direction == 1 and self.x < inKeen.x):
                        checkFacing = True
                    if abs(checkEnemyX - checkKeenX) < self.shootProximityX and abs(checkEnemyY - checkKeenY) < self.shootProximityY and checkFacing == True:
                        self.moveAmountX = 0
                        self.frame = self.shootFrame
                        if self.shotTimer == 0:
                            self.state = ENEMY_STATE_ATTACK
                            self.shotTimer = self.shotDelay
                
                else:
                    # Special check for the Hover (need to check diagonal lines, ie gradient ~ 1)
                    if self.y < inKeen.y:
                        checkFacing = False
                        if (self.direction == -1 and self.x > inKeen.x) or (self.direction == 1 and self.x < inKeen.x):
                            checkFacing = True
                        gradient = (self.y - inKeen.y - inKeen.height) / (self.x - inKeen.x)
                        if abs(gradient) > 0.8 and abs(gradient) < 1.2 and checkFacing == True:
                            self.moveAmountX = 0
                            self.frame = self.shootFrame
                            if self.shotTimer == 0:
                                self.state = ENEMY_STATE_ATTACK
                                self.shotTimer = self.shotDelay
                            
            # Random Shooters (eg Spider, Slug)
            else:
                RND = int(round(random.random() * (1 / t_elapsed) * self.shotRandomFreq))
                if RND == 0:
                    self.moveAmountX = 0
                    self.frame = self.shootFrame
                    if self.shotTimer == 0:
                        self.state = ENEMY_STATE_ATTACK
                        self.shotTimer = self.shotDelay
                        
        elif self.state == ENEMY_STATE_IDLE:
            if self.frame < self.idleFrame:
                self.frame = self.idleFrame
                self.last_update = t
            if t - self.last_update > (self.FPS * self.idleLag):
                self.frame += 1
                self.last_update = t
                if self.frame > self.idleMax:
                    # Let the Grey Robot charge for a little bit longer - at random
                    if self.id == SPRITE_ROBOT_GREY:
                        self.frame = self.idleFrame
                        RND = int(round(random.random() * 2))
                        if RND == 0: self.state = ENEMY_STATE_WALK
                    # If not the Grey Robot, back to walking
                    else:
                        self.frame = self.walkFrame
                        self.state = ENEMY_STATE_WALK
                    
        elif self.state == ENEMY_STATE_ATTACK:
                if self.frame < self.shootFrame:
                    self.frame = self.shootFrame
                    self.last_update = t
                elif t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.frame == self.shootRelease:
                        
                        if self.id != SPRITE_SLUG:
                            bullet = gcls_Enemy_Bullet(self.x / TILESIZE, self.y / TILESIZE, self.bulletSprite, self.direction)
                            inLevel.sprite_Enemies.add(bullet)
                        else:
                            poison = gcls_Enemy_Poison(self.x, self.y, self.bulletSprite, self.direction)
                            inLevel.sprite_Enemies.add(poison)
                            # Play slug sound if in range
                            if self.x > inLevel.mapX and self.x < inLevel.mapX + inLevel.playWidth:
                                if self.y > inLevel.mapY and self.y < inLevel.mapY + inLevel.playHeight:
                                    gfn_PlaySound(SFX_ENEMY_SLUG)
                            
                    if self.frame == self.shootMax:
                        self.frame = 0
                        self.state = ENEMY_STATE_WALK
                    self.last_update = t
                    
        elif self.state == ENEMY_STATE_DIE:
            if self.dieFrame != 0:
                if self.frame < self.dieFrame:
                    self.frame = self.dieFrame
                    self.last_update = t
                elif t - self.last_update > self.FPS * self.dieLag:
                    self.frame += 1
                    self.last_update = t
                    if self.frame > self.dieMax:
                        # Quick fix to continue the spinning head for the slug
                        if self.id != SPRITE_SLUG: self.frame = self.dieMax
                        else: self.frame = self.dieFrame + 1
                        
            else:
                self.fadeTime += t_elapsed
                
        if self.direction == -1: self.image = self.images[self.frame]
        elif self.direction == 1: self.image = pygame.transform.flip(self.images[self.frame], True, False)                    

        # Added extra to cope with fading deaths
        if self.state == ENEMY_STATE_DIE and self.dieFrame == 0:
            self.image.set_alpha(255 - ((self.fadeTime / self.fadeMax) * 255))
            if 255 - ((self.fadeTime / self.fadeMax) * 255) <= 0: self.kill()
            
        # Push player left/right, in 1-pixel increments
        if self.direction != 0:
            for i in range(int(abs(self.moveAmountX))):
                gfn_PushEnemy(self, inLevel, 1 * self.direction, 0)
            gfn_PushEnemy(self, inLevel, (self.moveAmountX % 1) * self.direction, 0)
            
        # GRAVITY:
        if self.moveAmountY < 0:
            for i in range(int(abs(self.moveAmountY))):
                gfn_PushEnemy(self, inLevel, 0, -1)
            gfn_PushEnemy(self, inLevel, 0, (self.moveAmountY % -1))
        elif self.moveAmountY > 0:
            for i in range(int(abs(self.moveAmountY))):
                if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, 1)
            if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, self.moveAmountY % 1)
            
            
        if self.onGround == False:
            self.vy += t_elapsed * self.gravity
            self.moveAmountY = t_elapsed * self.vy

        self.updateSubRect()
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)

        """
        # If a dead enemy is out of sight by half a playing field, remove it
        if self.state == ENEMY_STATE_DIE:
            if self.rect[0] + self.rect.width + (inLevel.playWidth / 2) < 0 or self.rect[0] - (inLevel.playWidth / 2) > inLevel.playWidth:
                self.kill()
            elif self.rect[1] + self.rect.height + (inLevel.playHeight / 2) < 0 or self.rect[1] - (inLevel.playHeight / 2) > inLevel.playHeight:
                self.kill()
        """
        
#_______________________________________________________________________________________________
# Enemy Class - ISONIAN
class gcls_Enemy_Isonian(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir):

        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.vx = 1
        self.vy = 0
        self.moveAmountX = 0
        self.moveAmountY= 0
        self.onGround = False
        self.last_update = pygame.time.get_ticks()
        self.oldTimer = pygame.time.get_ticks()
        t_elapsed = 0.1
        self.frame = 0
        self.dirChange = 0
        self.direction = inDir
        self.state = ENEMY_STATE_WALK
        self.bullet = False
        self.fadeTime = 0
        self.fadeMax = 1.5
        
        # Set a few initial properties
        # By default these won't change unless specified under a particular enemy
        self.canJump = False
        self.hasIdle = False
        self.jumpFreq = 0
        self.jumpAmount = 0
        self.jumpFrame = 0
        self.dieFrame = 0
        self.dieLag = 0.9
        self.idleFreq = 0
        self.idleLag = 0.5
        self.idleFrame = 16
        self.idleMax = 20
        self.shotRandom = False
        self.shotRandomFreq = 0
        self.shootProximityX = 0
        self.shootProximityY = 0
            
        #Green - Regular: walks around and shoots at you if he see you.
        #Red - Military: agressive, as above. If weak, will teleport away to recharge; if strong will teleport close and attack.
        #White - Scientist: runs away normally and does no damage, if attacked will fight back with high aggression and damage.

        # Now set stuff specific to all the individual enemies
        if inID == SPRITE_ISONIAN_GREEN:
            # Hit Points
            self.hitPoints = 10
            self.maxHit = 10.0
            self.damage = 2
            # Other
            self.images = gfnLoad_Splice(30, 40, gfn_Zip("enemy_isonian-green.png"), 1, 1)
            self.speedRun = 40
            self.FPS = 1000.0 / 8
            self.bulletSprite = SPRITE_ISONIAN_PROJ1g
            self.shootProximityX = 96
            self.shootProximityY = 16
            
        elif inID == SPRITE_ISONIAN_RED:
            # Hit Points
            self.hitPoints = 10
            self.maxHit = 10.0
            self.damage = 5
            # Other
            self.images = gfnLoad_Splice(30, 40, gfn_Zip("enemy_isonian-red.png"), 1, 1)
            self.speedRun = 30
            self.FPS = 1000.0 / 6
            self.dieLag = 0.675
            self.idleLag = 0.375
            self.bulletSprite = SPRITE_ISONIAN_PROJ1r
            self.shootProximityX = 96
            self.shootProximityY = 16
            
        elif inID == SPRITE_ISONIAN_WHITE:
            # Hit Points
            self.hitPoints = 10
            self.maxHit = 10.0
            self.damage = 1
            # Other
            self.images = gfnLoad_Splice(30, 40, gfn_Zip("enemy_isonian-white.png"), 1, 1)
            self.speedRun = 50
            self.FPS = 1000.0 / 10
            self.dieLag = 1.125
            self.idleLag = 0.625
            self.bulletSprite = SPRITE_ISONIAN_PROJ1w
            self.shootProximityX = 96
            self.shootProximityY = 16
            
        # Frame definitions
        self.image = self.images[self.frame]
        self.walkFrame = 0
        self.walkMax = 7
        self.shootFrame = 11
        self.shootRelease = 13
        self.shootMax = 15
        self.dieFrame = 24
        self.dieMax = 31
        # Physical properties
        self.gravity = 450
        self.shotDelay = 1
        self.shotTimer = 0
        # Rect properties
        self.rectOffsetX = 0
        self.rectOffsetY = 0
        self.rectW = self.image.get_width()
        self.rectH = self.image.get_height()           
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Teleporting stuff
        self.oldX = self.x
        self.oldY = self.y
        self.safe = 0
        # NB, the "safe" property is a "sub-state" of the IDLE state
        # 0 = normal
        # 1 = normal > safe (disappear)
        # 2 = normal > safe (reappear)
        # 3 = safe
        # 4 = safe > normal (disappear)
        # 5 = safe > normal (reappear)

        # Rect
        self.rect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def updateSubRect(self):
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def update(self, t, t_elapsed, inLevel, inKeen):

        self.dirChange -= t_elapsed
        if self.dirChange < 0: self.dirChange = 0

        # Adjust shot timer
        if self.shotTimer > 0: self.shotTimer -= t_elapsed
        if self.shotTimer <= 0: self.shotTimer = 0

        
        if self.state == ENEMY_STATE_WALK:
            self.moveAmountX = t_elapsed * self.speedRun
                    
            # Walking
            if self.onGround == True or self.gravity == 0:
                if t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.frame > self.walkMax: self.frame = self.walkFrame     
                    self.last_update = t


            # If health is below threshold, change state
            if self.safe == 0 and self.hitPoints < (self.maxHit / 2.0):
                self.moveAmountX = 0
                self.state = ENEMY_STATE_IDLE
                self.bullet = True
                self.safe = 1

            # If enemy is safe, add hitpoints
            elif self.safe == 3 and self.hitPoints < self.maxHit:
                self.hitPoints += t_elapsed / 3.0
                # If is fully recharged, change state
                if self.hitPoints >= self.maxHit:
                    self.hitPoints = self.maxHit
                    self.moveAmountX = 0
                    self.state = ENEMY_STATE_IDLE
                    self.bullet = True
                    self.safe = 4
               


                
            # If shotTimer is zero (ie they can shoot)
            
            # Precision Shooters
            if self.shotRandom == False:
                # Check if within shoot range, and if shooter is facing Keen (otherwise they shoot away from him)
                checkEnemyX = self.x + self.rectOffsetX + (self.rectW / 2.0)
                checkEnemyY = self.y + self.height
                checkKeenX = inKeen.x + (inKeen.width / 2.0)
                checkKeenY = inKeen.y + inKeen.height
                checkFacing = False
                if (self.direction == -1 and self.x > inKeen.x) or (self.direction == 1 and self.x < inKeen.x):
                    checkFacing = True

                # If within range...
                if abs(checkEnemyX - checkKeenX) < self.shootProximityX and abs(checkEnemyY - checkKeenY) < self.shootProximityY and checkFacing == True:

                    # The white Isonian only shoots if he has been shot
                    if self.id != SPRITE_ISONIAN_WHITE or (self.id == SPRITE_ISONIAN_WHITE and self.hitPoints < self.maxHit):
                        if self.shotTimer == 0:
                            self.moveAmountX = 0
                            self.frame = self.shootFrame
                            self.state = ENEMY_STATE_ATTACK
                            self.shotTimer = self.shotDelay

                    # Otherwise the white Isonian will change direction
                    elif self.id == SPRITE_ISONIAN_WHITE and self.dirChange == 0:
                        self.direction *= -1
                        self.dirChange = 2
                                      
        elif self.state == ENEMY_STATE_IDLE:

            # Set initial frame
            if (self.safe == 1 or self.safe == 4) and self.frame < self.idleFrame:
                self.frame = self.idleFrame
                self.last_update = t
                   
            if t - self.last_update > (self.FPS * self.idleLag):
                # Change frame
                if self.safe == 1 or self.safe == 4: self.frame += 1
                elif self.safe == 2 or self.safe == 5: self.frame -= 1
                self.last_update = t
                
                if self.safe == 1 and self.frame > self.idleMax:
                    # Update state
                    self.safe = 2
                    self.frame = self.idleMax
                    # Save old coordinates
                    self.oldX = self.x
                    self.oldY = self.y
                        
                    # Teleport (if there are any tele tiles)
                    if len(inLevel.EnemyTeleList) > 0:

                        # Find nearest tele spot
                        tempTile = None
                        for teleTile in inLevel.EnemyTeleList:
                            tempDistance = math.sqrt(((self.x - teleTile.x)**2) + ((self.y - teleTile.y)**2))
                            if tempTile == None:
                                tempTile = teleTile
                                tempTravel = tempDistance
                            else:
                                if tempDistance < tempTravel:
                                    tempTile = teleTile
                                    tempTravel = tempDistance
                                    
                        # Move to new spot
                        self.x = tempTile.x
                        self.y = tempTile.y + 8
                            
                elif self.safe == 4 and self.frame > self.idleMax:
                    # Update state
                    self.safe = 5
                    self.frame = self.idleMax
                    # Move to original spot
                    self.x = self.oldX
                    self.y = self.oldY

                elif self.safe == 2 and self.frame < self.idleFrame:
                    self.safe = 3
                    self.frame = self.walkFrame
                    self.state = ENEMY_STATE_WALK
                    self.bullet = False
                    
                elif self.safe == 5 and self.frame < self.idleFrame:
                    self.safe = 0
                    self.frame = self.walkFrame
                    self.state = ENEMY_STATE_WALK
                    self.bullet = False
                    
        elif self.state == ENEMY_STATE_ATTACK:
                if self.frame < self.shootFrame:
                    self.frame = self.shootFrame
                    self.last_update = t
                elif t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.frame == self.shootRelease:
                        bullet = gcls_Enemy_Bullet(self.x / TILESIZE, self.y / TILESIZE, self.bulletSprite, self.direction)
                        inLevel.sprite_Enemies.add(bullet)
                        
                    if self.frame == self.shootMax:
                        self.frame = 0
                        self.state = ENEMY_STATE_WALK
                    self.last_update = t
                    
        elif self.state == ENEMY_STATE_DIE:
            if self.dieFrame != 0:
                if self.frame < self.dieFrame:
                    self.frame = self.dieFrame
                    self.last_update = t
                elif t - self.last_update > self.FPS * self.dieLag:
                    self.frame += 1
                    self.last_update = t
                    if self.frame > self.dieMax: self.frame = self.dieMax


        if self.direction == -1: self.image = self.images[self.frame]
        elif self.direction == 1: self.image = pygame.transform.flip(self.images[self.frame], True, False)                    
            
        # Push player left/right, in 1-pixel increments
        if self.direction != 0:
            for i in range(int(abs(self.moveAmountX))):
                gfn_PushEnemy(self, inLevel, 1 * self.direction, 0)
            gfn_PushEnemy(self, inLevel, (self.moveAmountX % 1) * self.direction, 0)
            
        # GRAVITY:
        if self.moveAmountY < 0:
            for i in range(int(abs(self.moveAmountY))):
                gfn_PushEnemy(self, inLevel, 0, -1)
            gfn_PushEnemy(self, inLevel, 0, (self.moveAmountY % -1))
        elif self.moveAmountY > 0:
            for i in range(int(abs(self.moveAmountY))):
                if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, 1)
            if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, self.moveAmountY % 1)
            
        if self.onGround == False:
            self.vy += t_elapsed * self.gravity
            self.moveAmountY = t_elapsed * self.vy

        self.updateSubRect()
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)

        """
        # If a dead enemy is out of sight by half a playing field, remove it
        if self.state == ENEMY_STATE_DIE:
            if self.rect[0] + self.rect.width + (inLevel.playWidth / 2) < 0 or self.rect[0] - (inLevel.playWidth / 2) > inLevel.playWidth:
                self.kill()
            elif self.rect[1] + self.rect.height + (inLevel.playHeight / 2) < 0 or self.rect[1] - (inLevel.playHeight / 2) > inLevel.playHeight:
                self.kill()
        """
        
#_______________________________________________________________________________________________
# Enemy Class - SIMPLE BULLET
# This is the class for simple projectiles coming from enemy weapons
# They
class gcls_Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir):

        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.vx = 1
        self.vy = 0
        self.moveAmountX = 0
        self.moveAmountY= 0
        self.onGround = False
        self.last_update = pygame.time.get_ticks()
        self.oldTimer = pygame.time.get_ticks()
        t_elapsed = 0.1
        self.frame = 0
        self.direction = inDir
        self.bullet = True
        self.state = ENEMY_STATE_WALK
        
        # Now set stuff specific to all the individual enemies
        if inID == SPRITE_SPIDER_PROJ:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 5
            # Frame definitions
            self.images = gfnLoad_Splice(16, 16, gfn_Zip("enemy_spider-proj.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 10
            # Physical properties
            self.vy = -70
            self.y += 10
            self.x += 5 * self.direction
            self.speed = 65
            self.gravity = 200

        elif inID == SPRITE_RAT_BULLET:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 1              
            # Frame definitions
            self.images = gfnLoad_Splice(64, 48, gfn_Zip("enemy_rat-proj.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            # Physical properties
            self.speed = 200
            self.gravity = 0

        elif inID == SPRITE_DEMON_FIREBALL:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 1              
            # Frame definitions
            self.images = gfnLoad_Splice(48, 48, gfn_Zip("enemy_demon-proj.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            # Physical properties
            self.speed = 100
            self.gravity = 0

        elif inID == SPRITE_ROBOT_GREY_BULLET:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 1              
            # Frame definitions
            self.images = gfnLoad_Splice(32, 48, gfn_Zip("enemy_robot_grey-proj.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            # Physical properties
            self.speed = 200
            self.gravity = 0

        elif inID == SPRITE_ROBOT_RED_BULLET:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 8              
            # Frame definitions
            self.images = gfnLoad_Splice(48, 48, gfn_Zip("enemy_robot_red-proj.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            # Physical properties
            self.speed = 150
            self.gravity = 0

            
        elif inID == SPRITE_HOVER_BULLET:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 2              
            # Frame definitions
            self.images = gfnLoad_Splice(47, 40, gfn_Zip("enemy_hover-proj.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            # Physical properties
            self.speed = 300
            self.gravity = 500

        elif inID == SPRITE_SHAPESHIFTER_PROJ:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 1              
            # Frame definitions
            self.images = gfnLoad_Splice(32, 32, gfn_Zip("enemy_shapeshifter-proj.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            # Physical properties
            self.speed = 200
            self.gravity = 0
            self.y += 36
            self.x += 16

        elif inID == SPRITE_TELETURRET_PROJ:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 1              
            # Frame definitions
            self.images = gfnLoad_Splice(33, 25, gfn_Zip("enemy_teleturret-proj.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 6
            # Physical properties
            self.speed = 200
            self.gravity = 0

        elif inID == SPRITE_EVILKEEN_PROJ:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 1              
            # Frame definitions
            self.images = gfnLoad_Splice(32, 32, gfn_Zip("enemy_evilkeen-proj.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            # Physical properties
            self.speed = 200
            self.gravity = 0

        elif inID == SPRITE_ISONIAN_PROJ1g:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 2              
            # Frame definitions
            self.images = gfnLoad_Splice(12, 15, gfn_Zip("enemy_isonian-proj1.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            # Physical properties
            self.speed = 200
            self.gravity = 0
            self.x += 16 * self.direction
            self.y += 12

        elif inID == SPRITE_ISONIAN_PROJ1r:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 5              
            # Frame definitions
            self.images = gfnLoad_Splice(12, 15, gfn_Zip("enemy_isonian-proj1.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            # Physical properties
            self.speed = 200
            self.gravity = 0
            self.x += 16 * self.direction
            self.y += 12

        elif inID == SPRITE_ISONIAN_PROJ1w:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 9              
            # Frame definitions
            self.images = gfnLoad_Splice(12, 15, gfn_Zip("enemy_isonian-proj1.png"), 1, 1)
            self.image = self.images[self.frame]
            self.FPS = 1000.0 / 8
            # Physical properties
            self.speed = 200
            self.gravity = 0
            self.x += 16 * self.direction
            self.y += 12
        # Rect properties
        self.rectOffsetX = 0
        self.rectOffsetY = 0
        self.rectW = self.image.get_width()
        self.rectH = self.image.get_height()           
        self.width = self.image.get_width()
        self.height = self.image.get_height()
            
        self.rect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def updateSubRect(self):
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def update(self, t, t_elapsed, inLevel, inKeen):

         
        # Update position & move bullet (it is not "pushed")
        self.vy += t_elapsed * self.gravity
        self.moveAmountX = t_elapsed * self.speed   
        self.moveAmountY = t_elapsed * self.vy
        self.x += self.moveAmountX * self.direction
        self.y += self.moveAmountY
        
        # If it's the hover enemy, make the bullets go diagonally down (not normal gravity)
        if self.id == SPRITE_HOVER_BULLET: self.moveAmountY = t_elapsed * self.speed
        
        """
        # Check collisions with ground - *** TOO SLOW FOR MULTIPLE SIMULTANEOUS BULLETS ***
        self.rect = pygame.Rect(round(self.x), round(self.y), self.width, self.height)
        bulletCollide = pygame.sprite.spritecollide(self, inLevel.sprite_MaskAll, False, pygame.sprite.collide_rect)
        for possibleCollide in bulletCollide:
            if pygame.sprite.collide_mask(self, possibleCollide):
                self.kill()
                if self.id == SPRITE_SPIDER_PROJ: inLevel.sprite_Enemies.add(gcls_Enemy_Poison(self.x, self.y, self.id, self.direction))
                elif self.id == SPRITE_ROBOT_RED_BULLET: inLevel.sprite_Explosions.add(isis_weapons.gcls_Explode(self.x, self.y, self.id, self.direction))
        """

        # Check collisions with ground - if midpoint hits any INFO tile
        # Probably should be changed to a solid INFO tile...
        # NON-SPIDER PROJ
        if self.id != SPRITE_SPIDER_PROJ:
            testX = int((self.x + (self.width / 2.0)) / TILESIZE)
            testY = int((self.y + (self.height / 2.0)) / TILESIZE)
            if gfnSolid_Info(inLevel.INFO[testX][testY]):
                self.kill()
                if self.id == SPRITE_ROBOT_RED_BULLET:
                    inLevel.sprite_Explosions.add(isis_weapons.gcls_Explode(self.x, self.y, self.id, self.direction, 0, 0))
                elif self.id == SPRITE_ISONIAN_PROJ1g or self.id == SPRITE_ISONIAN_PROJ1w or self.id == SPRITE_ISONIAN_PROJ1r:
                    inLevel.sprite_Explosions.add(isis_weapons.gcls_Explode(self.x, self.y, self.id, self.direction, 0, 0))
                    
        # SPIDER PROJ
        elif self.id == SPRITE_SPIDER_PROJ:
            testX = int((self.x + (self.width / 2.0)) / TILESIZE)
            testY = int((self.y + self.height) / TILESIZE)
            if gfnSolid_Info(inLevel.INFO[testX][testY]):
                self.kill()
                inLevel.sprite_Enemies.add(gcls_Enemy_Poison(self.x, self.y, self.id, self.direction))
                
        # Check collisions with border - if it is out of region kill it
        if self.x + self.width < 0 or self.x > inLevel.width * TILESIZE or self.y + self.height < 0 or self.y > inLevel.height * TILESIZE:
            self.kill()
            
        # Update frame
        if t - self.last_update > self.FPS:
            self.frame += 1
            if self.frame >= len(self.images):
                 if self.id != SPRITE_SPIDER_PROJ: self.frame = 0
                 else: self.frame -= 1
                 
            self.last_update = t

        # Set image
        if self.direction == -1: self.image = self.images[self.frame]
        elif self.direction == 1: self.image = pygame.transform.flip(self.images[self.frame], True, False)
        
        # Set rect back to the display rect
        self.updateSubRect()
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)
#_______________________________________________________________________________________________
# Enemy Class - SIMPLE DROPLET
# This is the class for simple droplets
# They
class gcls_Enemy_Drop(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir):

        pygame.sprite.Sprite.__init__(self)
        # Put it in the middle of the tile
        self.x = (inX * TILESIZE) + 8
        self.y = (inY * TILESIZE) + 8
        self.id = inID
        self.vx = 0
        self.vy = 0
        self.moveAmountX = 0
        self.moveAmountY= 0
        self.onGround = False
        self.last_update = pygame.time.get_ticks()
        self.oldTimer = pygame.time.get_ticks()
        t_elapsed = 0.1
        self.frame = 0
        self.direction = inDir
        self.bullet = True
        self.state = ENEMY_STATE_WALK
        
        # Now set stuff specific to all the individual enemies
        if inID == SPRITE_WATER_DROP:
            # Initial x/y
            self.xi = self.x
            self.yi = self.y
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 0       
            # Frame definitions
            srfcDrop = pygame.Surface((1,1))
            self.colour = (0, 0, 255)
            srfcDrop.fill(self.colour)
            self.image = srfcDrop
            self.image.set_colorkey(TRANSCOLOUR)
            # Physical properties
            self.speed = 0
            self.gravity = 150
            self.pause = 1 + int(random.random() * 3)
            
        elif inID == SPRITE_ACID_DROP:
            # Initial x/y
            self.xi = self.x
            self.yi = self.y
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 1       
            # Frame definitions
            srfcDrop = pygame.Surface((1,1))
            self.colour = (0, 255, 0)
            srfcDrop.fill(self.colour)
            self.image = srfcDrop
            self.image.set_colorkey(TRANSCOLOUR)
            # Physical properties
            self.speed = 0
            self.gravity = 150
            self.pause = 1 + int(random.random() * 3)
            
        # Rect properties          
        self.width = self.image.get_width()
        self.height = self.image.get_height()
            
        self.rect = pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, t, t_elapsed, inLevel, inKeen):


        if t_elapsed > 0.1: t_elapsed = 0.1
        
        if self.state == ENEMY_STATE_WALK:
            # Update position & move drop
            self.vy += t_elapsed * self.gravity
            self.moveAmountX = t_elapsed * self.speed   
            self.moveAmountY = t_elapsed * self.vy
            self.x += self.moveAmountX * self.direction
            self.y += self.moveAmountY
            
            """
            # Check collisions with ground (RECT only) - TOO SLOW ON BIG LEVELS
            self.rect = pygame.Rect(round(self.x), round(self.y), self.width, self.height)
            bulletCollide = pygame.sprite.spritecollide(self, inLevel.sprite_MaskAll, False, pygame.sprite.collide_rect)
            #print self.x, self.y
            if inLevel.INFO[int(self.x / TILESIZE)][int(self.y / TILESIZE)] == INFO_WATER: bulletCollide = [1]
            for possibleCollide in bulletCollide:
                # explode
                if self.id == SPRITE_WATER_DROP: tempColour = (0, 0, 255)
                elif self.id == SPRITE_ACID_DROP: tempColour = (0, 255, 0)
                for i in range(10):
                    inLevel.sprite_Particles.add(gcls_Particle(self.x, self.y, pTYPE_OTHER, pygame.time.get_ticks(), tempColour))
            """
            
            # Check collisions with ground - if hits any INFO tile
            testX = int(self.x / TILESIZE)
            testY = int(self.y / TILESIZE)
            if gfnSolid_Info(inLevel.INFO[testX][testY]) or gfnTile_Water(inLevel.INFO[testX][testY]):

                # Play sound if within range
                if self.x > inLevel.mapX and self.x < inLevel.mapX + inLevel.playWidth:
                    if self.y > inLevel.mapY and self.y < inLevel.mapY + inLevel.playHeight:
                        gfn_PlaySound(SFX_ENEMY_DROPLET)

                # explode
                if self.id == SPRITE_WATER_DROP: tempColour = (0, 0, 255)
                elif self.id == SPRITE_ACID_DROP: tempColour = (0, 255, 0)
                for i in range(10):
                    inLevel.sprite_Particles.add(gcls_Particle(self.x, self.y, pTYPE_OTHER, pygame.time.get_ticks(), tempColour))
                    
                # reset
                self.x = self.xi
                self.y = self.yi
                self.vy = 0
                self.last_update = t
                self.image.fill(TRANSCOLOUR)
                self.state = ENEMY_STATE_IDLE
                    
            # Check collisions with border - if it is out of region kill it
            if self.x + self.width < 0 or self.x > inLevel.width * TILESIZE or self.y + self.height < 0 or self.y > inLevel.height * TILESIZE:
                # reset
                self.x = self.xi
                self.y = self.yi
                self.vy = 0
                self.last_update = t
                self.image.fill(TRANSCOLOUR)
                self.state = ENEMY_STATE_IDLE
                

        elif self.state == ENEMY_STATE_IDLE:
            if (t - self.last_update) / 1000.0 >= self.pause:
                self.image.fill(self.colour)
                self.state = ENEMY_STATE_WALK

        # Set rect
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)
        
#_______________________________________________________________________________________________
# Enemy Class - SIMPLE POISON
# This is the class for simple poison puddle
class gcls_Enemy_Poison(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir):

        pygame.sprite.Sprite.__init__(self)
        self.x = inX
        self.y = inY
        self.id = inID
        self.last_update = pygame.time.get_ticks()
        self.oldTimer = pygame.time.get_ticks()
        t_elapsed = 0.1
        self.frame = 0
        self.direction = inDir
        self.bullet = False
        self.state = ENEMY_STATE_WALK

        if inID == SPRITE_SPIDER_PROJ:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 5              
            # Frame definitions
            self.images = gfnLoad_Splice(16, 16, gfn_Zip("enemy_spider-proj.png"), 1, 1)
            self.image = self.images[6]
            self.frame = 6
            self.fixed = True
            self.FPS = 1000.0 / 8
            #Physical Properties
            self.maxLife = 10
            self.lifetime = 0

        elif inID == SPRITE_SLUG_PROJ:
            # Hit Points
            self.hitPoints = 999999
            self.maxHit = 999999.0
            self.damage = 1              
            # Frame definitions
            self.images = gfnLoad_Splice(32, 32, gfn_Zip("enemy_slug-proj.png"), 1, 1)
            self.image = self.images[0]
            self.frame = 0
            self.fixed = True
            self.FPS = 1000.0 / 8
            #Physical Properties
            self.maxLife = 12
            self.lifetime = 0
            
        # Rect properties
        self.rectOffsetX = 0
        self.rectOffsetY = 0
        self.rectW = self.image.get_width()
        self.rectH = self.image.get_height()           
        self.width = self.image.get_width()
        self.height = self.image.get_height()
            
        self.rect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def updateSubRect(self):
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def update(self, t, t_elapsed, inLevel, inKeen):


        self.lifetime += t_elapsed
        
        # Update frame
        if self.fixed == False:
            if t - self.last_update > self.FPS:
                self.frame += 1
                if self.frame >= len(self.images): self.frame = 0
                self.last_update = t

        # Set image
        if self.direction == -1: self.image = self.images[self.frame]
        elif self.direction == 1: self.image = pygame.transform.flip(self.images[self.frame], True, False)

        self.image.set_alpha(255 - ((self.lifetime / self.maxLife) * 255))
        if 255 - ((self.lifetime / self.maxLife) * 255) <= 100: self.kill()

        # Set rect back to the display rect
        self.updateSubRect()
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)

#_______________________________________________________________________________________________
# Enemy Class - EVIL KEEN
# A specific and more complicated enemy - Evil Keen
class gcls_Enemy_EvilKeen(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir):

        pygame.sprite.Sprite.__init__(self)
        # Initial parameters
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.vx = inDir
        self.vy = 0
        self.moveAmountX = 0
        self.moveAmountY= 0
        self.onGround = False
        self.bullet = False
        self.last_update = pygame.time.get_ticks()
        self.oldTimer = pygame.time.get_ticks()
        t_elapsed = 0.1        
        self.dirChange = 0
        self.direction = inDir
        self.state = ENEMY_STATE_WALK

        # Hit Points
        self.hitPoints = 2
        self.maxHit = 2.0
        self.damage = 1

        # Images & Frames
        self.frame = 0
        self.images = gfnLoad_Splice(38, 32, gfn_Zip("enemy_evilkeen.png"), 1, 1)
        self.image = self.images[self.frame]
        self.FPS = 1000.0 / 8
        self.walkFrame = 0
        self.walkMax = 3
        self.jumpFrame = 4
        self.pogoFrame = 6
        self.shootFrame = 8
        self.shootFrameTimer = 0
        self.shootFrameTimerMax = 0.5
        self.dieFrame = 11

        # Physical properties
        self.speedRun = 110
        self.jumpAmount = -250
        self.jumpFreq = 3
        self.gravity = 450
        self.bulletSprite = SPRITE_EVILKEEN_PROJ
        self.shootProximityX = 150
        self.shootProximityY = 10
        self.shotDelay = 3
        self.shotTimer = 0
        self.speedDieX = 100
        self.speedDieY = -200
        self.gravityDie = 250
        
        # Rect properties
        self.rectOffsetX = 0
        self.rectOffsetY = 0
        self.rectW = self.image.get_width()
        self.rectH = self.image.get_height()           
        self.width = self.image.get_width()
        self.height = self.image.get_height() 
        self.rect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def updateSubRect(self):
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def update(self, t, t_elapsed, inLevel, inKeen):

        
        self.dirChange -= t_elapsed
        if self.dirChange < 0: self.dirChange = 0

        # Adjust shot timer
        if self.shotTimer > 0: self.shotTimer -= t_elapsed
        elif self.shotTimer <= 0: self.shotTimer = 0

        # Adjust shot frame timer
        if self.shootFrameTimer > 0: self.shootFrameTimer -= t_elapsed
        elif self.shootFrameTimer <=0: self.shootFrameTimer = 0
        
        if self.state == ENEMY_STATE_WALK:
            # Move Keen if not shooting
            if self.shootFrameTimer == 0:
                self.moveAmountX = t_elapsed * self.speedRun

            # Check for Jumping State change
            if self.onGround == True:
                RND2 = int(random.random() * (1 / t_elapsed) * self.jumpFreq)
                if RND2 == 1:
                    self.vy = self.jumpAmount
                    self.moveAmountY = t_elapsed * self.vy
                    self.onGround = False
            
            if self.shotTimer == 0:
                # Check if within shoot range, and if shooter is facing Keen (otherwise they shoot away from him)
                checkEnemyX = self.x + self.rectOffsetX + (self.rectW / 2.0)
                checkEnemyY = self.y + self.height
                checkKeenX = inKeen.x + (inKeen.width / 2.0)
                checkKeenY = inKeen.y + inKeen.height
                checkFacing = False
                if (self.direction == -1 and self.x > inKeen.x) or (self.direction == 1 and self.x < inKeen.x):
                    if abs(checkEnemyX - checkKeenX) < self.shootProximityX and abs(checkEnemyY - checkKeenY) < self.shootProximityY:
                        self.moveAmountX = 0
                        self.state = ENEMY_STATE_ATTACK
                        self.shotTimer = self.shotDelay
                        
                    
        elif self.state == ENEMY_STATE_ATTACK:
                bullet = gcls_Enemy_Bullet(self.x / TILESIZE, self.y / TILESIZE, self.bulletSprite, self.direction)
                inLevel.sprite_Enemies.add(bullet)
                self.shootFrameTimer = self.shootFrameTimerMax
                self.state = ENEMY_STATE_WALK

                    
        elif self.state == ENEMY_STATE_DIE:
            self.x += t_elapsed * self.speedDieX
            self.vy += t_elapsed * self.gravityDie
            self.y += t_elapsed * self.vy
            if self.y - inLevel.mapY > inLevel.playHeight: self.kill
        
        # Frame Selection
        # Alive
        if self.state != ENEMY_STATE_DIE:
            # Shooting
            if self.shootFrameTimer > 0:
                if self.onGround == True: self.frame = self.shootFrame
                else: self.frame = self.shootFrame + 1
            # Walking
            elif self.onGround == True:
                if t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.frame > self.walkMax: self.frame = self.walkFrame     
                    self.last_update = t
            # Jumping
            else:
                if self.vy <= 0: self.frame = self.jumpFrame
                else: self.frame = self.jumpFrame + 1
        # Death
        else:
            self.frame = self.dieFrame
            
        # Mirror the frame       
        if self.direction == -1: self.image = self.images[self.frame]
        elif self.direction == 1: self.image = pygame.transform.flip(self.images[self.frame], True, False)                    


        if self.state != ENEMY_STATE_DIE:
            # Push player left/right, in 1-pixel increments
            if self.direction != 0:
                for i in range(int(abs(self.moveAmountX))):
                    gfn_PushEnemy(self, inLevel, 1 * self.direction, 0)
                gfn_PushEnemy(self, inLevel, (self.moveAmountX % 1) * self.direction, 0)
            
            # GRAVITY:
            if self.moveAmountY < 0:
                for i in range(int(abs(self.moveAmountY))):
                    gfn_PushEnemy(self, inLevel, 0, -1)
                gfn_PushEnemy(self, inLevel, 0, (self.moveAmountY % -1))
            elif self.moveAmountY > 0:
                for i in range(int(abs(self.moveAmountY))):
                    if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, 1)
                if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, self.moveAmountY % 1)
            
            self.vy += t_elapsed * self.gravity
            self.moveAmountY = t_elapsed * self.vy

        self.updateSubRect()
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)

        # If a dead enemy is out of sight by half a playing field, remove it
        if self.state == ENEMY_STATE_DIE:
            if self.rect[0] + self.rect.width + (inLevel.playWidth / 2) < 0 or self.rect[0] - (inLevel.playWidth / 2) > inLevel.playWidth:
                self.kill()
            elif self.rect[1] + self.rect.height + (inLevel.playHeight / 2) < 0 or self.rect[1] - (inLevel.playHeight / 2) > inLevel.playHeight:
                self.kill()

#_______________________________________________________________________________________________
# Enemy Class - SHAPESHIFTER
# A specific and more complicated enemy - SHAPESHIFTER
class gcls_Enemy_ShapeShifter(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir):

        pygame.sprite.Sprite.__init__(self)
        # Initial parameters
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.vx = inDir
        self.vy = 0
        self.moveAmountX = 0
        self.moveAmountY= 0
        self.onGround = False
        self.bullet = False
        self.last_update = pygame.time.get_ticks()
        self.oldTimer = pygame.time.get_ticks()
        t_elapsed = 0.1        
        self.dirChange = 0
        self.direction = inDir
        self.state = ENEMY_STATE_IDLE

        # Hit Points
        self.hitPoints = 2
        self.maxHit = 2.0
        self.damage = 1

        # Images & Frames
        self.frame = 0
        self.images = gfnLoad_Splice(64, 64, gfn_Zip("enemy_shapeshifter.png"), 1, 1)
        self.image = self.images[self.frame]
        self.FPS = 1000.0 / 8
        self.idleFrame = 0
        self.idleMax = 12
        self.idleLag = 0.75
        self.walkFrame = 13
        self.walkMax = 16
        self.jumpFrame = 17
        self.shootFrame = 20
        self.shootRelease = 22
        self.shootMax = 23
        self.shootLag = 1
        self.shootFrameTimer = 0
        self.shootFrameTimerMax = 0.5
        self.dieFrame = 26
        self.dieMax = 35
        self.dieLag = 1
        
        # Physical properties
        self.speedRun = 60
        self.jumpAmount = -190
        self.jumpFreq = 3
        self.gravity = 450
        self.bulletSprite = SPRITE_SHAPESHIFTER_PROJ
        self.shootProximityX = 100
        self.shootProximityY = 20
        self.idleProximityX = 50
        self.idleProximityY = 10
        self.shotDelay = 0.2
        self.shotTimer = 0
        
        # Rect properties
        self.rectOffsetX = 24
        self.rectOffsetY = 40
        self.rectW = 16
        self.rectH = 24          
        self.width = self.image.get_width()
        self.height = self.image.get_height() 
        self.rect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def updateSubRect(self):
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def update(self, t, t_elapsed, inLevel, inKeen):

        
        self.dirChange -= t_elapsed
        if self.dirChange < 0: self.dirChange = 0

        # Adjust shot timer
        if self.shotTimer > 0: self.shotTimer -= t_elapsed
        elif self.shotTimer <= 0: self.shotTimer = 0
        
        if self.state == ENEMY_STATE_WALK:
            # Move Keen if not shooting
            if self.shootFrameTimer == 0:
                self.moveAmountX = t_elapsed * self.speedRun

            # Check for Jumping State change
            if self.onGround == True:
                RND2 = int(random.random() * (1 / t_elapsed) * self.jumpFreq)
                if RND2 == 1:
                    self.vy = self.jumpAmount
                    self.moveAmountY = t_elapsed * self.vy
                    self.onGround = False
            
            if self.shotTimer == 0:
                # Check if within shoot range, and if shooter is facing Keen (otherwise they shoot away from him)
                checkEnemyX = self.x + self.rectOffsetX + (self.rectW / 2.0)
                checkEnemyY = self.y + self.height
                checkKeenX = inKeen.x + (inKeen.width / 2.0)
                checkKeenY = inKeen.y + inKeen.height
                checkFacing = False
                if (self.direction == -1 and self.x > inKeen.x) or (self.direction == 1 and self.x < inKeen.x):
                    if abs(checkEnemyX - checkKeenX) < self.shootProximityX and abs(checkEnemyY - checkKeenY) < self.shootProximityY:
                        self.moveAmountX = 0
                        self.state = ENEMY_STATE_ATTACK
                        
        elif self.state == ENEMY_STATE_IDLE:
            # Check if within wakeup range
            checkEnemyX = self.x + self.rectOffsetX + (self.rectW / 2.0)
            checkEnemyY = self.y + self.height
            checkKeenX = inKeen.x + (inKeen.width / 2.0)
            checkKeenY = inKeen.y + inKeen.height
            if abs(checkEnemyX - checkKeenX) < self.shootProximityX and abs(checkEnemyY - checkKeenY) < self.shootProximityY:
                self.state = ENEMY_STATE_WAKEUP
                        
        elif self.state == ENEMY_STATE_ATTACK:
            # Frame selection for attack
            if self.frame < self.shootFrame:
                self.frame = self.shootFrame
                self.last_update = t
            elif t - self.last_update > self.FPS * self.shootLag:
                self.frame += 1
                self.last_update = t
                if self.frame == self.shootRelease:
                    bullet = gcls_Enemy_Bullet(self.x / TILESIZE, self.y / TILESIZE, self.bulletSprite, self.direction)
                    inLevel.sprite_Enemies.add(bullet)
                    self.shotTimer = self.shotDelay
                elif self.frame > self.shootMax:
                    self.frame = self.walkFrame     
                    self.state = ENEMY_STATE_WALK 

                    
        elif self.state == ENEMY_STATE_DIE:
            self.moveAmountX = 0
            self.moveAmountY = 0
            self.vy = 0
        
        # Frame Selection, except attack frames
        # Idle
        if self.state == ENEMY_STATE_IDLE:
            self.frame = self.idleFrame
            
        # Wakeup
        elif self.state == ENEMY_STATE_WAKEUP:
            if t - self.last_update > self.FPS * self.idleLag:
                self.frame += 1
                self.last_update = t
                if self.frame > self.idleMax:
                    self.frame = self.walkFrame     
                    self.state = ENEMY_STATE_WALK      
        # Attack
        elif self.state == ENEMY_STATE_ATTACK:
            g = None
        # Alive
        elif self.state != ENEMY_STATE_DIE:
            # Shooting
            if self.shootFrameTimer > 0:
                if self.onGround == True: self.frame = self.shootFrame
                else: self.frame = self.shootFrame + 1
            # Walking
            elif self.onGround == True:
                if t - self.last_update > self.FPS:
                    self.frame += 1
                    if self.frame > self.walkMax: self.frame = self.walkFrame     
                    self.last_update = t
            # Jumping
            else:
                if self.vy <= 0: self.frame = self.jumpFrame
                else: self.frame = self.jumpFrame + 1
        # Death
        else:
            if self.frame < self.dieFrame:
                self.frame = self.dieFrame
                self.last_update = t
            elif t - self.last_update > self.FPS * self.dieLag:
                self.frame += 1
                self.last_update = t
                if self.frame > self.dieMax: self.frame = self.dieMax
            
        # Mirror the frame       
        if self.direction == -1: self.image = self.images[self.frame]
        elif self.direction == 1: self.image = pygame.transform.flip(self.images[self.frame], True, False)                    


        if self.state != ENEMY_STATE_DIE:
            # Push player left/right, in 1-pixel increments
            if self.direction != 0:
                for i in range(int(abs(self.moveAmountX))):
                    gfn_PushEnemy(self, inLevel, 1 * self.direction, 0)
                gfn_PushEnemy(self, inLevel, (self.moveAmountX % 1) * self.direction, 0)
            
            # GRAVITY:
            if self.moveAmountY < 0:
                for i in range(int(abs(self.moveAmountY))):
                    gfn_PushEnemy(self, inLevel, 0, -1)
                gfn_PushEnemy(self, inLevel, 0, (self.moveAmountY % -1))
            elif self.moveAmountY > 0:
                for i in range(int(abs(self.moveAmountY))):
                    if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, 1)
                if self.onGround == False: gfn_PushEnemy(self, inLevel, 0, self.moveAmountY % 1)
            
            self.vy += t_elapsed * self.gravity
            self.moveAmountY = t_elapsed * self.vy

        self.updateSubRect()
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)

        """
        # If a dead enemy is out of sight by half a playing field, remove it
        if self.state == ENEMY_STATE_DIE:
            if self.rect[0] + self.rect.width + (inLevel.playWidth / 2) < 0 or self.rect[0] - (inLevel.playWidth / 2) > inLevel.playWidth:
                self.kill()
            elif self.rect[1] + self.rect.height + (inLevel.playHeight / 2) < 0 or self.rect[1] - (inLevel.playHeight / 2) > inLevel.playHeight:
                self.kill()
        """
        
#_______________________________________________________________________________________________
# Enemy Class - ROCK
# A specific class for breakable rocks
class gcls_Enemy_Rock(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir):

        pygame.sprite.Sprite.__init__(self)
        # Initial parameters
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.direction = inDir
        self.bullet = False
        self.state = ENEMY_STATE_WALK
    
        # Hit Points
        self.hitPoints = 2
        self.maxHit = 2.0
        self.damage = 0

        # Images & Frames
        self.frame = inID - SPRITE_ROCK_GREY
        self.images = gfnLoad_Splice(48, 48, gfn_Zip("enemy_rocks.png"), 1, 1)
        self.image = self.images[self.frame]
        self.FPS = 1000.0 / 8
        
        # Rect properties
        self.rectOffsetX = 0
        self.rectOffsetY = 0
        self.rectW = self.image.get_width()
        self.rectH = self.image.get_height()           
        self.width = self.image.get_width()
        self.height = self.image.get_height() 
        self.rect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def updateSubRect(self):
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def update(self, t, t_elapsed, inLevel, inKeen):

        if self.state == ENEMY_STATE_DIE:
            # Remove SOLID INFO tiles & Mask
            TileX = int(self.x / TILESIZE)
            TileY = int(self.y / TILESIZE)
            if inKeen.state != kIN_WATER:
                inLevel.INFO[TileX+0][TileY+1] = 0
                inLevel.INFO[TileX+1][TileY+1] = 0
                inLevel.INFO[TileX+2][TileY+1] = 0
                inLevel.INFO[TileX+0][TileY+2] = 0
                inLevel.INFO[TileX+1][TileY+2] = 0
                inLevel.INFO[TileX+2][TileY+2] = 0
            else:
                inLevel.INFO[TileX+0][TileY+1] = INFO_WATER
                inLevel.INFO[TileX+1][TileY+1] = INFO_WATER
                inLevel.INFO[TileX+2][TileY+1] = INFO_WATER
                inLevel.INFO[TileX+0][TileY+2] = INFO_WATER
                inLevel.INFO[TileX+1][TileY+2] = INFO_WATER
                inLevel.INFO[TileX+2][TileY+2] = INFO_WATER
            
            for mask in inLevel.sprite_MaskAll:
                if mask.x == self.x + TILESIZE and mask.y == self.y + TILESIZE:
                    mask.kill()
            # Produce Shards
            for i in range(10):
                RND_X = int(round(random.random() * 48))
                RND_Y = int(round(random.random() * 48))
                inLevel.sprite_Explosions.add(gcls_Particle(self.x + RND_X, self.y + RND_Y, self.id, pygame.time.get_ticks(), 0))
            # Remove Rock
            self.kill()
            
        # Mirror the frame       
        if self.direction == -1: self.image = self.images[self.frame]
        elif self.direction == 1: self.image = pygame.transform.flip(self.images[self.frame], True, False)                    


        self.updateSubRect()
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)

#_______________________________________________________________________________________________
# Enemy Class - TELETURRET
# A specific class for the Tele Turret
class gcls_Enemy_TeleTurret(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir):

        pygame.sprite.Sprite.__init__(self)
        # Initial parameters
        self.x = inX * TILESIZE
        self.y = (inY * TILESIZE) - 8
        self.id = inID
        self.direction = inDir
        self.bullet = False
        self.state = ENEMY_STATE_WALK
        self.oldTimer = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        t_elapsed = 0.1
        
        # Hit Points
        self.hitPoints = 2
        self.maxHit = 2.0
        self.damage = 0

        # Images & Frames
        self.frame = 0
        self.images = gfnLoad_Splice(33, 25, gfn_Zip("enemy_teleturret.png"), 1, 1)
        self.image = self.images[self.frame]
        self.FPS = 1000.0 / 10
        self.walkFrame = 0
        self.idleFrame = 8
        self.idleMax = 15
        self.shootFrame = 1
        self.shootMax = 4
        self.dieFrame = 16
        self.dieMax = 21
        self.bulletSprite = SPRITE_TELETURRET_PROJ
        
        # Physical properties
        self.shootTimer = 0
        self.shootDelay = 0.5
        self.hideProximityY = 16
        
        # Rect properties
        self.rectOffsetX = 0
        self.rectOffsetY = 0
        self.rectW = self.image.get_width()
        self.rectH = self.image.get_height()           
        self.width = self.image.get_width()
        self.height = self.image.get_height() 
        self.rect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def updateSubRect(self):
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)

    def update(self, t, t_elapsed, inLevel, inKeen):


        # Shoot Timer
        if self.shootTimer > 0: self.shootTimer -= t_elapsed
        else: self.shootTimer = 0
        
        if self.state == ENEMY_STATE_WALK:
            self.frame = self.walkFrame
            # If Keen is nearby and facing, hide
            isFacing = False
            if (self.direction == -1 and self.x > inKeen.x) or (self.direction == 1 and self.x < inKeen.x): isFacing = True
            if (abs(self.y - inKeen.subRect[1]) < self.hideProximityY) and isFacing == True:
                self.frame = self.walkFrame
                self.hitPoints = 999999
                self.state = ENEMY_STATE_IDLE
                
            # Otherwise Shoot
            elif self.shootTimer == 0:
                self.state = ENEMY_STATE_ATTACK
                self.shootTimer = self.shootDelay

        elif self.state == ENEMY_STATE_IDLE:
            if self.frame < self.idleFrame:
                self.frame = self.idleFrame
                self.last_update = t
            elif t - self.last_update > self.FPS:
                self.frame += 1
                self.last_update = t
                if self.frame > self.idleMax:
                    self.frame = self.idleMax
                    if abs(self.y - inKeen.subRect[1]) > self.hideProximityY:
                        self.frame -= 1
                        self.state = ENEMY_STATE_WAKEUP

        elif self.state == ENEMY_STATE_WAKEUP:
            if t - self.last_update > self.FPS:
                self.frame -= 1
                self.last_update = t
                if self.frame < self.idleFrame:
                    self.hitPoints = self.maxHit
                    self.state = ENEMY_STATE_WALK
            
        elif self.state == ENEMY_STATE_ATTACK:
            if self.frame < self.shootFrame:
                self.frame = self.shootFrame
                self.last_update = t
            elif t - self.last_update > self.FPS:
                self.frame += 1
                self.last_update = t
                if self.frame > self.shootMax:
                    bullet = gcls_Enemy_Bullet(self.x / TILESIZE, self.y / TILESIZE, self.bulletSprite, self.direction)
                    inLevel.sprite_Enemies.add(bullet)
                    self.frame = self.walkFrame
                    self.state = ENEMY_STATE_WALK
                
        elif self.state == ENEMY_STATE_DIE:
            if self.frame < self.dieFrame:
                self.frame = self.dieFrame
                self.last_update = t
            elif t - self.last_update > self.FPS:
                self.frame += 1
                self.last_update = t
                if self.frame > self.dieMax: self.frame = self.dieMax
            
        # Mirror the frame       
        if self.direction == -1: self.image = self.images[self.frame]
        elif self.direction == 1: self.image = pygame.transform.flip(self.images[self.frame], True, False)                    

        self.updateSubRect()
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)
        
#________________________________________________________________________________________________
# This function will attempt to push the player by at most 1 pixel to the LEFT, RIGHT, UP or DOWN
# Only one direction will be processed at a time
# Depending on the tile it encounters, it may or may not be successful
def gfn_PushEnemy(inKeen, inLevel, inAmountX, inAmountY):
    
    try:
        #______________________
        # RIGHT
        if inAmountX > 0:

            # Push player RIGHT if more than one TILESIZE from right edge
            if inKeen.x + inKeen.width < (inLevel.width * TILESIZE) - 1:
                inKeen.x += inAmountX
                inKeen.updateSubRect()
                
            # 1. Check if we walk onto a slope
            TileX_Slope = int(inKeen.subRect.midbottom[0] / TILESIZE)
            TileY_Slope = int(inKeen.subRect.midbottom[1] / TILESIZE)

            # Up slopes
            if gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                inKeen.y -= 3 * inAmountX / 4.0
                inKeen.x -= inAmountX / 4.0
                
            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                inKeen.y -= inAmountX / 2.0

            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope-1]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                inKeen.y -= inAmountX / 2.0
                
            # Down slopes
            elif gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                inKeen.y += inAmountX 
                
            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                inKeen.y += inAmountX / 2.0

            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope+1]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                inKeen.y += inAmountX / 2.0

                
            else:

                # 2. Check if we hit a wall
                # Pixel coordinates - the left and right bounds of the Rect
                TileYpix = inKeen.subRect[1] - (inKeen.subRect[1] % TILESIZE) + 1
                TestEnd = inKeen.subRect[1] + inKeen.subRect.height - 1
                
                # Map coordinates
                TileX = int((inKeen.subRect[0] + inKeen.subRect.width) / TILESIZE)
                TileY = int(TileYpix / TILESIZE)

                xChange = False
                while TileYpix <= TestEnd:
                    if gfnTile_SolidEnemy(inLevel.INFO[TileX][TileY]) and not gfnTile_UpRight45(inLevel.INFO[TileX-1][TileY]):
                        if not gfnTile_UpRight30_1(inLevel.INFO[TileX-1][TileY]) and not gfnTile_UpRight30_2(inLevel.INFO[TileX-1][TileY]):
                            xChange = True
     
                    TileY +=1
                    TileYpix += TILESIZE

                if xChange == True and inKeen.bullet == False:
                    inKeen.x = (TileX * TILESIZE) - inKeen.subRect.width - inKeen.rectOffsetX - 2
                    inKeen.direction = inKeen.direction * -1
                            
                # 3. Check if we should fall
                fall = True
                TileXpix = inKeen.subRect[0] - (inKeen.subRect[0] % TILESIZE) + 4
                TestEnd = inKeen.subRect[0] + inKeen.subRect.width - 2
                
                # Map coordinates
                TileY = int((inKeen.subRect[1] + inKeen.subRect.height + 2) / TILESIZE)
                TileX = int(TileXpix / TILESIZE)

                while TileXpix <= TestEnd:
                    if gfnTile_SolidEnemy(inLevel.INFO[TileX][TileY]):
                        fall = False
                        
                    TileX +=1
                    TileXpix += TILESIZE

                if fall == True and inKeen.onGround == True:
                    inKeen.vy = 0
                    inKeen.onGround = False

                if inKeen.onGround == True and inKeen.y > (TileY * TILESIZE) - inKeen.subRect.height - inKeen.rectOffsetY - 1:
                    inKeen.y = (TileY * TILESIZE) - inKeen.subRect.height - inKeen.rectOffsetY - 1
                    
        #______________________
        # LEFT
        elif inAmountX < 0:

            # Push player LEFT if more than one TILESIZE from left edge
            if inKeen.x > 1:
                inKeen.x += inAmountX
                inKeen.updateSubRect()
                inKeen.message = "< Left"

            # 1. Check if we walk onto a slope
            TileX_Slope = int(inKeen.subRect.midbottom[0] / TILESIZE)
            TileY_Slope = int(inKeen.subRect.midbottom[1] / TILESIZE)

            # Up slopes
            if gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                inKeen.y += 3 * inAmountX / 4.0
                inKeen.x -= inAmountX / 4.0
                
            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                inKeen.y += inAmountX / 2.0

            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope-1]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                inKeen.y += inAmountX / 2.0
                
            # Down slopes
            elif gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                inKeen.y -= inAmountX
                
            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                inKeen.y -= inAmountX / 2.0

            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope+1]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                inKeen.y -= inAmountX / 2.0

                
            else:
                
                # Pixel coordinates - the left and right bounds of the Rect
                TileYpix = inKeen.subRect[1] - (inKeen.subRect[1] % TILESIZE) + 1
                TestEnd = inKeen.subRect[1] + inKeen.subRect.height - 1
                
                # Map coordinates
                TileX = int(inKeen.subRect[0] / TILESIZE)
                TileY = int(TileYpix / TILESIZE)

                xChange = False
                while TileYpix <= TestEnd:
                    if gfnTile_SolidEnemy(inLevel.INFO[TileX][TileY]) and not gfnTile_DownRight45(inLevel.INFO[TileX+1][TileY]):
                        if not gfnTile_UpRight45(inLevel.INFO[TileX+1][TileY-1]):
                            if not gfnTile_DownRight30_1(inLevel.INFO[TileX+1][TileY-1]) and not gfnTile_DownRight30_2(inLevel.INFO[TileX+1][TileY-1]):
                                xChange = True
                                

                    TileY +=1
                    TileYpix += TILESIZE

                if xChange == True and inKeen.bullet == False:
                    inKeen.x = ((TileX + 1) * TILESIZE) - inKeen.rectOffsetX + 2
                    inKeen.direction = inKeen.direction * -1
                            
                # Test to see if we've walking off a cliff
                fall = True
                TileXpix = inKeen.subRect[0] - (inKeen.subRect[0] % TILESIZE)
                TestEnd = inKeen.subRect[0] + inKeen.subRect.width
                
                # Map coordinates
                TileY = int((inKeen.subRect[1] + inKeen.subRect.height + 2) / TILESIZE)
                TileX = int(TileXpix / TILESIZE)

                while TileXpix <= TestEnd:
                    if gfnTile_SolidEnemy(inLevel.INFO[TileX][TileY]):
                        fall = False
                        
                    TileX +=1
                    TileXpix += TILESIZE

                if fall == True and inKeen.onGround == True:
                    inKeen.vy = 0
                    inKeen.onGround = False

                if inKeen.onGround == True and inKeen.y > (TileY * TILESIZE) - inKeen.subRect.height - inKeen.rectOffsetY - 1:
                    inKeen.y = (TileY * TILESIZE) - inKeen.subRect.height - inKeen.rectOffsetY - 1  
                
        #______________________
        # DOWN
        elif inAmountY > 0:

            # Push player DOWN if less than one TILESIZE from the bottom
            if inKeen.y < (inLevel.height * TILESIZE) - inKeen.height - TILESIZE:
                inKeen.y += inAmountY
                inKeen.updateSubRect()

            if inKeen.bullet == False:
                # Check for landing on slopes first
                TileX = int(inKeen.subRect.midbottom[0] / TILESIZE)        
                TileY = int((inKeen.subRect[1] + inKeen.subRect.height) / TILESIZE)
                if gfnTile_UpRight45(inLevel.INFO[TileX][TileY]):
                    if (inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE > TILESIZE - (inKeen.subRect.midbottom[0] % TILESIZE):
                        inKeen.y -= ((inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE) - (TILESIZE - (inKeen.subRect.midbottom[0] % TILESIZE))
                        inKeen.vy = 0
                        inKeen.onGround = True
                        
                elif gfnTile_UpRight30_1(inLevel.INFO[TileX][TileY]):
                    if (inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE > TILESIZE - ((inKeen.subRect.midbottom[0] % TILESIZE) * 0.5):
                        inKeen.y -= ((inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE) - (TILESIZE - ((inKeen.subRect.midbottom[0] % TILESIZE) * 0.5))
                        inKeen.vy = 0
                        inKeen.onGround = True

                elif gfnTile_UpRight30_2(inLevel.INFO[TileX][TileY]):
                    if (inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE > TILESIZE - ((inKeen.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5:
                        inKeen.y -= ((inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE) - (TILESIZE - ((inKeen.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5)
                        inKeen.vy = 0
                        inKeen.onGround = True

                elif gfnTile_DownRight45(inLevel.INFO[TileX][TileY]):
                    if (inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE >  inKeen.subRect.midbottom[0] % TILESIZE:
                        inKeen.y -= ((inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE) - (inKeen.subRect.midbottom[0] % TILESIZE)
                        inKeen.vy = 0
                        inKeen.onGround = True
                        
                elif gfnTile_DownRight30_1(inLevel.INFO[TileX][TileY]):
                    if (inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE >  (inKeen.subRect.midbottom[0] % TILESIZE) * 0.5:
                        inKeen.y -= ((inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE) - ((inKeen.subRect.midbottom[0] % TILESIZE) * 0.5)
                        inKeen.vy = 0
                        inKeen.onGround = True

                elif gfnTile_DownRight30_2(inLevel.INFO[TileX][TileY]):
                    if (inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE >  ((inKeen.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5:
                        inKeen.y -= ((inKeen.subRect[1] + inKeen.subRect.height) % TILESIZE) - (((inKeen.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5)
                        inKeen.vy = 0
                        inKeen.onGround = True
                        
                # If no slope, scan for a solid  
                else:
                    # Pixel coordinates - the left and right bounds of the Rect
                    TileXpix = inKeen.subRect[0] - (inKeen.subRect[0] % TILESIZE)
                    TestEnd = inKeen.subRect[0] + inKeen.subRect.width
                    
                    # Map coordinates
                    TileY = int((inKeen.subRect[1] + inKeen.subRect.height) / TILESIZE)
                    TileX = int(TileXpix / TILESIZE)

                    while TileXpix <= TestEnd:
                        if gfnTile_SolidEnemy(inLevel.INFO[TileX][TileY]):
                            inKeen.y = (TileY * TILESIZE) - inKeen.subRect.height - inKeen.rectOffsetY - 1
                            inKeen.onGround = True
                            inKeen.vy = 0
                            
                        TileX +=1
                        TileXpix += TILESIZE


        #______________________
        # UP
        elif inAmountY < 0:

            # Push player UP if more than one TILESIZE from the top
            if inKeen.y > TILESIZE:
                inKeen.y += inAmountY
                inKeen.updateSubRect()

            # Pixel coordinates - the left and right bounds of the Rect
            TileXpix = inKeen.subRect[0] - (inKeen.subRect[0] % TILESIZE)
            TestEnd = inKeen.subRect[0] + inKeen.subRect.width

            # Map coordinates
            TileY = int(inKeen.subRect[1] / TILESIZE)
            TileX = int(TileXpix / TILESIZE)

            while TileXpix <= TestEnd:
                if gfnTile_SolidFromBottom(inLevel.INFO[TileX][TileY]):
                    inKeen.vy = 0
                    inKeen.y -= inAmountY
                    
                TileX +=1
                TileXpix += TILESIZE

                
        # Update collision Rect
        inKeen.updateSubRect()

    # Error handling
    except IndexError:
        print ("ENEMY ERROR! enemyID = ", inKeen.id, " at (", inKeen.x, ",", inKeen.y, ") trying to go to inAmountX = ", inAmountX, ", inAmountY = ", inAmountY)
