# isis_music.py
# All music and sound fx

import pygame, os
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

# Music
MUSIC = []
MUSIC.append(os.path.join("data", "level01.ogg"))
MUSIC.append(os.path.join("data", "level02.ogg"))
MUSIC.append(os.path.join("data", "level03.ogg"))
MUSIC.append(os.path.join("data", "level04.ogg"))
MUSIC.append(os.path.join("data", "level05.ogg"))
MUSIC.append(os.path.join("data", "level06.ogg"))
MUSIC.append(os.path.join("data", "level07.ogg"))
MUSIC.append(os.path.join("data", "level08.ogg"))
MUSIC.append(os.path.join("data", "level09.ogg"))
MUSIC.append(os.path.join("data", "level0x.ogg"))
MUSIC.append(os.path.join("data", "level0x.ogg"))
MUSIC.append(os.path.join("data", "level0x.ogg"))
MUSIC.append(os.path.join("data", "level0x.ogg"))
MUSIC.append(os.path.join("data", "level0x.ogg"))
MUSIC.append(os.path.join("data", "level0x.ogg"))
MUSIC.append(os.path.join("data", "level0x.ogg"))


SFX = []

# Weapons
SFX.append(pygame.mixer.Sound(os.path.join("data", "w_blowgun.ogg")))    # id = 0 / plute
SFX.append(pygame.mixer.Sound(os.path.join("data", "w_blowgun.ogg")))    # id = 1 / hr
SFX.append(pygame.mixer.Sound(os.path.join("data", "w_blowgun.ogg")))    # id = 2 / solar
SFX.append(pygame.mixer.Sound(os.path.join("data", "w_blowgun.ogg")))    # id = 3 / pulsar
SFX.append(pygame.mixer.Sound(os.path.join("data", "w_blowgun.ogg")))    # id = 4 / zeffer
SFX.append(pygame.mixer.Sound(os.path.join("data", "w_blowgun.ogg")))    # id = 5 / blowgun
SFX.append(pygame.mixer.Sound(os.path.join("data", "w_blowgun.ogg")))    # id = 6 / harpoon
SFX.append(pygame.mixer.Sound(os.path.join("data", "w_blowgun.ogg")))    # id = 7 / raygun
SFX.append(pygame.mixer.Sound(os.path.join("data", "w_neural.ogg")))     # id = 8 / neural
SFX.append(pygame.mixer.Sound(os.path.join("data", "w_hitwall.ogg")))    # id = 9 / weapon hit wall

# Items
SFX.append(pygame.mixer.Sound(os.path.join("data", "item_points.ogg")))         # id = 10
SFX.append(pygame.mixer.Sound(os.path.join("data", "item_weapon.ogg")))         # id = 11
SFX.append(pygame.mixer.Sound(os.path.join("data", "item_weapon_neural.ogg")))  # id = 12
SFX.append(pygame.mixer.Sound(os.path.join("data", "item_key.ogg")))            # id = 13
SFX.append(pygame.mixer.Sound(os.path.join("data", "item_key_use.ogg")))        # id = 14
SFX.append(pygame.mixer.Sound(os.path.join("data", "item_1up.ogg")))            # id = 15

# Keen
SFX.append(pygame.mixer.Sound(os.path.join("data", "keen_jump.ogg")))       # id = 16
SFX.append(pygame.mixer.Sound(os.path.join("data", "keen_pogo.ogg")))       # id = 17
SFX.append(pygame.mixer.Sound(os.path.join("data", "keen_bubbles.ogg")))    # id = 18
SFX.append(pygame.mixer.Sound(os.path.join("data", "keen_splash.ogg")))     # id = 19
SFX.append(pygame.mixer.Sound(os.path.join("data", "keen_die.ogg")))        # id = 20
SFX.append(pygame.mixer.Sound(os.path.join("data", "keen_switch.ogg")))     # id = 21

# Enemies
SFX.append(pygame.mixer.Sound(os.path.join("data", "enemy_droplet.ogg")))   # id = 22
SFX.append(pygame.mixer.Sound(os.path.join("data", "enemy_slug.ogg")))      # id = 23
SFX.append(pygame.mixer.Sound(os.path.join("data", "enemy_mine.ogg")))      # id = 24
SFX.append(pygame.mixer.Sound(os.path.join("data", "enemy_shot1.ogg")))     # id = 25
SFX.append(pygame.mixer.Sound(os.path.join("data", "enemy_shot2.ogg")))     # id = 26
SFX.append(pygame.mixer.Sound(os.path.join("data", "enemy_shot3.ogg")))     # id = 27
SFX.append(pygame.mixer.Sound(os.path.join("data", "enemy_shot4.ogg")))     # id = 28
SFX.append(pygame.mixer.Sound(os.path.join("data", "enemy_shot5.ogg")))     # id = 29

# Weather
SFX.append(pygame.mixer.Sound(os.path.join("data", "wx_rain.ogg")))         # id = 30
SFX.append(pygame.mixer.Sound(os.path.join("data", "wx_lightning.ogg")))    # id = 31

# Level
SFX.append(pygame.mixer.Sound(os.path.join("data", "level_start.ogg")))     # id = 32
SFX.append(pygame.mixer.Sound(os.path.join("data", "level_finish.ogg")))    # id = 33

# Misc
SFX.append(pygame.mixer.Sound(os.path.join("data", "item_points_k4.ogg")))  # id = 34
SFX.append(pygame.mixer.Sound(os.path.join("data", "enemy_foog_jump.ogg")))  # id = 35
SFX.append(pygame.mixer.Sound(os.path.join("data", "enemy_splat.ogg")))  # id = 35

def gfn_PlaySound(soundID):
    # If Game.Sound
    SFX[soundID].play()
