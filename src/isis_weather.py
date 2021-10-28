# isis_weather.py
# Weather effects
import pygame, random
pygame.init()
from pygame.locals import *

from isis_draw import *
from isis_tiles import *
from isis_zip import *
from isis_music import *

# Initialise all pygame modules (required for any pygame)

weatherRAIN = 0
weatherSNOW = 1
weatherCLOUDS1 = 2
weatherCLOUDS2 = 3
weatherLIGHTNING = 4

srfcClouds = []
srfcClouds.append(pygame.image.load(gfn_Zip("clouds_big0.png")).convert_alpha())


# Particle Class
class gcls_Weather(pygame.sprite.Sprite):
    def __init__(self, inID, inBoundary):

        pygame.sprite.Sprite.__init__(self)
        
        # Standard properties - the initial (X,Y) coords are stored in the case of needing to reset a particle
        self.type = inID
        self.boundary = inBoundary * TILESIZE
        self.last_update = pygame.time.get_ticks()
        
        if self.type == weatherRAIN:
            self.x = int(random.random() * 256)
            self.y = int(random.random() * 192)
            self.width = 2
            self.height = 4
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(TRANSCOLOUR)
            self.image.set_at((0, 3), (0, 0, 155 + int(random.random() * 100)))
            self.image.set_at((0, 2), (0, 0, 155 + int(random.random() * 100)))
            self.image.set_at((1, 1), (0, 0, 155 + int(random.random() * 100)))
            self.image.set_at((1, 0), (0, 0, 155 + int(random.random() * 100)))
            self.image.set_alpha(0.95 * 255)
            self.image.set_colorkey(TRANSCOLOUR)
            self.vx = -50
            self.vy = 130

        elif self.type == weatherSNOW:
            self.x = int(random.random() * 256)
            self.y = self.boundary + int(random.random() * 192)
            self.width = 3
            self.height = 3
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(TRANSCOLOUR)
            RND = int(random.random() * 2)
            if RND == 0:
                col = int(random.random() * 50)
                self.image.set_at((1,1), (200 + col, 200 + col, 200 + col))
            else:
                col1 = int(random.random() * 50)
                col2 = int(random.random() * 50)
                col3 = int(random.random() * 50)
                col4 = int(random.random() * 50)
                col5 = int(random.random() * 50)
                self.image.set_at((1,1), (200 + col1, 200 + col1, 200 + col1))
                self.image.set_at((0,1), (200 + col1, 200 + col1, 200 + col1))
                self.image.set_at((2,1), (200 + col1, 200 + col1, 200 + col1))
                self.image.set_at((1,0), (200 + col1, 200 + col1, 200 + col1))
                self.image.set_at((1,2), (200 + col1, 200 + col1, 200 + col1))

            self.image.set_alpha(0.8 * 255)    
            self.image.set_colorkey(TRANSCOLOUR)
            self.vx = int(random.random() * 30) - 15
            self.vy = 20
            
        elif self.type == weatherCLOUDS1:
            self.width = 640
            self.height = 400
            self.x = 0
            self.y = self.boundary - self.height
            self.image = srfcClouds[int(random.random() * len(srfcClouds))]
            self.vx = -30

        elif self.type == weatherCLOUDS2:
            self.width = 640
            self.height = 400
            self.x = self.width
            self.y = self.boundary - self.height
            self.imageFull = srfcClouds[0]
            self.image = srfcClouds[int(random.random() * len(srfcClouds))]
            self.vx = -30

        elif self.type == weatherLIGHTNING:
            self.width = 320
            self.height = 200
            self.x = 0
            self.y = 0
            tempLightning = pygame.Surface((self.width, self.height))
            tempLightning.fill((250, 250, 200))
            self.image = tempLightning
            self.image.set_alpha(0)
            self.freq = 30
            self.fade = 0.7
            
        # Initial rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self, t, t_elapsed, inLevel):


        # Update the particle

        # Look for finished particles (lifetime expired, or out of the screen limits)
        if self.type == weatherRAIN:
            self.x += self.vx * t_elapsed
            self.y += self.vy * t_elapsed
            if self.x < inLevel.mapX or self.x > inLevel.mapX + inLevel.playWidth or self.y > inLevel.mapY + inLevel.playHeight:
                self.x = inLevel.mapX + int(random.random() * inLevel.playWidth)
                self.y = self.boundary + int(random.random() * ((inLevel.height * TILESIZE) - self.boundary)) - (random.random() * TILESIZE * 2)

        elif self.type == weatherSNOW:
            self.x += self.vx * t_elapsed
            self.y += self.vy * t_elapsed
            if self.x < inLevel.mapX or self.x > inLevel.mapX + inLevel.playWidth or self.y > inLevel.mapY + inLevel.playHeight:
                self.x = inLevel.mapX + int(random.random() * inLevel.playWidth)
                self.y = self.boundary + int(random.random() * ((inLevel.height * TILESIZE) - self.boundary)) - (random.random() * TILESIZE * 2)

                    
        elif self.type == weatherCLOUDS1 or self.type == weatherCLOUDS2:
            self.x += self.vx * t_elapsed
            # If the cloud is reached the end, make a new one
            if self.x + self.width <= 0:
                self.x = self.width
                self.image = srfcClouds[int(random.random() * len(srfcClouds))]

        elif self.type == weatherLIGHTNING:
            RND = int(random.random() * (1.0 / t_elapsed) * self.freq)
            if RND == 1:
                self.image.set_alpha(255)
                gfn_PlaySound(SFX_WX_LIGHTNING)

                
            currentAlpha = self.image.get_alpha()
            if currentAlpha > 0:
                newAlpha = currentAlpha - ((t_elapsed / self.fade) * 255)
                if newAlpha < 0: newAlpha = 0
                self.image.set_alpha(newAlpha)
                
                
        # Reset the timer
        self.last_update = t
        
        if self.type <> weatherLIGHTNING:
            self.rect = pygame.Rect(self.x - inLevel.mapX + inLevel.playX, self.y - inLevel.mapY + inLevel.playY, self.width, self.height)
