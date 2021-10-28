# isis_doors.py
# Contains processes for Doors (Locked), Switches & Platforms

import pygame, math, random
pygame.init()
from isis_draw import *
from isis_level import *
from isis_tiles import *
from isis_constants import *
from isis_zip import *

srfcDoors = gfnLoad_Splice(32, 64, gfn_Zip("doors.png"), 1, 1)
srfcPlatforms = gfnLoad_Splice(43, 32, gfn_Zip("platforms.png"), 1, 1)
srfcSwitches = gfnLoad_Splice(16, 16, gfn_Zip("switches.png"), 1, 1)

# Door Class
class gcls_Door(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID):

        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.tileX = inX
        self.tileY = inY
        self.id = inID
        self.image = srfcDoors[self.id]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(round(self.x), round(self.y), self.width, self.height)
        self.state = DOOR_STATE_CLOSED
        self.openSpeed = DOOR_OPEN_SPEED
        self.timeElapsed = 0
        self.oldTime = pygame.time.get_ticks()
        self.switchNum = 0
        
    def update(self, t, inLevel):

        if self.state == DOOR_STATE_OPEN:
            self.timeElapsed = (t - self.oldTime) / 1000.0
            
            # If door has reached the top
            if (self.tileY * TILESIZE) - self.y > self.height - 16:
                # Make the tiles open, and remove the SOLID INFO tiles
                inLevel.INFO[self.tileX][self.tileY] = 0
                inLevel.INFO[self.tileX][self.tileY+1] = 0
                inLevel.INFO[self.tileX][self.tileY+2] = 0
                self.state = DOOR_STATE_FINISHED
                
                # Also remove the masks (used in bullet collision testing)
                for mask in inLevel.sprite_MaskAll:
                    if (mask.x / TILESIZE) == self.tileX and (mask.y / TILESIZE) == self.tileY: mask.kill()
                    elif (mask.x / TILESIZE) == self.tileX and (mask.y / TILESIZE) == (self.tileY + 1): mask.kill()
                    elif (mask.x / TILESIZE) == self.tileX and (mask.y / TILESIZE) == (self.tileY + 2): mask.kill()
            # Else move it up
            else:
                self.y -= self.openSpeed * self.timeElapsed
                
        self.oldTime = t
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)

# Platform Class
class gcls_Platform(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inSwitchNum):
        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.switchNum = inSwitchNum
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.frame = 0
        self.maxFrames = 4
        self.FPS = 1000 / 8.0
        self.timeElapsed = 0.1
        self.oldTime = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        
        # Set initial velocities to 0
        self.vx, self.vy = 0, 0
        self.speed = 50
        
        # Platform images
        if self.id == SPRITE_PLATFORM_1: self.initFrame = 11
        elif self.id == SPRITE_PLATFORM_2: self.initFrame = 1
        elif self.id == SPRITE_PLATFORM_3: self.initFrame = 6
        
        self.image = srfcPlatforms[self.initFrame]
        self.mask = pygame.mask.from_surface(srfcPlatforms[self.initFrame-1])
        self.width = self.image.get_width()
        self.height = self.image.get_height()        
        self.rect = pygame.Rect(round(self.x), round(self.y), self.width, self.height)

        # Active
        if self.switchNum == 0: self.active = True
        else: self.active = False
        
    def update(self, t, inLevel, inKeen):

        # Update timer
        self.timeElapsed = (t - self.oldTime) / 1000.0
        self.oldTime = t

        # Only do anything if it is active
        if self.active == True:
            # Update frame
            if (t - self.last_update) > self.FPS:
                self.frame += 1
                if self.frame >= self.maxFrames: self.frame = 0
                self.image = srfcPlatforms[self.initFrame + self.frame]
                self.last_update = t
                
            moveX = self.timeElapsed * self.speed * self.vx
            moveY = self.timeElapsed * self.speed * self.vy

            # Move platform
            self.x += moveX
            self.y += moveY

            # Move Keen
            if inKeen.onPlatform == True and pygame.sprite.collide_mask(self, inKeen):
                inKeen.x += moveX
                inKeen.y += moveY
                
                # Update Keen Rects & camera
                inKeen.rect = pygame.Rect(inKeen.x - inLevel.mapX + inLevel.playX, inKeen.y - inLevel.mapY + inLevel.playY, 48, 48)
                inKeen.updateSubRect()
                inLevel.updateCamera(inKeen)
                            
            # Collisions with directions
            self.rect = pygame.Rect(round(self.x), round(self.y), self.width, self.height)
            platformCollide = pygame.sprite.spritecollide(self, inLevel.sprite_PlatformDirections, False, pygame.sprite.collide_rect)
            for tileDirection in platformCollide:
                self.vx = tileDirection.vx
                self.vy = tileDirection.vy

        # Change rect back for display purposes
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)


# Platform Directions Class
class gcls_Platform_Directions(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID):

        pygame.sprite.Sprite.__init__(self)
        self.x = inX * TILESIZE
        self.y = inY * TILESIZE
        self.id = inID
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.width = TILESIZE
        self.height = TILESIZE
        self.rect = pygame.Rect(round(self.x), round(self.y), self.width, self.height)
        
        # Hold the new velocities that the platform will take if it hits these tiles
        if self.id == INFO_PLATFORM_UP:
            self.vx = 0
            self.vy = -1
        elif self.id == INFO_PLATFORM_DOWN:
            self.vx = 0
            self.vy = 1
        elif self.id == INFO_PLATFORM_RIGHT:
            self.vx = 1
            self.vy = 0
        elif self.id == INFO_PLATFORM_LEFT:
            self.vx = -1
            self.vy = 0
        elif self.id == INFO_PLATFORM_UP_RIGHT:
            self.vx = 1
            self.vy = -1
        elif self.id == INFO_PLATFORM_DOWN_LEFT:
            self.vx = -1
            self.vy = 1
        elif self.id == INFO_PLATFORM_UP_LEFT:
            self.vx = -1
            self.vy = -1
        elif self.id == INFO_PLATFORM_DOWN_RIGHT:
            self.vx = 1
            self.vy = 1
            

    #def update(self, t, inLevel):
        #self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)

        
# Switch Class
class gcls_Switch(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inSwitchNum):

        pygame.sprite.Sprite.__init__(self)
        self.x = (inX * TILESIZE) + 8
        self.y = inY * TILESIZE
        self.id = inID
        self.switchNum = inSwitchNum
        self.state = DOOR_STATE_CLOSED
        
        if self.id == SPRITE_SWITCH_1: self.frame = 0
        elif self.id == SPRITE_SWITCH_2: self.frame = 2
        elif self.id == SPRITE_SWITCH_3: self.frame = 4
        
        self.onFrame = 0
        self.image = srfcSwitches[self.frame]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, t, inLevel):

        if self.state == DOOR_STATE_CLOSED: self.onFrame = 0
        else: self.onFrame = 1
        self.image = srfcSwitches[self.frame + self.onFrame]
        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)
