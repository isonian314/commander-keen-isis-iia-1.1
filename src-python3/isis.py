# -*- coding: cp1252 -*-
# Commander Keen: The Mystery of Isis IIa
# Geoff Sims, September 2010
#
# __________________________________________________________
# Initialisation

# Imports - standard
import pygame, os, sys
from pygame.locals import *
from isis_zip import *
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
displayWidth = 320
displayHeight = 200


icon = pygame.image.load(os.path.join("data", "icon.png"))
icon.set_colorkey(icon.get_at((0,0)))
pygame.display.set_icon(icon)
pygame.display.set_caption("Commander Keen - The Mystery of Isis IIa")

srfcScreen = pygame.display.set_mode((displayWidth*2, displayHeight*2))
#srfcScreen = pygame.display.set_mode((displayWidth*2, displayHeight*2), FULLSCREEN)


srfcLoading = pygame.image.load(gfn_Zip("cutscene-loading.png")).convert()
srfcLoading_2x = pygame.Surface((displayWidth*2, displayHeight*2))
pygame.transform.scale(srfcLoading, (displayWidth * 2, displayHeight * 2), srfcLoading_2x)
srfcScreen.blit(srfcLoading_2x, (0,0))
pygame.display.update()
    
# Imports - custom modules
from isis_draw import *
from isis_menu import *
from isis_tmx64 import *
from isis_level import *
from isis_keen import *
from isis_tiles import *
from isis_tiles_anim import *
from isis_particle import *
from isis_hud import *
from isis_items import *
from isis_enemies import *
from isis_doors import *
from isis_cutscenes import *
from isis_weather import *
from isis_music import *
from isis_font import *

# Initialise
debug = True
Game = gcls_Game()
Menu = gcls_Menu()
srfcBuffer = pygame.Surface((displayWidth, displayHeight))
srfcBuffer_2x = pygame.Surface((displayWidth*2, displayHeight*2))

#__________________________________________
    
particles = []
num_particles = 0

# __________________________________________________________
# Main Loop
Clock = pygame.time.Clock()
old_fps = 0

newTimer = pygame.time.get_ticks()
oldTimer = 0


Keen = gcls_Keen()
Level = gcls_Level()
Game.fadeTimer = Game.fadeTime

