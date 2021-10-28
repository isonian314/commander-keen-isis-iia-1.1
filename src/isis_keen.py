import pygame, math
pygame.init()

from isis_draw import *
from isis_tiles import *
from isis_level import *
from isis_weapons import *
from isis_tmx64 import *
from isis_particle import *
from isis_cutscenes import *
from isis_zip import *
from isis_music import *
from isis_constants import *

# Sprite direction constants
sDIR_STILL = 0
sDIR_LEFT = -1
sDIR_RIGHT = 1

# Keen sprite state constants
kSPRITE_NORMAL = 0
kSPRITE_GOD = 1
kSPRITE_CRAZY = 2
kSPRITE_EGA = 3
kSPRITE_DREAMS = 4



pwrNONE = 0
pwrSHOES = 1
pwrPOINTS = 2
pwrGOD = 3
pwrCRAZY = 4
pwrANTI = 5
pwrREGEN = 6
pwrDEGEN = 7
pwrTimes = [0, 10, 5, 10, 10, 3, 20, 20]

physNORMAL = 0
physSHOES = 1
physGOD = 2
physCRAZY = 3

# Keen Sprite
class gcls_Keen(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        
        # Fundamentals
        self.timer = 0
        self.width = 48
        self.height = 48
        self.frame = 0
        self.animation_timer = 0
        self.last_update = 0
        self.delay = 1000.0 / 8.0              # 1000 / fps
        self.state = kFALLING

        #self.infotiles = kLevelInfo
        self.checkTiles1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.checkTiles2 = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Animation delay in FPS (used for running) - these should be set according to the run speeds
        self.delay = []
        self.delay.append(7.5)     # Normal
        self.delay.append(10.0)    # Shoe Powerup
        self.delay.append(9.0)    # God
        self.delay.append(4.0)     # Crazy
        
        # Movement timers
        self.oldTimer = pygame.time.get_ticks()
        self.timeElapsed = 0.01
        self.moveAmountX, self.moveAmountY = 0, 0
        self.extraX, self.extraY = 0, 0
        
        # Idle timer, intervals and idle frame times (in SECONDS)
        # Shows LookingUp at idleMax
        # Shows Shrug at idleMax * 1.5
        # Shows Spew at idleMax * 3 (this will actually signal the end of the Crazy Keen phase)
        self.idleTimer = 0
        self.idleMax = 10
        self.idleLookTime = 1
        self.idleShrugTime = 1.5
        
        # Run speeds - in PIXELS PER SECOND
        self.RUN_SPEED = []
        self.RUN_SPEED.append(110)       # Run - Normal
        self.RUN_SPEED.append(140)       # Run - Shoe Powerup
        self.RUN_SPEED.append(170)       # Run - God Mode
        self.RUN_SPEED.append(50)        # Run - Crazy (will ultimately be random and changing)

        # Swim speeds - in PIXELS PER SECOND
        self.SWIM_SPEED = []
        self.SWIM_SPEED.append(55)       # Swim - Normal
        self.SWIM_SPEED.append(60)       # Swim - Shoe Powerup
        self.SWIM_SPEED.append(65)       # Swim - God Mode
        self.SWIM_SPEED.append(35)       # Swim - Crazy (will ultimately be random and changing)
        self.SWIM_GRAVITY = 12
        
        # Jump amounts - initial jump speed upward in PIXELS PER SECOND
        self.JUMP_AMOUNT = []
        self.JUMP_AMOUNT.append(-180)   # Initial Jump - Normal (-180)
        self.JUMP_AMOUNT.append(-220)   # Initial Jump - Shoe Powerup
        self.JUMP_AMOUNT.append(-240)   # Initial Jump - God Mode
        self.JUMP_AMOUNT.append(-150)   # Initial Jump - Crazy (will ultimately be random and changing)
        #self.JUMP_MAX = 0.025           # Factor that initial jump can increase by (holding CTRL)
        self.JUMP_MAX = -100
        self.jumpHold = 0.3             # How long to hold down the key for a FULL jump (in SECONDS)
        self.jumpTimer = 0
        
        # Gravity amounts - in PIXELS PER SECOND
        self.GRAVITY = []
        self.GRAVITY.append(450)      # Gravity - Normal (450)
        self.GRAVITY.append(450)      # Gravity - Shoe Powerup
        self.GRAVITY.append(400)      # Gravity - God Mode
        self.GRAVITY.append(450)      # Gravity - Crazy (will ultimately be random and changing)
        
        # Pogo speeds - in PIXELS PER SECOND - Idle Speed is x inertia, Idle Jump is the bounce without pushing CTRL
        self.POGO_IDLE_SPEED = []
        self.POGO_IDLE_SPEED.append(10)  # Normal
        self.POGO_IDLE_SPEED.append(15)  # Shoe Powerup
        self.POGO_IDLE_SPEED.append(20)  # God Mode
        self.POGO_IDLE_SPEED.append(5)   # Crazy
        self.POGO_SPEED = 1              # This is a proportion of the run speed that the pogo can go in the X direction
        
        self.POGO_IDLE_JUMP = []
        self.POGO_IDLE_JUMP.append(-200)    # Normal
        self.POGO_IDLE_JUMP.append(-220)    # Shoe
        self.POGO_IDLE_JUMP.append(-230)    # God
        self.POGO_IDLE_JUMP.append(-100)    # Crazy
        
        self.POGO_JUMP_AMOUNT = []
        self.POGO_JUMP_AMOUNT.append(-225)   # Pogo Jump - Normal (225)
        self.POGO_JUMP_AMOUNT.append(-265)   # Pogo Jump - Shoe Powerup
        self.POGO_JUMP_AMOUNT.append(-285)   # Pogo Jump - God Mode
        self.POGO_JUMP_AMOUNT.append(-205)   # Pogo Jump - Crazy (will ultimately be random and changing)
        #self.POGO_MAX = 0.021                 # Factor that initial pogo jump can increase by (holding CTRL)
        self.POGO_MAX = -120

        self.newPogoCurrent = 0 # Current pogo drift
        self.newPogoMax = 1   # Factor of run speed that the pogo is faster
        self.newPogoHold = 0.4    # Time to reach max pogo drift
        
        # Pole Climb speeds - in PIXELS PER SECOND
        self.POLE_DOWN = 100
        self.POLE_UP = 50
        
        # Display message
        self.message = "Testing"
        
        # Load Sprite Images & define locations of each image
        self.imgSprites = []
        self.imgSprites.append(gfnLoad_Splice(48, 48, gfn_Zip("keen_sprites0-normal.png"), 1, 1))
        #self.imgSprites.append(gfnLoad_Splice(48, 48, gfn_Zip("keen_sprites5-yorp.png"), 1, 1))
        #self.imgSprites.append(gfnLoad_Splice(48, 48, gfn_Zip("keen_sprites6-lindsay.png"), 1, 1))
        #self.imgSprites.append(gfnLoad_Splice(48, 48, gfn_Zip("keen_sprites7-council_page.png"), 1, 1))
        #self.imgSprites.append(gfnLoad_Splice(48, 48, gfn_Zip("keen_sprites8-council_member.png"), 1, 1))
        #self.imgSprites.append(gfnLoad_Splice(48, 48, gfn_Zip("keen_sprites9-vorticon.png"), 1, 1))
        self.imgSprites.append(gfnLoad_Splice(48, 48, gfn_Zip("keen_sprites1-god.png"), 1, 1))
        self.imgSprites.append(gfnLoad_Splice(48, 48, gfn_Zip("keen_sprites2-crazy.png"), 1, 1))
        self.imgSprites.append(gfnLoad_Splice(48, 48, gfn_Zip("keen_sprites3-ega.png"), 1, 1))
        self.imgSprites.append(gfnLoad_Splice(48, 48, gfn_Zip("keen_sprites4-dreams.png"), 1, 1))
        self.image = self.imgSprites[0][0]
        
        self.SPRITE_RUN_LEFT = 0
        self.SPRITE_JUMP_LEFT = 5
        self.SPRITE_POGO_LEFT = 8
        self.SPRITE_RUN_RIGHT = 13
        self.SPRITE_JUMP_RIGHT = 18
        self.SPRITE_POGO_RIGHT = 21
        self.SPRITE_LEDGE_LEFT = 26
        self.SPRITE_LEDGE_RIGHT = 31
        self.SPRITE_POLE_LEFT = 39
        self.SPRITE_POLE_RIGHT = 42
        self.SPRITE_POLE_DOWN = 45
        self.SPRITE_LOOK_UP = 52
        self.SPRITE_LOOK_DOWN = 53
        self.SPRITE_SHRUG = 55
        self.SPRITE_DOOR = 56
        self.SPRITE_TELEPORT = 65
        self.SPRITE_PLATFORM = 78
        self.SPRITE_DUCK_LEFT = 79
        self.SPRITE_DUCK_RIGHT = 80
        self.SPRITE_SHIELD = 81
        self.SPRITE_SHIELD_FALL = 83
        self.SPRITE_STUN = 86
        self.SPRITE_DIE = 86
        self.SPRITE_SWIM_LEFT = 117
        self.SPRITE_SWIM_RIGHT = 119
        self.SPRITE_SWIM_LEFT_HARPOON = 121
        self.SPRITE_SWIM_RIGHT_HARPOON = 123
        self.SPRITE_SWIM_DIE = 127

        self.SPRITE_SPEW = 91
        self.SPRITE_SPEW_MAX = 11
        
        self.SPRITE_SHOOT_PLUTEZARP = 130
        self.SPRITE_SHOOT_BLOWGUN = 138
        self.SPRITE_SHOOT_HARPOON = 125

        
        # State (normal/god/crazy)
        self.sprite = 0
        
        # Position, Accelleration, initial circumstances
        self.x = 0
        self.y = 0
        self.rect = None
        self.subRect = pygame.Rect(self.x + 11, self.y + 14, 26, 33)
        self.checkPoint = False
        self.checkX = 0
        self.checkY = 0
        
        self.vx = 0
        self.vy = 0
        self.ay = 0
        self.tilex = 0
        self.tiley = 0
        self.direction = 0
        self.dir = [-1, 1]
        self.makeSplash = False
        self.ledgeTimer = 0
        self.ledgeClimb = 1 # seconds to climb a ledge
        self.ledgeDelayTimer = 0
        self.ledgeDelay = 0.25
        self.ledgeFrame = 0
        
        self.onPogo = False

        # Looking Up/Down, Speed in PIXELS PER SECOND
        # Delay (how long until it happens) & MaxTime (how long until view reverts back to normal) are in SECONDS
        self.lookUp = False
        self.lookDown = False
        self.lookSpeed = 50
        self.lookSpeedReturn = 30
        self.lookOffsetX = 0
        self.lookOffsetY = 0
        self.lookDelay = 0.001 #0.2
        self.lookMaxTime = 2
        self.lookTimer1 = 0
        self.lookTimer2 = 0

        # Door stuff
        #self.inDoor = False
        self.doorNum = 0
        self.doorID = 0
        self.doorToX = 0
        self.doorToY = 0
        
        # Keycards
        self.hasKey = [False, False, False, False, False, False]
        self.itemTimer = 0
        
        # Weapons & Ammo
        self.weapon = WEAPON
        self.currentWeapon = -1
        self.oldWeapon = -1
        self.isGod = False
        self.timerWeapon = 0
        self.holdWeapon = 0.25   # Seconds to display shoot frame for
        self.shootUp = False
        self.shootDown = False

        # Powerups
        self.powerUp = pwrNONE
        self.powerUpTimer = 0
        self.pointMultiplier = 1
        self.physics = 0
        self.regenUpdate = 0

        # Inventory
        self.inventory = INVENTORY
        self.invCurrent = -1
        self.invRecharge = 2.0 # seconds per interval that it will recharge
        self.invItemTime = 1.0 # seconds per interval
        self.invMaxPower = 0
        self.invShield = 0
        self.invShieldTime = 0.5 # Seconds to display shield item
        
        # Health, Lives, Score
        self.health = 10
        self.lives = 3
        self.score = 0
        self.canHurt = 0
        self.HURT = 1 # Seconds of invinsibility
        self.healTimer = 0
        self.hurtTimer = 0
        self.yellowExtra = 0 # Offset caused by yellow enemy
        self.rectOffsetX = 15
        self.rectOffsetY = 16
        self.rectW = 20
        self.rectH = 30

        # Platforms
        self.onPlatform = False
        self.touchSwitch = False
        
        #self.update(pygame.time.get_ticks(), inLevel)

    def heal(self, inAmount):
        if self.health < 10:
            self.health += inAmount
            if self.health > 10: self.health = 10
            self.healTimer = 1 # Seconds
            self.hurtTimer = 0
            
    def hurt(self, inAmount, inGame, inLevel):
        if self.canHurt == 0:
            self.canHurt = self.HURT
            self.health -= inAmount
            self.hurtTimer = 1 # Seconds
            self.healTimer = 0

            # DEAD
            if self.health <= 0:
                pygame.mixer.music.fadeout(500)
                gfn_PlaySound(SFX_KEEN_DIE)
                self.onPogo = False
                self.lives -= 1
                self.health = 10
                if self.state <> kIN_WATER:
                    self.frame = self.SPRITE_DIE + int(round(random.random()))
                else:
                    self.frame = self.SPRITE_SWIM_DIE + int(round(random.random()))
                    
                self.state = kDYING
                self.vy = self.JUMP_AMOUNT[0]
                self.onPlatform = False
                
                if self.x - inLevel.mapX < inLevel.playWidth / 2.0: self.direction = 1
                else: self.direction = -1

                # Reset powerups
                self.powerUpTimer = 0
                self.powerUp = pwrNONE
                self.pointMultiplier = 1
                self.sprite = kSPRITE_NORMAL
                self.physics = physNORMAL                

    # Reset Keen (eg game over)
    def reset(self):
        self.hasKey = [False, False, False, False, False, False]
        for i in range(9):
            self.weapon[i].ammo = -1
            self.lives = 3
            self.health = 10
            self.score = 0
        self.currentWeapon = -1
        self.invCurrent = -1
        self.checkPoint = False
        self.checkX = 0
        self.checkY = 0
        
        # Reset powerups
        self.powerUpTimer = 0
        self.powerUp = pwrNONE
        self.pointMultiplier = 1
        self.sprite = kSPRITE_NORMAL
        self.physics = physNORMAL
            
    def updateSubRect(self):
        self.subRect = pygame.Rect(round(self.x) + self.rectOffsetX, round(self.y) + self.rectOffsetY, self.rectW, self.rectH)
        
    def update(self, t, t_elapsed, inLevel, inGame):

        # Calculate time elapsed since last update
        #self.timeElapsed = ((t - self.oldTimer) / 1000.0)
        #self.oldTimer = t
        self.timeElapsed = t_elapsed
        
        if self.timeElapsed > 0.1: self.timeElapsed = 0.1
        
        # Adjust weapon shoot timer
        if self.timerWeapon > 0: self.timerWeapon -= self.timeElapsed
        else: self.timerWeapon = 0

        # Adjust item collect timer
        if self.itemTimer > 0: self.itemTimer -= self.timeElapsed
        else: self.itemTimer = 0
        
        # If ammo is empty, and he is not shooting, choose another weapon
        if self.currentWeapon == W_HARPOON:
            if self.weapon[self.currentWeapon].ammo == 0 and self.timerWeapon == 0: self.currentWeapon = -1
        elif self.currentWeapon >= 0:
            # Check...
            if self.weapon[self.currentWeapon].ammo == 0 and self.timerWeapon == 0:
                # If Raygun/Neural, default to Blowgun first
                if self.currentWeapon == W_RAYGUN or self.currentWeapon == W_NEURAL: self.currentWeapon = W_BLOWGUN
                count = 0
                # Choose another weapon
                while self.weapon[self.currentWeapon].ammo <= 0 and count < 6:
                    self.currentWeapon += 1
                    if self.currentWeapon == 6: self.currentWeapon = 0
                    count += 1
                if count == 6: self.currentWeapon = -1
                            
        # Adjust invinsibility timer
        if self.canHurt > 0: self.canHurt -= self.timeElapsed
        else: self.canHurt = 0

        # Adjust powerup timer etc
        if self.powerUpTimer > 0:
            self.powerUpTimer -= self.timeElapsed
            # Processes Regen/Degen/Crazy powerups
            if self.powerUp == pwrREGEN:
                timeElapsed = (t - self.regenUpdate) / 1000.0
                if timeElapsed > 2.0:
                    self.heal(1)
                    self.regenUpdate = t
            elif self.powerUp == pwrDEGEN:
                timeElapsed = (t - self.regenUpdate) / 1000.0
                if timeElapsed > 2.0:
                    self.hurt(1, inGame, inLevel)
                    self.regenUpdate = t
            elif self.powerUp == pwrCRAZY:
                RND = int(random.random() * (1.5 / self.timeElapsed))
                if RND == 1:
                    self.RUN_SPEED[3] += int(random.random() * 150) - 75
                    self.SWIM_SPEED[3] += int(random.random() * 40) - 20
                    self.JUMP_AMOUNT[3] += int(random.random() * 60) - 30
                    self.POGO_IDLE_JUMP[3] += int(random.random() * 60) - 30
                    self.POGO_JUMP_AMOUNT[3] += int(random.random() * 40) - 20
                    if self.JUMP_AMOUNT[3] >= -50: self.JUMP_AMOUNT[3] = -50
                    if self.POGO_IDLE_JUMP[3] >= -50: self.POGO_IDLE_JUMP[3] = -50
                    if self.POGO_JUMP_AMOUNT[3] >= -50: self.POGO_JUMP_AMOUNT[3] = -50

        elif self.powerUpTimer < 0:

            # If was crazy, make him spew
            if self.powerUp == pwrCRAZY and self.state == kON_GROUND:
                self.state = kSPEW
                self.powerUpTimer = 0
                self.frame = 0
                self.image = self.imgSprites[self.sprite][self.SPRITE_SPEW]
                
            # Otherwise, reset Keen back to normal
            else:        
                self.powerUpTimer = 0
                self.powerUp = pwrNONE
                self.pointMultiplier = 1
                self.sprite = kSPRITE_NORMAL
                self.physics = physNORMAL
                
        # Adjust inventory
        if self.invCurrent <> -1 and self.inventory[self.invCurrent].power > 0:
            # Battery stuff - decereases at different rate as well as recharging others
            if self.invCurrent == 0:
                self.inventory[self.invCurrent].power -= self.timeElapsed * (1 / self.invRecharge)
                for i in range(3):
                    if self.inventory[i+1].power <> -1:
                        self.inventory[i+1].power += self.timeElapsed * (1 / self.invRecharge)
                        if self.inventory[i+1].power >= self.invMaxPower: self.inventory[i+1].power = self.invMaxPower
               
            # Other items - power just decreases with time
            else:
                self.inventory[self.invCurrent].power -= self.timeElapsed * (1 / self.invItemTime)
                
            if self.inventory[self.invCurrent].power <= 0:
                self.inventory[self.invCurrent].power = 0
                self.invCurrent = -1
            
        # Recharge the battery all the time, at half the recharge rate
        if self.inventory[0].power <> -1 and self.inventory[0].power < self.invMaxPower:
            self.inventory[0].power += self.timeElapsed * (1 / (2 * self.invRecharge))
            if self.inventory[0].power >= self.invMaxPower: self.inventory[0].power = self.invMaxPower

        # Shield timer
        if self.invShield > 0:
            self.invShield -= self.timeElapsed
            if self.invShield <= 0: self.invShield = 0
            
        # Adjust hurt / heal timers
        if self.healTimer > 0: self.healTimer -= self.timeElapsed
        else: self.healTimer = 0
        if self.hurtTimer > 0: self.hurtTimer -= self.timeElapsed
        else: self.hurtTimer = 0

        inKeys = pygame.key.get_pressed()
        gfnKeen_checkInput(self, inKeys, inLevel, inGame)
        gfnKeen_updatePosition(self, t, inKeys, inLevel, inGame)
        gfnKeen_selectFrame(self, t, inKeys, inLevel)

        
        # Randomly generate bubbles
        if self.state == kIN_WATER:
            RND = int(random.random() * (1.0 / self.timeElapsed / 0.5))
            if RND == 1:
                #gfn_PlaySound(SFX_KEEN_BUBBLES)
                if self.direction == sDIR_LEFT: offsetX = 10
                elif self.direction == sDIR_RIGHT: offsetX = 48
                offsetY = 26
                # Add 3 bubbles
                for i in range(3):
                    inLevel.sprite_Particles.add(gcls_Particle(self.x + offsetX, self.y + offsetY, pTYPE_BUBBLE, pygame.time.get_ticks(), 0))
                
        # Update rect for collision detection with onscreen items & enemies
        self.rect = pygame.Rect(self.x - inLevel.mapX + inLevel.playX, self.y - inLevel.mapY + inLevel.playY, 48, 48)
        self.updateSubRect()

        self.tilex = int((self.x + (self.width / 2)) / TILESIZE)
        self.tiley = int((self.y + self.height) / TILESIZE)

        # Reset extraX (YELLOW GUY)
        #self.extraX, self.extraY = 0, 0
        #self.moveAmountX = 0
        
    def keenPush(self, inLevel, inAmountX, inAmountY):
    
        # First extract the INFO layer from the Level
        # Also extract the width & height for edge-collision checking
        layerInfo = inLevel.INFO
        levelWidth = inLevel.width
        levelHeight = inLevel.height
        chkTiles1 = []
        chkTiles2 = []

        #______________________
        # RIGHT
        if inAmountX > 0:

            # Push player RIGHT if more than one TILESIZE from right edge
            if self.x + self.width < (levelWidth * TILESIZE) - 1:
                self.x += inAmountX
                self.updateSubRect()
                #self.message = "> Right"

            # 1. Check if we walk onto a slope
            TileX_Slope = int(self.subRect.midbottom[0] / TILESIZE)
            TileY_Slope = int(self.subRect.midbottom[1] / TILESIZE)

            # Up slopes
            if gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                if self.state == kON_GROUND:
                    self.y -= 3 * inAmountX / 4.0
                    self.x -= inAmountX / 4.0  
                
            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                if self.state == kON_GROUND:
                    self.y -= inAmountX / 2.0

            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope-1]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                if self.state == kON_GROUND:
                    self.y -= inAmountX / 2.0
                
            # Down slopes
            elif gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                if self.state == kON_GROUND:
                    self.y += inAmountX 
                
            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                if self.state == kON_GROUND:
                    self.y += inAmountX / 2.0

            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope+1]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                if self.state == kON_GROUND:
                    self.y += inAmountX / 2.0
              
            else:

                        
                # 2. Check if we hit a wall
                # Pixel coordinates - the left and right bounds of the Rect
                TileYpix = self.subRect[1] - (self.subRect[1] % TILESIZE) + 1
                TestEnd = self.subRect[1] + self.subRect.height - 1
                
                # Map coordinates
                TileX = int((self.subRect[0] + self.subRect.width) / TILESIZE)
                TileY = int(TileYpix / TILESIZE)

                while TileYpix <= TestEnd:
                    if gfnTile_SolidFromLeft(inLevel.INFO[TileX][TileY]) and not gfnTile_UpRight45(inLevel.INFO[TileX-1][TileY]):
                        if not gfnTile_UpRight30_1(inLevel.INFO[TileX-1][TileY]) and not gfnTile_UpRight30_2(inLevel.INFO[TileX-1][TileY]):
                            self.x = (TileX * TILESIZE) - self.subRect.width - self.rectOffsetX - 1
                            
                    TileY +=1
                    TileYpix += TILESIZE

                # 3. Check if we should fall
                fall = True
                TileXpix = self.subRect[0] - (self.subRect[0] % TILESIZE) + 4
                TestEnd = self.subRect[0] + self.subRect.width - 2
                
                # Map coordinates
                TileY = int((self.subRect[1] + self.subRect.height + 2) / TILESIZE)
                TileX = int(TileXpix / TILESIZE)

                while TileXpix <= TestEnd:
                    if gfnTile_SolidFromTop(inLevel.INFO[TileX][TileY]):
                        fall = False
                        
                    TileX +=1
                    TileXpix += TILESIZE

                if fall == True and self.state == kON_GROUND and self.onPlatform == False:
                    self.vy = 0
                    self.state = kFALLING
                    
                #if self.state == kON_GROUND and self.y > (TileY * TILESIZE) - self.subRect.height - self.rectOffsetY - 1:
                #    self.y = (TileY * TILESIZE) - self.subRect.height - self.rectOffsetY - 1
                    
        #______________________
        # LEFT
        elif inAmountX < 0:

            # Push player LEFT if more than one TILESIZE from left edge
            if self.x > 1:
                self.x += inAmountX
                self.updateSubRect()
                #self.message = "< Left"

            # 1. Check if we walk onto a slope
            TileX_Slope = int(self.subRect.midbottom[0] / TILESIZE)
            TileY_Slope = int(self.subRect.midbottom[1] / TILESIZE)

            # Up slopes
            if gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                if self.state == kON_GROUND:
                    self.y += 3 * inAmountX / 4.0
                    self.x -= inAmountX / 4.0
                
            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                if self.state == kON_GROUND:
                    self.y += inAmountX / 2.0

            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope-1]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                if self.state == kON_GROUND:
                    self.y += inAmountX / 2.0
                
            # Down slopes
            elif gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                if self.state == kON_GROUND:
                    self.y -= inAmountX
                
            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                if self.state == kON_GROUND:
                    self.y -= inAmountX / 2.0

            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope+1]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                if self.state == kON_GROUND:
                    self.y -= inAmountX / 2.0

                
            else:

                # Pixel coordinates - the left and right bounds of the Rect
                TileYpix = self.subRect[1] - (self.subRect[1] % TILESIZE) + 1
                TestEnd = self.subRect[1] + self.subRect.height - 1
                
                # Map coordinates
                TileX = int(self.subRect[0] / TILESIZE)
                TileY = int(TileYpix / TILESIZE)

                while TileYpix <= TestEnd:
                    if gfnTile_SolidFromRight(inLevel.INFO[TileX][TileY]) and not gfnTile_DownRight45(inLevel.INFO[TileX+1][TileY]):
                        if not gfnTile_UpRight45(inLevel.INFO[TileX+1][TileY-1]):
                            if not gfnTile_DownRight30_1(inLevel.INFO[TileX+1][TileY-1]) and not gfnTile_DownRight30_2(inLevel.INFO[TileX+1][TileY-1]):
                                self.x = ((TileX + 1) * TILESIZE) - self.rectOffsetX 
                    
                    TileY +=1
                    TileYpix += TILESIZE

       
                # Test to see if we've walking off a cliff
                fall = True
                TileXpix = self.subRect[0] - (self.subRect[0] % TILESIZE) + 2
                TestEnd = self.subRect[0] + self.subRect.width - 4
                
                # Map coordinates
                TileY = int((self.subRect[1] + self.subRect.height + 2) / TILESIZE)
                TileX = int(TileXpix / TILESIZE)

                while TileXpix <= TestEnd:
                    if gfnTile_SolidFromTop(inLevel.INFO[TileX][TileY]):
                        fall = False
                       
                    TileX +=1
                    TileXpix += TILESIZE

                if fall == True and self.state == kON_GROUND and self.onPlatform == False:
                    self.vy = 0
                    self.state = kFALLING

                # Snaps Keen to the ground if he is just below it
                #if self.state == kON_GROUND and self.y > (TileY * TILESIZE) - self.subRect.height - self.rectOffsetY - 1:
                #    self.y = (TileY * TILESIZE) - self.subRect.height - self.rectOffsetY - 1  


        #______________________
        # DOWN
        elif inAmountY > 0:

            # Push player DOWN if less than one TILESIZE from the bottom
            if self.y < (levelHeight * TILESIZE) - self.height - TILESIZE:
                self.y += inAmountY
                self.updateSubRect()
                #self.message = "V Down"
                
               
            # Check WATER first
            chkTiles1 = gfn_GetInfoTiles(inLevel, self.x, self.y, self.width, self.height, 0, 0, 0, 8)
            if gfnTile_Water(chkTiles1[7]):
                if self.state == kFALLING:
                    self.state = kIN_WATER
                    self.makeSplash = True
                    self.frame = 0
                    self.vy = 0
                    self.onPogo = False

                    # Change weapon to harpoon (if ammo), or nill (if no harpoon)
                    # Saves the old weapon so it reverts back to that one if Keen goes out of the water
                    if self.weapon[W_HARPOON].ammo > 0:
                        self.oldWeapon = self.currentWeapon
                        self.currentWeapon = W_HARPOON
                    else:
                        self.oldWeapon = self.currentWeapon
                        self.currentWeapon = -1


            # Check for landing on slopes first
            TileX = int(self.subRect.midbottom[0] / TILESIZE)        
            TileY = int((self.subRect[1] + self.subRect.height) / TILESIZE)
            if gfnTile_UpRight45(inLevel.INFO[TileX][TileY]):
                if (self.subRect[1] + self.subRect.height) % TILESIZE > TILESIZE - (self.subRect.midbottom[0] % TILESIZE):
                    self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - (TILESIZE - (self.subRect.midbottom[0] % TILESIZE))
                    self.vy = 0
                    self.state = kON_GROUND
                    
            elif gfnTile_UpRight30_1(inLevel.INFO[TileX][TileY]):
                if (self.subRect[1] + self.subRect.height) % TILESIZE > TILESIZE - ((self.subRect.midbottom[0] % TILESIZE) * 0.5):
                    self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - (TILESIZE - ((self.subRect.midbottom[0] % TILESIZE) * 0.5))
                    self.vy = 0
                    self.state = kON_GROUND

            elif gfnTile_UpRight30_2(inLevel.INFO[TileX][TileY]):
                if (self.subRect[1] + self.subRect.height) % TILESIZE > TILESIZE - ((self.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5:
                    self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - (TILESIZE - ((self.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5)
                    self.vy = 0
                    self.state = kON_GROUND

            elif gfnTile_DownRight45(inLevel.INFO[TileX][TileY]):
                if (self.subRect[1] + self.subRect.height) % TILESIZE >  self.subRect.midbottom[0] % TILESIZE:
                    self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - (self.subRect.midbottom[0] % TILESIZE)
                    self.vy = 0
                    self.state = kON_GROUND
                    
            elif gfnTile_DownRight30_1(inLevel.INFO[TileX][TileY]):
                if (self.subRect[1] + self.subRect.height) % TILESIZE >  (self.subRect.midbottom[0] % TILESIZE) * 0.5:
                    self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - ((self.subRect.midbottom[0] % TILESIZE) * 0.5)
                    self.vy = 0
                    self.state = kON_GROUND

            elif gfnTile_DownRight30_2(inLevel.INFO[TileX][TileY]):
                if (self.subRect[1] + self.subRect.height) % TILESIZE >  ((self.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5:
                    self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - (((self.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5)
                    self.vy = 0
                    self.state = kON_GROUND
                    
            # If no slope, scan for a solid  
            else:
                # Pixel coordinates - the left and right bounds of the Rect
                TileXpix = self.subRect[0] - (self.subRect[0] % TILESIZE) + 2
                TestEnd = self.subRect[0] + self.subRect.width - 2
                
                # Map coordinates
                TileY = int((self.subRect[1] + self.subRect.height) / TILESIZE)
                TileX = int(TileXpix / TILESIZE)

                while TileXpix <= TestEnd:
                    if gfnTile_SolidFromTop(inLevel.INFO[TileX][TileY]):
                        self.y = (TileY * TILESIZE) - self.subRect.height - self.rectOffsetY - 1
                        if self.state == kFALLING: self.state = kON_GROUND
                        self.vy = 0
                        
                    TileX +=1
                    TileXpix += TILESIZE
                
        #______________________
        # UP
        elif inAmountY < 0:

            # Push player UP if more than one TILESIZE from the top
            if self.y > TILESIZE:
                self.y += inAmountY
                self.updateSubRect()
                #self.message = "^ in Air"
                
            # Check WATER first
            chkTiles1 = gfn_GetInfoTiles(inLevel, self.x, self.y, self.width, self.height, 16, 16, 16, 4)
            if self.state == kIN_WATER:
                if not gfnTile_Water(chkTiles1[7]):
                    self.vy = self.JUMP_AMOUNT[self.sprite]
                    self.state = kFALLING
                    self.currentWeapon = self.oldWeapon
                    
            # Pixel coordinates - the left and right bounds of the Rect
            TileXpix = self.subRect[0] - (self.subRect[0] % TILESIZE)
            TestEnd = self.subRect[0] + self.subRect.width

            # Map coordinates
            TileY = int(self.subRect[1] / TILESIZE)
            TileX = int(TileXpix / TILESIZE)

            while TileXpix <= TestEnd:
                if gfnTile_SolidFromBottom(inLevel.INFO[TileX][TileY]):
                    #self.y = (TileY * TILESIZE)
                    self.vy = 0
                    self.jumpTimer = 0
                    self.y -= inAmountY
                    
                TileX +=1
                TileXpix += TILESIZE

                
        # Update collision Rect
        self.updateSubRect()
    
def gfnKeen_checkSingleKey(self, inEvent, inLevel, inGame):
    # Get keys pushed for shooting up/down
    keys = pygame.key.get_pressed()
    
    # Single push input
    if inEvent == K_RSHIFT or inEvent == K_LSHIFT:
        if self.onPogo == True:
            self.onPogo = False
        elif self.state == kON_GROUND or self.state == kFALLING:
            self.onPogo = True
            self.state = kFALLING
            self.lookUp, self.lookDown = False, False
            # NEW POGO CODE
            # Set pogo drift speed based on current speed
            if self.vx <> 0:
                self.newPogoCurrent = self.direction * (self.moveAmountX / self.timeElapsed)
            else:
                self.newPogoCurrent = 0
            

    elif inEvent == K_SPACE:
        # If Keen is in a shootable state
        if self.state <> kON_LEDGE and self.state <> kIN_DOOR and self.state <> kDYING and self.powerUp <> pwrCRAZY:
            
            if self.powerUp <> pwrGOD:
                # Not in Water
                if self.state <> kIN_WATER and self.weapon[self.currentWeapon].ammo > 0:
                    # No shooting if Blowgun/Plute and On Pole
                    if not (self.state == kON_POLE and (self.currentWeapon == W_BLOWGUN or self.currentWeapon == W_PLUTEZARP)) or self.lookDown == True:
                        self.lookUp, self.lookDown = False, False
                        shootUp, shootDown = False, False

                        gfn_PlaySound(self.currentWeapon)

                        self.timerWeapon = self.holdWeapon
                        self.weapon[self.currentWeapon].ammo -= 1
                        
                        if self.onPogo == True: self.onPogo = False

                        # Set shoot up/down flags, if applicable
                        if keys[K_UP] and (self.currentWeapon <> W_BLOWGUN and self.currentWeapon <> W_PLUTEZARP):
                            shootUp = True
                        elif keys[K_DOWN] and self.state <> kON_GROUND:
                            shootDown = True

                        inLevel.sprite_Projectiles.add(gcls_Shoot(self, shootUp, shootDown))
                        self.idleTimer = 0
  
                        
                # In Water
                elif self.state == kIN_WATER and self.currentWeapon == W_HARPOON and self.weapon[W_HARPOON].ammo > 0:
                    self.timerWeapon = self.holdWeapon
                    self.weapon[self.currentWeapon].ammo -= 1
                    inLevel.sprite_Projectiles.add(gcls_Shoot(self, False, False))                        
                    self.idleTimer = 0
                
            else:
                g = None
                
    # Weapon changes
    elif inEvent == K_6 and self.weapon[0].ammo > 0 and self.state <> kIN_WATER: self.currentWeapon = 0  # Plute
    elif inEvent == K_5 and self.weapon[1].ammo > 0 and self.state <> kIN_WATER: self.currentWeapon = 1  # HR-42
    elif inEvent == K_4 and self.weapon[2].ammo > 0 and self.state <> kIN_WATER: self.currentWeapon = 2  # Solarizer
    elif inEvent == K_3 and self.weapon[3].ammo > 0 and self.state <> kIN_WATER: self.currentWeapon = 3  # Pulsar
    elif inEvent == K_2 and self.weapon[4].ammo > 0 and self.state <> kIN_WATER: self.currentWeapon = 4  # Zeffer 3000
    elif inEvent == K_1 and self.weapon[5].ammo > 0 and self.state <> kIN_WATER: self.currentWeapon = 5  # Blowgun
    elif inEvent == K_7 and self.weapon[7].ammo > 0 and self.state <> kIN_WATER: self.currentWeapon = 7  # Raygun
    elif inEvent == K_8 and self.weapon[8].ammo > 0 and self.state <> kIN_WATER: self.currentWeapon = 8  # Neural Stunner

    # Inventory
    elif inEvent == K_F1 and self.inventory[0].power >= 1 and self.powerUp <> pwrCRAZY:
        if self.invCurrent <> 0: self.invCurrent = 0
        else: self.invCurrent = -1
        
    elif inEvent == K_F2 and self.inventory[1].power >= 1:
        if self.invCurrent <> 1: self.invCurrent = 1
        else: self.invCurrent = -1
        
    elif inEvent == K_F3 and self.inventory[2].power >= 1:
        if self.invCurrent <> 2: self.invCurrent = 2
        else: self.invCurrent = -1
        
    elif inEvent == K_F4 and self.inventory[3].power >= 1:
        if self.invCurrent <> 3: self.invCurrent = 3
        else: self.invCurrent = -1

    # Switches (pushing up, on the ground, and still)
    elif inEvent == K_UP and self.state == kON_GROUND and self.vx == 0 and self.touchSwitch == False:
        # See if we're touching a Switch
        Keen_X_Switches = pygame.sprite.spritecollide(self, inLevel.sprite_Switches, False, pygame.sprite.collide_rect)
        for possibleCollide in Keen_X_Switches:
            if pygame.sprite.collide_mask(self, possibleCollide):
                if possibleCollide.state == DOOR_STATE_CLOSED: possibleCollide.state = DOOR_STATE_OPEN
                else: possibleCollide.state = DOOR_STATE_CLOSED
                gfn_PlaySound(SFX_KEEN_SWITCH)
                self.touchSwitch = True
                self.last_update = pygame.time.get_ticks()

                # Activate platform
                for platform in inLevel.sprite_Platforms:
                    if platform.switchNum == possibleCollide.switchNum:
                        if possibleCollide.state == DOOR_STATE_OPEN: platform.active = True
                        else: platform.active = False
                        
    
    # Debug Stuff
    # HIDDEN AREAS
    elif inEvent == K_h:
        if inGame.debug.on:
            if inGame.debug.hidden == False: inGame.debug.hidden = True
            else: inGame.debug.hidden = False

    elif inEvent == K_j:
        if inGame.debug.on:
            if inGame.debug.jump == False: inGame.debug.jump = True
            else: inGame.debug.jump = False
            
    # KEYS
    elif inEvent == K_k:
        if inGame.debug.on:
            self.hasKey = [True, True, True, True, True, True]

    # LIVES
    elif inEvent == K_l:
        if inGame.debug.on:
            self.lives = 99
            self.health = 10
            
    # WEAPONS
    elif inEvent == K_w:
        if inGame.debug.on:
            for i in range(9):
                self.weapon[i].ammo = 99
            self.currentWeapon = W_BLOWGUN

    # WEAPONS
    elif inEvent == K_i:
        if inGame.debug.on:
            for i in range(4):
                self.inventory[i].power = 20
            self.invMaxPower = 20
                
    # LEVEL STATS
    elif inEvent == K_s:
        #if inGame.debug.on:
            if inGame.debug.message <> DEBUG_STATS: inGame.debug.message = DEBUG_STATS
            else: inGame.debug.message = DEBUG_NIL

    # LEVEL STATS
    elif inEvent == K_m:
        if inGame.debug.on:
            if inGame.debug.message <> DEBUG_HELLO: inGame.debug.message = DEBUG_HELLO
            else: inGame.debug.message = DEBUG_NIL

    # CYCLE DEBUG COLOUR
    elif inEvent == K_c:
        #if inGame.debug.on:
            if inGame.debug.messageCol < len(inGame.debug.COLS)-1: inGame.debug.messageCol += 1
            else: inGame.debug.messageCol = 0
    
    
def gfnKeen_checkInput(self, inKeys, inLevel, inGame):       

    # Update Look up/down offset
    if self.lookOffsetY <> 0 and self.lookUp == False and self.lookDown == False:

        # If the timer has expired, start resetting the view
        self.lookTimer2 += self.timeElapsed
        if self.lookTimer2 >= self.lookMaxTime:
            if self.lookOffsetY > 0:
                self.lookOffsetY -= self.timeElapsed * self.lookSpeedReturn
            else:
                self.lookOffsetY += self.timeElapsed * self.lookSpeedReturn
                    
            # If offset is less than 1 px, reset everything
            if abs(self.lookOffsetY) < 1:
                self.lookOffsetY = 0
                self.lookTimer2 = 0
                self.lookUp = False
                self.lookDown = False

                
    # Update Look left/right offset (essential for ledge grabs, mimmicks a look function)
    if self.lookOffsetX <> 0:
        
        # If the timer has expired, start resetting the view
        #if self.lookTimer2 >= self.lookMaxTime:
        if self.lookOffsetX > 0:
            self.lookOffsetX -= self.timeElapsed * self.lookSpeedReturn
        else:
            self.lookOffsetX += self.timeElapsed * self.lookSpeedReturn
                    
        # If offset is less than 1 px, reset everything
        if abs(self.lookOffsetX) < 1:
                self.lookOffsetX = 0



    
    # Look up
    # IF on a pole,
    # ELSE IF at a door
    # ELSE IF at a swtich
    # ELSE IF (looking)
    if inKeys[K_UP]:
        if self.state == kON_GROUND and not (inKeys[K_LEFT] or inKeys[K_RIGHT]) and not (inKeys[K_RCTRL] or inKeys[K_LCTRL]) and self.onPogo == False:
            # If Keens in front of a door, go in,
            chkTiles1 = gfn_GetInfoTiles(inLevel, self.x, self.y, self.width, self.height, 0, 0, 0, 0)
            if gfnTile_Door(chkTiles1[4]):
                doorType = 0 # 1st or 2nd door
                self.state = kIN_DOOR
                for i in range(len(inLevel.DoorList)):
                    if self.tilex == inLevel.DoorList[i].x1 and self.tiley - 2 == inLevel.DoorList[i].y1:
                        self.doorID = i
                        self.doorToX = (inLevel.DoorList[i].x2 - 1) * TILESIZE
                        self.doorToY = (inLevel.DoorList[i].y2 - 1) * TILESIZE
                        doorType = 0 # x1, y1
                        
                    elif self.tilex == inLevel.DoorList[i].x2 and self.tiley - 2 == inLevel.DoorList[i].y2:
                        self.doorID = i
                        self.doorToX = (inLevel.DoorList[i].x1 - 1) * TILESIZE
                        self.doorToY = (inLevel.DoorList[i].y1 - 1) * TILESIZE
                        doorType = 1 # x2, y2
                
                # Adjust x position depending on whether Keen is on the left or right door
                # Left door (ID is odd)
                if inLevel.DoorList[self.doorID].id % 2 == 1:
                    if doorType == 0: self.x = (inLevel.DoorList[self.doorID].x1 + 1) * TILESIZE - (self.width / 2.0)
                    elif doorType == 1: self.x = (inLevel.DoorList[self.doorID].x2 + 1) * TILESIZE - (self.width / 2.0)
                    
                # Right door (ID is even)
                else:
                    if doorType == 0: self.x = (inLevel.DoorList[self.doorID].x1) * TILESIZE - (self.width / 2.0)
                    elif doorType == 1: self.x = (inLevel.DoorList[self.doorID].x2) * TILESIZE - (self.width / 2.0)
    
            # Otherwise, try to look - if within range
            elif inLevel.playHeight - ((self.y - inLevel.mapY) % inLevel.playHeight) > TILESIZE * 4 and int(inLevel.mapY) > 0:
                # Check the shot timer isn;'t active
                if self.timerWeapon == 0:
                    # Check if we're not touching a switch
                    g = False
                    Keen_X_Switches = pygame.sprite.spritecollide(self, inLevel.sprite_Switches, False, pygame.sprite.collide_rect)
                    for possibleCollide in Keen_X_Switches:
                        if pygame.sprite.collide_mask(self, possibleCollide):
                            g = True
                    if g == False:
                        #if self.lookTimer2 == 0:
                        self.lookTimer1 += self.timeElapsed
                        if self.lookTimer1 > self.lookDelay:
                            self.lookOffsetY -= self.lookSpeed * self.timeElapsed
                            self.lookUp = True
                            self.lookTimer2 = 0
                    
                    
        # Climb a pole if Keen is falling down (not up, this because this way he can "fly" up a pole)
        elif self.state == kFALLING:
            if self.powerUp <> pwrCRAZY and self.vy >= 0:
                chkTiles1 = gfn_GetInfoTiles(inLevel, self.x, self.y, self.width, self.height, 28, 24, 24, 0)
                if (gfnTile_Pole(chkTiles1[0]) and not gfnTile_Pole(chkTiles1[1])):
                    self.state = kON_POLE
                    self.x += 7 - (int(self.x % TILESIZE))
                    
                elif gfnTile_Pole(chkTiles1[2]):
                    self.state = kON_POLE
                    if int(self.x % 16) >= 8:
                        self.x -= 1 + (int(self.x % TILESIZE) - 8)
                    else:
                        self.x -= int(self.x % TILESIZE) + 8 + 1
                
    elif self.lookUp == True:
        self.lookTimer1 = 0
        self.lookUp = False
    
    # Look Down
    # IF on a pole,
    # ELSE IF (looking)
    elif inKeys[K_DOWN] and not (inKeys[K_LEFT] or inKeys[K_RIGHT]) and self.state == kON_GROUND and self.onPogo == False:

        # If not Crazy, and on pole, climb pole
        chkTiles1 = gfn_GetInfoTiles(inLevel, self.x, self.y, self.width, self.height, 28, 24, 0, 3)
        if self.powerUp <> pwrCRAZY and (gfnTile_Pole(chkTiles1[6]) and not gfnTile_Pole(chkTiles1[7])):
            self.state = kON_POLE
            self.direction = sDIR_RIGHT
            self.x += 7 - (int(self.x % TILESIZE))
        elif self.powerUp <> pwrCRAZY and gfnTile_Pole(chkTiles1[8]):
            self.state = kON_POLE
            self.direction = sDIR_LEFT
            if int(self.x % 16) >= 8:
                self.x -= 1 + (int(self.x % TILESIZE) - 8)
            else:
                self.x -= int(self.x % TILESIZE) + 8 + 1
            
        # Jumping down through ONE WAY UP tiles
        elif (inKeys[K_RCTRL] or inKeys[K_LCTRL]):
            testTileX = int((self.x + (self.width / 2.0)) / TILESIZE)
            testTileY = int((self.y + self.height + 5) / TILESIZE)
            if not gfnTile_SolidFromBottom(inLevel.INFO[testTileX][testTileY]):
                self.vy = 0
                self.state = kFALLING
                self.y += 16

        # Otherwise Look down
        else:
        #elif self.lookTimer2 == 0:
            if (self.y - inLevel.mapY) > TILESIZE and int(inLevel.mapY) < (inLevel.height * TILESIZE) - inLevel.playHeight:
                self.lookTimer1 += self.timeElapsed
                if self.lookTimer1 > self.lookDelay:
                    self.lookOffsetY += self.lookSpeed * self.timeElapsed
                    self.lookDown = True
                    self.lookTimer2 = 0
                    
    elif self.lookDown == True:
        self.lookTimer1 = 0
        self.lookDown = False

    elif not inKeys[K_UP] and not inKeys[K_DOWN]:
        self.lookTimer1 = 0
            
    # Normal Key Input
    if self.state == kON_GROUND or self.state == kFALLING or self.state == kON_POLE:
        # Left & Right - only allow one at a time
        if inKeys[K_LEFT] and not (self.state == kON_GROUND and self.timerWeapon <> 0):
            self.lookUp, self.lookDown = False, False
            if self.powerUp <> pwrCRAZY:
                self.direction = sDIR_LEFT
                self.vx = -1
            else:
                self.direction = sDIR_RIGHT
                self.vx = -1
                
            if self.onPogo == False:
                self.moveAmountX = self.timeElapsed * self.RUN_SPEED[self.physics]
            else:
                #self.moveAmountX = self.timeElapsed * self.RUN_SPEED[self.physics] * self.POGO_SPEED
                # NEW POGO CODE
                self.newPogoCurrent -= (self.timeElapsed / self.newPogoHold) * self.newPogoMax * self.RUN_SPEED[self.physics]
                if self.newPogoCurrent < (-1 * self.newPogoMax * self.RUN_SPEED[self.physics]): self.newPogoCurrent = -1 * self.newPogoMax * self.RUN_SPEED[self.physics]
                if self.newPogoCurrent < 0:
                    self.vx = -1
                    self.direction = sDIR_LEFT
                elif self.newPogoCurrent > 0:
                    self.vx = 1
                    self.direction = sDIR_RIGHT
                else:
                    self.vx = 0

                self.moveAmountX = self.timeElapsed * abs(self.newPogoCurrent)
                self.message = self.newPogoCurrent
                
        elif inKeys[K_RIGHT] and not (self.state == kON_GROUND and self.timerWeapon <> 0):
            self.lookUp, self.lookDown = False, False
            if self.powerUp <> pwrCRAZY:
                self.direction = sDIR_RIGHT
                self.vx = -1
            else:
                self.direction = sDIR_LEFT
                self.vx = -1
                
            if self.onPogo == False:
                self.moveAmountX = self.timeElapsed * self.RUN_SPEED[self.physics]
            else:
                #self.moveAmountX = self.timeElapsed * self.RUN_SPEED[self.physics] * self.POGO_SPEED
                # NEW POGO CODE
                self.newPogoCurrent += (self.timeElapsed / self.newPogoHold) * self.newPogoMax * self.RUN_SPEED[self.physics]
                if self.newPogoCurrent > self.newPogoMax * self.RUN_SPEED[self.physics]: self.newPogoCurrent = self.newPogoMax * self.RUN_SPEED[self.physics]
                if self.newPogoCurrent < 0:
                    self.vx = -1
                    self.direction = sDIR_LEFT
                elif self.newPogoCurrent > 0:
                    self.vx = 1
                    self.direction = sDIR_RIGHT
                elif self.extraX == 0:
                    self.vx = 0
                self.moveAmountX = self.timeElapsed * abs(self.newPogoCurrent)
                self.message = self.newPogoCurrent
                
        elif self.onPogo == True:
            #if self.vx <> 0:
            #    self.vx = self.direction
            #self.moveAmountX = self.timeElapsed * self.POGO_IDLE_SPEED[self.physics]
            # NEW POGO CODE
            if self.newPogoCurrent < 0:
                self.vx = -1
                self.direction = sDIR_LEFT
            elif self.newPogoCurrent > 0:
                self.vx = 1
                self.direction = sDIR_RIGHT
            elif self.extraX == 0:
                self.vx = 0
            self.moveAmountX = self.timeElapsed * abs(self.newPogoCurrent)
                
        else:
            self.vx = 0

        # Jump
        if (inKeys[K_RCTRL] or inKeys[K_LCTRL]):
            self.lookUp, self.lookDown = False, False
            if self.state == kON_POLE and self.vy == 0:
                self.vy = self.JUMP_AMOUNT[self.physics] * 0.5
                self.state = kFALLING
                
                
            elif self.state == kON_GROUND or inGame.debug.jump == True:
                    
                # Initial jump/pogo velocities    
                if self.onPogo == False:
                    self.vy = self.JUMP_AMOUNT[self.physics]
                    self.moveAmountY = self.timeElapsed * self.vy
                    self.jumpTimer = 0.00001
                    self.state = kFALLING
                    if inGame.debug.jump == False: gfn_PlaySound(SFX_KEEN_JUMP)
                    
                elif self.onPogo == True:
                    self.vy = self.POGO_JUMP_AMOUNT[self.physics]
                    self.moveAmountY = self.timeElapsed * self.vy
                    self.jumpTimer = 0.00001
                    self.state = kFALLING
                    if inGame.debug.jump == False: gfn_PlaySound(SFX_KEEN_POGO)
                    
            else:
                # If CTRL is held down, increase until it hits the max (factor of .JUMPMAX)
                # The max will be reached after a set time (.jumpHold)
                if self.onPogo == False:
                    if self.jumpTimer <> 0:
                        self.jumpTimer += self.timeElapsed
                        if self.jumpTimer < self.jumpHold:
                            self.vy += self.timeElapsed * (self.JUMP_MAX / self.jumpHold)
                        else:
                            self.jumpTimer = 0
                elif self.onPogo == True:
                    if self.jumpTimer <> 0:
                        self.jumpTimer += self.timeElapsed
                        if self.jumpTimer < self.jumpHold:
                            self.vy += self.timeElapsed * (self.POGO_MAX / self.jumpHold)
                        else:
                            self.jumpTimer = 0             
            
        else:
            if self.state == kON_GROUND and self.onPogo == True:
                gfn_PlaySound(SFX_KEEN_POGO)
                self.vy = self.POGO_IDLE_JUMP[self.physics]
                self.moveAmountY = self.timeElapsed * self.vy
                self.state = kFALLING
                    

        # Ledge Grab
        # If near a ledge and pushing left/right, and falling down
        if self.state == kFALLING and self.vy >= 0 and (inKeys[K_LEFT] or inKeys[K_RIGHT]) and self.onPogo == False:

            if inKeys[K_LEFT] and self.ledgeTimer <=0:
                TileX1 = int((self.x - 16 + (self.width / 2.0)) / TILESIZE)
                TileY1 = int((self.y + 16) / TILESIZE)
                TileY2 = int((self.y + 17) / TILESIZE)
                if gfnTile_CanGrab(inLevel.INFO[TileX1][TileY2]) and not gfnTile_SolidFromRight(inLevel.INFO[TileX1][TileY1]):
                    self.state = kON_LEDGE
                    self.ledgeFrame = 0
                    self.x = (TileX1 * TILESIZE) + 2
                    
            if inKeys[K_RIGHT] and self.ledgeTimer <=0:
                TileX1 = int((self.x + 16 + (self.width / 2.0)) / TILESIZE)
                TileY1 = int((self.y + 16) / TILESIZE)
                TileY2 = int((self.y + 17) / TILESIZE)
                if gfnTile_CanGrab(inLevel.INFO[TileX1][TileY2]) and not gfnTile_SolidFromLeft(inLevel.INFO[TileX1][TileY1]):
                    self.state = kON_LEDGE
                    self.ledgeFrame = 0
                    self.x = ((TileX1-2) * TILESIZE) - 3

    # If on a ledge, halt movement and await user input (climb/fall off)
    #if self.onLedge == True:
    elif self.state == kON_LEDGE:
        
        self.vx = 0
        self.vy = 0

        self.ledgeDelayTimer += self.timeElapsed
            
        # If player pushes same direction or up, climb up
        if self.direction == sDIR_LEFT and (inKeys[K_UP] or inKeys[K_LEFT]) and self.ledgeTimer <= 0 and self.ledgeDelayTimer >= self.ledgeDelay:
            self.ledgeTimer = self.ledgeClimb
        elif self.direction == sDIR_RIGHT and (inKeys[K_UP] or inKeys[K_RIGHT]) and self.ledgeTimer <= 0 and self.ledgeDelayTimer >= self.ledgeDelay:
            self.ledgeTimer = self.ledgeClimb
            
        # If player pushes reverse direction, don't hang on
        elif self.ledgeTimer <= 0 and ((self.direction == sDIR_LEFT and inKeys[K_RIGHT]) or (self.direction == sDIR_RIGHT and inKeys[K_LEFT])):
            self.ledgeTimer = 0
            self.ledgeDelayTimer = 0
            self.state = kFALLING
                

    # Water Key Input
    elif self.state == kIN_WATER:
        # Adjustment if user is holding CTRL (swims faster)
        fastSwim = 1
        if (inKeys[K_RCTRL] or inKeys[K_LCTRL]):
            fastSwim = 1.5
            
        # Left/Right
        if inKeys[K_LEFT]:
            if self.powerUp <> pwrCRAZY:
                self.direction = sDIR_LEFT
                self.vx = -1
            else:
                self.direction = sDIR_RIGHT
                self.vx = -1

            self.moveAmountX = self.timeElapsed * self.SWIM_SPEED[self.physics] * fastSwim
                        
        elif inKeys[K_RIGHT]:
            if self.powerUp <> pwrCRAZY:
                self.direction = sDIR_RIGHT
                self.vx = -1
            else:
                self.direction = sDIR_LEFT
                self.vx = -1
            self.moveAmountX = self.timeElapsed * self.SWIM_SPEED[self.physics] * fastSwim

        else:
            self.vx = 0
            self.moveAmountX = 0
            
        # Up/Down
        if inKeys[K_UP]:
            self.vy -= self.timeElapsed * (self.SWIM_SPEED[self.physics] * 0.6)
            if self.vy < -1.5 * self.SWIM_GRAVITY: self.vy = -1.5 * self.SWIM_GRAVITY
            self.moveAmountY = -1 * self.timeElapsed * (self.SWIM_SPEED[self.physics] * 0.6) * fastSwim
                        
        elif inKeys[K_DOWN]:
            self.moveAmountY = self.timeElapsed * (self.SWIM_SPEED[self.physics] * 1.0) * fastSwim
        

# Update Position
def gfnKeen_updatePosition(self, t, inKeys, inLevel, inGame):
    
    # Push player left/right, in 1-pixel increments
    if self.vx <> 0 and (self.state == kON_GROUND or self.state == kFALLING or self.state == kIN_WATER):
        for i in range(int(abs(self.moveAmountX))):
            gfn_Push(self, inLevel, 1 * self.direction, 0)
        gfn_Push(self, inLevel, ((self.moveAmountX) % 1) * self.direction, 0)

    # GRAVITY:
            
    # Normal gravity - Push player up/down, in 1-pixel increments
    if self.state == kON_GROUND or self.state == kFALLING or self.state == kIN_WATER:

        if self.moveAmountY < 0:
            for i in range(int(abs(self.moveAmountY))):
                gfn_Push(self, inLevel, 0, -1)
            gfn_Push(self, inLevel, 0, (self.moveAmountY % -1))
        elif self.moveAmountY > 0:
            for i in range(int(abs(self.moveAmountY))):
                if self.state == kFALLING or self.state == kIN_WATER: gfn_Push(self, inLevel, 0, 1)
            if self.state == kFALLING or self.state == kIN_WATER: gfn_Push(self, inLevel, 0, self.moveAmountY % 1)
            
        if self.state == kFALLING:
            self.vy += self.timeElapsed * self.GRAVITY[self.sprite]
            if self.vy > 400: self.vy = 400
            
        elif self.state == kIN_WATER:
            self.vy += self.timeElapsed * self.SWIM_GRAVITY
            if self.vy > self.SWIM_GRAVITY and not inKeys[K_DOWN]: self.vy = self.SWIM_GRAVITY
        else:
            self.vy = 0
            
        self.moveAmountY = self.timeElapsed * self.vy

    # Pole climbing (not subject to gravity)
    elif self.state == kON_POLE:
        self.vy = 0
        if inKeys[K_DOWN]:
            self.y += self.timeElapsed * self.POLE_DOWN
            self.vy = 1
            chkTiles1 = gfn_GetInfoTiles(inLevel, self.x, self.y, self.width, self.height, 0, 16, 0, 20)
            if not gfnTile_Pole(chkTiles1[8]):
                self.state = kFALLING
                    
        elif inKeys[K_UP]:
            chkTiles1 = gfn_GetInfoTiles(inLevel, self.x, self.y, self.width, self.height, 0, 16, 0, 0)
            if gfnTile_Pole(chkTiles1[5]):
                self.y -= self.timeElapsed * self.POLE_UP
                self.vy = -1
            else:
                self.vy = 0
        else:
            self.vy = 0

    # Dying
    elif self.state == kDYING:
        self.x += self.timeElapsed * self.RUN_SPEED[0]
        self.vy += self.timeElapsed * self.GRAVITY[0]
        self.y += self.timeElapsed * self.vy
        if self.y - inLevel.mapY > inLevel.playHeight:
            pygame.time.wait(500)
            if self.lives >= 1:
                # Reload Level
                self.hasKey = [False, False, False, False, False, False]
                inGame.state = STATE_FADEOUT_KILL
                inGame.fadeTimer = inGame.fadeTime * 2
            else:
                inGame.state = STATE_FADEOUT_GAMEOVER
                inGame.fadeTimer = inGame.fadeTime * 2
#_______________________________________________________________________________________
# Animation & Frame Selection
# These algorithms will check various things (on ground, in water, using pogo, velocities, etc)
#   and decide which Keen frame to use. The various states (shoes, god, crazy, EGA) will also be
#   taken into account.
def gfnKeen_selectFrame(self, t, inKeys, inLevel):

        # Check Swim first
        if self.state == kIN_WATER:
            # Set an offset if Keen has any harpoons
            if self.weapon[W_HARPOON].ammo > 0: offset = 4
            else: offset = 0

            if self.timerWeapon == 0:
                # Swimming frames
                if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_SWIM_LEFT + self.frame + offset]
                elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_SWIM_RIGHT + self.frame + offset]

                if t - self.last_update > 3 * 1000 / self.delay[self.sprite]:
                    self.frame += 1
                    if self.frame >= 2: self.frame = 0
                    self.last_update = t
                    self.idleTimer = 0
            else:
                if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_SHOOT_HARPOON]
                elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_SHOOT_HARPOON + 1]                

        # Next, crazy spew
        elif self.state == kSPEW:
            delayExtra = 1
            if self.frame == 10: delayExtra = 6
            if t - self.last_update > delayExtra * 1000 / self.delay[0]:
                self.frame += 1
                self.image = self.imgSprites[self.sprite][self.SPRITE_SPEW + self.frame]
                self.last_update = t
                self.idleTimer = 0
                if self.frame >= self.SPRITE_SPEW_MAX:
                    self.frame = 1
                    self.sprite = kSPRITE_NORMAL
                    self.physics = physNORMAL
                    self.state = kON_GROUND
                    self.powerUp = pwrNONE
                
        # Look Up/Down
        elif self.lookUp == True:
            self.image = self.imgSprites[self.sprite][self.SPRITE_LOOK_UP]
            self.idleTimer = 0
        elif self.lookDown == True:
            self.idleTimer = 0
            if self.lookTimer1 / self.lookDelay < 1.1:
                self.image = self.imgSprites[self.sprite][self.SPRITE_LOOK_DOWN]
            else:
                self.image = self.imgSprites[self.sprite][self.SPRITE_LOOK_DOWN + 1]

        # Pole
        elif self.state == kON_POLE:

            if self.timerWeapon <> 0:
                if self.currentWeapon == W_RAYGUN or self.currentWeapon == W_NEURAL: offset = 2
                else: offset = 0
                spriteIndex = self.SPRITE_SHOOT_PLUTEZARP + ((self.currentWeapon - offset) * 13)

                if self.currentWeapon <> W_BLOWGUN and self.currentWeapon <> W_PLUTEZARP and self.shootUp == True: offset = 2
                elif self.currentWeapon <> W_BLOWGUN and self.currentWeapon <> W_PLUTEZARP and self.shootDown == True: offset = 4
                    
                if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][spriteIndex + 7 + offset]
                elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][spriteIndex + 7 + 1 + offset]

            elif self.vy > 0:
                if t - self.last_update > 1000 / self.delay[0]:
                    self.frame += 1
                    if self.frame >= 4: self.frame = 0
                    self.image = self.imgSprites[self.sprite][self.SPRITE_POLE_DOWN + self.frame]
                    self.last_update = t

            elif self.vy < 0:
                if t - self.last_update > 1000 / self.delay[0]:
                    self.frame += 1
                    if self.frame >= 3: self.frame = 0
                    if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_POLE_LEFT + self.frame]
                    elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_POLE_RIGHT + self.frame]
                    self.last_update = t
                    
            else:
                if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_POLE_LEFT]
                elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_POLE_RIGHT]

        # Door
        elif self.state == kIN_DOOR:
                if t - self.last_update > 1.5 * 1000 / self.delay[0]:
                    self.frame += 1
                    if self.frame >= 5:
                        self.frame = 0
                        self.x = self.doorToX
                        self.y = self.doorToY
                        self.canHurt = self.HURT    # Make invinsible incase of enemies
                        
                        # Reset door stuff
                        self.inDoor = False
                        self.state = kFALLING
                        self.vy = 0
                        self.doorNum = 0
                        self.doorID = 0
                        self.doorToX = 0
                        self.doorToY = 0

                        # Snap camera
                        inLevel.snapCamera(self)
                        
                    self.image = self.imgSprites[self.sprite][self.SPRITE_DOOR + self.frame]
                    self.last_update = t

        # Teleport
        elif self.state == kTELEPORT:
                if t - self.last_update > 1000 / self.delay[0]:
                    self.frame += 1
                    if self.frame >= 11:
                        self.frame = 0
                        self.x = self.doorToX
                        self.y = self.doorToY
                        
                        # Reset door stuff
                        self.inDoor = False
                        self.state = kFALLING
                        self.doorNum = 0
                        self.doorID = 0
                        self.doorToX = 0
                        self.doorToY = 0
                        
                    self.image = self.imgSprites[self.sprite][self.SPRITE_TELEPORT + self.frame]
                    self.last_update = t

                                        
        # Jumping & Pogo
        elif self.state == kFALLING:
            self.idleTimer = 0
            # Normal Jump
            if self.onPogo == False:
              
                if self.invShield > 0:
                    if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_SHIELD + 2]
                    elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_SHIELD + 3]
                    
                elif self.timerWeapon == 0:
                    if abs(self.vy) < abs(self.JUMP_AMOUNT[self.sprite]) / 5.0:
                        if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_JUMP_LEFT + 1]
                        elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_JUMP_RIGHT + 1]

                    # Up
                    elif self.vy < 0:
                        if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_JUMP_LEFT]
                        elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_JUMP_RIGHT]
                        
                    # Down
                    elif self.vy >= 0:
                        if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_JUMP_LEFT + 2]
                        elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_JUMP_RIGHT + 2]

                else:
                    if self.currentWeapon == W_RAYGUN or self.currentWeapon == W_NEURAL: offset = 2
                    else: offset = 0  
                    spriteIndex = self.SPRITE_SHOOT_PLUTEZARP + ((self.currentWeapon - offset) * 13)

                    if self.currentWeapon <> W_BLOWGUN and self.currentWeapon <> W_PLUTEZARP and self.shootUp == True:
                        self.image = self.imgSprites[self.sprite][spriteIndex + 5]
                    elif self.currentWeapon <> W_BLOWGUN and self.currentWeapon <> W_PLUTEZARP and self.shootDown == True:
                        self.image = self.imgSprites[self.sprite][spriteIndex + 6]
                    elif self.currentWeapon == W_BLOWGUN:
                        if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_SHOOT_BLOWGUN + 3]
                        elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_SHOOT_BLOWGUN + 3 + 1]
                    else:

                        if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][spriteIndex + 3]
                        elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][spriteIndex + 3 + 1]
                                
                # Stationary

                    
            # Pogo Jump
            # This sets the frame to the crouched Pogo while Keen is rising up
            # Once it is almost at the top, it will switch to the normal Pogo frame
            elif self.onPogo == True:
                if self.direction == sDIR_LEFT:
                    if self.vy < -120 or ((inKeys[K_RCTRL] or inKeys[K_LCTRL]) and self.vy < 0):
                        self.image = self.imgSprites[self.sprite][self.SPRITE_POGO_LEFT + 1]
                    else:
                        self.image = self.imgSprites[self.sprite][self.SPRITE_POGO_LEFT]
                elif self.direction == sDIR_RIGHT:
                    if self.vy < -120 or ((inKeys[K_RCTRL] or inKeys[K_LCTRL]) and self.vy < 0):
                        self.image = self.imgSprites[self.sprite][self.SPRITE_POGO_RIGHT + 1]
                    else:
                        self.image = self.imgSprites[self.sprite][self.SPRITE_POGO_RIGHT]

        # Ledge grab, stationary
        elif self.state == kON_LEDGE:
            if self.ledgeTimer <=0:
                if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_LEDGE_LEFT + self.ledgeFrame]
                elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_LEDGE_RIGHT + self.ledgeFrame]
                self.last_update = self.ledgeClimb

                
            elif self.ledgeTimer > 0:
                self.ledgeDelayTimer = 0
                self.ledgeTimer -= self.timeElapsed

                if (self.last_update - self.ledgeTimer) > (self.ledgeClimb / 6.0):
                    self.ledgeFrame += 1
                    self.last_update = self.ledgeTimer

                    # When the climb begins, offset the (x,y) position
                    if self.ledgeFrame == 1:
                        self.y -= 18
                
                    elif self.ledgeFrame == 5:
                            self.x += self.direction * 16
                            self.y -= 12
                            self.state = kON_GROUND
                            self.ledgeTimer = 0
                            self.lookOffsetX = 16 * self.direction * -1
                            #self.lookTimer2 = 0
                        
                    if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_LEDGE_LEFT + self.ledgeFrame]
                    elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_LEDGE_RIGHT + self.ledgeFrame]

                    # If just off a ledge, set to the stationary frame
                    if self.state == kON_GROUND:
                        if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_RUN_LEFT]
                        elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_RUN_RIGHT]                    
                    

		
        # Walking
        elif self.state == kON_GROUND:

            
            if self.onPogo == False:

                # Switch
                if self.touchSwitch == True:
                    self.image = self.imgSprites[self.sprite][self.SPRITE_DOOR]
                    if t - self.last_update > 2 * 1000 / self.delay[self.sprite]:
                        self.touchSwitch = False
                    
                # Normal Walk
                elif self.vx <> 0 and (inKeys[K_LEFT] or inKeys[K_RIGHT]):
                    if t - self.last_update > 1000 / self.delay[self.sprite]:
                        self.frame += 1
                        if self.frame >= 5: self.frame = 1
                        if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_RUN_LEFT + self.frame]
                        elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_RUN_RIGHT + self.frame]
                        self.last_update = t
                        self.idleTimer = 0

                else:
                    self.idleTimer += self.timeElapsed
                    # Idle frames
                    if self.idleTimer > self.idleMax and self.idleTimer < self.idleMax + self.idleLookTime:
                        self.image = self.imgSprites[self.sprite][self.SPRITE_LOOK_UP]
                    elif self.idleTimer > self.idleMax * 1.5 and self.idleTimer < (self.idleMax * 1.5) + self.idleShrugTime:
                        self.image = self.imgSprites[self.sprite][self.SPRITE_SHRUG]
                            
                    # Standing still
                    else:
                        if self.invShield > 0:
                            if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_SHIELD]
                            elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_SHIELD + 1]
                            
                        elif self.onPlatform == True and self.timerWeapon == 0:
                            self.image = self.imgSprites[self.sprite][self.SPRITE_PLATFORM]
                            
                        elif self.timerWeapon == 0:
                            if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_RUN_LEFT]
                            elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_RUN_RIGHT]
                            self.frame = 0
                        else:
                            if self.currentWeapon == W_RAYGUN or self.currentWeapon == W_NEURAL: offset = 2
                            else: offset = 0
                            spriteIndex = self.SPRITE_SHOOT_PLUTEZARP + ((self.currentWeapon - offset) * 13)
                            
                            if self.currentWeapon <> W_BLOWGUN and self.currentWeapon <> W_PLUTEZARP and self.shootUp == True:
                                self.image = self.imgSprites[self.sprite][spriteIndex + 2]
                            elif self.currentWeapon == W_BLOWGUN:
                                if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][self.SPRITE_SHOOT_BLOWGUN]
                                elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][self.SPRITE_SHOOT_BLOWGUN + 1]
                            else:

                                if self.direction == sDIR_LEFT: self.image = self.imgSprites[self.sprite][spriteIndex]
                                elif self.direction == sDIR_RIGHT: self.image = self.imgSprites[self.sprite][spriteIndex + 1]
                                
                    if self.idleTimer >= (self.idleMax * 1.5) + self.idleShrugTime and self.sprite <> kSPRITE_CRAZY:
                        self.idleTimer = 0
                    elif self.idleTimer >= (self.idleMax * 3) + 5 and self.sprite == kSPRITE_CRAZY:
                        self.idleTimer = 0
                        
        # Dead
        elif self.state == kDYING:
            self.image = self.imgSprites[self.sprite][self.frame]

        # Set a blank sprite to flash if Keen is invincible
        if self.state <> kDYING and self.canHurt > 0 and self.onPlatform == False:
            tempTiming = (t % 1000) % 200
            if tempTiming < 100:
                self.image = self.imgSprites[0][10]
                #self.image.set_alpha(50)
            #else:
                #self.image.set_alpha(255)
                        
