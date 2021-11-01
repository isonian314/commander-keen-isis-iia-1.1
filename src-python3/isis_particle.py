import pygame, random, math, sys
from pygame.locals import *

from isis_draw import *
from isis_tiles import *
from isis_zip import *

# Initialise all pygame modules (required for any pygame)
pygame.init()

LIFE = []
LIFE.append(1.0)
LIFE.append(2.0)
LIFE.append(1.0)
LIFE.append(1.0)
LIFE.append(1.0)
LIFE.append(1.0)

pTYPE_SPLASH = 0
pTYPE_OTHER = 1
pTYPE_ZEFFER = 2
pTYPE_RAIN = 3
pTYPE_BUBBLE = 4
pTYPE_SPLASH_LAVA = 5
srfcBubbles = []

for x in range(4):
    bubble = pygame.Surface((12, 12))
    bubble.fill(TRANSCOLOUR)
    pygame.draw.circle(bubble, (0,0,0), (5,5), x + 1, 1)
    bubble.set_colorkey(TRANSCOLOUR)
    srfcBubbles.append(bubble)

# Particle Class
class gcls_Particle(pygame.sprite.Sprite):
    def __init__(self, X, Y, xType, Ti, inCol):

        pygame.sprite.Sprite.__init__(self)
        
        # Standard properties - the initial (X,Y) coords are stored in the case of needing to reset a particle
        self.active = True
        self.type = xType
        self.last_update = Ti - 0.01
        self.x0 = X
        self.y0 = Y

        
        # Specific properties (lifetime in SECONDS, vx, vy & g in PIXELS/SECOND) that depend upon the TYPE

        if xType == pTYPE_SPLASH:
            self.lifetime = LIFE[xType]
            self.x = ((random.random() * 10) - 5) + self.x0         # Random X position, +/- 5 pixels
            self.y = ((random.random() * 10) - 5) + self.y0         # Random Y position, +/- 5 pixels
            self.vx = (random.random() * 80) - 40
            self.vy = (random.random() * 150) * -1
            self.g = 200.0
            col = 255 - int(random.random() * 100)
            self.colour = (50, 50, col)
            self.image = pygame.Surface((1, 1))
            self.image.fill(self.colour)
            self.width = 1
            self.height = 1

        elif xType == pTYPE_SPLASH_LAVA:
            self.lifetime = LIFE[xType]
            self.x = ((random.random() * 10) - 5) + self.x0         # Random X position, +/- 5 pixels
            self.y = ((random.random() * 10) - 5) + self.y0         # Random Y position, +/- 5 pixels
            self.vx = (random.random() * 80) - 40
            self.vy = (random.random() * 150) * -1
            self.g = 200.0
            col = 255 - int(random.random() * 100)
            self.colour = (col, 50, 50)
            self.image = pygame.Surface((1, 1))
            self.image.fill(self.colour)
            self.width = 1
            self.height = 1
            
        elif xType == pTYPE_OTHER:
            self.lifetime = LIFE[xType]
            self.x = ((random.random() * 10) - 5) + self.x0         # Random X position, +/- 5 pixels
            self.y = ((random.random() * 10) - 5) + self.y0         # Random Y position, +/- 5 pixels
            self.vx = (random.random() * 80) - 40
            self.vy = (random.random() * 150) * -1
            self.g = 200.0
            self.colour = inCol
            self.image = pygame.Surface((1, 1))
            self.image.fill(self.colour)
            self.width = 1
            self.height = 1
            
        elif xType == pTYPE_ZEFFER:
            self.lifetime = LIFE[xType]
            self.x = self.x0 + 16
            self.y = self.y0 + 16
            self.colour = inCol
            self.image = pygame.Surface((1, 1))
            self.image.fill(self.colour)
            self.width = 1
            self.height = 1

        elif xType == pTYPE_RAIN:
            self.lifetime = LIFE[xType]
            self.x = int(random.random() * 256)
            self.y = int(random.random() * 192)
            self.width = 2
            self.height = 4
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(TRANSCOLOUR)
            self.image.set_at((0, 3), (0, 0, 255))
            self.image.set_at((0, 2), (0, 0, 255))
            self.image.set_at((1, 1), (0, 0, 255))
            self.image.set_at((1, 0), (0, 0, 255))
            self.image.set_colorkey(TRANSCOLOUR)
            self.vx = -50
            self.vy = 150

        elif xType == pTYPE_BUBBLE:
            self.lifetime = LIFE[xType]
            self.x = self.x0 + int(random.random() * 5) - 10
            self.y = self.y0 + int(random.random() * 5) - 10
            self.width = 12
            self.height = 12
            self.vx = 15
            self.vy = 10
            rand = int(random.random() * 10)
            if rand < 5: self.image = self.frame = 0
            elif rand >= 5 and rand < 8: self.frame = 1
            elif rand >= 8 and rand <= 9: self.frame = 2
            self.image = srfcBubbles[self.frame]

        elif xType == SPRITE_ROCK_GREY or xType == SPRITE_ROCK_MOSS:
            self.lifetime = 1
            self.x = X
            self.y = Y
            self.vx = (random.random() * 400) - 200
            self.vy = ((random.random() * 500) - 100) * -1
            self.g = 350.0
            self.width = 16
            self.height = 16
            tempImage = gfnLoad_Splice(16, 16, gfn_Zip("enemy_rocks-shards.png"), 1, 1)
            RND = int(round(random.random() * 4))
            self.image = tempImage[RND]
                      
        elif xType == SPRITE_ROCK_BROWN:
            self.lifetime = 1
            self.x = X
            self.y = Y
            self.vx = (random.random() * 400) - 200
            self.vy = ((random.random() * 500) - 100) * -1
            self.g = 350.0
            self.width = 16
            self.height = 16
            tempImage = gfnLoad_Splice(16, 16, gfn_Zip("enemy_rocks-shards.png"), 1, 1)
            RND = int(round(random.random() * 4))
            self.image = tempImage[RND + 5]

        elif xType == SPRITE_ROBOT_FLASHER:
            self.lifetime = 1
            self.x = X
            self.y = Y
            self.vx = (random.random() * 400) - 200
            self.vy = ((random.random() * 500) - 100) * -1
            self.g = 350.0
            self.width = 16
            self.height = 16
            tempImage = gfnLoad_Splice(16, 16, gfn_Zip("enemy_rocks-shards.png"), 1, 1)
            RND = int(round(random.random() * 4))
            self.image = tempImage[RND + 10]
            
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self, t, t_elapsed, inLevel, inKeen, inGame):

        if self.active == True:

            # Update the particle
            # NB: the velocities are scaled depending on the amount of time elapsed, which is the essence of frame-rate independent motion
            self.lifetime -= t_elapsed

            
            # Look for finished particles (lifetime expired, or out of the screen limits)
            # What happens will again depend on the particle type
            if self.type == pTYPE_SPLASH or self.type == pTYPE_SPLASH_LAVA:
                self.x += self.vx * t_elapsed
                self.y += self.vy * t_elapsed
                self.vy += self.g * t_elapsed
                if self.lifetime <= 0: #or self.x < 0 or self.x > maxWidth or self.y > maxHeight:
                    self.kill()
                    
            elif self.type == pTYPE_OTHER:
                self.x += self.vx * t_elapsed
                self.y += self.vy * t_elapsed
                self.vy += self.g * t_elapsed
                """
                if self.lifetime <= 0: #or self.x < 0 or self.x > maxWidth or self.y > maxHeight:
                    self.kill()
                """
                if self.x < 0 or self.x > (inLevel.width * TILESIZE) or self.y > (inLevel.height * TILESIZE):
                    self.kill()
                else:
                    # Kill if hits a wall
                    testX = int(self.x / TILESIZE)
                    testY = int(self.y / TILESIZE)
                    if gfnSolid_Info(inLevel.INFO[testX][testY]): 
                        self.kill()
                    
            elif self.type == pTYPE_ZEFFER:
                self.image.set_alpha(255 * (self.lifetime / LIFE[self.type]))
                if self.lifetime <= 0: #or self.x < 0 or self.x > maxWidth or self.y > maxHeight:
                    self.kill()

            elif self.type == pTYPE_RAIN:
                self.x += self.vx * t_elapsed
                self.y += self.vy * t_elapsed
                if self.x < 0 or self.x > inLevel.playWidth or self.y > inLevel.playHeight:
                    self.x = int(random.random() * 256)
                    self.y = 0

            elif self.type == pTYPE_BUBBLE:
                rand = round(random.random())
                if rand == 0: direc = -1
                else: direc = 1
                self.x += self.vx * t_elapsed * direc
                self.y -= self.vy * t_elapsed
                if inLevel.INFO[int(self.x / TILESIZE)][int(self.y / TILESIZE)] != INFO_WATER: self.kill()

                RND = int(random.random() * (1.0 / t_elapsed / 0.25))
                if RND == 1:
                    if self.frame < 3:
                        self.frame += 1
                        self.image = srfcBubbles[self.frame]
                     

            if self.type == SPRITE_ROCK_GREY or self.type == SPRITE_ROCK_BROWN or self.type == SPRITE_ROCK_MOSS or self.type == SPRITE_ROBOT_FLASHER:
                # Update positions
                self.x += self.vx * t_elapsed
                self.y += self.vy * t_elapsed
                self.vy += self.g * t_elapsed
                
                # Check if it's off-screen
                actualX = self.x - inLevel.mapX + inLevel.playX
                actualY = self.y - inLevel.mapY + inLevel.playY
                if actualX < 0 or actualX > inLevel.playWidth or actualY > inLevel.playHeight:
                    self.kill()
                    
            # Reset the timer
            self.last_update = t
            self.rect = pygame.Rect(self.x - inLevel.mapX + inLevel.playX, self.y - inLevel.mapY + inLevel.playY, self.width, self.height)