done = False
Clock.tick()
while not done:

    # Tick the clock
    # The clock gives us FPS and TimeElapsed
    Clock.tick()
    # Update timer for animation & other stuff
    newTime = pygame.time.get_ticks()
    timeElapsed = Clock.get_time() / 1000.0
        
    # Menu Handling
    if Game.state == STATE_MENU:
        Menu.active = True
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            if event.type == KEYDOWN:
                done = gfn_MenuInput(Menu, event.key, timeElapsed, Game, Keen)
               
        if Menu.menuType == MENU_DISPLAYTEXT: gfn_MenuInput2(Menu, timeElapsed)      
        Menu.update(Game)
        srfcBuffer.blit(Menu.srfcCurrent, (0,0))
        if Menu.active == False:
            Game.srfcCutScenes = gfnLoad_Splice(320, 200, gfn_Zip(Game.CSNames[Game.level_ID]), 0, 0)
            Game.state = STATE_CUTSCENE
            Game.fadeTime
                
    # Cut Scene Handling
    elif Game.state == STATE_CUTSCENE:
        # Get Input - ESC skips, any other key progresses sequence
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if Game.level_ID != 0:
                        # TO EXIT
                        Game.state = STATE_MENU
                        Game.cutScene_ID = 0
                        # TO SKIP
                        #Game.fadeOut = True
                        #Game.fadeTimer = Game.fadeTime
                    else: Game.state = STATE_MENU
                else:
                    if not Game.fadeOut and not Game.fadeIn:
                        if Game.cutScene_ID < len(Game.srfcCutScenes) - 1:
                            Game.cutScene_ID += 1
                        else:
                            Game.fadeOut = True
                            Game.fadeTimer = Game.fadeTime

                    elif Game.fadeIn or Game.fadeOut:
                        Game.fadeTimer = 0

        # Print the current CutScene
        srfcBuffer.fill((0,0,0))
        srfcBuffer.blit(Game.srfcCutScenes[Game.cutScene_ID], (0,0))
       
        if Game.fadeIn:
            Game.srfcCutScenes[Game.cutScene_ID].set_alpha(255 - (255 * (Game.fadeTimer / Game.fadeTime)))
            Game.fadeTimer -= (Clock.get_time() / 1000.0)
            if Game.fadeTimer <= 0:
                Game.fadeTimer = 0
                Game.fadeIn = False
                
        elif Game.fadeOut:
            Game.srfcCutScenes[Game.cutScene_ID].set_alpha(255 * (Game.fadeTimer / Game.fadeTime))
            Game.fadeTimer -= (Clock.get_time() / 1000.0)
            if Game.fadeTimer <= 0:
                Game.fadeOut = False
                Game.fadeIn = True
                Game.fadeTimer = Game.fadeTime
                Game.cutScene_ID = 0
                
                if Game.level_ID > 0 and Game.level_ID <= len(Game.level):

                    # Display world map
                    if Game.custom == False:
                        tempWorldMap = gfnLoad_Splice(320, 200, gfn_Zip("map.png"), 0, 0)
                        tempWorldMap = tempWorldMap[Game.level_ID - 1]
                        txtLoading = "Loading level " + str(Game.level_ID) + ": " + Game.level_names[Game.level_ID - 1] + "..."
                        textLoading = fontCK_MEDIUM.render(txtLoading, 1, (255, 255, 255))
                    else:
                        tempWorldMap = gfnLoad_Splice(320, 200, gfn_Zip("custom.png"), 0, 0)
                        tempWorldMap = tempWorldMap[0]
                        txtLoading = "Loading custom level..."
                        textLoading = fontCK_MEDIUM.render(txtLoading, 1, (255, 255, 255))
                        
                    srfcBuffer.blit(tempWorldMap, (0,0))
                    #srfcBuffer.blit(textLoading, (5, 185))
                    pygame.transform.scale(srfcBuffer, (Game.displayWidth * 2, Game.displayHeight * 2), srfcBuffer_2x)
                    srfcScreen.blit(srfcBuffer_2x, (0,0))
                    pygame.display.update()
                    pygame.time.wait(2000)
                    
                    # Play sound and load level
                    gfn_PlaySound(SFX_LEVEL_START)
                    Level.reset()

                    if Game.custom == False: gfn_LoadTMX(Game.level[Game.level_ID-1], Level, Game)
                    else: gfn_LoadTMX(Game.customLevel, Level, Game)
                    
                    Level.update(Game, Keen)
                    HUD = gcls_HUD(Keen, srfcBuffer)
                    Game.state = STATE_LEVEL
                    Clock.tick()
                    Keen.timeElapsed = 0.01
                    Keen.moveAmountX = 0
                    Keen.moveAmountY = 0
                    Keen.checkPoint = False
                    if Game.custom == False: pygame.mixer.music.load(MUSIC[Game.level_ID - 1])
                    else: pygame.mixer.music.load(MUSIC[15])
                    pygame.mixer.music.play(-1)
                    
                elif Game.level_ID == 0:
                    Game.state = STATE_MENU
                    Game.level_ID += 1

                elif Game.level_ID > len(Game.level):
                    Game.state = STATE_MENU
                    Game.level_ID = 1
                    Keen.reset()

                

                

                            

                        
    # Level Handling   
    elif Game.state == STATE_LEVEL:
        
        # Single key strokes (different from holding keys down)
        for event in pygame.event.get():
            # Allow us to quit
            if event.type == QUIT:
                done = True

            # And take us back to the menu
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.music.fadeout(500)
                    # Potentially might want to change this if want to implement "return to game" stuff
                    Keen.reset()
                    Game.reset()
                    Game.custom = False
                    Game.state = STATE_MENU
                else:
                    gfnKeen_checkSingleKey(Keen, event.key, Level, Game)

        
        # Update player based on key presses
        Keen.update(newTime, timeElapsed, Level, Game)
        
        # Update BG & FG animated tiles
        if newTime - animLastUpdate > 1000 / ANIM_FPS:
            animFrame += 1
            animLastUpdate = newTime
            if animFrame > 3: animFrame = 0    

        # Update camera if Keen is alive
        if Keen.state != kDYING: Level.updateCamera(Keen)

        # Update game objects         
        Level.sprite_AnimBG.update(animFrame, Level)
        Level.sprite_AnimFG.update(animFrame, Level)
        Level.sprite_Items.update(animFrame, Level, Keen, Level.sprite_Floats, Game)
        Level.sprite_Floats.update(newTime, Level)
        Level.sprite_Projectiles.update(timeElapsed, Level, Level.sprite_Enemies)
        Level.sprite_Explosions.update(newTime, timeElapsed, Level, Keen, Game)
        Level.sprite_Particles.update(newTime, timeElapsed, Level, Keen, Game)
        Level.sprite_Enemies.update(newTime, timeElapsed, Level, Keen)
        Level.sprite_Doors.update(newTime, Level)
        Level.sprite_Exits.update(Level)
        Level.sprite_CheckPoints.update(Level)
        Level.sprite_Hurt.update(Level)
        Level.sprite_WeatherBG.update(newTime, timeElapsed, Level)
        Level.sprite_WeatherFG.update(newTime, timeElapsed, Level)
        Level.sprite_Platforms.update(newTime, Level, Keen)
        Level.sprite_Switches.update(newTime, Level)
        
        # Check collisions if Keen is alive and not entering a door
        # We don't want items being collected, etc during the death animation
        if Keen.state != kDYING and Keen.state != kIN_DOOR:

            # Make splash if entered water
            if Keen.makeSplash == True:
                gfn_PlaySound(SFX_KEEN_SPLASH)
                Keen.makeSplash = False
                num_particles = 50

                # Check lava
                lavaX, lavaY = int((Keen.x + (Keen.width / 2.0)) / TILESIZE), int((Keen.y + Keen.height) / TILESIZE)
                chkTilesLava = Level.FG_TRANS[lavaX][lavaY]  
                if chkTilesLava == 2327:
                    for i in range(num_particles):
                        Level.sprite_Particles.add(gcls_Particle(Keen.x + (Keen.width / 2), Keen.y + (Keen.height / 2), pTYPE_SPLASH_LAVA, pygame.time.get_ticks(), (0,0,255)))
                else:
                    for i in range(num_particles):
                        Level.sprite_Particles.add(gcls_Particle(Keen.x + (Keen.width / 2), Keen.y + (Keen.height / 2), pTYPE_SPLASH, pygame.time.get_ticks(), (0,0,255)))

            # Check collisions: Keen x Items (Pixel Perfect)
            Keen_X_Items_Rect = pygame.sprite.spritecollide(Keen, Level.sprite_Items, False, pygame.sprite.collide_rect)
            for possibleCollide in Keen_X_Items_Rect:
                if pygame.sprite.collide_mask(Keen, possibleCollide):
                    possibleCollide.collected = True

            # Check collisions: Keen x Hurt Tiles (Pixel Perfect)
            # Not checked if GOD powerup is active
            if Keen.powerUp != pwrGOD:
                Keen_X_Hurt_Rect = pygame.sprite.spritecollide(Keen, Level.sprite_Hurt, False, pygame.sprite.collide_rect)
                for possibleCollide in Keen_X_Hurt_Rect:
                    if pygame.sprite.collide_mask(Keen, possibleCollide):
                        Keen.hurt(possibleCollide.id, Game, Level)
                    
            # Check collisions: Keen x Exits (Rect only)
            exitCollide = pygame.sprite.spritecollide(Keen, Level.sprite_Exits, False, pygame.sprite.collide_rect)
            #for tileExit in exitCollide:
            if len(exitCollide) > 0:
                pygame.mixer.music.fadeout(500) # Fade out music
                Keen.sprite = 0                 # Make keen's sprite sheet back to normal
                
                if Game.custom == False:
                    tileExit = exitCollide[0]
                    oldLevel = Game.level_ID
                    Game.level_ID = tileExit.id
                    Game.srfcCutScenes = gfnLoad_Splice(320, 200, gfn_Zip(Game.CSNames[Game.level_ID]), 0, 0)
                    Game.drawStats(Level, Keen, oldLevel, tileExit.id)
                    Game.state = STATE_FADEOUT_NEXTLEVEL
                    Game.fadeTimer = Game.fadeTime * 2
                    gfn_PlaySound(SFX_LEVEL_FINISH)
                    Keen.checkPoint = False
                else:
                    Game.fadeTimer = Game.fadeTime * 2
                    gfn_PlaySound(SFX_LEVEL_FINISH)
                    Game.state = STATE_FADEOUT_GAMEOVER
                    
                
            # Check collisions: Keen x Enemies (Pixel Perfect)
            # NB: Not checked if GOD powerup is active
            if Keen.powerUp != pwrGOD:
                enemyCollide = pygame.sprite.spritecollide(Keen, Level.sprite_Enemies, False, pygame.sprite.collide_rect)
                
                for possibleCollide in enemyCollide:
                    # First check if Keen is using the shield and Rect collided with a bullet
                    #Also require Keen to be normal/falling state, and facing the approaching bullet
                    if possibleCollide.bullet == True and (Keen.state == kON_GROUND or Keen.state == kFALLING) and Keen.invCurrent == 1 and Keen.inventory[1].power >= 0 and ((Keen.direction == sDIR_RIGHT and Keen.x < possibleCollide.x) or (Keen.direction == sDIR_LEFT and Keen.x > possibleCollide.x)):
                        Keen.invShield = Keen.invShieldTime
                        possibleCollide.kill()

                    # If not, do Pixel Perfect collision as normal
                    else:
                        if pygame.sprite.collide_mask(Keen, possibleCollide):
                            if possibleCollide.state != ENEMY_STATE_DIE:
                                # If it is spider, and Keen is on Pogo, kill the spider
                                if possibleCollide.id == SPRITE_SPIDER and Keen.onPogo == True and Keen.vy > 0:
                                    possibleCollide.state = ENEMY_STATE_DIE
                                    possibleCollide.vx = 0
                                    possibleCollide.moveAmountX = 0
                                    gfn_PlaySound(SFX_ENEMY_SPLAT)
                                    Level.stats_NumEnemies += 1
                                    
                                # Otherwise proceed as normal
                                else:
                                    # Only hurt Keen if the damage is > 0
                                    # This prevents non-hurting enemies from making Keen invincible for a second
                                    if possibleCollide.damage > 0:
                                        Keen.hurt(possibleCollide.damage, Game, Level)
                                    if possibleCollide.bullet == True:
                                        if (
                                                possibleCollide.id != SPRITE_SPIDER_PROJ
                                            and possibleCollide.id != SPRITE_WATER_DROP
                                            and possibleCollide.id != SPRITE_ACID_DROP
                                            and possibleCollide.id != SPRITE_ISONIAN_GREEN
                                            and possibleCollide.id != SPRITE_ISONIAN_RED
                                            and possibleCollide.id != SPRITE_ISONIAN_WHITE
                                            ):
                                            possibleCollide.kill()

        
            # Check collisions: Keen x Doors (Rect only)
            doorCollide = pygame.sprite.spritecollide(Keen, Level.sprite_Doors, False, pygame.sprite.collide_rect)
            for door in doorCollide:
                if Keen.hasKey[door.id] and door.state == DOOR_STATE_CLOSED:
                    gfn_PlaySound(SFX_ITEM_KEY_USE)
                    door.state = DOOR_STATE_OPEN
                    Keen.hasKey[door.id] = False

            # Check collisions: Keen x Check Points
            possibleCollide = pygame.sprite.spritecollide(Keen, Level.sprite_CheckPoints, False, pygame.sprite.collide_rect)
            for checkPoint in possibleCollide:
                if pygame.sprite.collide_mask(Keen, checkPoint):
                    if checkPoint.active == True:
                        checkPoint.active = False
                        checkPoint.image = srfcCheckPoints[1]
                        Keen.checkPoint = True
                        Level.initX, Keen.checkX = checkPoint.x, checkPoint.x
                        Level.initY, Keen.checkY = checkPoint.y, checkPoint.y
            
            # Check collisions: Keen x Platforms (if Keen is falling)
            Keen_X_Platforms = pygame.sprite.spritecollide(Keen, Level.sprite_Platforms, False, pygame.sprite.collide_rect)
            for possibleCollide in Keen_X_Platforms:
                if pygame.sprite.collide_mask(Keen, possibleCollide):
                    #if Keen.vy >= 0 and Keen.y + Keen.height < possibleCollide.y + (possibleCollide.height * 0.75):
                        Keen.vy = 0
                        Keen.onPlatform = True
                        Keen.state = kON_GROUND
                        Keen.idleTimer = 0
                        
                # If Keen is on a platform but now not touching one, he falls
                elif Keen.onPlatform == True:
                    Keen.onPlatform = False
                    Keen.state = kFALLING

                # If no collision at all, make sure he is flagged as not on platform
                else:
                    Keen.onPlatform = False
            

        # Draw PBG, BG Weather (Rain and/or Snow), BG Trans, BG
        #print Level.bgX, Level.bgY
        
        srfcBuffer.blit(Level.srfcPBG.subsurface(round(Level.bgX), round(Level.bgY), Level.playWidth, Level.playHeight), (Level.playX, Level.playY))
        Level.sprite_WeatherBG.draw(srfcBuffer)
        srfcBuffer.blit(Level.srfcBG_TRANS.subsurface(round(Level.mapX), round(Level.mapY), Level.playWidth, Level.playHeight), (Level.playX, Level.playY))
        srfcBuffer.blit(Level.srfcBG.subsurface(round(Level.mapX), round(Level.mapY), Level.playWidth, Level.playHeight), (Level.playX, Level.playY))

        # Draw sprite objects
        
        Level.sprite_AnimBG.draw(srfcBuffer)
        Level.sprite_Items.draw(srfcBuffer)
        Level.sprite_Particles.draw(srfcBuffer)
        Level.sprite_Enemies.draw(srfcBuffer)
        Level.sprite_Projectiles.draw(srfcBuffer)
        Level.sprite_Explosions.draw(srfcBuffer)
        Level.sprite_Doors.draw(srfcBuffer)
        Level.sprite_Platforms.draw(srfcBuffer)
        Level.sprite_Switches.draw(srfcBuffer)
        Level.sprite_CheckPoints.draw(srfcBuffer)
        
        
        # Draw Enemy hit points if Ion Scanner selected
        if Keen.invCurrent == iIonScanner:
            for enemy in Level.sprite_Enemies:
                if enemy.state != ENEMY_STATE_DIE and enemy.bullet == False:
                    gfn_IonScan(srfcBuffer, enemy)

        # Draw Enemey Rects - DEBUGGING
        #for enemy in Level.sprite_Enemies:
        #    adjustRect = pygame.Rect(enemy.subRect[0] - Level.mapX + Level.playX, enemy.subRect[1] - Level.mapY + Level.playY, enemy.subRect[2], enemy.subRect[3])
        #    pygame.draw.rect(srfcBuffer, (255,0,0), adjustRect, 1)
                
        # Draw Keen, if he is alive
        if Keen.state != kDYING: srfcBuffer.blit(Keen.image, (round(Keen.x - Level.mapX) + Level.playX, round(Keen.y - Level.mapY) + Level.playY))

        """
        # If SHOES powerup, draw the ghosts
        if Keen.powerUp == pwrSHOES:
            m = 5
            b = 10
            if Keen.vx != 0 or Keen.vy != 0:
                tempOffX, tempOffY = 0, 0
                tempOffX = Keen.direction * -1
                
                if Keen.vy > 0: tempOffY = -1
                elif Keen.vy < 0: tempOffY = 1
                else: tempOffY = 0
                
                srfcGhost1, srfcGhost2, srfcGhost3, srfcGhost4 = Keen.image.copy(), Keen.image.copy(), Keen.image.copy(), Keen.image.copy()
                srfcGhost1.set_alpha(150)
                srfcGhost2.set_alpha(100)
                srfcGhost3.set_alpha(50)
                srfcGhost4.set_alpha(25)
                srfcBuffer.blit(srfcGhost1, (round(Keen.x - Level.mapX) + Level.playX + (5 * tempOffX), round(Keen.y - Level.mapY) + Level.playY + (5 * tempOffY)))
                srfcBuffer.blit(srfcGhost2, (round(Keen.x - Level.mapX) + Level.playX + (10 * tempOffX), round(Keen.y - Level.mapY) + Level.playY + (10 * tempOffY)))
                srfcBuffer.blit(srfcGhost3, (round(Keen.x - Level.mapX) + Level.playX + (15 * tempOffX), round(Keen.y - Level.mapY) + Level.playY + (15 * tempOffY)))
                srfcBuffer.blit(srfcGhost4, (round(Keen.x - Level.mapX) + Level.playX + (20 * tempOffX), round(Keen.y - Level.mapY) + Level.playY + (20 * tempOffY)))
        """
        
        # Draw Keen's rect
        #testRect = pygame.Rect(Keen.subRect[0] - Level.mapX + Level.playX, Keen.subRect[1] - Level.mapY + Level.playY, Keen.subRect[2], Keen.subRect[3])
        #pygame.draw.rect(srfcBuffer, (255,0,0), testRect, 1)
        
        # Draw FG, FG Anim, FG Trans, FG Weather (Clouds)
        srfcBuffer.blit(Level.srfcFG.subsurface(round(Level.mapX), round(Level.mapY), Level.playWidth, Level.playHeight), (Level.playX, Level.playY))
        Level.sprite_AnimFG.draw(srfcBuffer)
        srfcBuffer.blit(Level.srfcFG_TRANS.subsurface(round(Level.mapX), round(Level.mapY), Level.playWidth, Level.playHeight), (Level.playX, Level.playY))
        Level.sprite_Floats.draw(srfcBuffer)
        Level.sprite_WeatherFG.draw(srfcBuffer)

       
        # Draw Night Mode
        if Level.night == True:
            # Change darkness of Night Mode
            if Level.totalNight <= Level.maxNight: Level.totalNight += timeElapsed
            Game.srfcNight.set_alpha((Level.totalNight/Level.maxNight) * 0.4 * 255)

            # Print night overlay
            srfcBuffer.blit(Game.srfcNight, (Level.playX, Level.playY))

        # Draw Keen, if he is dying (i.e., on top of everything else)
        if Keen.state == kDYING: srfcBuffer.blit(Keen.image, (round(Keen.x - Level.mapX) + Level.playX, round(Keen.y - Level.mapY) + Level.playY))
        
        # Debug
        if Game.debug.on == False: #quick hack so it still works with Debug off
            
            DEBUG_COL = Game.debug.COLS[Game.debug.messageCol]
            
            # Calculate FPS
            fps = int((old_fps + Clock.get_fps()) / 2.0)
            old_fps = fps
            #text_fps = fontCK_SMALL.render(str(fps) + " fps", 1, DEBUG_COL)
            #srfcBuffer.blit(text_fps, (Level.playX + 5, Level.playY + 5))

            # Message
            if Game.debug.message == DEBUG_HELLO:
                #Keen.message = "Welcome to the Mystery of Isis IIa"
                #Keen.message = str(t2-t1) + "," + str(t3-t2)
                #Keen.message = Keen.state
                Keen.message = str(round(Keen.extraX, 3))
                #text_message = fontCK_SMALL.render(str(Keen.message), 1, DEBUG_COL)
                #srfcBuffer.blit(text_message, (Level.playX + 5, Level.playY + 15))

            # Stats
            elif Game.debug.message == DEBUG_STATS:
                if Level.stats_NumItems_Tot != 0: tempItemsPercent = round((Level.stats_NumItems / Level.stats_NumItems_Tot) * 100.0, 1)
                else: tempItemsPercent = 100
                if Level.stats_NumPoints_Tot != 0: tempPointsPercent = round((Level.stats_NumPoints / Level.stats_NumPoints_Tot) * 100.0, 1)
                else: tempPointsPercent = 100
                if Level.stats_NumEnemies_Tot != 0: tempEnemiesPercent = round((Level.stats_NumEnemies / Level.stats_NumEnemies_Tot) * 100.0, 1)
                else: tempEnemiesPercent = 100
                txt_Item1 = "- Items Collected: " + str(Level.stats_NumItems) + "/" + str(int(Level.stats_NumItems_Tot)) + " (" + str(tempItemsPercent) + "%)"
                txt_Item2 = "- Points Scored: " + str(Level.stats_NumPoints) + "/" + str(int(Level.stats_NumPoints_Tot)) + " (" + str(tempPointsPercent) + "%)"
                txt_Item3 = "- Enemies Killed: " + str(Level.stats_NumEnemies) + "/" + str(int(Level.stats_NumEnemies_Tot)) + " (" + str(tempEnemiesPercent) + "%)"
                text_message1 = fontCK_SMALL.render(txt_Item1, 1, DEBUG_COL)
                text_message2 = fontCK_SMALL.render(txt_Item2, 1, DEBUG_COL)
                text_message3 = fontCK_SMALL.render(txt_Item3, 1, DEBUG_COL)
                srfcBuffer.blit(text_message1, (Level.playX + 5, Level.playY +  5)) #was 15
                srfcBuffer.blit(text_message2, (Level.playX + 5, Level.playY + 15)) #was 25
                srfcBuffer.blit(text_message3, (Level.playX + 5, Level.playY + 25)) #was 35

            # Hidden Areas
            if Game.debug.hidden:
                Level.sprite_MaskAll.update(Level)
                Level.sprite_MaskAll.draw(srfcBuffer)
            
           
            
        # Update HUD (includes blitting to buffer) - must be blitted last to coverup the edges of any sprites
        HUD.update(Keen, srfcBuffer)

        
    # Fadeouts  
    elif Game.state == STATE_FADEOUT_NEXTLEVEL or Game.state == STATE_FADEOUT_KILL or Game.state == STATE_FADEOUT_GAMEOVER:
        if Game.fadeTimer == Game.fadeTime * 2: srfcTempBuffer = srfcBuffer.copy()

        srfcTempBuffer.set_alpha(255 * (Game.fadeTimer / Game.fadeTime))
        srfcBuffer.fill((0,0,0))
        srfcBuffer.blit(srfcTempBuffer, (0,0))
        Game.fadeTimer -= (Clock.get_time() / 1000.0)
        
        if Game.fadeTimer <= 0:
            if Game.state == STATE_FADEOUT_NEXTLEVEL:
                Game.state = STATE_CUTSCENE
            elif Game.state == STATE_FADEOUT_KILL:
                # Display world map
                if Game.custom == False:
                    tempWorldMap = gfnLoad_Splice(320, 200, gfn_Zip("map.png"), 0, 0)
                    tempWorldMap = tempWorldMap[Game.level_ID - 1]
                    txtLoading = "Loading level " + str(Game.level_ID) + ": " + Game.level_names[Game.level_ID - 1] + "..."
                    textLoading = fontCK_MEDIUM.render(txtLoading, 1, (255, 255, 255))
                else:
                    tempWorldMap = gfnLoad_Splice(320, 200, gfn_Zip("custom.png"), 0, 0)
                    tempWorldMap = tempWorldMap[0]
                    txtLoading = "Loading custom level..."
                    textLoading = fontCK_MEDIUM.render(txtLoading, 1, (255, 255, 255))
                        
                srfcBuffer.blit(tempWorldMap, (0,0))
                srfcBuffer.blit(textLoading, (5, 185))
                pygame.transform.scale(srfcBuffer, (Game.displayWidth * 2, Game.displayHeight * 2), srfcBuffer_2x)
                srfcScreen.blit(srfcBuffer_2x, (0,0))
                pygame.display.update()

                # Reset Level
                Level.reset()
                
                if Game.custom == False: gfn_LoadTMX(Game.level[Game.level_ID-1], Level, Game)
                else: gfn_LoadTMX(Game.customLevel, Level, Game)
                    
                Level.update(Game, Keen)
                Keen.state = kFALLING
                Game.state = STATE_LEVEL
                Clock.tick()
                Keen.timeElapsed = 0.01
                Keen.moveAmountX = 0
                Keen.moveAmountY = 0
                if Game.custom == False: pygame.mixer.music.load(MUSIC[Game.level_ID - 1])
                else: pygame.mixer.music.load(MUSIC[15])
                pygame.mixer.music.play(-1)
                
            elif Game.state == STATE_FADEOUT_GAMEOVER:
                Keen.reset()
                Game.reset()
                Game.custom = False
                Game.state = STATE_MENU




    # Scale the buffer surface 2x the size, and Update display
    pygame.transform.scale(srfcBuffer, (Game.displayWidth * 2, Game.displayHeight * 2), srfcBuffer_2x)
    srfcScreen.blit(srfcBuffer_2x, (0,0))

    pygame.display.update()



# __________________________________________________
# Will only end up here if main loop finishes - Quit
pygame.quit()
sys.exit()




