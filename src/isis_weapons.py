# TILES: isis_weapons.py
#
# Includes all weapon definitions and projectile AI
# Also includes inventory stuff

import pygame, math, random
pygame.init()
from isis_draw import *
from isis_tiles import *
from isis_particle import *
from isis_enemies import *
from isis_constants import *
from isis_zip import *

# Weapon Class
class gcls_Weapon():
    def __init__(self, inAmmo, inDamage):
        # If ammo = -1, it means that the weapon is yet to be collected
        # As such, it won't display on the HUD until ammo >= 0
        self.ammo = inAmmo
        self.damage = inDamage

# Weapon list, for Keen
WEAPON = []
WEAPON.append(gcls_Weapon(-1, 32))   # Plutezarp
WEAPON.append(gcls_Weapon(-1, 16))   # HR-42
WEAPON.append(gcls_Weapon(-1, 8))    # Solarizer
WEAPON.append(gcls_Weapon(-1, 4))    # Pulsar
WEAPON.append(gcls_Weapon(-1, 2))    # Zeffer 3000
WEAPON.append(gcls_Weapon(-1, 1))    # Blowgun
WEAPON.append(gcls_Weapon(-1, 1))    # Harpoon
WEAPON.append(gcls_Weapon(-1, 1))    # Raygun
WEAPON.append(gcls_Weapon(-1, 1))    # Neural Stunner

# Index definitions - they should match the Weapon list order
W_PLUTEZARP = 0
W_HR42 = 1
W_SOLARIZER = 2
W_PULSAR = 3
W_ZEFFER = 4
W_BLOWGUN = 5
W_HARPOON = 6
W_RAYGUN = 7
W_NEURAL = 8

W_EXPLODE = 9 # Random explosion

class gcls_Inventory():
    def __init__(self):
        self.maxPower = 0
        self.power = -1
INVENTORY = []
INVENTORY.append(gcls_Inventory()) # Battery
INVENTORY.append(gcls_Inventory()) # Shield
INVENTORY.append(gcls_Inventory()) # Ion Scanner
INVENTORY.append(gcls_Inventory()) # Unknown

iBattery = 0
iShield = 1
iIonScanner = 2
iUnknown = 3


# Projectile images
srfcProjectiles = gfnLoad_Splice(32, 32, gfn_Zip("projectiles.png"), 1, 1)
PROJ_BLOWGUN = 0
PROJ_ZEFFER = 2
PROJ_PULSAR = 4
PROJ_SOLARIZER = 8
PROJ_HR42 = 11
PROJ_PLUTEZARP = 15
PROJ_HARPOON = 16
PROJ_RAYGUN = 17
PROJ_NEURAL = 18

# Explosion images
srfcExplosions = gfnLoad_Splice(32, 32, gfn_Zip("explosions.png"), 1, 1)
srfcExplosions2 = gfnLoad_Splice(54, 55, gfn_Zip("explosions2.png"), 1, 1)
srfcExplosionsIsonian = gfnLoad_Splice(12, 15, gfn_Zip("enemy_isonian-proj1_xplod.png"), 1, 1)

XPLOD_ZEFFER = 0
XPLOD_PULSAR = 2
XPLOD_SOLARIZER = 8
XPLOD_HR42 = 13
XPLOD_PLUTEZARP = 20
XPLOD_RAYGUN = 28
XPLOD_NEURAL = 30
XPLOD_REDROBOT = 32

BLOWGUN_SPEED = 200 # Pixels / second
BLOWGUN_TIME = 0.5 # Seconds before falling
BLOWGUN_GRAVITY = 450 # Pixels / second ^2

ZEFFER_SPEED = 250
ZEFFER_AMP = 5
ZEFFER_PERIOD = 0.05
ZEFFER_YDEV = 40 # max possible y-deviation in pixels/second

PULSAR_SPEED = 250
SOLARIZER_SPEED = 150
HR42_SPEED = 150

PLUTEZARP_LIFE = 0.75
PLUTE_SPEED = 50
PLUTE_MAXLENGTH = 100

HARPOON_SPEED = 100
RAYGUN_SPEED = 200
NEURAL_SPEED = 200