#________________________________________________________________________________________________
# This function will attempt to push the player by at most 1 pixel to the LEFT, RIGHT, UP or DOWN
# Only one direction will be processed at a time
# Depending on the tile it encounters, it may or may not be successful
def gfn_Push(self, inLevel, inAmountX, inAmountY):

    # First extract the INFO layer from the Level
    # Also extract the width & height for edge-collision checking
    layerInfo = inLevel.INFO
    levelWidth = inLevel.width
    levelHeight = inLevel.height
    chkTiles1 = []
    chkTiles2 = []

    #______________________
    # RIGHT
    if inAmountX > 0:

        # Push player RIGHT if more than one TILESIZE from right edge
        if self.x + self.width < (levelWidth * TILESIZE) - 1:
            self.x += inAmountX
            self.updateSubRect()
            #self.message = "> Right"

        # !Check WATER first
        chkTiles1 = gfn_GetInfoTiles(inLevel, self.x, self.y, self.width, self.height, 0, 0, 0, 4)
        if gfnTile_Water(chkTiles1[7]):
            if self.state == kON_GROUND:
                self.state = kIN_WATER
                self.makeSplash = True
                self.frame = 0
                self.vy = 0
                self.onPogo = False
                
                # Change weapon to harpoon (if ammo), or nill (if no harpoon)
                # Saves the old weapon so it reverts back to that one if Keen goes out of the water
                if self.weapon[W_HARPOON].ammo > 0:
                    self.oldWeapon = self.currentWeapon
                    self.currentWeapon = W_HARPOON
                else:
                    self.oldWeapon = self.currentWeapon
                    self.currentWeapon = -1
                    
        elif self.state == kIN_WATER:
            self.state = kON_GROUND
            self.currentWeapon = self.oldWeapon
            
        # 1. Check if we walk onto a slope
        TileX_Slope = int(self.subRect.midbottom[0] / TILESIZE)
        TileY_Slope = int(self.subRect.midbottom[1] / TILESIZE)

        yorpy = False         
        # Check for solid enemies (e.g. YORP)
        enemyCollide = pygame.sprite.spritecollide(self, inLevel.sprite_Enemies, False, pygame.sprite.collide_rect)
        for possibleCollide in enemyCollide:
            if pygame.sprite.collide_mask(self, possibleCollide):
                if gfn_IsPushEnemy(possibleCollide.id) and possibleCollide.state <> ENEMY_STATE_DIE:
                    if (self.x + (self.width / 2.0) < possibleCollide.x + (possibleCollide.width / 2.0)) or possibleCollide.id == SPRITE_DRAGONFLY:
                        self.x -= inAmountX
                        yorpy = True


        if yorpy == False:
            # Up slopes
            if gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                if self.state == kON_GROUND or self.state == kIN_WATER:
                    # 1. FAST CLIMB
                    #self.y -= inAmountX
                    
                    # 2. SLOW CLIMB
                    #self.y -= inAmountX / 2.0
                    #self.x -= inAmountX / 2.0

                    # 3. MEDIUM CLIMB
                    self.y -= 3 * inAmountX / 4.0
                    self.x -= inAmountX / 4.0                
                
            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                if self.state == kON_GROUND or self.state == kIN_WATER:
                    self.y -= inAmountX / 2.0

            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope-1]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                if self.state == kON_GROUND or self.state == kIN_WATER:
                    self.y -= inAmountX / 2.0
                
            # Down slopes
            elif gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                if self.state == kON_GROUND:
                    self.y += inAmountX 
                
            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                if self.state == kON_GROUND:
                    self.y += inAmountX / 2.0

            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope+1]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                if self.state == kON_GROUND:
                    self.y += inAmountX / 2.0

                
            else:
                
                # 2. Check if we hit a wall
                # Pixel coordinates - the left and right bounds of the Rect
                TileYpix = self.subRect[1] - (self.subRect[1] % TILESIZE) + 1
                TestEnd = self.subRect[1] + self.subRect.height - 1
                
                # Map coordinates
                TileX = int((self.subRect[0] + self.subRect.width) / TILESIZE)
                TileY = int(TileYpix / TILESIZE)

                while TileYpix <= TestEnd:
                    if gfnTile_SolidFromLeft(inLevel.INFO[TileX][TileY]) and not gfnTile_UpRight45(inLevel.INFO[TileX-1][TileY]):
                        if not gfnTile_UpRight30_1(inLevel.INFO[TileX-1][TileY]) and not gfnTile_UpRight30_2(inLevel.INFO[TileX-1][TileY]):
                            self.x = (TileX * TILESIZE) - self.subRect.width - self.rectOffsetX - 1
                            self.newPogoCurrent = 0
                            
                    TileY +=1
                    TileYpix += TILESIZE

                # 3. Check if we should fall
                fall = True
                TileXpix = self.subRect[0] - (self.subRect[0] % TILESIZE) + 4
                TestEnd = self.subRect[0] + self.subRect.width - 2
                
                # Map coordinates
                TileY = int((self.subRect[1] + self.subRect.height + 2) / TILESIZE)
                TileX = int(TileXpix / TILESIZE)

                while TileXpix <= TestEnd:
                    if gfnTile_SolidFromTop(inLevel.INFO[TileX][TileY]):
                        fall = False
                        
                    TileX +=1
                    TileXpix += TILESIZE

                if fall == True and self.state == kON_GROUND and self.onPlatform == False:
                    self.vy = 0
                    self.state = kFALLING
                    
                #if self.state == kON_GROUND and self.y > (TileY * TILESIZE) - self.subRect.height - self.rectOffsetY - 1:
                #    self.y = (TileY * TILESIZE) - self.subRect.height - self.rectOffsetY - 1
                
    #______________________
    # LEFT
    elif inAmountX < 0:

        # Push player LEFT if more than one TILESIZE from left edge
        if self.x > 1:
            self.x += inAmountX
            self.updateSubRect()
            #self.message = "< Left"

        # !Check WATER first
        chkTiles1 = gfn_GetInfoTiles(inLevel, self.x, self.y, self.width, self.height, 0, 0, 0, 4)
        if gfnTile_Water(chkTiles1[7]):
            if self.state == kON_GROUND:
                self.state = kIN_WATER
                self.makeSplash = True
                self.frame = 0
                self.vy = 0
                self.onPogo = False

                # Change weapon to harpoon (if ammo), or nill (if no harpoon)
                # Saves the old weapon so it reverts back to that one if Keen goes out of the water
                if self.weapon[W_HARPOON].ammo > 0:
                    self.oldWeapon = self.currentWeapon
                    self.currentWeapon = W_HARPOON
                else:
                    self.oldWeapon = self.currentWeapon
                    self.currentWeapon = -1
                    
        elif self.state == kIN_WATER:
            self.state = kON_GROUND
            self.currentWeapon = self.oldWeapon


        # 1. Check if we walk onto a slope
        TileX_Slope = int(self.subRect.midbottom[0] / TILESIZE)
        TileY_Slope = int(self.subRect.midbottom[1] / TILESIZE)

        yorpy = False
        # Check for solid enemies (e.g. YORP)
        enemyCollide = pygame.sprite.spritecollide(self, inLevel.sprite_Enemies, False, pygame.sprite.collide_rect)
        for possibleCollide in enemyCollide:
            if pygame.sprite.collide_mask(self, possibleCollide):
                if gfn_IsPushEnemy(possibleCollide.id) and possibleCollide.state <> ENEMY_STATE_DIE:
                    if (self.x + (self.width / 2.0) > possibleCollide.x + (possibleCollide.width / 2.0)) or possibleCollide.id == SPRITE_DRAGONFLY:
                        self.x -= inAmountX
                        yorpy = True
        if yorpy == False:
            # Up slopes
            if gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight45(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                if self.state == kON_GROUND or self.state == kIN_WATER:
                    self.y += 3 * inAmountX / 4.0
                    self.x -= inAmountX / 4.0
                
            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                if self.state == kON_GROUND or self.state == kIN_WATER:
                    self.y += inAmountX / 2.0

            elif gfnTile_DownRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope-1]) or gfnTile_DownRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope-1]):
                if self.state == kON_GROUND or self.state == kIN_WATER:
                    self.y += inAmountX / 2.0
                
            # Down slopes
            elif gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight45(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                if self.state == kON_GROUND:
                    self.y -= inAmountX
                
            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope]):
                if self.state == kON_GROUND:
                    self.y -= inAmountX / 2.0

            elif gfnTile_UpRight30_1(inLevel.INFO[TileX_Slope][TileY_Slope+1]) or gfnTile_UpRight30_2(inLevel.INFO[TileX_Slope][TileY_Slope+1]):
                if self.state == kON_GROUND:
                    self.y -= inAmountX / 2.0

                
            else:

                # Pixel coordinates - the left and right bounds of the Rect
                TileYpix = self.subRect[1] - (self.subRect[1] % TILESIZE) + 1
                TestEnd = self.subRect[1] + self.subRect.height - 1
                
                # Map coordinates
                TileX = int(self.subRect[0] / TILESIZE)
                TileY = int(TileYpix / TILESIZE)

                while TileYpix <= TestEnd:
                    if gfnTile_SolidFromRight(inLevel.INFO[TileX][TileY]) and not gfnTile_DownRight45(inLevel.INFO[TileX+1][TileY]):
                        if not gfnTile_UpRight45(inLevel.INFO[TileX+1][TileY-1]):
                            if not gfnTile_DownRight30_1(inLevel.INFO[TileX+1][TileY-1]) and not gfnTile_DownRight30_2(inLevel.INFO[TileX+1][TileY-1]):
                                self.x = ((TileX + 1) * TILESIZE) - self.rectOffsetX
                                self.newPogoCurrent = 0
                    
                    TileY +=1
                    TileYpix += TILESIZE

       
                # Test to see if we've walking off a cliff
                fall = True
                TileXpix = self.subRect[0] - (self.subRect[0] % TILESIZE) + 2
                TestEnd = self.subRect[0] + self.subRect.width - 4
                
                # Map coordinates
                TileY = int((self.subRect[1] + self.subRect.height + 2) / TILESIZE)
                TileX = int(TileXpix / TILESIZE)

                while TileXpix <= TestEnd:
                    if gfnTile_SolidFromTop(inLevel.INFO[TileX][TileY]):
                        fall = False
                       
                    TileX +=1
                    TileXpix += TILESIZE

                if fall == True and self.state == kON_GROUND and self.onPlatform == False:
                    self.vy = 0
                    self.state = kFALLING

                # Snaps Keen to the ground if he is just below it
                #if self.state == kON_GROUND and self.y > (TileY * TILESIZE) - self.subRect.height - self.rectOffsetY - 1:
                #    self.y = (TileY * TILESIZE) - self.subRect.height - self.rectOffsetY - 1  


    #______________________
    # DOWN
    elif inAmountY > 0:

        # Push player DOWN if less than one TILESIZE from the bottom
        if self.y < (levelHeight * TILESIZE) - self.height - TILESIZE:
            self.y += inAmountY
            self.updateSubRect()
            #self.message = "V Down"
            
           
        # Check WATER first
        chkTiles1 = gfn_GetInfoTiles(inLevel, self.x, self.y, self.width, self.height, 0, 0, 0, 8)
        if gfnTile_Water(chkTiles1[7]):
            if self.state == kFALLING:
                self.state = kIN_WATER
                self.makeSplash = True
                self.frame = 0
                self.vy = 0
                self.onPogo = False

                # Change weapon to harpoon (if ammo), or nill (if no harpoon)
                # Saves the old weapon so it reverts back to that one if Keen goes out of the water
                if self.weapon[W_HARPOON].ammo > 0:
                    self.oldWeapon = self.currentWeapon
                    self.currentWeapon = W_HARPOON
                else:
                    self.oldWeapon = self.currentWeapon
                    self.currentWeapon = -1


        # Check for landing on slopes first
        TileX = int(self.subRect.midbottom[0] / TILESIZE)        
        TileY = int((self.subRect[1] + self.subRect.height) / TILESIZE)
        if gfnTile_UpRight45(inLevel.INFO[TileX][TileY]):
            if (self.subRect[1] + self.subRect.height) % TILESIZE > TILESIZE - (self.subRect.midbottom[0] % TILESIZE):
                self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - (TILESIZE - (self.subRect.midbottom[0] % TILESIZE))
                self.vy = 0
                if self.state <> kIN_WATER: self.state = kON_GROUND
                
        elif gfnTile_UpRight30_1(inLevel.INFO[TileX][TileY]):
            if (self.subRect[1] + self.subRect.height) % TILESIZE > TILESIZE - ((self.subRect.midbottom[0] % TILESIZE) * 0.5):
                self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - (TILESIZE - ((self.subRect.midbottom[0] % TILESIZE) * 0.5))
                self.vy = 0
                if self.state <> kIN_WATER: self.state = kON_GROUND

        elif gfnTile_UpRight30_2(inLevel.INFO[TileX][TileY]):
            if (self.subRect[1] + self.subRect.height) % TILESIZE > TILESIZE - ((self.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5:
                self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - (TILESIZE - ((self.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5)
                self.vy = 0
                if self.state <> kIN_WATER: self.state = kON_GROUND

        elif gfnTile_DownRight45(inLevel.INFO[TileX][TileY]):
            if (self.subRect[1] + self.subRect.height) % TILESIZE >  self.subRect.midbottom[0] % TILESIZE:
                self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - (self.subRect.midbottom[0] % TILESIZE)
                self.vy = 0
                if self.state <> kIN_WATER: self.state = kON_GROUND
                
        elif gfnTile_DownRight30_1(inLevel.INFO[TileX][TileY]):
            if (self.subRect[1] + self.subRect.height) % TILESIZE >  (self.subRect.midbottom[0] % TILESIZE) * 0.5:
                self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - ((self.subRect.midbottom[0] % TILESIZE) * 0.5)
                self.vy = 0
                if self.state <> kIN_WATER: self.state = kON_GROUND

        elif gfnTile_DownRight30_2(inLevel.INFO[TileX][TileY]):
            if (self.subRect[1] + self.subRect.height) % TILESIZE >  ((self.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5:
                self.y -= ((self.subRect[1] + self.subRect.height) % TILESIZE) - (((self.subRect.midbottom[0] % TILESIZE) + TILESIZE) * 0.5)
                self.vy = 0
                if self.state <> kIN_WATER: self.state = kON_GROUND
                
        # If no slope, scan for a solid  
        else:
            # Pixel coordinates - the left and right bounds of the Rect
            TileXpix = self.subRect[0] - (self.subRect[0] % TILESIZE) + 2
            TestEnd = self.subRect[0] + self.subRect.width - 2
            
            # Map coordinates
            #TileY = int((self.subRect[1] + self.subRect.height) / TILESIZE)
            TileY = int((self.subRect[1] + self.subRect.height + 1) / TILESIZE)
            TileX = int(TileXpix / TILESIZE)

            while TileXpix <= TestEnd:
                if gfnTile_SolidFromTop(inLevel.INFO[TileX][TileY]):
                    self.y = (TileY * TILESIZE) - self.subRect.height - self.rectOffsetY - 1
                    if self.state == kFALLING: self.state = kON_GROUND
                    self.vy = 0
                    
                TileX +=1
                TileXpix += TILESIZE
            
    #______________________
    # UP
    elif inAmountY < 0:

        # Push player UP if more than one TILESIZE from the top
        if self.y + self.subRect[1] > TILESIZE:
            self.y += inAmountY
            self.updateSubRect()
            #self.message = "^ in Air"
            
        # Check WATER first
        chkTiles1 = gfn_GetInfoTiles(inLevel, self.x, self.y, self.width, self.height, 16, 16, 16, 4)
        if self.state == kIN_WATER:
            if not gfnTile_Water(chkTiles1[7]):
                self.vy = self.JUMP_AMOUNT[self.sprite]
                self.state = kFALLING
                self.currentWeapon = self.oldWeapon
                
        # Pixel coordinates - the left and right bounds of the Rect
        TileXpix = self.subRect[0] - (self.subRect[0] % TILESIZE)
        TestEnd = self.subRect[0] + self.subRect.width

        # Map coordinates
        TileY = int(self.subRect[1] / TILESIZE)
        TileX = int(TileXpix / TILESIZE)

        while TileXpix <= TestEnd:
            if gfnTile_SolidFromBottom(inLevel.INFO[TileX][TileY]):
                #self.y = (TileY * TILESIZE)
                self.vy = 0
                self.jumpTimer = 0
                self.y -= inAmountY
                
            TileX +=1
            TileXpix += TILESIZE

            
    # Update collision Rect
    self.updateSubRect()




    
#________________________________________________________________________________________________
# This function will take in a gcls_Level object, and the position to check
# The width, height and buffers determine the limits
def gfn_GetInfoTiles(inLevel, inX, inY, inW, inH, leftBuffer, rightBuffer, topBuffer, bottomBuffer):
    layerInfo = inLevel.INFO
    checkTiles = []

    # Check the 9 positions
    checkTiles.append(layerInfo[int((inX+leftBuffer) / TILESIZE)][int((inY+topBuffer) / TILESIZE)])
    checkTiles.append(layerInfo[int((inX + (inW/2))/ TILESIZE)][int((inY+topBuffer) / TILESIZE)])
    checkTiles.append(layerInfo[int((inX-rightBuffer + inW) / TILESIZE)][int((inY+topBuffer) / TILESIZE)])
        
    checkTiles.append(layerInfo[int((inX+leftBuffer) / TILESIZE)][int((inY + (inH/2)) / TILESIZE)])
    checkTiles.append(layerInfo[int((inX + (inW/2))/ TILESIZE)][int((inY + (inH/2)) / TILESIZE)])
    checkTiles.append(layerInfo[int((inX-rightBuffer + inW) / TILESIZE)][int((inY + (inH/2)) / TILESIZE)])

    checkTiles.append(layerInfo[int((inX+leftBuffer) / TILESIZE)][int((inY-bottomBuffer + inH) / TILESIZE)])
    checkTiles.append(layerInfo[int((inX + (inW/2))/ TILESIZE)][int((inY-bottomBuffer + inH) / TILESIZE)])
    checkTiles.append(layerInfo[int((inX-rightBuffer + inW) / TILESIZE)][int((inY-bottomBuffer + inH) / TILESIZE)])
    
    # Return the result
    return checkTiles