# Projectile class
class gcls_Shoot(pygame.sprite.Sprite):
    def __init__(self, inKeen, inUp, inDown):
        pygame.sprite.Sprite.__init__(self)

        if inKeen.direction == -1:
            self.x0 = inKeen.x - 9
            self.x = inKeen.x - 9
        elif inKeen.direction == 1:
            self.x0 = inKeen.x + 24
            self.x = inKeen.x + 24
            
        self.y0 = inKeen.y + 11
        self.y = inKeen.y + 11
        
        self.id = inKeen.currentWeapon
        self.power = inKeen.weapon[self.id].damage
        self.direction = inKeen.direction
        self.timer = 0
        self.frame = 0
        self.last_update = 0
        self.up = inUp
        self.down = inDown
        inKeen.shootUp = inUp
        inKeen.shootDown = inDown
        
        if inKeen.currentWeapon == W_BLOWGUN:
            if inKeen.direction == 1:
                self.image = srfcProjectiles[PROJ_BLOWGUN]
            elif inKeen.direction == -1:
                self.image = pygame.transform.flip(srfcProjectiles[PROJ_BLOWGUN], True, False)
                
        elif inKeen.currentWeapon == W_ZEFFER:
            if self.up:
                self.x += 16 * self.direction * -1
                self.y -= 20
            elif self.down:
                self.x += 16 * self.direction * -1
                self.y += 20
            else: self.x += 10 * self.direction

            self.x0 = self.x
            self.y0 = self.y
            
            self.image = srfcProjectiles[PROJ_ZEFFER]
            self.delay = 1 / 8.0
            self.offsetX = random.random() * 100
            if int(random.random() * 2) == 1:
                self.offsetY = random.random() * ZEFFER_YDEV
            else:
                self.offsetY = 0
        elif inKeen.currentWeapon == W_PULSAR:
            if self.up:
                self.x += 16 * self.direction * -1
                self.y -= 10
            elif self.down:
                self.x += 16 * self.direction * -1
                self.y += 10
            else: self.x += 5 * self.direction
            
            if inKeen.direction == 1:
                self.image = pygame.transform.flip(srfcProjectiles[PROJ_PULSAR], True, False)
            elif inKeen.direction == -1:
                self.image = srfcProjectiles[PROJ_PULSAR] 
            self.delay = 1 / 8.0
            
        elif inKeen.currentWeapon == W_SOLARIZER:
            if self.up:
                self.x += 16 * self.direction * -1
                self.y -= 20
            elif self.down:
                self.x += 16 * self.direction * -1
                self.y += 20
            else: self.x += 10 * self.direction
            
            if inKeen.direction == 1:
                self.image = pygame.transform.flip(srfcProjectiles[PROJ_SOLARIZER], True, False)
            elif inKeen.direction == -1:
                self.image = srfcProjectiles[PROJ_SOLARIZER] 
            self.delay = 1 / 8.0
            
        elif inKeen.currentWeapon == W_HR42:
            if self.up:
                self.x += 16 * self.direction * -1
                self.y -= 20
            elif self.down:
                self.x += 16 * self.direction * -1
                self.y += 20
            else: self.x += 12 * self.direction
            
            if inKeen.direction == 1:
                self.image = srfcProjectiles[PROJ_HR42]
            elif inKeen.direction == -1:
                self.image = pygame.transform.flip(srfcProjectiles[PROJ_HR42], True, False) 
            self.delay = 1 / 8.0

        elif inKeen.currentWeapon == W_PLUTEZARP:
            self.x += 18 * self.direction
            self.image = pygame.transform.scale(srfcProjectiles[PROJ_PLUTEZARP], (1, 32))
            self.image.set_alpha(0.01 * 255)
            self.image.set_colorkey(TRANSCOLOUR)

        if inKeen.currentWeapon == W_HARPOON:
            self.y += 10
            self.x += 2 * self.direction
            if inKeen.direction == 1:
                self.image = srfcProjectiles[PROJ_HARPOON]
            elif inKeen.direction == -1:
                self.image = pygame.transform.flip(srfcProjectiles[PROJ_HARPOON], True, False)
                
        elif inKeen.currentWeapon == W_RAYGUN:
            self.image = srfcProjectiles[PROJ_RAYGUN]

            if self.up:
                self.x += 16 * self.direction * -1
                self.y -= 15
                self.image = pygame.transform.rotate(srfcProjectiles[PROJ_RAYGUN], 90)
            elif self.down:
                self.x += 16 * self.direction * -1
                self.y += 15
                self.image = pygame.transform.rotate(srfcProjectiles[PROJ_RAYGUN], 90)
            else:
                self.x += 8 * self.direction
                self.y += 1
                
            

        elif inKeen.currentWeapon == W_NEURAL:
            if self.up:
                self.x += 16 * self.direction * -1
                self.y -= 10
            elif self.down:
                self.x += 16 * self.direction * -1
                self.y += 10
            else:
                self.x += 8 * self.direction
                
            self.image = srfcProjectiles[PROJ_NEURAL]
            self.delay = 1 / 8.0            

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
    def update(self, t, inLevel, inEnemies):
        if self.id == W_BLOWGUN:
            self.timer += t
            if self.direction == 1:
                self.x += t * BLOWGUN_SPEED
                if self.timer >= BLOWGUN_TIME:
                    self.image = srfcProjectiles[PROJ_BLOWGUN + 1]
                    self.y += t * (self.timer - BLOWGUN_TIME) * BLOWGUN_GRAVITY
            elif self.direction == -1:
                self.x -= t * BLOWGUN_SPEED
                if self.timer >= BLOWGUN_TIME:
                    self.image = pygame.transform.flip(srfcProjectiles[PROJ_BLOWGUN + 1], True, False)
                    self.y += t * (self.timer - BLOWGUN_TIME) * BLOWGUN_GRAVITY

        elif self.id == W_ZEFFER:
            self.timer += t

            if self.up == True:
                self.x = self.x0 + (ZEFFER_AMP * math.sin((ZEFFER_PERIOD *  self.y) - (ZEFFER_PERIOD * self.offsetX)))
                self.x -= self.offsetY * self.timer
                self.y -= t * ZEFFER_SPEED
            elif self.down == True:
                self.x = self.x0 + (ZEFFER_AMP * math.sin((ZEFFER_PERIOD *  self.y) - (ZEFFER_PERIOD * self.offsetX)))
                self.x -= self.offsetY * self.timer
                self.y += t * ZEFFER_SPEED
            else:
                self.y = self.y0 + (ZEFFER_AMP * math.sin((ZEFFER_PERIOD *  self.x) - (ZEFFER_PERIOD * self.offsetX)))
                self.y -= self.offsetY * self.timer
                self.x += t * ZEFFER_SPEED * self.direction
            
            if (self.timer - self.last_update) > self.delay:
                self.last_update = self.timer
                self.frame += 1
                if self.frame == 2: self.frame = 0
                self.image = srfcProjectiles[PROJ_ZEFFER + self.frame]
            inLevel.sprite_Explosions.add(gcls_Particle(self.x, self.y, pTYPE_ZEFFER, pygame.time.get_ticks(), (150,0,150)))
            
        elif self.id == W_PULSAR:
            self.timer += t
            if self.up == True: self.y -= t * PULSAR_SPEED
            elif self.down == True: self.y += t * PULSAR_SPEED
            else: self.x += t * PULSAR_SPEED * self.direction
            
            if (self.timer - self.last_update) > self.delay:
                self.last_update = self.timer
                self.frame += 1
                if self.frame == 4: self.frame = 0
                if self.direction == 1:
                    self.image = pygame.transform.flip(srfcProjectiles[PROJ_PULSAR + self.frame], True, False)
                elif self.direction == -1:
                    self.image = srfcProjectiles[PROJ_PULSAR + self.frame]

        elif self.id == W_SOLARIZER:
            self.timer += t
            
            if self.up == True: self.y -= t * SOLARIZER_SPEED
            elif self.down == True: self.y += t * SOLARIZER_SPEED
            else: self.x += t * SOLARIZER_SPEED * self.direction
            
            if (self.timer - self.last_update) > self.delay:
                self.last_update = self.timer
                self.frame += 1
                if self.frame == 3: self.frame = 0
                if self.direction == 1:
                    self.image = pygame.transform.flip(srfcProjectiles[PROJ_SOLARIZER + self.frame], True, False)
                elif self.direction == -1:
                    self.image = srfcProjectiles[PROJ_SOLARIZER + self.frame]

        elif self.id == W_HR42:
            self.timer += t
            
            if self.up == True: self.y -= t * HR42_SPEED
            elif self.down == True: self.y += t * HR42_SPEED
            else: self.x += t * HR42_SPEED * self.direction
            
            if (self.timer - self.last_update) > self.delay:
                self.last_update = self.timer
                self.frame += 1
                if self.frame == 4: self.frame = 0
                if self.direction == 1:
                    self.image = srfcProjectiles[PROJ_HR42 + self.frame]
                elif self.direction == -1:
                    self.image = pygame.transform.flip(srfcProjectiles[PROJ_HR42 + self.frame], True, False)

        elif self.id == W_PLUTEZARP:
            self.timer += t
            # Fade in
            if self.timer < (PLUTEZARP_LIFE / 2.0):
                w = int(round(self.timer / (PLUTEZARP_LIFE / 2.0) * PLUTE_MAXLENGTH))
                self.image = pygame.transform.scale(srfcProjectiles[PROJ_PLUTEZARP], (w, 32))
                if self.direction == -1: self.x = self.x0 - w + 13

                amount = 255 * self.timer / (PLUTEZARP_LIFE / 2.0)
                if amount > 255: amount = 255
                self.image.set_alpha(amount)

                    
            # Fade out      
            elif self.timer < PLUTEZARP_LIFE:
                #w = PLUTE_MAXLENGTH - int(round((self.timer - (PLUTEZARP_LIFE / 2.0)) / (PLUTEZARP_LIFE / 2.0) * PLUTE_MAXLENGTH))
                #self.image = pygame.transform.scale(srfcProjectiles[PROJ_PLUTEZARP], (w, 32))

                amount = 255 - (255 * (self.timer - (PLUTEZARP_LIFE / 2.0)) / (PLUTEZARP_LIFE / 2.0))
                if amount < 0: amount = 0
                self.image.set_alpha(amount)

            # Kill
            else:
                self.kill()
                
        elif self.id == W_HARPOON:
            self.timer += t
            if self.direction == 1:
                self.x += t * HARPOON_SPEED
            elif self.direction == -1:
                self.x -= t * HARPOON_SPEED


                    
        elif self.id == W_RAYGUN:
            self.timer += t

            if self.up == True: self.y -= t * RAYGUN_SPEED
            elif self.down == True: self.y += t * RAYGUN_SPEED
            else: self.x += t * RAYGUN_SPEED * self.direction
            
        elif self.id == W_NEURAL:
            self.timer += t

            if self.up == True: self.y -= t * NEURAL_SPEED
            elif self.down == True: self.y += t * NEURAL_SPEED
            else: self.x += t * NEURAL_SPEED * self.direction

            if (self.timer - self.last_update) > self.delay:
                self.last_update = self.timer
                self.frame += 1
                if self.frame == 4: self.frame = 0
                self.image = srfcProjectiles[PROJ_NEURAL + self.frame]
                
        # Update rect (for collision purposes)
        self.rect = pygame.Rect(self.x, self.y, 24, 24)

        """
        # Check collisions with Ground (explosions) - *** TOO SLOW FOR MULTIPLE SIMULTANEOUS BULLETS ***
        GroundCollisions = pygame.sprite.spritecollide(self, inLevel.sprite_MaskAll, False, pygame.sprite.collide_rect)
        for hit in GroundCollisions:
           if pygame.sprite.collide_mask(self, hit):
                if self.id == W_BLOWGUN:
                    for i in range(50):
                        inLevel.sprite_Explosions.add(gcls_Particle(self.x + 16, self.y + 16, pTYPE_OTHER, pygame.time.get_ticks(),(50, 50, 50)))
                elif self.id == W_PLUTEZARP:
                    continue
                elif self.id == W_HARPOON:
                    for i in range(50):
                        inLevel.sprite_Explosions.add(gcls_Particle(self.x, self.y, pTYPE_OTHER, pygame.time.get_ticks(),(255, 255, 255)))
                else:
                    inLevel.sprite_Explosions.add(gcls_Explode(self.x, self.y, self.id, self.direction))

                self.kill()
        """
        
        # Check collisions with ground - if midpoint hits any INFO tile
        testX = int((self.x + (self.width / 2.0)) / TILESIZE)
        testY = int((self.y + (self.height / 2.0)) / TILESIZE)
        if gfnSolid_Info(inLevel.INFO[testX][testY]):        
            gfn_PlaySound(SFX_W_HITWALL)

            if self.id == W_BLOWGUN:
                for i in range(75):
                    inLevel.sprite_Explosions.add(gcls_Particle(self.x + 16, self.y + 16, pTYPE_OTHER, pygame.time.get_ticks(),(50, 50, 50)))
            elif self.id == W_PLUTEZARP:
                g = None
            elif self.id == W_HARPOON:
                for i in range(75):
                    inLevel.sprite_Explosions.add(gcls_Particle(self.x + 16, self.y + 16, pTYPE_OTHER, pygame.time.get_ticks(),(255, 255, 255)))
            elif self.id == W_SOLARIZER:
                for i in range(100):
                    RND1 = int(random.random() * 50)
                    RND2 = int(random.random() * 100)
                    inLevel.sprite_Explosions.add(gcls_Particle(self.x+16, self.y+16, pTYPE_OTHER, pygame.time.get_ticks(),(200 + RND1, 150 + RND2, 0)))
                    inLevel.sprite_Explosions.add(gcls_Explode(self.x, self.y, self.id, self.direction, self.up, self.down))
            else:
                inLevel.sprite_Explosions.add(gcls_Explode(self.x, self.y, self.id, self.direction, self.up, self.down))

            self.kill()
                
        # Update rect (for display purposes)
        self.rect = pygame.Rect(self.x - inLevel.mapX + 4, self.y - inLevel.mapY + 4, 24, 24)

        # Check collisions with Enemies
        GroundCollisions = pygame.sprite.spritecollide(self, inEnemies, False, pygame.sprite.collide_rect)
        for enemy in GroundCollisions:
           if pygame.sprite.collide_mask(self, enemy):
                if enemy.bullet == False and enemy.state <> ENEMY_STATE_DIE:
                    if self.id == W_BLOWGUN:
                        for i in range(20):
                            inLevel.sprite_Explosions.add(gcls_Particle(self.x + 16, self.y + 16, pTYPE_OTHER, pygame.time.get_ticks(),(50, 50, 50)))
                    elif self.id == W_PLUTEZARP:
                        g = None
                    elif self.id == W_HARPOON:
                        for i in range(20):
                            inLevel.sprite_Explosions.add(gcls_Particle(self.x, self.y, pTYPE_OTHER, pygame.time.get_ticks(),(255, 255, 255)))
                    elif self.id == W_PULSAR:
                        for i in range(10):
                            RND1 = int(random.random() * 40)
                            RND2 = int(random.random() * 40)
                            RND3 = int(random.random() * 40)
                            inLevel.sprite_Explosions.add(gcls_Particle(self.x, self.y, pTYPE_OTHER, pygame.time.get_ticks(),(200 + RND1, 55 + RND2, 200 + RND3)))
                    else:
                        inLevel.sprite_Explosions.add(gcls_Explode(self.x, self.y, self.id, self.direction, self.up, self.down))

                    enemy.hitPoints -= self.power


                    # Special fix for DRAGONFLY properties
                    # Health < 50%, fall & change to walk
                    # Health < 25%, slow down
                    if enemy.id == SPRITE_DRAGONFLY:

                        if enemy.hitPoints <= 0.25 * enemy.maxHit:
                            enemy.FPS = 2 * enemy.FPS
                            enemy.speedRun = 0.25 * enemy.speedRun

                        elif enemy.hitPoints <= 0.5 * enemy.maxHit:
                            enemy.gravity = 100
                            enemy.moveAmountX = 0
                            enemy.walkFrame = 5
                            enemy.walkMax = 6
                            enemy.FPS = 1000 / 2.0
                            enemy.speedRun = 15
                            enemy.y += 15

                        

                    # Special fix for dead Rat killed with Solarizer:
                    if enemy.id == SPRITE_RAT and enemy.hitPoints <= 0 and self.id == W_SOLARIZER:
                        enemy.dieFrame = 14
                        enemy.dieMax = 19

                        
                    # Kill it (unless it is Pulsar)
                    if self.id == W_PULSAR:
                        if (not self.up) and (not self.down):
                            self.x += enemy.width * self.direction
                        self.power = int(self.power / 2.0)
                        if self.power == 0: self.power = 1
                    else:
                        self.kill()
                        
                    if enemy.hitPoints <= 0:
                        enemy.moveAmountX = 0
                        enemy.moveAmountY = 0
                        enemy.state = ENEMY_STATE_DIE

                        # Enemy stats
                        if gfn_IsEnemy(enemy.id): inLevel.stats_NumEnemies += 1
                        
                        # Set initial speed for Evil Keen
                        if enemy.id == SPRITE_EVILKEEN:
                            enemy.vy = enemy.speedDieY
                            enemy.onGround = False
                            
                        # Make extra explosions for truck guys
                        elif enemy.id == SPRITE_TRUCKGUY1 or enemy.id == SPRITE_TRUCKGUY2:
                            for i in range(2):
                                randX = enemy.x + (random.random() * enemy.width) - (srfcExplosions2[0].get_width() / 2.0)
                                randY = enemy.y + (random.random() * enemy.height) - (srfcExplosions2[0].get_height() / 2.0)
                                inLevel.sprite_Explosions.add(gcls_Explode(randX, randY, W_EXPLODE, enemy.direction, 0, 0))

                            # Set random direction
                            RND = int(round(random.random() * 1))
                            if RND == 0: RND = -1

                            # Create a shooter jumping out of the truck
                            if enemy.id == SPRITE_TRUCKGUY1:
                                inLevel.sprite_Enemies.add(gcls_Enemy_Shooter(randX / TILESIZE, (randY / TILESIZE) - 2, SPRITE_TRUCKGUY1_WALK, RND))
                            elif enemy.id == SPRITE_TRUCKGUY2:
                                inLevel.sprite_Enemies.add(gcls_Enemy_Shooter(randX / TILESIZE, (randY / TILESIZE) - 2, SPRITE_TRUCKGUY2_WALK, RND))

                        # Move Garnak over
                        elif enemy.id == SPRITE_GARNAK:
                            enemy.x += 22 * enemy.direction * -1

                        # Move Bluemouth over
                        elif enemy.id == SPRITE_BLUEMOUTH:
                            enemy.x += 15 * enemy.direction * -1

                        # Move the army salves over (lemmings/truckguys/rats)
                        elif enemy.id == SPRITE_LEMMING or enemy.id == SPRITE_TRUCKGUY1_WALK or enemy.id == SPRITE_TRUCKGUY2_WALK or enemy.id == SPRITE_RAT:
                            enemy.x += 11 * enemy.direction * -1

                        # Produce Flasher shards
                        elif enemy.id == SPRITE_ROBOT_FLASHER:
                            for i in range(10):
                                RND_X = int(round(random.random() * 48))
                                RND_Y = int(round(random.random() * 48))
                                inLevel.sprite_Explosions.add(gcls_Particle(enemy.x + RND_X, enemy.y + RND_Y, enemy.id, pygame.time.get_ticks(), 0))

        # Check boundaries
        if self.x < 0 or self.x > inLevel.width * TILESIZE or self.y < 0 or self.y > inLevel.height * TILESIZE:
            self.kill()
            

# Explosion Class
class gcls_Explode(pygame.sprite.Sprite):
    def __init__(self, inX, inY, inID, inDir, inUp, inDown):
        pygame.sprite.Sprite.__init__(self)
        self.x = inX
        self.y = inY
        self.id = inID
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.init_frame = 0
        self.rect = pygame.Rect(1,1,1,1)
        self.direction = inDir
        self.up = inUp
        self.down = inDown
        
        # Adjust the coordinates for the tilted perspective
        self.x += 4 * self.direction * -1
        
        # Weapon Explosions
        if self.id == W_ZEFFER:
            self.init_frame = XPLOD_ZEFFER
            self.max_frames = 1.0
            self.fps = 4.0
        elif self.id == W_PULSAR:
            self.init_frame = XPLOD_PULSAR
            self.max_frames = 5.0
            self.fps = 10.0
            if self.up: self.y += 6
            elif self.down: self.y -= 6
        elif self.id == W_SOLARIZER:
            self.init_frame = XPLOD_SOLARIZER
            self.max_frames = 4.0
            self.fps = 10.0
        elif self.id == W_HR42:
            self.init_frame = XPLOD_HR42
            self.max_frames = 6.0
            self.fps = 8.0
        elif self.id == W_RAYGUN:
            self.init_frame = int(XPLOD_RAYGUN + round(random.random()))
            self.max_frames = 0
            self.fps = 1
        elif self.id == W_NEURAL:
            self.init_frame = XPLOD_NEURAL
            self.max_frames = 1.0
            self.fps = 4.0 
        elif self.id == SPRITE_ROBOT_RED_BULLET:
            self.init_frame = XPLOD_REDROBOT
            self.max_frames = 5.0
            self.fps = 8.0
            self.x += 5 * self.direction
            self.y += 13

            
            
        self.image = srfcExplosions[self.init_frame]

        # Other Explosions
        if self.id == W_EXPLODE:
            self.init_frame = int(round(random.random() * 1)) * 5
            self.max_frames = 4.0
            self.fps = 10.0
            self.image = srfcExplosions2[self.init_frame]
            
        elif self.id == SPRITE_ISONIAN_PROJ1r or self.id == SPRITE_ISONIAN_PROJ1g or self.id == SPRITE_ISONIAN_PROJ1w:
            self.init_frame = 0
            self.max_frames = 4
            self.fps = 8
            self.image = srfcExplosionsIsonian[self.init_frame]
            
        self.width, self.height = self.image.get_width(), self.image.get_height()
        
    def update(self, t, t_elapsed, inLevel, inKeen, inGame):
        
        if t - self.last_update >  1000.0 / self.fps:
            if self.frame < self.max_frames:
                self.frame += 1
                if self.id == SPRITE_ISONIAN_PROJ1r or self.id == SPRITE_ISONIAN_PROJ1g or self.id == SPRITE_ISONIAN_PROJ1w:
                    if self.direction == -1: self.image = srfcExplosionsIsonian[self.init_frame + self.frame]
                    else: self.image = pygame.transform.flip(srfcExplosionsIsonian[self.init_frame + self.frame], True, False)                    
                elif self.id < W_EXPLODE:
                    if self.direction == -1: self.image = srfcExplosions[self.init_frame + self.frame]
                    else: self.image = pygame.transform.flip(srfcExplosions[self.init_frame + self.frame], True, False)
                else:
                    if self.direction == -1: self.image = srfcExplosions2[self.init_frame + self.frame]
                    else: self.image = pygame.transform.flip(srfcExplosions2[self.init_frame + self.frame], True, False)
                    
                #self.image.set_alpha(255 - (255 * ((self.frame+1) / (self.max_frames+1))))
            else:
                self.kill()
            self.last_update = t

        # Rotate it, if need be
        if self.id == W_PULSAR:
            if   self.up:   self.image = pygame.transform.rotate(srfcExplosions[self.init_frame + self.frame], -90)
            elif self.down: self.image = pygame.transform.rotate(srfcExplosions[self.init_frame + self.frame],  90)
        
        # Check Solarizer collision with Keen - if so, kill Keen
        if self.id == W_SOLARIZER:
            if pygame.sprite.collide_mask(self, inKeen):
                inKeen.hurt(10, inGame, inLevel)

        self.rect = pygame.Rect(round(self.x - inLevel.mapX) + inLevel.playX, round(self.y - inLevel.mapY) + inLevel.playY, self.width, self.height)

        


# Sprite group for projectiles
sprite_Projectiles = pygame.sprite.RenderPlain()
sprite_Explosions = pygame.sprite.RenderPlain()


